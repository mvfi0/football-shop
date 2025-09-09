from django.shortcuts import render

def identity(request):
    context = {
        "app_name": "Football Shop",   # change if needed
        "student_name": "Muhammad Vegard Fathul Islam",   # replace with your name
        "student_class": "KKI", # replace with your class
    }
    return render(request, "main/main.html", context)
