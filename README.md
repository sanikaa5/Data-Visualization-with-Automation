# Data-Visualization-with-Automation

This project demonstrates a real-time data monitoring and visualization system using Google Sheets for data storage, email notifications for data sharing, and Matplotlib for data visualization.

## Overview

The system consists of two main components: sender and receiver.

### Sender Side:
- Generates fake data (timestamp and moisture value).
- Appends the generated data to a Google Sheets document.
- Sends an email notification containing the link to the Google Sheets document if it hasn't been sent already.

### Receiver Side:
- Retrieves the link to the Google Sheets document from the receiver's email inbox using IMAP.

### Visualization:
- Visualizes the data from the Google Sheets document using Matplotlib.

## Setup

1. Install the required Python libraries:

2. Enable the Gmail API and Google Sheets API and download the credentials JSON file.
- For Gmail API: https://developers.google.com/gmail/api/quickstart/python
- For Google Sheets API: https://developers.google.com/sheets/api/quickstart/python
- Google Sheets API Setup:
Credentials for accessing the Google Sheets API are set up using the ServiceAccountCredentials class.

3. Enable IMAP in your Gmail account settings.

4. Update the following variables in the code:
- `receiver_email`: Receiver's email address.
- `receiver_password`: Receiver's app password for IMAP.
- `sender_email`: Sender's email address.
- `sender_password`: Sender's app password for SMTP.
- `sheets_link`: Link to the Google Sheets document.

5. Run the Python script `visualize.py`.

## Usage

1. Run the Python script `realtime_data_monitoring.py`.
2. The script will continuously generate fake data, append it to the Google Sheets document, send email notifications with the link to the document, and visualize the data.
3. Check your email inbox for notifications and access the Google Sheets document for real-time data monitoring.

## Dependencies

- Python 3.x
- gspread
- oauth2client
- matplotlib

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request.
