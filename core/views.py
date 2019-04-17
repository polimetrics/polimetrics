from django.shortcuts import render, get_object_or_404
from core.models import Candidate

# Create your views here.

def index(request):
    return render(request, "index.html")


# def candidate(request, slug):
#     candidate = get_object_or_404(Candidate, slug=slug)
#     return render(request, "candidate.html")



def candidates(request):
    return render( request, "candidates.html")

def candidateDetail(request):
    return render(request, "candidateDetail.html")


def tags(request):
    return render(request, "tags.html")


def about(request):
    return render(request, "about.html")
