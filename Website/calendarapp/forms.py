from django.forms import ModelForm, DateInput
from calendarapp.models import Event
from django import forms
from app.models import Formation,Salle

class EventForm(ModelForm):
    class Meta:
        model = Event
        salle = forms.ModelChoiceField(queryset=Salle.objects.all(),
                                             empty_label='',
                                             widget=forms.Select(attrs={'class': 'form-select salle' 'input', 'id': 'selection'}))
        fields = ["title", "salle", "formation", "start_time", "end_time"]
        # datetime-local is a HTML5 input type
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["formation"].queryset = Formation.objects.filter(active=False)
                    
        
        
        
