from django.shortcuts import render, redirect
from .forms import add_data
from .models import Database
from num2words import num2words


def home(request):
    form = add_data(request.POST or None)
    if form.is_valid():
        form.save()
        form = add_data()
        return redirect("search")
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
    year = request.GET.get("year")
    medical = request.GET.get("medical")
    leaveallowance = request.GET.get("leaveallowance")
    mobile = request.GET.get("mobile")
    internet = request.GET.get("internet")
    conveyance = request.GET.get("conveyance")
    leaves = request.GET.get("leaves")
    working = request.GET.get("working")
    reimbursement = request.GET.get("reimbursement")
    leavededuction = request.GET.get("leavededuction")
    protax = request.GET.get("protax")
    inctax = request.GET.get("inctax")
    pfdeduc = request.GET.get("pfdeduc")
    otherdeduc = request.GET.get("otherdeduc")
    medicalins = request.GET.get("medicalins")
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
    totalearning = (
        float(basic)
        + float(hra)
        + float(medical)
        + float(leaveallowance)
        + float(mobile)
        + float(internet)
        + float(conveyance)
        + float(reimbursement)
    )
    totaldeduction = (
        float(leavededuction)
        + float(protax)
        + float(inctax)
        + float(pfdeduc)
        + float(otherdeduc)
    )

    netpay = totalearning - totaldeduction
    netpay = round(netpay)
    netpay_in_words = num2words(netpay).title()
    totalearning = f"{totalearning:.2f}"
    totaldeduction = f"{totaldeduction:.2f}"
    context = {
        "employee": employee,
        "basic": basic,
        "hra": hra,
        "pf": pf,
        "leave": leave,
        "medical": medical,
        "leaveallowance": leaveallowance,
        "mobile": mobile,
        "internet": internet,
        "monthname": monthname,
        "conveyance": conveyance,
        "reimbursement": reimbursement,
        "leaves": leaves,
        "working": working,
        "leavededuction": leavededuction,
        "protax": protax,
        "inctax": inctax,
        "pfdeduc": pfdeduc,
        "otherdeduc": otherdeduc,
        "totalearning": totalearning,
        "totaldeduction": totaldeduction,
        "netpay": netpay,
        "netpay_in_words": netpay_in_words,
        "medicalins": medicalins,
        "year": year,
    }
    return render(request, "payroll.html", context)


def convert_to_words(number):
    integer_part_words = num2words(int(number))
    decimal_part = int((number % 1) * 100)
    decimal_part_words = num2words(decimal_part)
    result = f"{integer_part_words}"
    return result
