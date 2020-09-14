from django.http import HttpResponse
from django.shortcuts import render, redirect
import pandas as pd
import pdfplumber
import os
import xlsxwriter

# Create your views here.
from django.urls import reverse
from django.views.generic import UpdateView, CreateView

from WorkflowEngine.settings import BASE_DIR, MEDIA_ROOT
from sitedb.models import SiteLogInfo, Site
from wfautomation.forms import POIForm, SiteSurveyDocumentsForm
from wfautomation.models import POIDescription, SiteSurveyDocuments


def pdf_extraction(request):
    file_path = os.path.join(BASE_DIR, 'wfautomation/documents_folder/4361_Noosa 2_Sectorisation_FC_Ver6_11102017.pdf')
    # filepath = "D:/Python Project/005 VHA Macro site workflow/4361_Noosa 2_Sectorisation_FC_Ver6_11102017.pdf"
    pdf_file = pdfplumber.open(file_path)
    p4 = pdf_file.pages[4]
    p4_table = p4.extract_tables()[1]

    site_info = {}
    list_a = []
    for item in p4_table:
        key_name = item[0]
        if key_name:
            site_info[key_name] = [x for x in item[1:] if x]

    site_info_select = {k: site_info[k] for k in
                        ('SECTOR No.', 'AZIMUTH', 'HEIGHT AT JCL ANTENNA', 'ANTENNA TYPE', 'DIMENSIONS (L x W x D)',
                         'OPERATOR', 'FIBRE TYPE', 'FIBRE LENGTH') if k in site_info}

    df = pd.DataFrame(site_info_select)
    output_path = os.path.join(BASE_DIR, 'wfautomation/documents_folder/export_dataframe.xlsx')
    df.to_excel(output_path, index=False, header=True)

    return HttpResponse('Excel File Exported')


def generate_site_survey_report(request):
    # Create an new Excel file and add a worksheet.
    file_path = os.path.join(BASE_DIR, 'wfautomation/documents_folder/site_survey_report.xlsx')
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()

    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 30)

    # image_width = 140.0
    # image_height = 182.0
    #
    # cell_width = 64.0
    # cell_height = 20.0
    #
    # x_scale = cell_width / image_width
    # y_scale = cell_height / image_height

    # Insert an image.
    image_path_1 = os.path.join(BASE_DIR, 'wfautomation/documents_folder/Extra Photos a.jpg')
    worksheet.write('A2', 'Site Survey Photo 1:')
    worksheet.insert_image('B2', image_path_1,
                           {'x_scale': 0.11, 'y_scale': 0.11})

    # Insert an image offset in the cell.
    image_path_2 = os.path.join(BASE_DIR, 'wfautomation/documents_folder/Extra Photos b.jpg')
    worksheet.write('A18', 'Site Survey Photo 2:')
    worksheet.insert_image('B18', image_path_2,
                           {'x_scale': 0.11, 'y_scale': 0.11})

    workbook.close()
    return HttpResponse('Site Survey Report Generated')


class POICreateView(CreateView):
    model = POIDescription
    form_class = POIForm
    # slug_field = 'site_id'
    # slug_url_kwarg = 'site_id'
    template_name = 'wfautomation/poi_update.html'

    def form_valid(self, form, **kwargs):
        """If the form is valid, save the associated model."""
        for item in form.changed_data:
            new_log = SiteLogInfo()
            new_log.log_user = self.request.user.get_username()
            new_log.log_site_id = self.kwargs['site_id']
            new_log.log_info = '{} Changed to {}'. \
                format(POIDescription._meta.get_field(item).verbose_name, form.cleaned_data[item])
            new_log.save()
        # When creating with Foreign Key, this need to be added
        form.instance.site_id = self.kwargs['site_id']
        self.object = form.save(commit=False)
        self.object = form.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.cleaned_data)
        return HttpResponse("form is invalid.. this is just an HttpResponse object")

    def get_context_data(self, **kwargs):
        context = super(POICreateView, self).get_context_data(**kwargs)
        context['site_id'] = self.kwargs['site_id']
        context['task_name'] = self.kwargs['task_name']
        context['ins_id'] = self.kwargs['ins_id']

        return context

    def get_success_url(self, **kwargs):
        print(self.kwargs['site_id'])
        return reverse('sitedb:complete_task', args=[self.kwargs['task_name'],
                                                     self.kwargs['site_id'],
                                                     self.kwargs['ins_id']
                                                     ])
        # return redirect('sitedb:complete_task', site_id=self.kwargs['site_id'], task_name=self.kwargs['task_name'],
        #                 ins_id=self.kwargs['ins_id'])


def upload_site_survey(request, task_name, site_id, ins_id):
    if request.method == 'POST':
        form = SiteSurveyDocumentsForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.site_id = site_id
            print(site_id)
            form.save()
            # return reverse('sitedb:complete_task', args=[task_name, site_id, ins_id])
            return redirect('sitedb:complete_task', site_id=site_id, task_name=task_name,
                            ins_id=ins_id)
        else:
            return HttpResponse("Form is not valid")
    else:
        form = SiteSurveyDocumentsForm()
        site_poi_description = list(POIDescription.objects.filter(site_id=site_id).values())[0]
        print(site_poi_description)

        return render(request, 'wfautomation/upload_site_survey.html', locals())


def generate_site_survey_report2(request, task_name, site_id, ins_id):
    file_path = os.path.join(MEDIA_ROOT, 'site_{0}/site_survey_report.xlsx'.format(site_id))
    print(MEDIA_ROOT)
    print(file_path)
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()

    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 30)

    site_documents = list(SiteSurveyDocuments.objects.filter(site_id=site_id).values())[0]
    site_info = list(Site.objects.filter(site_id=site_id))[0]
    poi_description = list(POIDescription.objects.filter(site_id=site_id).values())[0]
    output = site_documents['poi_3_measurement']

    # Site Basic Info
    worksheet.write('A2', 'Site ID')
    worksheet.write('B2', site_info.site_id)
    worksheet.write('A3', 'Site Name')
    worksheet.write('B3', site_info.site_name)
    worksheet.write('A4', 'Site Latitude')
    worksheet.write('B4', site_info.site_lat)
    worksheet.write('A5', 'Site Longitude')
    worksheet.write('B5', site_info.site_long)
    worksheet.write('A6', 'Site State')
    worksheet.write('B6', site_info.site_state)

    # Site Survey POI - 1 Photos.
    worksheet.write('A11', 'POI 1')
    worksheet.write('A12', poi_description['poi_1'])
    worksheet.write('A14', 'POI 1 Feedback')
    worksheet.write('A15', site_documents['poi_1_description'])
    worksheet.write('A17', 'POI 1 Measurement')
    worksheet.write('A18', site_documents['poi_1_measurement'])

    worksheet.write('A20', 'POI 1 Photo')
    image_path_poi_1 = os.path.join(MEDIA_ROOT, site_documents['poi_1_document'])
    worksheet.insert_image('A21', image_path_poi_1,
                           {'x_scale': 0.11, 'y_scale': 0.11})

    # Site Survey POI - 2 Photos.
    worksheet.write('H11', 'POI 2')
    worksheet.write('H12', poi_description['poi_2'])
    worksheet.write('H14', 'POI 2 Feedback')
    worksheet.write('H15', site_documents['poi_2_description'])
    worksheet.write('H17', 'POI 2 Measurement')
    worksheet.write('H18', site_documents['poi_2_measurement'])

    worksheet.write('H20', 'POI 2 Photo')
    image_path_poi_2 = os.path.join(MEDIA_ROOT, site_documents['poi_2_document'])
    worksheet.insert_image('H21', image_path_poi_2,
                           {'x_scale': 0.11, 'y_scale': 0.11})

    # Site Survey POI - 3 Photos.
    worksheet.write('Q11', 'POI 3')
    worksheet.write('Q12', poi_description['poi_3'])
    worksheet.write('Q14', 'POI 3 Feedback')
    worksheet.write('Q15', site_documents['poi_3_description'])
    worksheet.write('Q17', 'POI 3 Measurement')
    worksheet.write('Q18', site_documents['poi_3_measurement'])

    worksheet.write('Q20', 'POI 3 Photo')
    image_path_poi_3 = os.path.join(MEDIA_ROOT, site_documents['poi_3_document'])
    worksheet.insert_image('Q21', image_path_poi_3,
                           {'x_scale': 0.11, 'y_scale': 0.11})

    # Site Survey POI - 4 Photos.
    worksheet.write('Z11', 'POI 4')
    worksheet.write('Z12', poi_description['poi_4'])
    worksheet.write('Z14', 'POI 4 Feedback')
    worksheet.write('Z15', site_documents['poi_4_description'])
    worksheet.write('Z17', 'POI 4 Measurement')
    worksheet.write('Z18', site_documents['poi_4_measurement'])

    worksheet.write('Z20', 'POI 4 Photo')
    image_path_poi_4 = os.path.join(MEDIA_ROOT, site_documents['poi_4_document'])
    worksheet.insert_image('Z21', image_path_poi_4,
                           {'x_scale': 0.11, 'y_scale': 0.11})

    # Site Survey POI - 5 Photos.
    worksheet.write('AJ11', 'POI 5')
    worksheet.write('AJ12', poi_description['poi_5'])
    worksheet.write('AJ14', 'POI 5 Feedback')
    worksheet.write('AJ15', site_documents['poi_5_description'])
    worksheet.write('AJ17', 'POI 5 Measurement')
    worksheet.write('AJ18', site_documents['poi_5_measurement'])

    worksheet.write('AJ20', 'POI 5 Photo')
    image_path_poi_5 = os.path.join(MEDIA_ROOT, site_documents['poi_5_document'])
    worksheet.insert_image('AJ21', image_path_poi_5,
                           {'x_scale': 0.11, 'y_scale': 0.11})

    workbook.close()
    return redirect('sitedb:complete_task', site_id=site_id, task_name=task_name,
                    ins_id=ins_id)
