# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import render
from shortlink.models import LinkEntry
from shortlink.forms import LinkShortenForm
import json

def index(request):
   return render(request, 'index.tpl', { 'link_form': LinkShortenForm() })

def shorten(request):
   if 'x-www-form-urlencoded' in request.content_type:
      caption = request.POST.get('caption', None)
      target_url = request.POST['target_url']
   elif 'json' in request.content_type:
      data = json.loads(request.body)
      caption = data.get('caption', None)
      target_url = data.get('target_url')
   else:
      return HttpResponse(status=406) # Not Acceptable

   try:
      link_entry = LinkEntry.create(target_url, caption=caption)
   except Exception, e:
      return HttpResponse(e, status=400)

   return JsonResponse({
         'short_link': '//{}/{}'.format(request.get_host(), link_entry.short_link),
         'target_url': target_url,
      }, status=201)

def follow(request, short_link):
   try:
      link_entry = LinkEntry.objects.get(short_link=short_link)
   except LinkEntry.DoesNotExist:
      return HttpResponseNotFound()

   return HttpResponsePermanentRedirect(link_entry.target_url)
