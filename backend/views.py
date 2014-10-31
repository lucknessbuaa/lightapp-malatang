import logging

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import django.contrib.auth as auth
from django.views.decorators.csrf import ensure_csrf_cookie
from django_render_json import render_json, json

from backend.utils import RET_CODES

logger = logging.getLogger(__name__)

@ensure_csrf_cookie
def login(request):
    if request.method == 'GET':
        return render(request, "backend/login.html", {})
    else:
        user = request.POST.get('username', None)
        logger.debug(user)
        password = request.POST.get('password', None)
        logger.debug(password)
        user = auth.authenticate(username=user, password=password)

        if not user:
            return render_json({'ret_code': RET_CODES["auth-failure"]})

        auth.login(request, user)
        return render_json({'ret_code': RET_CODES["ok"]})

def exit(request):
    auth.logout(request)
    return redirect('/backend/login')

def index(request):
    if not request.user.is_authenticated():
        return redirect('/backend/login')
    elif not request.user.is_staff:
        logger.debug(request.user.is_staff)
        return redirect('/backend/login')
    else:
        return redirect('/backend/takeout')


