from slack_sdk import WebClient

import datetime
import logging

from . import alerts
import database as db
import settings
import utils

class Tracker():
    
    def __init__(self) -> None:
        self.client = WebClient(token=settings.SLACK_BOT['BOT_TOKEN'])
        self.current_time = datetime.datetime.now()
        self.current_date = self.current_time.strftime("%Y-%m-%d")
        med_times_result = db.commands.read(settings.DATABASES['query']['ALL_MED_TIMES'])
        self.med_times_data = med_times_result.to_dict('records')
        self.time_range = 30
        
    def main(self):
        for patient_data in self.med_times_data:
            self.check_meds_taken(patient_data)
            
    def check_meds_taken(self, patient_data):
        med_time = str(patient_data['medication_time'])
        target_time = utils.date_utils.splitDateTime_getHoursMinutes(med_time)
        target_hoursmins = f"{target_time['hour']}:{target_time['minute']}"
        meds_taken_result = db.commands.read(query=f"select * from patient_medication_history where patient_name = '{patient_data['patient_name']}' and CAST(time_given as DATE) = '{self.current_date}' and target_time = '{target_hoursmins}'")
        meds_taken_data = meds_taken_result.to_dict('records')
        if meds_taken_data == []:
            self.track_time(patient_data)        
        
    def track_time(self, patient_data):
        med_time = str(patient_data['medication_time'])
        target_time = utils.date_utils.splitDateTime_getHoursMinutes(med_time)
        if self.current_time.hour == int(target_time['hour']) and self.current_time.minute == int(target_time['minute']):
            logging.info(f"It's time for {patient_data['patient_name']} to take {patient_data['medication']}!")
            message = alerts.give_medication_alert(med_data=patient_data, target_time=f"{target_time['hour']}:{target_time['minute']}")
            self.client.chat_postMessage(channel=settings.SLACK_BOT['WEBHOOK'], attachments=message['attachments'])
        elif self.current_time.hour > int(target_time['hour']) or (self.current_time.hour == int(target_time['hour']) and self.current_time.minute >= int(target_time['minute']) + self.time_range):
            logging.info(f"You MISSED giving {patient_data['patient_name']} his medication: {patient_data['medication']} at {target_time['hour']}:{target_time['minute']}!")
            message = alerts.missed_dosage_alert(med_data=patient_data, target_time=f"{target_time['hour']}:{target_time['minute']}")
            self.client.chat_postMessage(channel=settings.SLACK_BOT['WEBHOOK'], attachments=message['attachments'])
        else:
            logging.info("no medications missed...")