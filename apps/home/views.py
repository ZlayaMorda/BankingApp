from django.shortcuts import render
from django.views import View


class HomeView(View):
    template_name = 'home/home.html'
    
    def get(self, request):
        return render(request, template_name=self.template_name)
