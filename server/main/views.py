from django.views.generic import CreateView

from .models import Contact
from .forms import ContactForm
# from .service import send
# from .tasks import send_spam_email

class ContactView(CreateView):

    model = Contact
    form_class = ContactForm
    success_url = '/'
    template_name = 'main/contact.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)