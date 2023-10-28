import utils

def gave_medication_alert(medication_history):
    '''
    Alert that medication was given:
    - Time Given - xx:xx am/pm
    - Given By - Slack User who marked medication given
    '''
    time_range_given = utils.date_utils.time_in_range(medication_history['time_given'])
    time_given = utils.date_utils.splitDate_getTime(medication_history['time_given'])
    
    message = {
        "attachments": [
            {
                "color": "#00FF00",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"{medication_history['patient_name']} {time_range_given}",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f">*Medication:* *`{medication_history['medication']}`*\n>*Dosage:* *`{medication_history['dosage_amount']}`* \n> *Time Given:* *`{time_given}`* \n> *Given By:* @{medication_history['given_by']}"
                        }
                    }
                ]
            }
        ]
    }
    return message

def give_medication_alert(med_data, target_time):
    '''
    Alert that it is time to give a patient their medicaiton 
    - based on the target time set for medicaiton
    '''
    message = {
        "attachments": [
            {
                "color": "#ffa500",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Medication Reminder  :alarm_clock:",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*It's time for `{med_data['patient_name']}` to take his medication* \n\n>*Medication:*  *`{med_data['medication']}`*  \n>*Dosage*: *`{med_data['dosage_amount']}`* \n>*Target Time:*  *`{target_time}`*"
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Give Medication",
                                    "emoji": True
                                },
                                "style": "primary",
                                "value": med_data['patient_name'],
                                "action_id": "button-action-mark-medication_given"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    return message

def missed_dosage_alert(med_data, target_time):
    '''
    Alert that medication was missed:
    - Actions to kick off alert:
        - Phone disconnects from wifi
        - Phone's location moves away from home
        - Time limit: 9:30 AM/PM
    - Sends alert to channel
    - Action button to mark medication given
    '''
    message = {
        "attachments": [
            {
                "color": "#800000",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Missed Medication Alert!  :rotating_light:",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f">*`{med_data['patient_name']}`* did not received his medication (*`{med_data['medication']}`*) at *`{target_time}`*"
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Give Medication",
                                    "emoji": True
                                },
                                "style": "primary",
                                "value": med_data['patient_name'],
                                "action_id": "button-action-mark-medication_given"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    return message

