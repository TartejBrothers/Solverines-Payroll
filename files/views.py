from django.shortcuts import render
from .forms import add_data
from .models import Values


def home(request):
    form = add_data(request.POST or None)
    if form.is_valid():
        form.save()
        form = add_data()
    context = {"form": form}
    return render(request, "index.html", context)


def search(request):
    return render(request, "search.html")


def payroll(request):
    query = request.GET.get("query")
    print(query)
    results = Values.objects.all()
    print(results)
    if query:
        results = Values.objects.filter(id=query)
    context = {"results": results}
    print(context)
    return render(request, "payroll.html", context)
