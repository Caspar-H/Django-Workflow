from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
import pdfplumber
import os
import xlsxwriter


# Create your views here.
from WorkflowEngine.settings import BASE_DIR


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
