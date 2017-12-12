# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import render
from shortlink.models import LinkEntry
from shortlink.forms import LinkShortenForm

def index(request):
   return render(request, 'index.tpl', { 'link_form': LinkShortenForm() })

def shorten(request):
   caption = request.POST['caption'] if 'caption' in request.POST else None
   target_url = request.POST['target_url']

   try:
      link_entry = LinkEntry.create(target_url, caption=caption)
   except:
      return HttpResponse(status=400)

   return JsonResponse({
         'short_link': link_entry.short_link,
         'target_url': target_url,
      }, status=201)

def follow(request, short_link):
   try:
      link_entry = LinkEntry.objects.get(short_link=short_link)
   except LinkEntry.DoesNotExist:
      return HttpResponseNotFound()

   return HttpResponsePermanentRedirect(link_entry.target_url)
