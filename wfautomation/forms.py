from django import forms

from wfautomation.models import POIDescription, SiteSurveyDocuments


class POIForm(forms.ModelForm):

    class Meta:
        model = POIDescription
        fields = ['poi_1', 'poi_2', 'poi_3', 'poi_4', 'poi_5']

    def __init__(self, *args, **kwargs):
        super(POIForm, self).__init__(*args, **kwargs)
        self.fields['poi_2'].required = False
        self.fields['poi_3'].required = False
        self.fields['poi_4'].required = False
        self.fields['poi_5'].required = False


class SiteSurveyDocumentsForm(forms.ModelForm):
    class Meta:
        model = SiteSurveyDocuments
        fields = ('poi_1_description', 'poi_1_measurement', 'poi_1_document',
                  'poi_2_description', 'poi_2_measurement', 'poi_2_document',
                  'poi_3_description', 'poi_3_measurement', 'poi_3_document',
                  'poi_4_description', 'poi_4_measurement', 'poi_4_document',
                  'poi_5_description', 'poi_5_measurement', 'poi_5_document',)

