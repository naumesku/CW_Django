from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from blog.models import Blog
from client.models import Client
from mailing.forms import MailingMessageForm, MailingSettingsForm
from mailing.models import MailingMessage, MailingSettings, MailingLogs

class MailingMessageListView(LoginRequiredMixin, ListView):
    model = MailingMessage

class MailingMessageCreateView(LoginRequiredMixin, CreateView):
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(MailingMessage, MailingSettings, form=MailingSettingsForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = SubjectFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if formset.is_valid():
            self.object.owner = self.request.user
            formset.instance = self.object
            formset.save()

            return super().form_valid(form)

        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

class MailingMessageDetailView(LoginRequiredMixin, DetailView):
    model = MailingMessage
    # success_url = reverse_lazy('mailing:mailingmessage_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailingsetting'] = MailingSettings.objects.filter(message_id=self.kwargs.get('pk'))
        return context_data

class MailingMessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing:index')

    # permission_required = 'product.change_product'

    # def get_success_url(self):
    #     return reverse('mailing:mailing_update', args=[self.kwargs.get('pk')])

    # def get_form_class(self):
    #     if not self.request.user.has_perm('product.set_published'):
    #         return ModeratorForm
    #     return MailingMessageForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # if self.request.user == self.object.user_own or self.request.user.is_superuser:
        SettingsFormset = inlineformset_factory(MailingMessage, MailingSettings, form=MailingSettingsForm, extra=1)
        if self.request.method == 'POST':
            formset = SettingsFormset(self.request.POST, instance=self.object)
            # context_data['version'] = get_object_or_404(MailingSettings, pk=self.kwargs.get('pk'))
        else:
            formset = SettingsFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if formset.is_valid():
            self.object.owner = self.request.user
            formset.instance = self.object
            formset.save()

            return super().form_valid(form)

        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

class MailingMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:index')
    # def test_func(self):
    #     return self.request.user.is_superuser

# @login_required
def toggle_activity(request, pk):
    message_item = get_object_or_404(MailingMessage, pk=pk)
    if message_item.is_active:
        message_item.is_active = False
    else:
        message_item.is_active = True
    message_item.save()
    return redirect(reverse('mailing:index'))

@login_required
def main_page(request):
    """Представление для отображения главной страницы"""
    few_blog_list = Blog.objects.order_by('?')[:3]
    mailing_count_all = MailingSettings.objects.count()
    mailing_count_active = MailingSettings.objects.filter(status_choices=MailingSettings.StatusChoice.RUNING).count()
    client_count = Client.objects.values('email').annotate(total=Count('email')).count()

    context_data = {
        'few_blog_list': few_blog_list,
        'mailing_count_all': mailing_count_all,
        'mailing_count_active': mailing_count_active,
        'client_count': client_count
    }

    return render(request, 'mailing/main_page.html', context_data)

@login_required
def mailing_logs(request):
    logs_all = MailingLogs.objects.all()
    mailing = MailingMessage.objects.all()

    context_data = {
        'logs_all': logs_all,
        'mailing': mailing,
         }

    return render(request, 'mailing/logs.html', context_data)