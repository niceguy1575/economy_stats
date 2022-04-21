import smtplib
import os
import re
import pandas as pd

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class SendEmail:

	def __init__(self, senderEmailServer, senderEmail, senderPW):
		try: 
			# 587 -> outlook port number
			self.smtp = smtplib.SMTP(senderEmailServer, 587)
			self.smtp.ehlo() # say Hello
			self.smtp.starttls() # TLS 사용시 필요
			self.smtp.login(senderEmail, senderPW) 
		except Exception as e:
			print(e)
			self.smtp = smtplib.SMTP(senderEmailServer, 587)
			self.smtp.ehlo() # say Hello
			# self.smtp.starttls() # TLS 사용시 필요
			self.smtp.login(senderEmail, senderPW) 
			
	def MailSender(self, message, subject, senderEmail, targetEmail):
		
		# send with message
		#msg = MIMEText(message) 

		# send with HTML
		msg = MIMEMultipart('alternative')
		msg['Subject'] = subject
		msg['From'] = senderEmail
		msg['To'] = targetEmail
		
		# attach HTML
		msg.attach( MIMEText(message, 'html') )

		self.smtp.sendmail(senderEmail, targetEmail, msg.as_string()) 
		self.QuitSMTP()
		
	def QuitSMTP(self):
		self.smtp.quit()
		
		
		
if __name__ == '__main__':

	save_path = "/home/ec2-user/economyAlert/data"
	log_path = "/home/ec2-user/economyAlert/log"
	today = datetime.today()
	today_str = str(today.strftime("%Y-%m-%d"))

	log_message = '5. mail'
	os.system( 'echo "' + log_message + '" >> ' + log_path + '/economy_alert_log.txt' )
	
	data_dir = save_path + "/"
	files = os.listdir(data_dir)

	txt_regex = re.compile('mail')
	mail_file = list(filter(txt_regex.search, files))
	report_link = pd.read_csv(data_dir + mail_file[0], sep = "|")
	page_link = report_link['0'][0]


	SenderMailServer = 'smtp.gmail.com'
	SenderEmail = ''
	SenderPW = ''
	SMail = SendEmail(SenderMailServer, SenderEmail, SenderPW) # 수신 메일 설정 

	TargetEmail = ''
	Subject = "📧 " + " 경제 리포트"

	Message = \
	"""<html>
			<head>
				<meta charset="utf-8">
			</head>
			<body>
				<h2> 당신을 위한 오늘의 경제 리포트 👀 </h2>
				<a href='""" + page_link + """'> Visit Your Report! </a>
			</body>
		</html>
	"""

	SMail.MailSender(Message, Subject, SenderEmail, TargetEmail)
    
	log_message = '5. mail success'
	os.system( 'echo "' + log_message + '" >> ' + log_path + '/economy_alert_log.txt' )
    
	# delete data folder
	print("delete files! " + today_str)
	os.system("rm " + data_dir + "*")
    
	log_message = '99. delete files'
	os.system( 'echo "' + log_message + '" >> ' + log_path + '/economy_alert_log.txt' )