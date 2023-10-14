from typing import Any, Dict
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,FormView,ListView,UpdateView,DeleteView,DetailView
from core.log.utils import MyLoginRequiredMixin
from .forms import *
from .models import Prediction
from django.contrib import messages
# Create your views here.

class PredictionCreateView(MyLoginRequiredMixin,FormView):
    template_name='add_pred.html'
    form_class=PredictionForm
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(request,form)
        else:
            return self.form_invalid(request,form,"data no válida")
    
    def form_invalid(self,request,form,rason=""):
        messages.error(request,f'Error al crear predicción, {rason}')
        return super().form_invalid(form)
    
    def form_valid(self,request,form):
        try:
            form.save()
        except Exception as e:
            return self.form_invalid(request,form,e)
        messages.success(request,'Creada nueva predicción correctamente')
        return redirect('pred_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Nueva Predicción"
        return context

class PredictionListView(MyLoginRequiredMixin,ListView):
    paginate_by = 10
    template_name='list_pred.html'
    model=Prediction
    
    def get_queryset(self):
       return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url']=reverse_lazy('reg') 
        return context
    


class PredictionDeleteView(MyLoginRequiredMixin,DeleteView):
    model=Prediction
    template_name = 'delete_pred.html'
    #permission_required="user.delete_user"
    success_url=reverse_lazy('pred_list')
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Eliminar Prediccion"
        context['url_cancel']=reverse_lazy('pred_list')   
        context['name']=self.object.measuring.name
        return context
