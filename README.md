# medi

## Introduction
Medi is a Slack bot designed to enhance the management of medication schedules within caregiving settings, specifically aimed at aiding in the supervision of children's medication routines. It is implemented in Python and utilizes Slack's API to interact within the Slack environment.

## System Architecture

### Slack Integration
- **Slack SDK:** Medi uses the `slack_sdk` Python package to interact with the Slack API. This integration allows Medi to send messages, create reminders, and manage interactive components within Slack.
- **Event Subscriptions:** The bot subscribes to specific Slack events, enabling it to react in real-time to messages and user interactions.

### Medication Scheduling
- **Datetime Handling:** The bot relies on Python’s `datetime` module to process and compare time, ensuring medication reminders are sent according to the schedule.
- **Cron Jobs:** Scheduled tasks are managed through cron jobs, which trigger the bot's functions at predefined times.

### Database Operations
- **Database Integration:** A database is used to store medication schedules, user preferences, and logs of medication administration.
- **CRUD Operations:** Medi supports Create, Read, Update, and Delete operations, allowing for dynamic management of medication records and user settings.

## Core Functionalities

### Alert System
- **Scheduled Reminders:** Users receive automated reminders when it's time for a child’s medication.
- **Missed Medication Notifications:** If a scheduled medication time passes without an update, Medi sends an alert to inform caregivers.

### User Interaction
- **App Home Tab:** Caregivers can add or remove patients, toggle alerts, and view medication schedules directly within the Medi app home tab on Slack.
- **Interactive Messages:** Medi uses Slack's interactive messages feature, enabling users to mark medications as administered with a simple click.

### Logging and History Tracking
- **Medication Logs:** All actions related to medication administration are logged for accountability.
- **Calendar View:** Medi provides a calendar view for caregivers to see the historical data of when medications were administered.

### Notifications Customization
- **Custom Alert Windows:** Caregivers can set custom time windows for receiving reminders, making the bot adaptable to different routines.
- **Do Not Disturb:** Users can specify periods during which alerts should be muted.

## Development and Extension

### Scalability
- **Modular Design:** Medi is built with scalability in mind, allowing for future enhancements and additional features without significant refactoring.

### API Endpoints
- **Endpoints for Extension:** Medi is designed to support additional Slack API endpoints, making it possible to extend functionality to include more interactive components, workflows, or even integration with external healthcare APIs.

### Continuous Integration/Continuous Deployment (CI/CD)
- **Automated Testing:** The codebase includes a suite of automated tests to ensure stability with each iteration.
- **Deployment Pipeline:** A CI/CD pipeline is configured for smooth deployments and updates to the live bot.

## Conclusion
Medi aims to provide a seamless and reliable system for medication schedule management through Slack. Its technical foundation allows for a user-friendly experience, coupled with robust backend functionality to ensure timely and accurate medication administration for children.

For a more detailed look at the source code, installation instructions, and usage guidelines, please refer to the subsequent sections of this `README` or explore the repository.

