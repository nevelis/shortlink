# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from shortlink.models import LinkEntry

class ShortLinkTests(TestCase):
   def test_shorten_a_link(self):
      url = 'http://www.iamahugelink.com/withaverylongpath'
      link_entry = LinkEntry.create(url)

      self.assertLess(len(link_entry.short_link), len(url))
      self.assertEqual(url, link_entry.target_url)
