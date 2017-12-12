# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import random
import string


class LinkEntry(models.Model):
   '''Length of the shortlinks we generate'''
   SHORTLINK_LENGTH = 5

   '''Maximum length of the link if specified by user'''
   MAX_LINK_LENGTH = 32

   '''Maximum length of target URL'''
   MAX_TARGET_LENGTH = 4096

   '''Set of characters allowed in a shortlink'''
   ALLOWED_CHARS = string.ascii_uppercase \
                 + string.ascii_lowercase \
                 + string.digits

   short_link = models.CharField(max_length=MAX_LINK_LENGTH, unique=True)
   target_url = models.CharField(max_length=MAX_TARGET_LENGTH)

   @staticmethod
   def create(url, caption=None):
      entry = LinkEntry()
      if caption:
         entry.short_link = caption.translate(
               ''.join(LinkEntry.ALLOWED_CHARS))[:LinkEntry.MAX_LINK_LENGTH]
      else:
         entry.short_link = ''.join(random.choice(LinkEntry.ALLOWED_CHARS)
               for _ in range(LinkEntry.SHORTLINK_LENGTH))
      entry.target_url = url
      entry.save()
      return entry
