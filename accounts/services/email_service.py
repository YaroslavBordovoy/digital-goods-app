from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

class EmailService:
    from_email = settings.EMAIL_HOST_USER

    def send_activation_email(
            self,
            username: str,
            domain: str,
            to_email: str,
            uid: str,
            token: str
    ) -> None:
        mail_subject = "Activation link has been sent to your email id"
        context = {
            "username": username,
            "domain": domain,
            "uid": uid,
            "token": token,
        }

        message = render_to_string("registration/acc_activate_email.html", context)
        send_mail(mail_subject, message, self.from_email, [to_email])
