from django.core.mail import send_mail


def send(user_email, name):
    send_mail(
        'Здравствуйте, {}'.format(name),
        'Вы подписались на рассылку\nМы будем присылать Вам много спама',
        'P.S. MishaniaHomi',
        [user_email],
        fail_silently=False
    )