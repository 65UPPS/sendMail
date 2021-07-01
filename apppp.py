# https://realpython.com/python-send-email/


from fpdf import FPDF
from app import data_table_base
from datetime import datetime, timedelta
import smtplib
import time


now = (datetime.now().date() - timedelta(days=1)).strftime("%d.%m.%Y")

data = [data_table_base.columns.values.tolist()] + data_table_base.values.tolist()
pdf = FPDF(format='letter', unit='in')
# Effective page width, or just epw

pdf.add_font('Bernard MT', '', r'C:\Windows\Fonts\BERNHC.TTF', uni=True)

pdf.add_font('Roboto', '', r'assets\font\Roboto-Bold.ttf', uni=True)

pdf.add_page()

pdf.set_font('Roboto', '', 10)

epw = pdf.w - 2 * pdf.l_margin

# Set column width to 1/4 of effective page width to distribute content
# evenly across table and page
col_width = epw / 5

th = pdf.font_size

pdf.cell(epw, 0.0, f'Показатели за предыдущие сутки - {now}', align='C')
pdf.set_font('Roboto', '', 10.0)
pdf.ln(0.5)

# Here we add more padding by passing 2*th as height
for row in data:
    for datum in row:
        # Enter data in colums
        pdf.cell(col_width, 2 * th, str(datum), border=1, align='C')
    pdf.ln(2 * th)

pdf.output('reportDayly.pdf', 'F')


import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = f"Отчет за {now}"
body = f"Уважаемый пользователь, во вложении отчет о деятельности УППС за {now}"
sender_email = "65upps@gmail.com"
receiver_email = "65upps@gmail.com"
password = 'kpxydlqiyekixuns'


message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  # Recommended for mass emails


message.attach(MIMEText(body, "plain"))

filename = "reportDayly.pdf"

with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
def send_mail():
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


while (True):
    send_mail()
    time.sleep(34200)
