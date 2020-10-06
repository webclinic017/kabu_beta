from django.http.response import HttpResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template import loader
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.template import Context
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
import base64

class mailController:
    def __init__(self,subject,to_address):
        self.from_address           ='zhanglizhu.tokyo@gmail.com'
        self.to_address             =to_address
        self.login_emailaddress     =self.from_address
        self.login_emailpassword    ='tokyo12345'
        self.smtpserver             ='smtp.gmail.com'

        self.subject                =subject
        return

    #init html
    def init_htmlmail(self,template,context):
        message             = render_to_string(template, context)
        msg                 = MIMEMultipart('alternative')
        text_content        = "Hi!\nHow are you?\n"
        msg                 = EmailMultiAlternatives(self.subject, text_content, self.from_address, [self.to_address])
        return msg

#     def sendPlainMail(self,obj):
#         if not obj['Subject']:
#             return 'failure'
#         if not obj['body']:
#             return 'failure'
#         if not obj['to_address']:
#             return 'failure'
#
#         msg                 = MIMEMultipart('alternative')
#         msg['Subject']      = obj['Subject']
#         msg['To']           = obj['to_address']
# #         part                = MIMEText(obj['body'], 'html')
#         part                = MIMEText(self.getTemplatestr(), 'html')
#
#         msg.attach(part)
#
#         s = smtplib.SMTP(self.smtpserver,587)
#
#         s.ehlo()
#         s.starttls()
#         s.ehlo()
#         s.login(self.login_emailaddress, self.login_emailpassword)
#         s.sendmail(self.login_emailaddress, obj['to_address'], msg.as_string())
#         s.quit()
#         return 'success'

#     def sendTemplateMail(self,template,context):
#         message         = render_to_string(template, context)
#
#         from_email      = self.from_address
#         recipient_list  = [self.to_address]  # 宛先リスト
#         send_mail(self.subject, message, from_email, recipient_list,html_message=message)
#         return 'success'

    def sendHtmlMail(self):
        self.init_htmlmail(self.template, self.context)

#         self.attach_img_company(msg, context)
#
#         msg.attach_alternative(message, "text/html")
        msg.send()
        #reference
        #https://stackoverflow.com/questions/1633109/creating-a-mime-email-template-with-images-to-send-with-python-django
        #https://stackoverflow.com/questions/38360758/base64-encoded-image-in-email
        return 'success'



    #
    def attach_img(self,msg,key,value):
        img     =MIMEImage(base64.b64decode(value), 'png')
        img.add_header('Content-Id', '<{0}>'.format(key))
        msg.attach(img)



