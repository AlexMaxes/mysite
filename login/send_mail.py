import os
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'Django_testcode.settings'

if __name__ == '__main__':
    subject = 'This is an auto send mail from my web test!'
    from_email = 'wushuangmail@foxmail.com'
    to_email = '544046044@qq.com '
    text_content = 'Just test content! There will be more in future!'
    html_content = '<p>welcome to my site:<a href="http://127.0.0.1:8000/login/" target=blank>www.wushuang.com</a>'\
                   '(There is empty, just for now :)</p> <p>AlexMaxes</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
