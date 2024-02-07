from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from client.forms import ClientForm
from client.models import Client


class ClientListView(LoginRequiredMixin, ListView):
    # paginate_by = 50
    model = Client
    # extra_context = {'title': 'Подписчики'}
    success_url = reverse_lazy('create:create_list')

def get_queryset(self):
    queryset = super().get_queryset()
    # if self.request.user.has_perm('clients.view_client'):
    # return queryset
    # else:
    return queryset.filter(owner=self.request.user)



class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:client_list')

    def form_valid(self, form):
        if form.is_valid():
            new_client = form.save()
            new_client.owner = self.request.user
            new_client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client:client_list')

    # def test_func(self):
    #     obj = self.get_object()
    #     return self.request.user.is_superuser or obj.owner == self.request.user
