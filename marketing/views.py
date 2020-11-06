# from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from CLOTH.settings import CURRENT_PATH
import os

ROBOTS_PATH = os.path.join(BASE_DIR, 'marketing/robots.txt')

def robots(request):
    """ view for robots.txt file """
    return HttpResponse(open(ROBOTS_PATH).read(), 'text/plain')