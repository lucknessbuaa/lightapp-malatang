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

from base.decorators import active_tab
from base.utils import fieldAttrs, with_valid_form, RET_CODES
from backend.models import Dishes
from backend import models

logger = logging.getLogger(__name__)

@require_GET
@login_required
@active_tab('dishes')
def dishes(request):
    dishes = Dishes.objects.all()
    search = False
    if 'q' in request.GET and request.GET['q'] <> "":
        logger.error(request.GET['q'])
        dishes = dishes.filter(Q(name__contains=request.GET['q']))
        if not dishes.exists() :
            search = True
    elif 'q' in request.GET and request.GET['q'] == "":
        return HttpResponseRedirect(request.path)
    table = DishesTable(dishes)
    if search :
        table = DishesTable(dishes, empty_text='没有搜索结果')
    form = DishesForm()
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, "backend/dishes.html", {
        "table": table,
        "form": form
    })


class DishesTable(tables.Table):
    pk = tables.columns.Column(verbose_name='ID')
    name = tables.columns.Column(verbose_name='名称', empty_values=(), orderable=False)
    cover = tables.columns.Column(verbose_name='封面', empty_values=(), orderable=False)
    price = tables.columns.Column(verbose_name='价格', empty_values=(), orderable=False)
    desc = tables.columns.Column(verbose_name='描述', empty_values=(), orderable=False)
    ops = tables.columns.TemplateColumn(verbose_name='操作', template_name='backend/dishes_ops.html', orderable=False)

    class Meta:
        model = Dishes
        empty_text = u'没有宣讲会信息'
        fields = ("name", "cover", "price", "desc", "ops")
        exclude = {'pk'}
        attrs = {
            'class': 'table table-bordered table-striped'
        }


class DishesForm(forms.ModelForm):

    pk = forms.IntegerField(required=False,
        widget=forms.HiddenInput(attrs=us.extend({}, fieldAttrs)))

    name = forms.CharField(label=u"名称",
        widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        })))

    #todo
    cover = forms.CharField(label=u"封面",
        widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        })))

    desc = forms.CharField(label=u"描述",
        widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        })))

    price = forms.FloatField(label=u"价格",
        widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        })))

    class Meta:
        model = Dishes


@require_POST
@json
def add_dishes(request):

    def _add_dishes(form):
        form.save()
        return {'ret_code': RET_CODES["ok"]}

    return with_valid_form(DishesForm(request.POST), _add_dishes)


@require_POST
@json
def delete_dishes(request):
    Dishes.objects.filter(pk=request.POST["id"]).delete()
    return {'ret_code': RET_CODES['ok']}


@require_POST
@json
def edit_dishes(request, id):
    dishes = Dishes.objects.get(pk=id)
    form = DishesForm(request.POST, instance=dishes)

    def _edit_dishes(form):
        form.save()
        return {'ret_code': RET_CODES["ok"]}

    return with_valid_form(form, _edit_dishes)


@require_GET
@login_required
@as_csv(filename='export.csv')
def export_csv(request):
    talkId = request.GET.get('id', None)
    if not talkId:
        return [[u'宣讲会id', u'用户姓名', u'用户邮箱', u'用户手机']]        

    try:
        talk = Talk.objects.get(pk=talkId)
        seats = TalkSeats.objects.filter(talk=talk)

        def map_seat(seat):
            return [
                seat.talk.pk,
                seat.consumer.name,
                seat.consumer.email,
                seat.consumer.phone
            ]

        return [[u'宣讲会id', u'用户姓名', u'用户邮箱', u'用户手机']] + map(map_seat, seats)
    except:
        return [[u'宣讲会id', u'用户姓名', u'用户邮箱', u'用户手机']]        

