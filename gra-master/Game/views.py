from django.shortcuts import render
from .models import GRA

def score_response(request):
    score = GRA.objects.all()
    return render(request, 'wyniki.html', {'x':score})

# Create your views here.
