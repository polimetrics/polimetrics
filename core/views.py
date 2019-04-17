from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html")


def candidates(request):
    return render( request, "candidates.html")

def candidateDetail(request):
    return render(request, "candidateDetail.html")


def tags(request):
    return render(request, "tags.html")


def about(request):
    return render(request, "about.html")



