from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
import lightkurve as lk

# Create your views here.
def home(request):
    return render(request,'PH_app/search.html')

def search_star(target_name):
    if target_name == '' :
        print("No Target Name input/ Author selected")
        dataJSON = dumps(search_result)
        return render(request, '/home', {'data': dataJSON})
    else:
        search_result = lk.search_lightcurve(target_name)
        filtered = False
        dataJSON = dumps(search_result)
        return render(request, '/home', {'data': dataJSON})