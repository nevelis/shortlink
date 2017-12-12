# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from shortlink.models import LinkEntry

def shorten(request):
   caption = request.POST['caption'] if 'caption' in request.POST else None
   target_url = request.POST['target_url']

   link_entry = LinkEntry.create(target_url, caption=caption)
   return JsonResponse({
         '': link_entry.short_link,
         'target_url': target_url,
      }, status=201)
