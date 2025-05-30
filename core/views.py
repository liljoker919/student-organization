from django.urls import path
from django.shortcuts import render


# Views
def home_page(request):
    return render(request, "core/home.html")


def demo_view(request):
    return render(request, "core/demo.html")
