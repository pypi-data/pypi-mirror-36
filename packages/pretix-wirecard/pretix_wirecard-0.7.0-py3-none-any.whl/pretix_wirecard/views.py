import hashlib
import hmac
import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from pretix.base.models import Order, Quota, OrderPayment
from pretix.multidomain.urlreverse import eventreverse

logger = logging.getLogger('pretix_wirecard')


class WirecardOrderView:
    def dispatch(self, request, *args, **kwargs):
        try:
            self.order = request.event.orders.get(code=kwargs['order'])
            if hashlib.sha1(self.order.secret.lower().encode()).hexdigest() != kwargs['hash'].lower():
                raise Http404('<QPAY-CONFIRMATION-RESPONSE result="NOK" message="Unknown order." />')
        except Order.DoesNotExist:
            # Do a hash comparison as well to harden timing attacks
            if 'abcdefghijklmnopq'.lower() == hashlib.sha1('abcdefghijklmnopq'.encode()).hexdigest():
                raise Http404('<QPAY-CONFIRMATION-RESPONSE result="NOK" message="Unknown order." />')
            else:
                raise Http404('<QPAY-CONFIRMATION-RESPONSE result="NOK" message="Unknown order." />')
        return super().dispatch(request, *args, **kwargs)

    @cached_property
    def pprov(self):
        return self.payment.payment_provider

    @property
    def payment(self):
        return get_object_or_404(
            self.order.payments,
            pk=self.kwargs['payment'],
            provider__istartswith='wirecard',
        )


@method_decorator(xframe_options_exempt, 'dispatch')
class RedirectView(WirecardOrderView, TemplateView):
    template_name = 'pretix_wirecard/redirecting.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['params'] = self.pprov.sign_parameters(self.pprov.params_for_payment(self.payment, self.request))
        return ctx


def validate_fingerprint(request, prov):
    if 'responseFingerprint' not in request.POST or 'responseFingerprintOrder' not in request.POST:
        return False
    if 'secret' not in request.POST.get('responseFingerprintOrder'):
        return False
    fpo = request.POST.get('responseFingerprintOrder').split(',')
    payload = ''
    for k in fpo:
        if k == 'secret':
            payload += prov.settings.get('secret')
        else:
            payload += request.POST[k]
    fp = hmac.new(
        prov.settings.get('secret').encode(), payload.encode(), hashlib.sha512
    ).hexdigest().upper()
    return fp == request.POST.get('responseFingerprint').upper()


def process_result(request, payment, prov):
    payment.info_data = dict(request.POST.items())
    payment.save()
    if payment.state in (
            OrderPayment.PAYMENT_STATE_PENDING, OrderPayment.PAYMENT_STATE_CREATED
    ) and request.POST.get('paymentState') == 'SUCCESS':
        payment.confirm()


@method_decorator(csrf_exempt, name='dispatch')
class ConfirmView(WirecardOrderView, View):
    def post(self, request, *args, **kwargs):
        if not validate_fingerprint(request, self.pprov):
            raise PermissionDenied('<QPAY-CONFIRMATION-RESPONSE result="NOK" message="Invalid fingerprint." />')
        self.order.log_action('pretix_wirecard.wirecard.event', data=dict(request.POST.items()))
        try:
            process_result(request, self.payment, self.pprov)
        except Quota.QuotaExceededException:
            pass
        return HttpResponse('<QPAY-CONFIRMATION-RESPONSE result="OK" />')


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(xframe_options_exempt, 'dispatch')
class ReturnView(WirecardOrderView, View):
    def get(self, request, *args, **kwargs):
        messages.error(
            request, _('The payment failed without an error message. You can click below to try again.')
        )
        return self._redirect_to_order()

    def post(self, request, *args, **kwargs):
        if not validate_fingerprint(request, self.pprov):
            messages.error(self.request, _('Sorry, we could not validate the payment result. Please try again or '
                                           'contact the event organizer to check if your payment was successful.'))
            return self._redirect_to_order()

        self.order.log_action('pretix_wirecard.wirecard.event', data=dict(request.POST.items()))
        if request.POST.get('paymentState') == 'CANCEL':
            messages.error(self.request, _('The payment process was canceled. You can click below to try again.'))
            return self._redirect_to_order()

        if request.POST.get('paymentState') == 'FAILURE':
            messages.error(
                self.request, _('The payment failed with the following message: {message}. '
                                'You can click below to try again.').format(message=request.POST.get('message')))
            return self._redirect_to_order()

        if request.POST.get('paymentState') == 'PENDING':
            messages.warning(
                self.request, _('Your payment has been started processing and will take a while to complete. We will '
                                'send you an email once your payment is completed. If this takes longer than expected, '
                                'contact the event organizer.')
            )
            return self._redirect_to_order()

        try:
            process_result(request, self.payment, self.pprov)
        except Quota.QuotaExceededException as e:
            messages.error(request, str(e))
        return self._redirect_to_order()

    def _redirect_to_order(self):
        if self.request.session.get('wirecard_order_secret') != self.order.secret:
            messages.error(self.request, _('Sorry, there was an error in the payment process. Please check the link '
                                           'in your emails to continue.'))
            return redirect(eventreverse(self.request.event, 'presale:event.index'))

        return redirect(eventreverse(self.request.event, 'presale:event.order', kwargs={
            'order': self.order.code,
            'secret': self.order.secret
        }) + ('?paid=yes' if self.order.status == Order.STATUS_PAID else ''))
