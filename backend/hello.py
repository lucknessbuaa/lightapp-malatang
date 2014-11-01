# coding: utf-8
import time
import logging

from django.db.models import Q
from django import forms
from django.core.cache import get_cache
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.conf import settings 
from django.utils.safestring import mark_safe
import django_tables2 as tables
from django_tables2 import RequestConfig
from underscore import _ as us
from django_render_json import json
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from base.decorators import active_tab,active_record
from base.utils import fieldAttrs, RET_CODES, with_valid_form
from base.models import Account
from backend.models import Page, UploadFile, Dialog, PageItem
from backend import wps

MEDIA_URL = settings.MEDIA_URL
cache = get_cache('default')
logger = logging.getLogger(__name__)


class PageForm(forms.ModelForm):
    pk = forms.IntegerField(required=False,
            widget=forms.HiddenInput(attrs=us.extend({}, fieldAttrs)))
    title = forms.CharField(label=_(u'Title'),  
            widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
                'parsley-required': '','parsley-maxlength': '50',
            })))
    cover = forms.CharField(label=_(u'Cover'), required=False,
            widget=forms.TextInput(attrs=us.extend({}, fieldAttrs)))
    desc = forms.CharField(label=_(u'Desc'), required=False,
            widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {'parsley-maxlength':'255',})))
    url = forms.CharField(label=_(u'URL'),
            widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
                'parsley-required': '','parsley-maxlength':'255' ,
            })))

    class Meta:
        model = Page
        exclude = ('pk', 'account')


class PageTable(tables.Table):
    ops = tables.columns.TemplateColumn(verbose_name=_('Ops'), template_name='page_ops.html', orderable=False)

    def render_url(self, value):
        LIMIT = 75
        if len(value) > LIMIT:
            ellipsis = "<span style='display: inline-block;'>...</span>"
            name = value[0:LIMIT] + ellipsis
        else:
            name = value
        return mark_safe(u'<a href="%s" title="%s">%s</a>' % (value, value, name))

    def render_cover(self, value):
        if value != '':
            url = value
            return mark_safe('<a href="%s"><img src="%s" class="img-thumbnail"></a>' % (url, url))
        else:
            return mark_safe('<a><img></a>')

    class Meta:
        model = Page
        empty_text = _(u'no pages')
        orderable=False
        exclude=('id', 'account')
        attrs = {
            'class': 'table table-bordered table-striped'
        }

@require_GET
@login_required
@active_tab('pages')
@active_record
def pages(request):
    account = Account.objects.get(user__pk=request.user.pk)
    pages = Page.objects.filter(account=account)
    if 'q' in request.GET and request.GET['q'] <> "":
        message = request.GET['q']
        pages = pages.filter(Q(title__contains=message)|\
        Q(desc__contains=message))
    elif 'q' in request.GET and request.GET['q'] == "":
        return HttpResponseRedirect(request.path)
    table = PageTable(pages)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    form = PageForm()
    return render(request, "pages.html", {'table': table, 'form': form})

@require_POST
@login_required(login_url="/login.json")
@json
def add_page(request):
    def _add_page(form):
        page = form.save(commit=False)
        page.account = Account.objects.get(user__pk=request.user.pk)
        page.save()
        return {'ret_code': RET_CODES["ok"]}
    return with_valid_form(PageForm(request.POST), _add_page)


@require_POST
@login_required(login_url="/login.json")
@json
def edit_page(request, id):
    account = Account.objects.get(user__pk=request.user.pk)
    page = Page.objects.get(pk=id, account=account)
    form = PageForm(request.POST, instance=page)

    def _edit_page(form):
        form.save()
        if len(PageItem.objects.filter(page=page)) > 0:
            wps.emitChangeEvent(account)
        return {'ret_code': RET_CODES["ok"]}

    return with_valid_form(form, _edit_page)


@require_POST
@login_required(login_url="/login.json")
@json
def delete_page(request):
    account = Account.objects.get(user__pk=request.user.pk)
    Page.objects.filter(pk=request.POST["id"], account=account).delete()
    wps.emitChangeEvent(account)
    return {'ret_code': RET_CODES['ok']}
    
