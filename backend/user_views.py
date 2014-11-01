# coding: utf-8
import logging
from datetime import datetime

from underscore import _ as us
from django.db.models import Q
from django import forms
from django.core.cache import get_cache
from django.core.urlresolvers import reverse
from django.db import InternalError
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.conf import settings 
from django.utils.safestring import mark_safe
import django_tables2 as tables
from django_tables2 import RequestConfig
from django_render_json import json
from django_render_csv import as_csv
from django.http import HttpResponseRedirect
from social_auth.db.django_models import UserSocialAuth
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.html import escape

from base.decorators import active_tab
from base.utils import fieldAttrs, with_valid_form, RET_CODES
from backend.models import Dishes
from backend import models

logger = logging.getLogger(__name__)

@require_GET
@login_required
@active_tab('user')
def user(request):
    user = User.objects.filter(is_staff=False)
    search = False
    if 'q' in request.GET and request.GET['q'] <> "":
        logger.error(request.GET['q'])
        user = user.filter(Q(name__contains=request.GET['q']))
        if not user.exists() :
            search = True
    elif 'q' in request.GET and request.GET['q'] == "":
        return HttpResponseRedirect(request.path)
    table = UserTable(user)
    if search :
        table = UserTable(user, empty_text='没有搜索结果')
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, "backend/user.html", {
        "table": table
    })


class UserTable(tables.Table):
    username = tables.columns.Column(verbose_name='昵称', empty_values=(), orderable=False)
    id = tables.columns.Column(verbose_name='头像', empty_values=(), orderable=False)
    date_joined = tables.columns.DateTimeColumn(verbose_name='创建时间', empty_values=(), format='Y-m-d H:i')
    last_login = tables.columns.DateTimeColumn(verbose_name='最近登录时间', empty_values=(), format='Y-m-d H:i')


    def render_id(id, value):
        user = User.objects.get(id=value)
        social = UserSocialAuth.objects.get(user=user)
        imgUrl = ""
        if social.provider == 'baidu':
            imgUrl = 'http://tb.himg.baidu.com/sys/portrait/item/{portrait}' % social.extra_data
        elif social.provider == 'weibo':
            imgUrl =  social.extra_data['profile_image_url']
        elif social.provider == 'qq':
            imgUrl = social.extra_data['figureurl_2']
        return mark_safe('<img src="%s" />' % escape(imgUrl))
        
    class Meta:
        model = User
        empty_text = u'没有用户信息'
        fields = ("username", "id", "date_joined", "last_login")
        attrs = {
            'class': 'table table-bordered table-striped'
        }

