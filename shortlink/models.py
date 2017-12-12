# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, IntegrityError
from django.core.validators import URLValidator

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
         bad_characters = set(caption) - set(LinkEntry.ALLOWED_CHARS)
         if bad_characters:
            raise Exception('Invalid characters in caption: ' + ' '.join(bad_characters))
         if len(caption) > LinkEntry.MAX_LINK_LENGTH:
            raise Exception('Caption is too long')
      else:
         entry.short_link = ''.join(random.choice(LinkEntry.ALLOWED_CHARS)
               for _ in range(LinkEntry.SHORTLINK_LENGTH))

      validator = URLValidator()
      validator(url)

      entry.target_url = url

      try:
         entry.save()
      except IntegrityError, e:
         if 'Duplicate' in str(e):
            raise Exception('A link with this caption already exists')
         raise
      return entry
