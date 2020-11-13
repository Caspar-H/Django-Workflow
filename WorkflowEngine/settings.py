"""
Django settings for WorkflowEngine project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nfn#6a-0cuqs=%mvxy&s56p9ur2ibf8xe@id=@2lyrykg8lvp!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sitedb',
    'userlogin',
    'crispy_forms',
    'comment',
    'mptt',
    'notifications',
    'fileupload',
    'wfautomation',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'WorkflowEngine.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'WorkflowEngine.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'ranrefresh',
    #     'USER': 'caspar',
    #     'PASSWORD': 'tpg12345',
    #     'PORT': 30010,
    #     'HOST': '10.224.44.127',
    #     'OPTIONS': {
    #         "init_command": "SET foreign_key_checks = 0;",
    #     }
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ranrefresh',
        'USER': 'root',
        'PASSWORD': 'hpf6600',
        'PORT': 3306,
        'HOST': 'localhost',
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Sydney'
# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# for file upload
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Custom Django auth settings
AUTH_USER_MODEL = 'userlogin.User'

LOGIN_URL = 'userlogin:login'

LOGOUT_URL = 'userlogin:logout'

LOGIN_REDIRECT_URL = 'sitedb:home'

LOGOUT_REDIRECT_URL = 'userlogin:login'

# Email related
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'smtp.caspar@gmail.com'
EMAIL_HOST_PASSWORD = 'smtp6600'

# Minio file server
MINIO_HOST = 'localhost:9000'

# Camunda host address
CAMUNDA_HOST = 'http://localhost:8080/engine-rest'
WORKFLOW_NAME = 'SITESURVEY'
ACTIVATION_WORKFLOW_NAME = 'rollout_workflow_v2'

# Activation Program sub milestone list
# ACTIVATION_LIST_READY = ['neighbouring_sites', 'cme_dump', 'testing_scenario', 'testing_route', 'acma_check',
#                          'emeg_status', 'l1800_simulations', 'overlap_analysis',
#                          'cell_list_update_based_on_simulation', 'site_power_up', 'shut_down_close_macrol700',
#                          'activate_small_cell', 'pre_testing', 'collect_tx_design_info', 'allocate_id',
#                          'pci_conflict', 'rf_script', 'check_rf_script', 'ran_script', 'dark_fibre_check',
#                          'tx_cutover', 'apply_cr', 'rfnsa_update', 'cell_group_define', ]
ACTIVATION_LIST_READY = [
    'repowering_up', 'inter_transmission_merge', 'rfi', 'rfnsa_check', 'acma_check', 'bbu_status_check', 'shutdown_cr',
    'ssv_pre_cutover', 'naming_convention', 'bbu_cutover_cr', 'bbu_cutover', 'site_list_check', 'overlap_simulation',
    'pci_conflict', 'rfnsa_update', 'acma_update', 'prs_cellgroup', 'rf_script', 'activation_cr', 'emeg_check',
]
# ACTIVATION_ACTIVATION_READY = ['site_activation', 'service_verification', 'parameter_audit', 'day1_kpi_monitoring', ]
ACTIVATION_ACTIVATION_READY = [
    'cell_activation', 'ssv_post_cutover',
]
# ACTIVATION_POST_ACTIVATION = ['ric_checklist', 'isn_report_and_upload', 'apply_cr_for_phase2_parameters',
#                               'phase2_parameters_kpi_monitoring', 'rf_script_for_phase2_parameters', 'dsa7_report', ]
ACTIVATION_POST_ACTIVATION = [
    'service_notification', 'isn_upload', 'dsa7_upload',
]
