from django import forms
from .models import Model
from core.tra.models import Training
#from core.meas.models import Measuring,MeasuringData
import time
#from config.utils import is_at_migrations
class ModelForm(forms.ModelForm):
    trainings = forms.CharField(widget=forms.Textarea(),label="Entrenamientos",required=False,disabled=True)
    search=forms.CharField(label='Buscar Entrenamientos',max_length=20, required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Buscar Entrenamiento'}),)
    class Meta:
        model =Model
        fields = 'name','trainings','search',
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
        }
        
    def save(self,_list):

        m=Model.objects.create(
            name=self.cleaned_data.get('name'),
            #file_model=f"{self.cleaned_data.get('name')}.txt"
        )
        for l in _list:
            Training.objects.get(pk=l).models.add(m)
        d=[]
        l=[]
        for t in m.training_model.all():
            for measuring in t.measuring_trainig.all():
                d.append(measuring.get_list_data()) 
                l.append(measuring.get_predict_index())
        print(d)
        print(l)
        
        
class ModelUpdateForm(forms.ModelForm):
    class Meta:
        model =Model
        fields = 'name',
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
        }
    def update(self,pk):
        obj=Model.objects.get(pk=pk)
        obj.name=self.cleaned_data['name']
        obj.save()
        
    