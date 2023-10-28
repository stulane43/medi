##########################################
# Slack Block Kit Builder
##########################################
import pprint
import datetime
import time

class Builder():
    
    def __init__(self, view_type: dict, modal_data):
        self.view = view_type
        if self.view == {"type": "modal"}:
            self.type_modal(modal_data)
        self.block = {"blocks": []}
        
    def type_modal(self, modal_data):
        if modal_data['submit']:
            self.view = {
                "type": "modal",
                "title": {
                    "type": "plain_text",
                    "text": modal_data['title']
                },
                "submit": {
                    "type": "plain_text",
                    "text": modal_data['submit_text'],
                    "emoji": True
                },
                "close": {
                    "type": "plain_text",
                    "text": modal_data['close_text']
                },
                "callback_id": modal_data['callback_id'],
                "external_id": modal_data['external_id'],
                "private_metadata": modal_data['private_metadata']
            }
        else:
            self.view = {
                "type": "modal",
                "title": {
                    "type": "plain_text",
                    "text": modal_data['title']
                },
                "close": {
                    "type": "plain_text",
                    "text": modal_data['close_text']
                },
                "callback_id": modal_data['callback_id'],
                "external_id": modal_data['external_id'],
                "private_metadata": modal_data['private_metadata']
            }
            

    def update_view(self):
        self.view.update(self.block)

    def append_block(self, text):
        self.block["blocks"].append(text)

    def divider(self):
        '''
        Adds divider to json file used to send alert message
        '''
        divider = {'type': 'divider'}
        self.append_block(divider)

    def header(self, text):
        '''
        Adds header to json file used to send alert message
        '''
        header = {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{text}",
            }
        }
        self.append_block(header)
        
    def context(self, type, text):
        context = {
            "type": "context",
            "elements": [
                {
                    "type": f"{type}",
                    "text": f"{text}"
                }
            ]
        }
        self.append_block(context)
        
    def context2(self, type1, type2, text1, text2):
        context = {
            "type": "context",
            "elements": [
                {
                    "type": f"{type1}",
                    "text": f"{text1}"
                },
                {
                    "type": f"{type2}",
                    "text": f"{text2}"
                }
            ]
        }
        self.append_block(context)

    def sectionMrkdwn(self, text):
        '''
        Adds markdown section to json file used to send alert message
        '''
        sectionTitles = ['type', 'text']
        sectionDetails = ['mrkdwn', text]
        data = dict(zip(sectionTitles, sectionDetails))
        section = {'type': 'section', 'text': data}
        self.append_block(section)
        
    def sectionMrkdwn_overflow(self, text, overflow_text, overflow_value, overflow_action_id):
        '''
        Adds markdown section to json file used to send alert message
        '''
        sectionTitles = ['type', 'text']
        sectionDetails = ['mrkdwn', text]
        data = dict(zip(sectionTitles, sectionDetails))
        section = {
            'type': 'section', 
            'text': data,
            "accessory": {
				"type": "overflow",
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": overflow_text,
							"emoji": True
						},
						"value": overflow_value
					}
				],
				"action_id": overflow_action_id
			}
        }
        self.append_block(section)
        
    def sectionFields(self, field1, field2):
        sectionFields = {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"{field1}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"{field2}"
                }
            ]
        }
        self.append_block(sectionFields)
    
    def staticSelect2(self, initialOption, options, actionId):
        staticSelect = {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select an item",
                    "emoji": True
                },
                "initial_option": {
                        "text": {
                            "type": "plain_text",
                            "text": f"{initialOption['text']}",
                            "emoji": True
                        },
                        "value": f"{initialOption['value']}"
                    },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": f"{options['first']['text']}",
                            "emoji": True
                        },
                        "value": f"{options['first']['value']}"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": f"{options['second']['text']}",
                            "emoji": True
                        },
                        "value": f"{options['second']['value']}"
                    }
                ],
                "action_id": f"{actionId}"
            },
            "label": {
                "type": "plain_text",
                "text": " ",
                "emoji": True
            }
        }
        self.append_block(staticSelect)
        
    def staticSelect4(self, initialOption, options, actionId):
        staticSelect = {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select an item",
                    "emoji": True
                },
                "initial_option": {
                        "text": {
                            "type": "plain_text",
                            "text": f"{initialOption['text']}",
                            "emoji": True
                        },
                        "value": f"{initialOption['value']}"
                    },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": f"{options['first']['text']}",
                            "emoji": True
                        },
                        "value": f"{options['first']['value']}"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": f"{options['second']['text']}",
                            "emoji": True
                        },
                        "value": f"{options['second']['value']}"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": f"{options['third']['text']}",
                            "emoji": True
                        },
                        "value": f"{options['third']['value']}"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": f"{options['fourth']['text']}",
                            "emoji": True
                        },
                        "value": f"{options['fourth']['value']}"
                    }
                ],
                "action_id": f"{actionId}"
            },
            "label": {
                "type": "plain_text",
                "text": " ",
                "emoji": True
            }
        }
        self.append_block(staticSelect)
        
    def multilineInput(self, label, actionId):
        multilineInput = {
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"multiline": True,
				"action_id": f"{actionId}"
			},
			"label": {
				"type": "plain_text",
				"text": f"{label}",
				"emoji": True
			},
            "optional": True
		}
        self.append_block(multilineInput)
        
    def input_timepicker(self, label, block_id, action_id):
        timepicker_input = {
            "type": "input",
            "block_id": block_id,
            "element": {
                "type": "timepicker",
                "initial_time": "12:00",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select time",
                    "emoji": True
                },
                "action_id": action_id
            },
            "label": {
                "type": "plain_text",
                "text": label,
                "emoji": True
            }
        }
        self.append_block(timepicker_input)
        
    def sectionButton(self, text, buttonText, value, actionId):
        sectionButton = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"{text}"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": f"{buttonText}",
					"emoji": True
				},
				"value": f"{value}",
				"action_id": f"{actionId}"
			}
		}
        self.append_block(sectionButton)
            
    def button(self, text, value, actionId, style):
        button = {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": f"{text}",
                        "emoji": True
                    },
                    "style": style,
                    "value": f"{value}",
                    "action_id": f"{actionId}"
                }
            ]
        }
        self.append_block(button)
    
    def double_button(self, button1_text, button1_value, button1_action_id, button2_text, button2_value, button2_action_id):
        double_button = {
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": f"{button1_text}",
						"emoji": True
					},
					"style": "primary",
					"value": f"{button1_value}",
					"action_id": f"{button1_action_id}"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": f"{button2_text}",
						"emoji": True
					},
					"style": "danger",
					"value": f"{button2_value}",
					"action_id": f"{button2_action_id}"
				}
			]
		}
        self.append_block(double_button)
        
    def section_mrkdwn_accessory_button(self, section_text, accessory_text, accessory_value, accessory_action_id):
        section = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": section_text,
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": accessory_text,
                    "emoji": True
                },
                "value": accessory_value,
                "action_id": accessory_action_id
            }
        }
        self.append_block(section)
        
    def actions_itemDateButton(self, item_placeholder, item_options, item_action_id, initial_date, date_action_id, button_text, button_value, button_action_id):
        options = []
        
        for i in item_options:
            option = {
                "text": {
                    "type": "plain_text",
                    "text": i['patient_name'],
                    "emoji": True
                },
                "value": i['patient_name']
            }
            options.append(option)
        
        actions = {
            "type": "actions",
            "block_id": "show_history",
            "elements": [
                {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": item_placeholder,
                        "emoji": True
                    },
                    "initial_option": {
                        "text": {
                            "type": "plain_text",
                            "text": item_options[0]['patient_name'],
                            "emoji": True
                        },
                        "value": item_options[0]['patient_name']
                    },
                    "options": options,
                    "action_id": item_action_id
                },
                {
                    "type": "datepicker",
                    "initial_date": initial_date,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date",
                        "emoji": True
                    },
                    "action_id": date_action_id
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": button_text,
                        "emoji": True
                    },
                    "style": "primary",
                    "value": button_value,
                    "action_id": button_action_id
                }
            ]
        }
        self.append_block(actions)
        
    def input_plain_text(self, label_text, block_id, action_id):
        input = {
			"type": "input",
			"block_id": block_id,
			"element": {
				"type": "plain_text_input",
				"action_id": action_id
			},
			"label": {
				"type": "plain_text",
				"text": label_text,
				"emoji": True
			}
        }
        self.append_block(input)
        
    def input_number(self, label_text, block_id, action_id):
        input = {
			"type": "input",
			"block_id": block_id,
			"element": {
				"type": "number_input",
				"is_decimal_allowed": False,
				"action_id": action_id
			},
			"label": {
				"type": "plain_text",
				"text": label_text,
				"emoji": True
			}
		}
        self.append_block(input)
        
    def staticSelect(self, placeholder_text, item_options, actionId):
        options = []
        
        for i in item_options:
            option = {
                "text": {
                    "type": "plain_text",
                    "text": i['patient_name'],
                    "emoji": True
                },
                "value": i['patient_name']
            }
            options.append(option)
        
        staticSelect = {
            "type": "actions",
            "elements": [
                {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": placeholder_text,
                        "emoji": True
                    },
                    "options": options,
                    "action_id": f"{actionId}"
                }
            ]
        }
        self.append_block(staticSelect)
        
    def button_confirm(self, button_text, confirm_title, confirm_text, deny_text, style, value, action_id):
        button = {
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": button_text,
						"emoji": True
					},
					"confirm": {
						"title": {
							"type": "plain_text",
							"text": confirm_title
						},
						"confirm": {
							"type": "plain_text",
							"text": confirm_text
						},
						"deny": {
							"type": "plain_text",
							"text": deny_text
						}
					},
					"style": style,
					"value": value,
					"action_id": action_id
				}
			]
		}
        self.append_block(button)
        
    def input_user_select(self, placeholder, user_id):
        user_select = {
			"type": "input",
			"block_id": "user_selected",
			"element": {
				"type": "users_select",
				"placeholder": {
					"type": "plain_text",
					"text": placeholder,
					"emoji": True
				},
                "initial_user": user_id,
				"action_id": "user_selected-action"
			},
			"label": {
				"type": "plain_text",
				"text": placeholder,
				"emoji": True
			}
		}
        self.append_block(user_select)
        
    def input_date_time(self, block_id, label_text):
        
        now = datetime.datetime.now()

        initial_date_time = int(time.mktime(now.timetuple()))        
        # date_time = {
		# 	"type": "input",
        #     "block_id": block_id,
		# 	"element": {
		# 		"type": "datetimepicker",
		# 		"action_id": "datetimepicker-action",
        #         "initial_date": initial_date,
		# 	},
		# 	"label": {
		# 		"type": "plain_text",
		# 		"text": label_text,
		# 		"emoji": True
		# 	}
		# }
        
        date_time = {
            "type": "input",
            "block_id": block_id,
            "element": {
                "type": "datetimepicker",
                "action_id": "datetimepicker-action",
                "initial_date_time": initial_date_time
            },
            "label": {
                "type": "plain_text",
                "text": label_text
            }
        }
        self.append_block(date_time)
        
    def actions_itembutton(self, item_placeholder, item_options, item_action_id, button_text, button_value, button_action_id):
        options = []
        
        for i in item_options:
            option = {
                "text": {
                    "type": "plain_text",
                    "text": i['patient_name'],
                    "emoji": True
                },
                "value": i['patient_name']
            }
            options.append(option)
        
        actions = {
            "type": "actions",
            "block_id": "give_medication",
            "elements": [
                {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": item_placeholder,
                        "emoji": True
                    },
                    "initial_option": {
                        "text": {
                            "type": "plain_text",
                            "text": item_options[0]['patient_name'],
                            "emoji": True
                        },
                        "value": item_options[0]['patient_name']
                    },
                    "options": options,
                    "action_id": item_action_id
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": button_text,
                        "emoji": True
                    },
                    "style": "primary",
                    "value": button_value,
                    "action_id": button_action_id
                }
            ]
        }
        self.append_block(actions)
        
    def staticSelect_options(self, block_id, placeholder_text, item_options, actionId):
        options = []
        
        now = datetime.datetime.now().time()
        # Define your desired times
        time1 = datetime.time(7, 30)
        time2 = datetime.time(20, 0)
        # Calculate the time differences between the current time and each desired time
        diff1 = datetime.datetime.combine(datetime.date.today(), time1) - datetime.datetime.combine(datetime.date.today(), now)
        diff2 = datetime.datetime.combine(datetime.date.today(), time2) - datetime.datetime.combine(datetime.date.today(), now)
        
        for i in item_options:
            option = {
                "text": {
                    "type": "plain_text",
                    "text": i,
                    "emoji": True
                },
                "value": i
            }
            options.append(option)
        
        try:
        # Compare the time differences to see which time is closer
            if abs(diff1) < abs(diff2):
                # Do something if it's closer to time1
                initial_option = item_options[0]
            else:
                # Do something else if it's closer to time2
                initial_option = item_options[1]
        except IndexError:
            initial_option = item_options[0]

        staticSelect = {
            "type": "input",
            "block_id": block_id,
            "element":
                {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": placeholder_text,
                        "emoji": True
                    },
                    "initial_option": {
                        "text": {
                            "type": "plain_text",
                            "text": initial_option,
                            "emoji": True
                        },
                        "value": initial_option
                    },
                    "options": options,
                    "action_id": f"{actionId}"
                },
            "label": {
				"type": "plain_text",
				"text": placeholder_text,
				"emoji": True
			}
        }
        self.append_block(staticSelect)