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
    month = request.GET.get("month")
    basic = request.GET.get("basic")
    hra = request.GET.get("hra")
    pf = request.GET.get("pf")
    leave = request.GET.get("leave")
    medical = request.GET.get("medical")
    mobile = request.GET.get("mobile")
    internet = request.GET.get("internet")
    conveyance = request.GET.get("conveyance")
    reimbursement = request.GET.get("reimbursement")
    print(month)
    month = int(month)
    monthname = None
    if month == 1:
        monthname = "January"
    elif month == 2:
        monthname = "February"
    elif month == 3:
        monthname = "March"
    elif month == 4:
        monthname = "April"
    elif month == 5:
        monthname = "May"
    elif month == 6:
        monthname = "June"
    elif month == 7:
        monthname = "July"
    elif month == 8:
        monthname = "August"
    elif month == 9:
        monthname = "September"
    elif month == 10:
        monthname = "October"
    elif month == 11:
        monthname = "November"
    elif month == 12:
        monthname = "December"

    results = Database.objects.all()

    if query:
        employee = Database.objects.get(id=query)
    salary = employee.salary
    print(salary)
    print(employee)
    # basic = salary * 0.3
    # hra = basic * 0.6
    # pf = basic * 0.12
    # leave = 3333
    # medical = 8333
    # mobile = 4000
    # internet = 2000
    # conveyance = salary - basic - hra - pf - leave - medical - mobile - internet

    context = {
        "employee": employee,
        "basic": basic,
        "hra": hra,
        "pf": pf,
        "leave": leave,
        "medical": medical,
        "mobile": mobile,
        "internet": internet,
        "monthname": monthname,
        "conveyance": conveyance,
        "reimbursement": reimbursement,
    }
    return render(request, "payroll.html", context)
