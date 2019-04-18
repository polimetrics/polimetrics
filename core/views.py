from django.shortcuts import render, get_object_or_404
from core.models import Candidate

# Create your views here.

def index(request):
    return render(request, "index.html")


# def candidates(request, slug):
#     candidate = get_object_or_404(Candidate, slug=slug)
#     return render(request, "candidates.html")

def candidates(request):
    return render(request, "candidates.html")

def tags(request):
    return render(request, "tags.html")

def methodology(request):
    return render(request, "methodology.html")

def about(request):
    return render(request, "about.html")
