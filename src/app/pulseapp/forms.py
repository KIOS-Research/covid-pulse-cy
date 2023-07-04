import datetime
from django import forms
from . import models
import re
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.forms import DateTimeInput

max_date = datetime.date(2100,1,1)
class DateInput(forms.DateInput):
    input_type = 'date'

class OTPAuthenticationForm(AuthenticationForm):
    def clean(self):
        super(OTPAuthenticationForm, self).clean()

class WWWmeasureDataFormSet(forms.ModelForm):
    type = forms.CharField(max_length = 200, required = False)
    unit = forms.CharField(max_length = 200, required = False)
    class Meta:
        model = models.wwmeasure

        fields = [
            'id',
            'covtype',
            'analysisdate',
            'value',
            'notes'
        ]
        labels = {
            'covtype': 'Type',
        }
        widgets = {
            'analysisdate': forms.TextInput (attrs = {'type': 'date'})
        }

    def clear(self):
        """Backend Validation Checks"""
        cleaned_data = super().clean()

    def __init__(self, *args, **kwargs):
        super(WWWmeasureDataFormSet, self).__init__(*args, **kwargs)
        self.fields['covtype'].widget.attrs['required'] = 'required'

class SampleDataForm(forms.ModelForm):
    analysis_date = forms.DateField(label = 'Analysis Date', widget = forms.TextInput (attrs = {'type': 'date'} ))
    class Meta:
        model = models.sampledata
        fields = [
            'id',
            'location',
            'datestart',
            'dateend',
            'notes'
        ]
        labels = {
            'id': 'No',
            'location': 'Location',
            'datestart': 'Start Date',
            'dateend': 'End Date',
            'notes': 'Sample Notes'
        }
        widgets = {
            'datestart': forms.TextInput (attrs = {'type': 'date'}),
            'dateend': forms.TextInput (attrs = {'type': 'date'}),
        }

    def clear(self):
        """Backend Validation Checks"""
        cleaned_data = super().clean()
        datetimestart = cleaned_data.get('datestart')
        datetimeend = cleaned_data.get('dateend')
        analysis_date = cleaned_data.get('analysis_date')


        if datetimeend < datetimestart:
            raise forms.ValidationError("End date should be greater than start date.")

        if analysis_date < datetimeend:
            raise forms.ValidationError("Analysis date should be greater than end date.")


    def __init__(self, *args, **kwargs):
        super(SampleDataForm, self).__init__(*args, **kwargs)
        self.fields['location'].widget.attrs['required'] = 'required'
        self.fields['datestart'].widget.attrs['required'] = 'required'
        self.fields['dateend'].widget.attrs['required'] = 'required'
        self.fields['datestart'].widget.attrs['onchange'] = 'set_max_date(this)'
        self.fields['dateend'].widget.attrs['onchange'] = 'set_max_date_analysis(this)'


class TrendsForm(forms.ModelForm):
    class Meta:
        model = models.trends
        fields = [
            'fromdate',
            'todate',
            'loginname',
        ]
        labels = {
            'fromdate':'Start Day',
            'todate':'End Day',
            'loginname':'login user',
        }

    def clear(self):
        """Backend Validation Checks"""
        cleaned_data = super().clean()
        fromdate = cleaned_data.get('fromdate')
        todate = cleaned_data.get('todate')

        if fromdate is None:
            raise forms.ValidationError("Start date can not be empty")

        if todate is None:
            raise forms.ValidationError("End date can not be empty")

        if todate < fromdate:
            raise forms.ValidationError("End date should be greater than start date.")

    def __init__(self, *args, **kwargs):
        super(TrendsForm, self).__init__(*args, **kwargs)
        self.fields['fromdate'].widget = forms.TextInput (attrs = {'type': 'date', 'max': datetime.date.today ()})
        self.fields['todate'].widget = forms.TextInput (attrs = {'type': 'date', 'max': datetime.date.today ()})
        self.fields['fromdate'].widget.attrs['required'] = 'required'
        self.fields['todate'].widget.attrs['required'] = 'required'
        self.fields['fromdate'].widget.attrs['onchange'] = 'set_max_date(this)'

class TrendsFormSet(forms.ModelForm):
    station = forms.CharField(max_length = 200, required = False)
    class Meta:
        model = models.trends
        fields = [
            'fromdate',
            'todate',
            'loginname',
            'samplestationid',
            'value'
        ]
        labels = {

            'samplestationid':'Sample Station',
            'value':'Value'
        }


    def clear(self):
        """Backend Validation Checks"""
        cleaned_data = super().clean()
        samplestationid = cleaned_data.get('samplestationid')
        value = cleaned_data.get ('value')

        if samplestationid is None:
            raise forms.ValidationError("Please choose a sample station")

        # if value is None:
        #     raise forms.ValidationError("Value can not be empty")

    def __init__(self, *args, **kwargs):
        super(TrendsFormSet, self).__init__(*args, **kwargs)
        #self.fields['sampledata_zone'].widget.attrs['onchange'] = "zonechange()"
        #self.fields['sampledata_samplingpoint'].widget.attrs['onchange'] = "samplingpointchange()"
        # self.fields['value'].widget.attrs['required'] = 'required'
        self.fields['station'].widget.attrs['readonly'] = True

class TrendsEditForm(forms.ModelForm):
    class Meta:
        model = models.trends
        fields = [
            'fromdate',
            'todate',
            'loginname',
            'samplestationid',
            'value'
        ]
        labels = {
            'fromdate':'Start Day',
            'todate':'End Day',
            'loginname':'login user',
            'samplestationid':'Sample Station',
            'value': 'Value'
        }

    def clear(self):
        """Backend Validation Checks"""
        cleaned_data = super().clean()
        fromdate = cleaned_data.get('fromdate')
        todate = cleaned_data.get('todate')
        samplestationid = cleaned_data.get ('samplestationid')
        value = cleaned_data.get ('value')

        if samplestationid is None:
            raise forms.ValidationError ("Please choose a sample station")

        if value is None:
            raise forms.ValidationError("Value can not be empty")

        if fromdate is None:
            raise forms.ValidationError("Start date can not be empty")

        if todate is None:
            raise forms.ValidationError("End date can not be empty")

        if todate < fromdate:
            raise forms.ValidationError("End date should be greater than start date.")

    def __init__(self, *args, **kwargs):
        super(TrendsEditForm, self).__init__(*args, **kwargs)
        self.fields['fromdate'].widget.attrs['required'] = 'required'
        self.fields['todate'].widget.attrs['required'] = 'required'
        self.fields['value'].widget.attrs['required'] = 'required'
        self.fields['samplestationid'].widget.attrs['required'] = 'required'
        self.fields['fromdate'].widget = forms.TextInput (attrs = {'type': 'date','max':datetime.date.today()})
        self.fields['todate'].widget = forms.TextInput (attrs = {'type': 'date','max':datetime.date.today()})
        self.fields['fromdate'].widget.attrs['onchange'] = 'set_max_date(this)'

class VariantsForm(forms.ModelForm):
    n_variants= forms.ChoiceField(label='Variant')
    new_variant=forms.CharField(max_length = 200, required = False)
    class Meta:
        model = models.variants
        fields = [
            'location',
            'sampleid',
            'Lineage',
            'VariantType',
            'comment',
            'dateend',
        ]
        labels = {
            'location':'Sample Station',
            'Lineage':'Main Lineage',
            'VariantType':'Variant',
            'comment': 'Comment',
            'dateend': 'End Date'
        }

    def clean(self):
        """Backend Validation Checks"""
        cleaned_data = super().clean()
        selected_variant=cleaned_data.get('n_variants')
        location = cleaned_data.get('location')
        dateend = cleaned_data.get('dateend')

        if location is None:
            raise forms.ValidationError("Please choose a location")

        if dateend is None:
            raise forms.ValidationError("End date can not be empty")

        if selected_variant=='Other':
            obj, created=models.variantType.objects.get_or_create(name=cleaned_data['new_variant'])
            cleaned_data['VariantType']=obj
        else:
            variant=models.variantType.objects.filter(pk=selected_variant)
            if len(variant)!=0:
                cleaned_data['VariantType'] = variant[0]

        if cleaned_data['VariantType'] is None:
            raise forms.ValidationError("Please choose a variant")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(VariantsForm, self).__init__(*args, **kwargs)
        self.fields['dateend'].widget = forms.TextInput (attrs = {'type': 'date', 'max': datetime.date.today ()})
        self.fields['dateend'].widget.attrs['required'] = 'required'
        self.fields['location'].widget.attrs['required'] = 'required'
        variants= self.fields['VariantType']
        n_variants= self.fields['n_variants']
        n_variants.choices= list(variants.choices)
        n_variants.choices.append(tuple(('Other', 'Other')))
        n_variants.widget.attrs['onchange'] = 'check_select(this)'
        try:
            self.initial['n_variants'] = self.initial['VariantType']
        except:
            pass


class VariantsTypeForm(forms.ModelForm):
    class Meta:
        model = models.variantType
        fields = [
            'name',
        ]
        labels = {
            'name':'Variant Name',
        }


    # def clean(self):
    #     """Backend Validation Checks"""
    #     cleaned_data = super().clean()
    #     samplestationid = cleaned_data.get('samplestationid')
    #     value = cleaned_data.get ('value')
    #
    #     if samplestationid is None:
    #         raise forms.ValidationError("Please choose a sample station")
    #
    #     # if value is None:
    #     #     raise forms.ValidationError("Value can not be empty")

    def __init__(self, *args, **kwargs):
        super(VariantsTypeForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True

