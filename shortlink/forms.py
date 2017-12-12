from django import forms
from models import LinkEntry

class LinkShortenForm(forms.Form):
   caption = forms.CharField(label='Caption', max_length=LinkEntry.MAX_LINK_LENGTH)
   target_url = forms.CharField(label='Target URL', max_length=LinkEntry.MAX_TARGET_LENGTH)
