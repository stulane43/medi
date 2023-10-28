import os
from pathlib import Path
import dotenv

dotenv.load_dotenv('.env')

BASE_DIR = Path(os.path.abspath(__file__)).parents[2]

SLACK_BOT = {
    'BOT_TOKEN': os.environ['BOT_TOKEN'],
    'APP_TOKEN': os.environ['APP_TOKEN'],
    'SIGNING_SECRET': os.environ['SIGNING_SECRET'],
    'WEBHOOK': os.environ['WEBHOOK'],
    'TRACKER_SERVICE': 'mediTracker'
}

DATABASES = {
    'server': {
        'HOST': os.environ['SERVER_HOST'],
        'USER': os.environ['SERVER_USER'],
        'PASS': os.environ['SERVER_PASS'],
        'BIND_ADDRESS': os.environ['BIND_ADDRESS'],
        'BIND_PORT': os.environ['BIND_PORT']
    },
    'mysql': {
        'DATABASE': os.environ['DATABASE'],
        'USER': os.environ['DATABASE_USER'],
        'PASS': os.environ['DATABASE_PASS']
    },
    'query': {
        'ALL_PATIENTS': 'select * from patients',
        'ALL_MED_TIMES': 'select * from medication_times',
        'TRACKER_STATUS': 'select * from medi_tracker order by id desc limit 1'
    }
}

TEMPLATES = {
    'APP_HOME': 'src/app/templates/apphome.json'
}

DF_ASTYPE = {
    'PATIENTS': {
        'patient_name': 'string',
        'age': 'int',
        'medication': 'string',
        'times_taken_per_day': 'int'
    },
    'PATIENT_MEDICATIONS': {
        'patient_name': 'string',
        'medication': 'string',
        'times_taken_per_day': 'int'
    },
    'MEDICATION_TIMES': {
        'patient_name': 'string',
        'medication': 'string',
        'dosage_amount': 'string',
        'medication_time': 'datetime64[s]'
    },
    'MEDICATION_HISTORY': {
        'patient_name': 'string',
        'medication': 'string',
        'dosage_amount': 'string',
        'time_given': 'datetime64[s]',
        'time_category': 'string',
        'given_by': 'string',
        'target_time': 'string'
    },
    'TRACKER_STATUS': {
        'status': 'string'
    }
}
