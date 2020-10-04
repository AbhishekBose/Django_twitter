from django import forms

from .models import Tweet

MAX_TWEET_LENGTH = 240
class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']

    def clean_content(self):
        #in order to make sure that content doesn't cross a length
        content = self.cleaned_data.get("content")
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("this tweet is too long")
        return content