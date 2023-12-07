from django.template.loader import render_to_string
from django.core.mail import send_mail
from banking.settings import EMAIL_BASE_ADDRESS


class AuthEmail:
    __template_path = 'email/login_email.html'
    __subject = 'Banking System Email Login Verification'
    __from_email = EMAIL_BASE_ADDRESS

    def send_login_mail(self, message, url, to_email):
        message = render_to_string(self.__template_path, {'message': message, 'url': url})

        send_mail(subject=self.__subject, html_message=message, message=message, from_email=self.__from_email,
                  recipient_list=to_email)
