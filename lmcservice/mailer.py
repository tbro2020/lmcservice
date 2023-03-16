from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives


class Mailer:
    def __init__(self, template, context, subject, to):
        html_content = get_template(template).render(context)
        text_content = strip_tags(html_content)
        self.message = EmailMultiAlternatives(subject, text_content, to=to, from_email=settings.DEFAULT_FROM_EMAIL)
        self.message.attach_alternative(html_content, "text/html")

    def send(self):
        self.message.send()
