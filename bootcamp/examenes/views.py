from rest_framework import viewsets
from examenes.models import Examen
from examenes.serializer import ExamenSerializer
from django.views.generic import TemplateView


class ExamenViewSet(viewsets.ModelViewSet):
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["examenes"] = Examen.objects.all()
        return context