#encoding:utf-8
import datetime
import random

from django.views.generic import ListView, View
from django.views.generic.detail import DetailView
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.text import slugify

from braces.views import LoginRequiredMixin

from kstore.helpers.mixins import JerarquiaMixin
from kstore_mail.models import MailMessage
from kstore_mail.forms import ComposeMailForm


class LoginJerarquiaListViewMixin(LoginRequiredMixin, JerarquiaMixin,ListView):
    """
        Mixin que aglutina los mixins habituales y variables generales.
    """
    model = MailMessage
    context_object_name = 'messages'

class LoginJerarquiaViewMixin(LoginRequiredMixin, JerarquiaMixin,View):
    """
        Mixin que aglutina los mixins habituales.
    """
    pass

class MailView(LoginJerarquiaListViewMixin):
    """
        Vista donde se listan los mensajes de la bandeja de entrada.
        Son los mensajes recibidos.
    """
    template_name = 'kstore_mail/inbox.html'
    jerarquia = [_('Mail'), _('Inbox')]

    def get_context_data(self, **kwargs):
        context = super(MailView, self).get_context_data(**kwargs)
        message_list = MailMessage.objects.inbox(self.request.user)
        paginator = Paginator(message_list, 10)
        page = self.request.GET.get('page')
        try:
            context['messages'] = paginator.page(page)
        except PageNotAnInteger:
            context['messages'] = paginator.page(1)
        except EmptyPage:
            context['messages'] = paginator.page(paginator.num_pages)

        context['new_messages'] = MailMessage.objects.new_messages(self.request.user).count()
        context['num_drafts'] = MailMessage.objects.draft(self.request.user).count()
        context['num_trash'] = MailMessage.objects.deleted(self.request.user).count()

        return context

class SentMailView(LoginJerarquiaListViewMixin):
    """
        Vista donde se listan los mensajes enviados.
    """
    template_name = 'kstore_mail/sent.html'
    jerarquia = [_('Mail'), _('Sent')]

    def get_context_data(self, **kwargs):
        context = super(SentMailView, self).get_context_data(**kwargs)
        message_list = MailMessage.objects.sent(self.request.user)
        paginator = Paginator(message_list, 10)
        page = self.request.GET.get('page')
        try:
            context['messages'] = paginator.page(page)
        except PageNotAnInteger:
            context['messages'] = paginator.page(1)
        except EmptyPage:
            context['messages'] = paginator.page(paginator.num_pages)

        context['new_messages'] = MailMessage.objects.new_messages(self.request.user).count()
        context['num_drafts'] = MailMessage.objects.draft(self.request.user).count()
        context['num_trash'] = MailMessage.objects.deleted(self.request.user).count()

        return context

class DraftMailView(LoginJerarquiaListViewMixin):
    """
        Vista donde se listan los mensajes que han sido
        guardados como borradores (no enviados).
    """
    template_name = 'kstore_mail/draft.html'
    jerarquia = [_('Mail'), _('Draft')]

    def get_context_data(self, **kwargs):
        context = super(DraftMailView, self).get_context_data(**kwargs)
        message_list = MailMessage.objects.draft(self.request.user)
        paginator = Paginator(message_list, 10)
        page = self.request.GET.get('page')
        try:
            context['messages'] = paginator.page(page)
        except PageNotAnInteger:
            context['messages'] = paginator.page(1)
        except EmptyPage:
            context['messages'] = paginator.page(paginator.num_pages)

        context['new_messages'] = MailMessage.objects.new_messages(self.request.user).count()
        context['num_drafts'] = MailMessage.objects.draft(self.request.user).count()
        context['num_trash'] = MailMessage.objects.deleted(self.request.user).count()

        return context

class ImportantMailView(LoginJerarquiaListViewMixin):
    """
        Vista donde se listan los mensajes marcados como importantes.
    """
    template_name = 'kstore_mail/important.html'
    jerarquia = [_('Mail'), _('Favorite inbox')]

    def get_context_data(self, **kwargs):
        context = super(ImportantMailView, self).get_context_data(**kwargs)
        message_list = MailMessage.objects.important(self.request.user)
        paginator = Paginator(message_list, 10)
        page = self.request.GET.get('page')
        try:
            context['messages'] = paginator.page(page)
        except PageNotAnInteger:
            context['messages'] = paginator.page(1)
        except EmptyPage:
            context['messages'] = paginator.page(paginator.num_pages)

        context['new_messages'] = MailMessage.objects.new_messages(self.request.user).count()
        context['num_drafts'] = MailMessage.objects.draft(self.request.user).count()
        context['num_trash'] = MailMessage.objects.deleted(self.request.user).count()

        return context

class MessageMailView(LoginJerarquiaViewMixin):
    """
        Vista donde el usuario lee el mensaje.
    """
    template_name = 'kstore_mail/mailmessage_detail.html'
    jerarquia = [_('Mail'), _('Message')]

    def get(self, request, slug):
        message = MailMessage.objects.get(slug=slug)
        if message.recipient != request.user:
            return redirect('kstore:mail:inbox')
        message.readed=True
        message.save()
        return render(request, self.template_name, {'message': message})

class ComposeMailView(LoginJerarquiaViewMixin):
    """
        Vista donde escribiremos los emails. La CBV con metodo GET solo
        entrega el formulario vacio. Con metodo POST crea el mensaje en
        la base de datos directamente. Hay que cambiarlo para que sea
        el formulario através de su metodo save() el que grabe.
    """
    template_name = 'kstore_mail/compose_mail.html'
    form_class = ComposeMailForm

    def get(self, request):
        form = ComposeMailForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = ComposeMailForm(request.POST)
        if form.is_valid():
            for dest in form.cleaned_data["destinatario"]:
                msg = MailMessage(
                    subject=form.cleaned_data["subject"],
                    recipient=dest,
                    sender=request.user,
                    slug=slugify(form.cleaned_data["subject"]+str(random.randint(0,1000))),
                    sended_at=datetime.datetime.now(),
                    message=form.cleaned_data["message"],
                    sended=True
                )
                msg.save()

            return redirect('kstore:mail:inbox')
        else:
            return render(request, self.template_name, {'form':form})

class TrashMailView(LoginJerarquiaListViewMixin):
    """
        Vista donde se muestran la papelera de los correos antes de
        borrarlos definitivamente.
    """
    template_name = 'kstore_mail/trash.html'
    jerarquia = [_('Mail'), _('Trash')]

    def get_context_data(self, **kwargs):
        context = super(TrashMailView, self).get_context_data(**kwargs)
        message_list = MailMessage.objects.deleted(self.request.user)
        paginator = Paginator(message_list, 10)
        page = self.request.GET.get('page')
        try:
            context['messages'] = paginator.page(page)
        except PageNotAnInteger:
            context['messages'] = paginator.page(1)
        except EmptyPage:
            context['messages'] = paginator.page(paginator.num_pages)

        context['new_messages'] = MailMessage.objects.new_messages(self.request.user).count()
        context['num_drafts'] = MailMessage.objects.draft(self.request.user).count()
        context['num_trash'] = message_list.count()
        return context

class DeleteMailFromMessageView(LoginRequiredMixin, View):
    """
        Vista donde se ejecuta el borrado del mensaje, desde la vista de lectura
        del mensaje.
    """
    def get(self, request, slug):
        message = MailMessage.objects.get(slug=slug)
        if message.recipient != request.user:
            return redirect('kstore:mail:inbox')
        message.deleted = True
        message.save()
        return redirect('kstore:mail:inbox')
