from django.shortcuts import render
from .forms import add_data
from .models import Database


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

    results = Database.objects.all()
    ibasic = None
    if results.exists():
        total_salary = sum(result.salary for result in results)
        basic = total_salary * 0.3

    if query:
        results = Database.objects.filter(id=query)
    hra = basic * 0.6
    pf = basic * 0.12
    leave = 3333
    medical = 8333
    mobile = 4000
    internet = 2000
    conveyance = total_salary - basic - hra - pf - leave - medical - mobile - internet
    context = {
        "results": results,
        "basic": basic,
        "hra": hra,
        "pf": pf,
        "leave": leave,
        "medical": medical,
        "mobile": mobile,
        "internet": internet,
        "conveyance": conveyance,
    }
    print(conveyance)
    return render(request, "payroll.html", context)
