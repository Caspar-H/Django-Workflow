from django import forms
from django.forms import TextInput

from sitedb.models import Site

STATES = (
    ('ACT', 'ACT'),
    ('NSW', 'NSW'),
    ('VIC', 'VIC'),
    ('QLD', 'QLD'),
    ('SA', 'SA'),
    ('WA', 'WA'),
    ('NT', 'NT'),
    ('TAS', 'TAS'),
)

POLE_OWNER = (
    ('Ausgrid Pole', 'Ausgrid Pole'),
    ('City of Sydney Council - Smart Pole', 'City of Sydney Council - Smart Pole'),
)


class SiteForm(forms.ModelForm):

    class Meta:
        model = Site
        # fields = ['site_name', 'site_lat', 'site_long', 'site_cluster', 'site_state',
        #           'site_pole_owner', 'site_pole_id', 'site_rfnsa_id', 'site_acma_id']
        fields = ['site_name', 'site_lat', 'site_long', 'site_state']
        widgets = {
            'site_state': forms.Select(choices=STATES),
            # 'site_pole_owner': forms.Select(choices=POLE_OWNER),
        }

    def __init__(self, *args, **kwargs):
        super(SiteForm, self).__init__(*args, **kwargs)
        # self.fields['site_rfnsa_id'].required = False
        # self.fields['site_acma_id'].required = False

