from django.views.generic.base import TemplateView
import os

MAPS_KEY_LABEL = 'MAPS_KEY'
GOOGLE_MAPS_API_KEY = os.environ.get(MAPS_KEY_LABEL)

class MapperView(TemplateView):

    template_name = 'mapper/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[MAPS_KEY_LABEL] = GOOGLE_MAPS_API_KEY
        return context
