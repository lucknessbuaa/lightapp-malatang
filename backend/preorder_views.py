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
from backend.models import SeatOrder
from backend import models

logger = logging.getLogger(__name__)

@require_GET
@login_required
@active_tab('preorder')
def preorder(request):
    preorder = SeatOrder.objects.exclude(status=-1)
    preorder = SeatOrder.objects.all()
    table = PreorderTable(preorder)
    form = PreorderForm()
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, "backend/preorder.html", {
        "table": table,
        "form": form
    })


class PreorderTable(tables.Table):
    pk = tables.columns.Column(verbose_name='ID')
    time = tables.columns.DateTimeColumn(verbose_name='创建时间', empty_values=(), orderable=False, format='Y-m-d H:i')
    start = tables.columns.DateTimeColumn(verbose_name='起始时间', empty_values=(), orderable=False, format='Y-m-d H:i')
    end = tables.columns.DateTimeColumn(verbose_name='结束时间', empty_values=(), orderable=False, format='Y-m-d H:i')
    number = tables.columns.Column(verbose_name='人数', empty_values=(), orderable=False)
    status = tables.columns.Column(verbose_name='状态', empty_values=(), orderable=False)
    ops = tables.columns.TemplateColumn(verbose_name='操作', template_name='backend/preorder_ops.html', orderable=False)
    
    def render_status(status, value):
        if value == 0:
            return '未处理'
        elif value == 1:
            return '已完成'
        elif value == -1:
            return '已删除'
        else :
            return '未知状态'

    class Meta:
        model = SeatOrder
        empty_text = u'没有预约信息'
        fields = ('time', 'start', 'end', 'number', 'status', 'ops') 
        exclude = {'pk'}
        attrs = {
            'class': 'table table-bordered table-striped'
        }


class PreorderForm(forms.ModelForm):

    pk = forms.IntegerField(required=False,
        widget=forms.HiddenInput(attrs=us.extend({}, fieldAttrs)))

    start = forms.CharField(label=u"起始时间",
        widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        })))

    end = forms.CharField(label=u"结束时间",
        widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        })))

    number = forms.IntegerField(label=u"人数",
        widget=forms.NumberInput(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        })))

    class Meta:
        model = SeatOrder


@require_POST
@json
def delete_preorder(request):
    preorder = SeatOrder.objects.get(pk=request.POST["id"])
    preorder.status = -1
    preorder.save()
    return {'ret_code': RET_CODES['ok']}


@require_POST
@json
def complete_preorder(request):
    preorder = SeatOrder.objects.get(pk=request.POST["id"])
    preorder.status = 1
    preorder.save()
    return {'ret_code': RET_CODES['ok']}


@require_POST
@json
def edit_preorder(request, id):
    preorder = SeatOrder.objects.get(pk=id)
    try:
        preorder.start = request.POST['start']
        preorder.end = request.POST['end']
        preorder.number = request.POST['number']
        preorder.save()
    except:
        return {'ret_code': RET_CODES['form-invalid']}

    return {'ret_code': RET_CODES['ok']}

