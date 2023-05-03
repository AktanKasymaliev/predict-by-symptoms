from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = 'patient/login/'

    def get(self, request, *args, **kwargs):
        return super(ChatView, self).get(request, *args, **kwargs)