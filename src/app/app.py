from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt import App
from slack_sdk import WebClient
import pandas as pd

import json
import logging
from pathlib import Path
import datetime as datetime_base
from datetime import datetime
import os

import database as db
from . import views
from . import alerts
import settings
import utils

app = App(token=settings.SLACK_BOT['BOT_TOKEN'], signing_secret=settings.SLACK_BOT['SIGNING_SECRET'])
current_path = Path().absolute()
db.commands.create_tables(True)

@app.event("app_home_opened")
def appHomeOpened(client: WebClient, event):
    '''
    Visualize App Home Surface
    '''
    try:
        user_info = client.users_info(user=event['user'])
        result = db.commands.read(settings.DATABASES['query']['ALL_PATIENTS'])
        patient_data = result.to_dict('records')
        if patient_data == []:
            os.chdir('/home/slane/medi')
            print(current_path)
            with open(settings.TEMPLATES['APP_HOME'], 'r') as f:
                view = json.load(f)
        else:
            builder = views.app_home_opened(user_info.data, patient_data)
            view = builder.view
        client.views_publish(user_id=user_info.data['user']['id'], view=view)
    except Exception as e:
        logging.error(e)

@app.action("select-action-patient_name")
def selected_patient(ack):
    ack()
    pass
    
@app.action("date-action-selected")
def selected_date(ack):
    ack()
    pass
    
@app.action("button-action-show_patient_history")
def patient_history(ack, body, client: WebClient):
    '''
    Show modal of patient history
    '''
    try:
        ack()
        block_id = body['actions'][0]['block_id']
        patient_selected = body['view']['state']['values'][block_id]['select-action-patient_name']['selected_option']['value']
        date_selected = body['view']['state']['values'][block_id]['date-action-selected']['selected_date']
        history_result = db.commands.read(f"select * from patient_medication_history where patient_name = '{patient_selected}' and CAST(time_given as DATE) = '{date_selected}'")
        patient_history = history_result.to_dict('records')
        patient_result = db.commands.read(settings.DATABASES['query']['ALL_PATIENTS'])
        patient_data = patient_result.to_dict('records')
        if patient_history == []:
            builder = views.app_home_opened(body, patient_data)
            view = builder.view
        else:
            builder = views.app_home_patient_history(body, patient_data, patient_history)
            view = builder.view
        client.views_publish(user_id=body['user']['id'], view=view)
    except Exception as e:
        logging.error(e)

@app.action("action-settings")
def settings_modal(ack, body, client: WebClient):
    '''
    Show settings and give users ability to add and remove patients
    '''
    all_patient_data = []
    try:
        ack()
        patient_result = db.commands.read(settings.DATABASES['query']['ALL_PATIENTS'])
        tracker_status = db.commands.read(settings.DATABASES['query']['TRACKER_STATUS'])
        tracker_data = tracker_status.to_dict('records')
        patient_data = patient_result.to_dict('records')
        for patient in patient_data:    
            med_data = db.commands.read(f"Select * from patient_medications where patient_name='{patient['patient_name']}'")
            patient_medications = med_data.to_dict('records')
            if patient_medications == []:
                continue
            medications = []
            for p in patient_medications:
                medications.append(p['medication'])
            all_patient_data.append({
                "patient_name": patient['patient_name'],
                "age": patient['age'],
                "medications": medications
            })
        

        if patient_data == []:
            builder = views.settings_modal(all_patient_data, tracker_data[0]['status'])
            view = builder.view
        else:
            builder = views.settings_modal(all_patient_data, tracker_data[0]['status'])
            view = builder.view
        client.views_open(trigger_id=body['trigger_id'], view_id=body['view']['id'], hash = body["view"]["hash"], notify_on_close = True, view=view)
    except Exception as e:
        logging.error(e)
        
@app.action("action_edit_patient")
def action_edit_patient(ack, body, client: WebClient):        
    '''
    show edit options for a patient in medi
    '''
    #This is still under development - doesn't do anything yet
    try:
        ack()
        edit_selection = body['actions'][0]['selected_option']['value']
        patient_selected = utils.str_utils.splitAction_getName(edit_selection)
        patient_data = {
            "patient_name": patient_selected,
        }
        builder = views.addPatientContinued_modal(patient_data)
        client.views_update(view_id=body['view']['root_view_id'], view=builder.view)
    except Exception as e:
        logging.error(e)
            
@app.action("action-add_patient_modal")
def add_patient_modal(ack, body, client: WebClient):
    '''
    show options for adding patient to medi
    '''
    try:
        ack()
        builder = views.addPatient_modal()
        client.views_push(trigger_id=body['trigger_id'], view_id=body['view']['id'], hash=body['view']['hash'], notify_on_close=True, view=builder.view)
    except Exception as e:
        logging.error(e)
        
@app.view("addpatient_modal_continued")
def add_patient_modal_continued(ack, body, client: WebClient, view):
    '''
    show continued options for adding patient to medi
    - based on how many times medication is taken per day
    '''
    try:
        ack()
        patient_data = {
            "patient_name": view['state']['values']['patient_name']['input-name']['value'],
            "age": int(view['state']['values']['patient_age']['input-age']['value']),
            "medication": view['state']['values']['patient_medication']['input-medication']['value'],
            "times_taken_per_day": int(view['state']['values']['patient_times_taken']['input-times_taken']['value'])
        }
        builder = views.addPatientContinued_modal(patient_data)
        client.views_update(view_id=body['view']['root_view_id'], view=builder.view)
    except Exception as e:
        logging.error(e)
        
@app.view("action-add_patient")
def action_add_patient(ack, view):
    '''
    adds a new patient to medi
    '''
    patient_data = []
    medication_times = []
    try:
        patient_metadata = utils.str_utils.json_acceptable_string(view['private_metadata'])
        patient_data.append(patient_metadata)
        total_med_times = int(len(view['state']['values'])/2)
        for i in range(total_med_times):
            n = i + 1
            medication_times.append(
                {
                    "patient_name": patient_metadata['patient_name'],
                    "medication": patient_metadata['medication'],
                    "dosage_amount": view['state']['values'][f"dosage_amount_{n}"]['input-dosage_amount']['value'],
                    "medication_time": view['state']['values'][f"time_taken_{n}"]['action-time_taken']['selected_time']
                }
            )
        patient_medications = [
            {
                "patient_name": patient_metadata['patient_name'],
                "medication": patient_metadata['medication'],
                "times_taken_per_day": patient_metadata['times_taken_per_day']
            }
        ]
        patient_data_df = pd.DataFrame(patient_data)
        patient_data_dfat = patient_data_df.astype(settings.DF_ASTYPE['PATIENTS'])
        patient_medications_df = pd.DataFrame(patient_medications)
        patient_medications_dfat = patient_medications_df.astype(settings.DF_ASTYPE['PATIENT_MEDICATIONS'])
        medication_times_df = pd.DataFrame(medication_times)
        medication_times_dfat = medication_times_df.astype(settings.DF_ASTYPE['MEDICATION_TIMES'])
        db.commands.insert(table="patients", df=patient_data_dfat)
        db.commands.insert(table="patient_medications", df=patient_medications_dfat)
        db.commands.insert(table="medication_times", df=medication_times_dfat)
        builder = views.patient_added(patient_data)
        ack(response_action="update", view=builder.view)
    except Exception as e:
        logging.error(f'***App-Error*** action_add_patient: {e}')
    
@app.view("close_view")
def close_modal_view(ack):
    ack(response_action="clear")
    
@app.action("action-remove_patient_modal")
def remove_patient_modal(ack, body, client: WebClient):
    '''
    show options for adding patient to medi
    '''
    try:
        ack()
        patient_result = db.commands.read(settings.DATABASES['query']['ALL_PATIENTS'])
        patient_data = patient_result.to_dict('records')
        if patient_data == []:
            pass
        else:
            builder = views.removePatient_modal(patient_data)
        client.views_push(trigger_id=body['trigger_id'], view_id=body['view']['id'], hash=body['view']['hash'], notify_on_close=True, view=builder.view)
    except Exception as e:
        logging.error(e)
        
@app.action("action-select_remove_patient")
def select_remove_patient(ack):
    ack()
    pass
        
@app.action("action-remove_patient")
def action_remove_patient(ack, body, client: WebClient):
    '''
    deletes a patient in medi
    '''
    try:
        ack()
        state_value = body['view']['state']['values']
        key = list(state_value.keys())[0]
        patient_selected = body['view']['state']['values'][key]['action-select_remove_patient']['selected_option']['value']
        db.commands.delete_patient_data(value=patient_selected)
        builder = views.patient_removed(patient_selected)
        client.views_push(trigger_id=body['trigger_id'], view_id=body['view']['id'], hash=body['view']['hash'], notify_on_close=True, view=builder.view)
    except Exception as e:
        logging.error(f'***App-Error*** action_add_patient: {e}')

@app.action("button-action-mark-medication_given")
def give_medication_modal(ack, body, client: WebClient):
    '''
    show give_medication modal when user clicks on the give_medication button
    '''
    patient_medication = []
    dosages = []
    target_times = []
    try:
        ack()
        try:
            patient = body['view']['state']['values']['give_medication']['action-user_selected']['selected_option']['value']
        except:
            patient = body['actions'][0]['value']
        patient_result = db.commands.get_patient_data(patient)
        patient_data = patient_result['patient']._mapping
        for medication in patient_result['med_times']:
            patient_medication.append(medication._mapping['medication'])
            dosages.append(medication._mapping['dosage_amount'])
            med_time = str(medication._mapping['medication_time'])
            target_time = utils.date_utils.splitDateTime_getHoursMinutes(med_time)
            target_times.append(f"{target_time['hour']}:{target_time['minute']}")
        med_data = utils.str_utils.remove_list_dups(patient_medication)
        builder = views.give_medication_modal(patient_data=patient_data, medication_data=med_data, dosages=dosages, target_times=target_times, user_id=body['user']['id'])
        client.views_open(trigger_id=body['trigger_id'], notify_on_close = True, view=builder.view)
    except Exception as e:
        logging.error(f'***App-Error*** giveMedicationModal: {e}')
        
@app.action("action-user_selected")
def user_selected(ack):
    ack()
    pass        
        
@app.view("medication_given")
def gave_medication_modal(ack, client: WebClient, view):
    '''
    From give_medication_modal: Handle event based on user's selection,
    Send alert to slack channel that medication has been given
    '''
    medication_history = []
    try:
        patient_metadata = utils.str_utils.json_acceptable_string(view['private_metadata'])
        user_info = client.users_info(user=view['state']['values']['user_selected']['user_selected-action']['selected_user'])
        given_by = user_info.data['user']['name']
        utc_dt = view['state']['values']['time_selected']['datetimepicker-action']['selected_date_time']
        time_given = datetime.fromtimestamp(utc_dt, tz = None)
        # Fix bug on my phone where it randomly assigns the datetime for now with the year 1991...
        if time_given.year == 1991:
            time_given = time_given.replace(year=2022)
        # target_time = utils.str_utils.add_letter(view['state']['values']['target_time_selected']['target_time_selected']['selected_option']['value'], 5, '0')

        now = datetime_base.datetime.now().time()
        # Define your desired times
        time1 = datetime_base.time(7, 30)
        time2 = datetime_base.time(20, 0)
        # Calculate the time differences between the current time and each desired time
        diff1 = datetime_base.datetime.combine(datetime_base.date.today(), time1) - datetime_base.datetime.combine(datetime_base.date.today(), now)
        diff2 = datetime_base.datetime.combine(datetime_base.date.today(), time2) - datetime_base.datetime.combine(datetime_base.date.today(), now)
        # Compare the time differences to see which time is closer
        if abs(diff1) < abs(diff2):
            # Do something if it's closer to time1
            target_time = '07:30'
        else:
            # Do something else if it's closer to time2
            target_time = '20:00'
                    
        medication_history.append(
            {
                "patient_name": patient_metadata['patient_name'],
                "medication": view['state']['values']['medication_selected']['medication_selected']['selected_option']['value'],
                "dosage_amount": view['state']['values']['dosage_selected']['dosage_selected']['selected_option']['value'],
                "time_given": time_given,
                "time_category": "testing time_category",
                "given_by": given_by,
                "target_time": target_time
            }
        )
        medication_history_df = pd.DataFrame(medication_history)
        medication_history_dfat = medication_history_df.astype(settings.DF_ASTYPE['MEDICATION_HISTORY'])
        db.commands.insert(table="patient_medication_history", df=medication_history_dfat)
        builder = views.medication_given(medication_history)
        ack(response_action="update", view=builder.view)
        message = alerts.gave_medication_alert(medication_history[0])
        client.chat_postMessage(channel=settings.SLACK_BOT['WEBHOOK'], attachments=message['attachments'])
    except Exception as e:
        logging.error(f'***App-Error*** gave_medication_modal: {e}')

@app.action("button-action-stop_tracker")
def action_stop_tracker(ack, body, client: WebClient):
    try:
        ack()
        medi_tracker_status = []
        utils.str_utils.stop_mediTracker_service(settings.SLACK_BOT['TRACKER_SERVICE'])
        medi_tracker_status.append(
            {
                "status": "stopped"
            }
        )
        medi_tracker_df = pd.DataFrame(medi_tracker_status)
        medi_tracker_dfat = medi_tracker_df.astype(settings.DF_ASTYPE['TRACKER_STATUS'])
        db.commands.insert(table="medi_tracker", df=medi_tracker_dfat)
        builder = views.mediTracker_service_stopped()
        client.views_push(trigger_id=body['trigger_id'], view_id=body['view']['id'], hash=body['view']['hash'], notify_on_close=True, view=builder.view)
    except Exception as e:
        logging.error(f'***App-Error*** action_stop_tracker: {e}')
        
@app.action("button-action-start_tracker")
def action_start_tracker(ack, body, client: WebClient):
    try:
        ack()
        medi_tracker_status = []
        utils.str_utils.start_mediTracker_service(settings.SLACK_BOT['TRACKER_SERVICE'])
        medi_tracker_status.append(
            {
                "status": "active"
            }
        )        
        medi_tracker_df = pd.DataFrame(medi_tracker_status)
        medi_tracker_dfat = medi_tracker_df.astype(settings.DF_ASTYPE['TRACKER_STATUS'])
        db.commands.insert(table="medi_tracker", df=medi_tracker_dfat)        
        builder = views.mediTracker_service_started()
        client.views_push(trigger_id=body['trigger_id'], view_id=body['view']['id'], hash=body['view']['hash'], notify_on_close=True, view=builder.view)
    except Exception as e:
        print(e)
        logging.error(f'***App-Error*** action_start_tracker: {e}')

def run():
    logging.info("Started Medi App!")
    SocketModeHandler(app=app, app_token=settings.SLACK_BOT['APP_TOKEN']).start()