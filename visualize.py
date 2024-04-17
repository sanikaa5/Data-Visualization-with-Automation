import smtplib
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.parser import BytesParser
from email import policy
import imaplib

# Global variables
email_sent = False
sheets_link = "enter sheets link here"#enter the google sheets link

# Sender side code(generating fake data, can be easily modified to link to real generated data)
def generate_single_data_point():
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    data_point = [
        timestamp,
        round(random.uniform(0, 1), 2)
    ]
    return data_point

def append_data_to_google_sheets(data, sheet):
    sheet.append_row(data)

def send_data_to_gmail(spreadsheet, data, email_sent_flag):
    if not email_sent_flag:
        receiver_email = "receiver@gmail.com"#enter receiver email here
        spreadsheet.share(receiver_email, perm_type='user', role='writer')

        sender_email = "sender@gmail.com"#enter sender email here
        sender_password = "enter app password here"  # App password of sender
        receiver_email = "receiver@gmail.com"
        subject = "Link to Data Google Sheets"
        body = f"Please find the link to the shared Google Sheets file: {spreadsheet.url}"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())

            print(f"Email sent successfully at {data[0]}!")
            email_sent_flag = True

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    return email_sent_flag

# Receiver side code
def retrieve_data_from_email():
    receiver_email = "receiver@gmail.com"#enter receiver email
    receiver_password = "enter receiver app password"  # App password of receiver

    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(receiver_email, receiver_password)
    mail.select("inbox")

    # Search for emails with the specified subject
    result, data = mail.search(None, '(SUBJECT "Link to Data Google Sheets")')
    email_ids = data[0].split()

    if not email_ids:
        print("No emails found.")
        return

    # Retrieve the latest email with the link
    latest_email_id = email_ids[-1]
    result, message_data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = message_data[0][1]

    # Parse the raw email using BytesParser
    msg = BytesParser(policy=policy.default).parsebytes(raw_email)

    # Extract the link from the email body
    body = msg.get_body(preferencelist=('plain', 'html'))
    link = str(body.get_payload())

   

    # Logout from the IMAP server
    mail.logout()

def visualize_data_from_google_sheets(sheets_link):
    # Open the Google Sheets file using the provided link
    gc = gspread.service_account(r"credentials_path.json")#json credential file path obtained from google console service acc
    sh = gc.open_by_url(sheets_link)

    # Get the first sheet in the spreadsheet
    worksheet = sh.get_worksheet(0)

    # Read the data from the sheet
    data = worksheet.get_all_values()

    # Extract columns for visualization
    timestamps = [row[0] for row in data[1:]]
    moisture_values = [float(row[1]) for row in data[1:]]

    # Data visualization using Matplotlib
    plt.plot(timestamps, moisture_values, marker='o')
    plt.xlabel('Timestamp')
    plt.ylabel('Data')
    plt.title('Data Visualization')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

# Set up Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(r"credentials_path.json", scope)
client = gspread.authorize(creds)

spreadsheet_name = 'Data'
try:
    spreadsheet = client.open(spreadsheet_name)
except gspread.SpreadsheetNotFound:
    spreadsheet = client.create(spreadsheet_name)

sheet = spreadsheet.get_worksheet(0)


# Function to update data and plot
def update_and_plot(frame):
    global email_sent, sheets_link
    
    current_time = time.time()
    print(f"Execution time: {current_time}")

    data_point = generate_single_data_point()
    append_data_to_google_sheets(data_point, sheet)
    email_sent = send_data_to_gmail(spreadsheet, data_point, email_sent)
    retrieve_data_from_email()
    visualize_data_from_google_sheets(sheets_link)

# Create an animation that updates and plots data every 1 seconds(time can be modified in interval)
animation = FuncAnimation(plt.gcf(), update_and_plot, interval=1, cache_frame_data=False)


# Show the plot
plt.show()