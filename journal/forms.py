from django.forms import ModelForm, DateInput, TimeInput
from .models import *


class BugForm(ModelForm):
    class Meta:
        model = Bug
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BugForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-3 shadow-sm'


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-3 shadow-sm'


class OrnithologyObservationForm(ModelForm):
    class Meta:
        model = OrnithologyObservation
        fields = ['longitude',
                  'latitude', 'altitude', 'species', 'date', 'time', 'image', 'note', 'min_no', 'max_no',
                  'sociality', 'age', 'sex', 'voice', 'breeding_code', 'habitats', 'locality', 'region', ]

        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'time': TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'longitude': 'Longitude',
            'latitude': 'Latitude',
            'altitude': 'Altitude',
            'species': 'Species',
            'date': 'Observation Date',
            'time': 'Observation Time',
            'note': 'Notes',
            'min_no': 'Minimum Number of Individuals',
            'max_no': 'Maximum Number of Individuals',
            'sociality': 'Sociality',
            'age': 'Age',
            'sex': 'Sex',
            'voice': 'Voice',
            'breeding_code': 'Breeding Code',
            'habitats': 'Habitat description',
            'locality': 'Locality',
            'region': 'Region',
            'image': 'Select an image',
        }

    def __init__(self, *args, **kwargs):
        super(OrnithologyObservationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control  shadow-sm w-100'
