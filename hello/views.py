from django.shortcuts import render
from django.http import HttpResponse
from githubwoocommerce.Bridge import Bridge
import json

from .models import Greeting

# Create your views here.
def index(request):
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        bridge = Bridge()
        return HttpResponse(json.dumps(bridge.insert(body)), content_type="application/json")
    except Exception:
        print("Exception caught")
    finally:
        return HttpResponse('')

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

