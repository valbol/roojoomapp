from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from .models import IssueForm


def helper_check(check_data, test_with, message) -> bool:
    global result
    if check_data == test_with:
        result = message
        return True
    return False

def helper_only_numbers() -> None:
    global result
    result = "Bad serial number"

def check_24x(args) -> None:
    global result
    result = "please upgrade your device"

def check_36x(args) -> None:
    if helper_check(args, ['OFF','OFF','OFF'], "Turn on the device"):
        return
    elif helper_check(args, ["ON","ON","ON"], "All is OK"):
        return
    elif args.count('BLINK') == 2:
        global result 
        result = "Please wait"
  

def check_48z(args) -> None:
    if helper_check(args, ['OFF','OFF','OFF'], "Turn on the device"):
        return
    elif helper_check(args[0], 'BLINK', "Please wait"):
        return
    elif args.count('ON') > 1 and args.count('BLINK') == 0:
        global result
        result = "All is OK"
   

def check_51b(args) -> None:
    if helper_check(args, ['OFF','OFF','OFF'], "Turn on the device"):
        return
    elif helper_check(args[0], 'BLINK', "Please wait"):
        return
    elif args.count('ON') > 0 and args.count('BLINK') == 0:
        global result
        result = "All is OK"
   

def default(args) -> None:
    global result
    result = "Unknown device"

def resolve_issue(serial, args) -> None:
    if serial.isnumeric(): 
        helper_only_numbers()
    else:
        serial_prefix = serial[:4].lower()
        switcher = {"24-x": check_24x, "36-x": check_36x, "48-z": check_48z, "51-b": check_51b}
        switcher.get(serial_prefix, default)(args)

def generate_response(form) -> HttpResponse:
    issue = form.save(commit=False)
    resolve_issue(form.cleaned_data["serial"], [form.cleaned_data["light_status1"], form.cleaned_data["light_status2"], form.cleaned_data["light_status3"]]) 
    issue.save()
    response = f"The Resolution is: {result}"
    return HttpResponse(response, status=200)

def index(request) -> render:
    global result 
    if request.method == 'POST':
        form = IssueForm(request.POST)   
        if form.is_valid():
            return generate_response(form)
    else:
        form = IssueForm()
    return render(request, 'issues/form.html', {'form': form})