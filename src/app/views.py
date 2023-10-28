from block_builder import Builder
import utils
from slack_sdk import WebClient
from slack_bolt import App

def builder_type(type, modal_data=None):
    builder = Builder({"type": type}, modal_data)
    return builder

def app_home_opened(user_info, patient_data):
    todays_date = utils.date_utils.get_todays_date()
    builder = builder_type("home")
    builder.section_mrkdwn_accessory_button(section_text=f"*Hi @{user_info['user']['name']}, Welcome to Medi*  :pill:",
                                            accessory_text=":gear:  Settings", 
                                            accessory_value="medi_settings", 
                                            accessory_action_id="action-settings")
    builder.sectionMrkdwn("*`Medi`* allows you to *Mark* and *Track* when your child has received his/her medication.")
    builder.sectionMrkdwn("\n\n")
    builder.header("Mark  :heavy_check_mark:")
    builder.divider()
    builder.actions_itembutton(item_placeholder="Select a patient", item_options=patient_data,
                               item_action_id="action-user_selected", button_text="Give Medication",
                               button_value="medi_give_medication", button_action_id="button-action-mark-medication_given")
    builder.sectionMrkdwn("\n\n")
    builder.header("Track :calendar:")
    builder.divider()
    builder.actions_itemDateButton(item_placeholder="Select a patient",
                                   item_options=patient_data,
                                   item_action_id="select-action-patient_name",
                                   initial_date=todays_date,
                                   date_action_id="date-action-selected",
                                   button_text="Show History",
                                   button_value="button-action-show_patient_history",
                                   button_action_id="button-action-show_patient_history")
    builder.update_view()
    return builder

def app_home_patient_history(user_info, patient_data, patient_history):
    builder = app_home_opened(user_info, patient_data)
    builder.divider()
    for i in patient_history:
        time_given = utils.date_utils.splitDate_getTime(i['time_given'])
        builder.sectionMrkdwn(f"*`{i['patient_name']}`*\n>Medication: `{i['medication']}`\n>Dosage: `{i['dosage_amount']}`\n>Time Given: `{time_given}`\n>Given By: @{i['given_by']}")
        builder.divider()
    builder.update_view()
    return builder

def settings_modal(patient_data, tracker_status):
    external_id = utils.num_utils.get_random_number()
    builder = builder_type("modal", {"title": ":gear:  Settings", 
                                     "submit": False, 
                                     "close_text": "Close", 
                                     "callback_id": "action-settings", 
                                     "external_id": str(external_id), 
                                     "private_metadata": "patient_data"})
    if tracker_status == 'active':
        builder.header("Medi Tracker Alerts:  :large_green_circle:  Enabled")
        builder.divider()
        builder.button(text="Disable Alerts", value="stop_tracker", actionId="button-action-stop_tracker", style="danger")
    elif tracker_status == 'stopped':
        builder.header("Medi Tracker Alerts:  :x:  Disabled")
        builder.divider()
        builder.button(text="Enable Alerts", value="start_tracker", actionId="button-action-start_tracker", style="primary")
    else:
        builder.double_button(button1_text="Enable Alerts",
                            button1_value="start_tracker",
                            button1_action_id="button-action-start_tracker",
                            button2_text="Disable Alerts",
                            button2_value="stop_tracker",
                            button2_action_id="button-action-stop_tracker")
    builder.sectionMrkdwn(" ")
    builder.header(":building_construction:  Manage Patients")
    builder.divider()
    builder.double_button(button1_text="Add Patient",
                          button1_value="add_patient",
                          button1_action_id="action-add_patient_modal",
                          button2_text="Remove Patient",
                          button2_value="remove_patient",
                          button2_action_id="action-remove_patient_modal")
    builder.sectionMrkdwn(" ")
    builder.header(":stethoscope:  Medi Patients")
    builder.divider()
    for i in patient_data:
        medications_str = ", "
        medications = medications_str.join(i['medications'])
        builder.sectionMrkdwn_overflow(text=f">*Patient Name:*  *`{i['patient_name']}`*\n>*Age:*  *`{i['age']}`*\n>*Medications:*  *`{medications}`*",
                                       overflow_text="Edit Patient", 
                                       overflow_value=f"edit_patient_{i['patient_name']}",
                                       overflow_action_id=f"action_edit_patient")
        # builder.sectionMrkdwn(f">*Patient Name:*  *`{i['patient_name']}`*\n>*Age:*  *`{i['age']}`*\n>*Medications:*  *`{medications}`*")
        builder.divider()
    builder.update_view()
    return builder
    
def addPatient_modal():
    external_id = utils.num_utils.get_random_number()
    builder = builder_type("modal", {"title": ":pill:  Add Patient",
                                     "submit": True,
                                     "submit_text": "Next",
                                     "close_text": "Cancel",
                                     "callback_id": "addpatient_modal_continued",
                                     "external_id": str(external_id),
                                     "private_metadata": "addpatient_modal"})
    builder.input_plain_text(block_id="patient_name",
                              action_id="input-name",
                              label_text="Name")
    builder.input_number(block_id="patient_age",
                         action_id="input-age",
                         label_text="Age")
    builder.input_plain_text(block_id="patient_medication",
                             action_id="input-medication",
                             label_text="Medication")
    builder.input_number(block_id="patient_times_taken",
                         action_id="input-times_taken",
                         label_text="Times Medication Taken Per Day")
    builder.update_view()
    return builder

def addPatientContinued_modal(patient_data):
    external_id = utils.num_utils.get_random_number()
    builder = builder_type("modal", {"title": ":pill:  Add Patient",
                                     "submit": True,
                                     "submit_text": "Submit",
                                     "close_text": "Cancel",
                                     "callback_id": "action-add_patient",
                                     "external_id": str(external_id),
                                     "private_metadata": f"{patient_data}"})
    for i in range(patient_data['times_taken_per_day']):
        n = int(i) + 1
        builder.input_timepicker(f"Medication Time {n}", f"time_taken_{n}", f"action-time_taken")
        builder.input_plain_text(label_text=f"Dosage Amount {n}", block_id=f"dosage_amount_{n}", action_id="input-dosage_amount")
    builder.update_view()
    return builder

def patient_added(patient_data):
    external_id = utils.num_utils.get_random_number()
    builder = builder_type("modal", {"title": ":pill:  Patient Added", 
                                     "submit": False, 
                                     "close_text": "Close", 
                                     "callback_id": "view-patient_added", 
                                     "external_id": str(external_id), 
                                     "private_metadata": "action-patient_added"})
    builder.sectionMrkdwn(f"{patient_data[0]['patient_name']} was successfully added as a patient in Medi  :smile:")
    builder.update_view()
    return builder

def removePatient_modal(patient_data):
    external_id = utils.num_utils.get_random_number()
    builder = builder_type("modal", {"title": ":x:  Remove Patient", 
                                     "submit": False, 
                                     "close_text": "Close", 
                                     "callback_id": "action-remove_patient", 
                                     "external_id": str(external_id), 
                                     "private_metadata": f"{patient_data}"})
    builder.staticSelect(placeholder_text="Select a patient", item_options=patient_data, actionId="action-select_remove_patient")
    builder.button_confirm(button_text="Remove Patient",
                           confirm_title="This will permanently delete this patient in Medi...",
                           confirm_text="Remove Patient",
                           deny_text="Cancel",
                           style="danger",
                           value="action-remove_patient",
                           action_id="action-remove_patient")
    builder.update_view()
    return builder

def patient_removed(patient_removed):
    external_id = utils.num_utils.get_random_number()
    builder = builder_type("modal", {"title": ":x:  Patient Removed", 
                                     "submit": False, 
                                     "close_text": "Close", 
                                     "callback_id": "view-patient_added", 
                                     "external_id": str(external_id), 
                                     "private_metadata": "action-patient_added"})
    builder.sectionMrkdwn(f"{patient_removed} was successfully removed as a patient in Medi")
    builder.update_view()
    return builder

def give_medication_modal(patient_data, medication_data, dosages, target_times, user_id):
    external_id = utils.num_utils.get_random_number()
    builder = builder_type("modal", {"title": f"Give {patient_data['patient_name']} Medication",
                                     "submit": True,
                                     "submit_text": "Submit",
                                     "close_text": "Cancel",
                                     "callback_id": "medication_given",
                                     "external_id": str(external_id),
                                     "private_metadata": f"{patient_data}"})
    builder.staticSelect_options(block_id="medication_selected", placeholder_text="Medication", item_options=medication_data, actionId="medication_selected")
    builder.staticSelect_options(block_id="dosage_selected", placeholder_text="Dosage", item_options=dosages, actionId="dosage_selected")
    # builder.staticSelect_options(block_id="target_time_selected", placeholder_text="Target Medication Time", item_options=target_times, actionId="target_time_selected")
    builder.input_user_select(placeholder="Administrator", user_id=user_id)
    builder.input_date_time(block_id="time_selected", label_text="Date/Time Given")
    builder.update_view()
    return builder
    
def medication_given(patient_data):
    external_id = utils.num_utils.get_random_number()
    builder = builder_type("modal", {"title": "Medication Given", 
                                     "submit": False, 
                                     "close_text": "Close", 
                                     "callback_id": "view-medication_given", 
                                     "external_id": str(external_id), 
                                     "private_metadata": "view-medication_given"})
    builder.sectionMrkdwn(f"{patient_data[0]['patient_name']} was given their medication  :smile:")
    builder.update_view()
    return builder

def mediTracker_service_stopped():
    external_id = utils.num_utils.get_random_number()
    builder = builder_type("modal", {"title": "Medi Tracker Stopped", 
                                     "submit": False, 
                                     "close_text": "Close", 
                                     "callback_id": "view-service_stopped", 
                                     "external_id": str(external_id), 
                                     "private_metadata": "action-service_stopped"})
    builder.sectionMrkdwn(f":x:  Medi Tracker was stopped. Alerts will no longer appear \n*Turn Medi Tracker back on in the Medi App*")
    builder.update_view()
    return builder

def mediTracker_service_started():
    external_id = utils.num_utils.get_random_number()
    builder = builder_type("modal", {"title": "Medi Tracker Started", 
                                     "submit": False, 
                                     "close_text": "Close", 
                                     "callback_id": "view-service_started", 
                                     "external_id": str(external_id), 
                                     "private_metadata": "action-service_started"})
    builder.sectionMrkdwn(f":large_green_circle:  Medi Tracker was started. Alerts will now appear")
    builder.update_view()
    return builder