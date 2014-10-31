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

#from base.decorators import active_tab
#from base.utils import fieldAttrs, with_valid_form, RET_CODES
#from backend.models import Talk, TalkSeats
from backend import models
#from base.models import City, University
#from ajax_upload.widgets import AjaxClearableFileInput

logger = logging.getLogger(__name__)

@login_required
def user(request):
    return render(request, 'backend/user.html', {    
    }) 
