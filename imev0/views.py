
from django.views.generic import TemplateView, View
from django.http import HttpResponse
import json

class Index(TemplateView):
    template_name = 'test.html'
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        return context


class Datas(View):
    def get(self, request, *args, **kwargs):

        labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
        datas = [28, 48, 40, 19, 86, 27, 90]
        output = {'labels': labels, 'datas': datas}
        return HttpResponse(json.dumps(output))
