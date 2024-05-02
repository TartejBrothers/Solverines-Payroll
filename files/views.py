from django.shortcuts import render
from django.http import Http404, HttpRequest, HttpResponse
from .forms import add_data
from django.template import loader



def home(request):
    form = add_data(request.POST or None)
    if form.is_valid():
        form.save()
        form = add_data()
    dict5 = {"form": form}
    return render(request, "index.html", dict5)
