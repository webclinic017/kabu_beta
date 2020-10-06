from mail.controller.mailcontroller import  mailController
import datetime
from django.template.loader import render_to_string
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

class dailysummaryController(mailController):
    def __init__(self,contx):
        self.template   ='daily_summary.html'
        now             = datetime.datetime.now()
        subject         = '【株リサーチ公式サイト】{0}サマリー'.format(now.strftime("%Y/%m/%d"))
        to_address      ='lizhu_zhang@rubygroupe.jp'

        self.contx      =contx
        super().__init__(subject,to_address)
        return

    def sendMail(self):
        msg         =self.init_htmlmail()
        self.attach_img_company(msg,self.contx)
        #japan GDP
        self.attach_img(msg, 'japan_gdp', self.contx['indicator']['japan_gdp'])
        #Armenia gdp
        self.attach_img(msg, 'usagdp', self.contx['indicator']['usagdp'])
        #China gdp
        self.attach_img(msg, 'china_gdp', self.contx['indicator']['china_gdp'])
        #japan pmi
        self.attach_img(msg, 'japan_pmi', self.contx['indicator']['japanpmi'])
        #china pmi
        self.attach_img(msg, 'china_pmi', self.contx['indicator']['chinapmi'])
        #usa pmi
        self.attach_img(msg, 'usa_pmi', self.contx['indicator']['usapmi'])
        #japan cpi
        self.attach_img(msg, 'japan_cpi', self.contx['indicator']['japancpi'])
        #
        self.attach_img(msg, 'china_cpi', self.contx['indicator']['chinacpi'])
        #
        self.attach_img(msg, 'usa_cpi', self.contx['indicator']['usacpi'])

        message             = render_to_string(self.template, self.contx)
        msg.attach_alternative(message, "text/html")
        msg.send()
#         return obj.sendHtmlMail()#sendTemplateMail

    def attach_img_company(self,msg,contx):
        companylistnews_img            =contx['companylistnews_img']
        for company in companylistnews_img:
            img_data                    =company['news_img']
            img                         =MIMEImage(base64.b64decode(img_data), 'png')
            img.add_header('Content-Id', '<{0}>'.format(company['company_code']))
            msg.attach(img)


    def attach_img(self,msg,key,value):
        img     =MIMEImage(base64.b64decode(value), 'png')
        img.add_header('Content-Id', '<{0}>'.format(key))
        msg.attach(img)

    def init_htmlmail(self):
        msg                 = MIMEMultipart('alternative')
        text_content        = "Hi!\nHow are you?\n"
        msg                 = EmailMultiAlternatives(self.subject, text_content, self.from_address, [self.to_address])
        return msg