#from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from .models import FortiGroup

from django.http import HttpResponse

#@login_required
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'groupaccess/index.html'
    context_object_name = 'group_list'

    def get_queryset(self):
        """Return the group list order by name."""
        return FortiGroup.objects.order_by('name')


class DetailView(generic.DetailView):
    model = FortiGroup
    template_name = 'groupaccess/detail.html'

class FortiGroupList(ListView):
    model = FortiGroup


class FortiGroupCreate(CreateView):
    model = FortiGroup
    fields = ['name','enabled']

class FortiGroupUpdate(LoginRequiredMixin, UpdateView):
    model = FortiGroup
    fields = ['enabled']
    success_url = reverse_lazy('groupaccess:index')

class FortiGroupDelete(DeleteView):
    model = FortiGroup
    success_url = reverse_lazy('fortigroup-list')
