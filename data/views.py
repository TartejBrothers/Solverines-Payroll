from decimal import Decimal, InvalidOperation

from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from num2words import num2words

from .forms import add_data
from .models import Database

MONTH_NAMES = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

ZERO = Decimal("0")


def money(value):
    """Format a Decimal as a two-decimal string for number inputs."""
    return f"{value:.2f}"


def payroll_defaults(employee):
    """
    Calculate monthly payroll defaults from yearly CTC.

    Salary components are based on monthly CTC. ESI eligibility and employer
    ESI are solved algebraically so eligibility never creates a circular
    reference. User-entered values on the search form remain editable.
    """

    medical_insurance = Decimal("677.00")

    fields = (
        "monthly_ctc",
        "basic",
        "hra",
        "special",
        "pf_employee",
        "pf_employer",
        "medical_insurance",
        "esi_employee",
        "esi_employer",
        "gross",
    )

    if employee.ctc is None or employee.ctc == "":
        return {
            **{field: "" for field in fields},
            "medical_insurance": money(medical_insurance),
        }

    monthly_ctc = Decimal(str(employee.ctc)) / Decimal("12")
    basic = monthly_ctc * Decimal("0.50")
    hra = basic * Decimal("0.50")

    # PF is calculated on Basic, subject to the configured base ceiling.
    # Medical insurance is outside CTC and does not affect this base.
    pf_base = basic
    pf_base = min(Decimal("25000"), max(ZERO, pf_base))

    pf_employee = pf_base * Decimal("0.12")
    pf_employer = pf_base * Decimal("0.13")

    # Gross = monthly CTC - employer PF - employer ESI. Solve the eligible
    # case as G = (CTC - employer PF) / (1 + employer ESI rate).
    gross_without_esi = monthly_ctc - pf_employer
    gross_with_esi = gross_without_esi / Decimal("1.0325")

    if gross_with_esi <= Decimal("21000"):
        esi_employer = gross_with_esi * Decimal("0.0325")
        gross = monthly_ctc - pf_employer - esi_employer
        esi_employee = gross * Decimal("0.0075")
    else:
        gross = gross_without_esi
        esi_employee = ZERO
        esi_employer = ZERO

    special = monthly_ctc - basic - hra

    return {
        "monthly_ctc": money(monthly_ctc),
        "basic": money(basic),
        "hra": money(hra),
        "special": money(special),
        "pf_employee": money(pf_employee),
        "pf_employer": money(pf_employer),
        "medical_insurance": money(medical_insurance),
        "esi_employee": money(esi_employee),
        "esi_employer": money(esi_employer),
        "gross": money(gross),
    }


def home(request):
    form = add_data(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("search")
    return render(request, "index.html", {"form": form})


def search(request):
    employee_id = request.GET.get("query", "").strip()

    # Save the CTC submitted from the search page.
    if request.method == "POST":
        employee_id = request.POST.get("query", "").strip()
        employee = get_object_or_404(Database, id=employee_id)

        try:
            ctc = Decimal(request.POST.get("ctc", "").strip())
            if ctc < 0:
                raise InvalidOperation
        except (InvalidOperation, TypeError, AttributeError):
            return HttpResponseBadRequest("Enter a valid, non-negative CTC.")

        employee.ctc = ctc
        employee.save(update_fields=["ctc"])

        return redirect(f"/search/?query={employee.id}")

    employee = None
    defaults = {
        "medical_insurance": "677.00",
    }

    if employee_id:
        employee = get_object_or_404(Database, id=employee_id)
        defaults = payroll_defaults(employee)

    return render(
        request,
        "search.html",
        {
            "employee": employee,
            "defaults": defaults,
            "query": employee_id,
        },
    )


def payroll(request):
    employee_id = request.GET.get("query", "").strip()
    if not employee_id:
        return HttpResponseBadRequest("An employee ID is required.")

    employee = get_object_or_404(Database, id=employee_id)

    try:
        month = int(request.GET.get("month", ""))
        monthname = MONTH_NAMES[month]
    except (TypeError, ValueError, KeyError):
        return HttpResponseBadRequest("Month must be a number from 1 to 12.")

    amount_fields = [
        "basic",
        "hra",
        "special",
        "reimbursement",
        "leavededuction",
        "protax",
        "inctax",
        "pf_employee",
        "pf_employer",
        "medical_insurance",
        "esi_employee",
        "esi_employer",
        "volunteer_pf",
    ]

    amounts = {}
    try:
        for field in amount_fields:
            value = request.GET.get(field, "").strip()
            amounts[field] = Decimal(value) if value else ZERO
    except (InvalidOperation, AttributeError):
        return HttpResponseBadRequest("Payroll amounts must be valid numbers.")

    # Employee PF, ESI, VPF, and medical insurance are salary deductions.
    pf_employee = amounts["pf_employee"]
    esi_employee = amounts["esi_employee"]
    monthly_ctc = Decimal(str(employee.ctc or ZERO)) / Decimal("12")
    gross = monthly_ctc - amounts["pf_employer"] - amounts["esi_employer"]
    # Recalculate this from the final gross and entered Basic/HRA so the
    # payslip always follows the salary-list formula, including edits.
    special = gross - amounts["basic"] - amounts["hra"]
    otherdeduc = amounts["volunteer_pf"] + amounts["medical_insurance"]
    totalearning = gross + amounts["reimbursement"]

    totaldeduction = (
        amounts["leavededuction"]
        + amounts["protax"]
        + amounts["inctax"]
        + pf_employee
        + esi_employee
        + otherdeduc
    )
    netpay = round(gross - totaldeduction + amounts["reimbursement"], 0)
    netpay_in_words = num2words(netpay, lang="en_IN").title()

    context = {
        "employee": employee,
        "monthname": monthname,
        "year": request.GET.get("year"),
        "leaves": request.GET.get("leaves"),
        "working": request.GET.get("working"),
        "gross": money(gross),
        "special": money(special),
        "pf_employee": money(pf_employee),
        "esi_employee": money(esi_employee),
        "esi_employer": money(amounts["esi_employer"]),
        "pf_employer": money(amounts["pf_employer"]),
        "reimbursement": money(amounts["reimbursement"]),
        "medical_insurance": money(amounts["medical_insurance"]),
        "volunteer_pf": money(amounts["volunteer_pf"]),
        "otherdeduc": money(otherdeduc),
        "totalearning": money(totalearning),
        "totaldeduction": money(totaldeduction),
        "netpay": netpay,
        "netpay_in_words": netpay_in_words,
    }

    # Also pass the submitted amount fields to the template.
    context.update({key: money(value) for key, value in amounts.items() if key != "special"})

    return render(request, "payroll.html", context)
