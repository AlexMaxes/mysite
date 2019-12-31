import os
from django.core.mail import send_mail
os.environ['DJANGO_SETTINGS_MODULE']='Django_testcode.settings'

if __name__ == '__main__':
    subject = 'This is an auto send mail from my web test!'
    from_email = 'wushuangmail@foxmail.com'
    to_email = '544046044@qq.com '
    text_content = 'Just test content! There will be more in future!'
    send_mail(subject,text_content,from_email,[to_email])
