# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import Client, TestCase
from shortlink.models import LinkEntry

# Requirements:
# - Random numbers for ours (no counter)
# - Allow a user to specify own caption
# - Characters not allowed should be replaced
# - Don't collide

class ShortLinkTests(TestCase):
   def test_shorten_a_link(self):
      url = 'http://www.iamahugelink.com/withaverylongpath'
      link_entry = LinkEntry.create(url)

      self.assertLess(len(link_entry.short_link), len(url))
      self.assertEqual(url, link_entry.target_url)

   def test_shorten_link_with_caption(self):
      url = 'https://docs.python.org/2/library/unittest.html#setupmodule-and-teardownmodule'
      link_entry = LinkEntry.create(url, caption='Python Unit Tests! abcdefghijabcdefghijkk')

      # As the caption was specified, it should be greater than SHORTLINK_LENGTH
      self.assertGreater(len(link_entry.short_link), LinkEntry.SHORTLINK_LENGTH)

      # And the caption should be trimmed to the maximum length
      self.assertLessEqual(len(link_entry.short_link), LinkEntry.MAX_LINK_LENGTH)

      # Make sure the users caption has been removed of disallowed characters
      bad_characters = [x for x in link_entry.short_link if x not in
            LinkEntry.ALLOWED_CHARS]

      self.assertFalse(bad_characters)


class APITests(TestCase):
   def test_create_link_via_api(self):
      c = Client()
      response = c.post('/shorten/', {
         'target_url': 'https://docs.djangoproject.com/en/1.11/topics/testing/tools/',
      })
      self.assertEqual(201, response.status_code)

   def test_reject_invalid_urls(self):
      c = Client()
      response = c.post('/shorten/', {
         'target_url': 'HUEHEHUEHUE',
      })
      self.assertEqual(400, response.status_code)
