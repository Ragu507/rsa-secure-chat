# forms.py

from django import forms
from .models import *
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_image'].widget.attrs.update({'class': 'form-control-file'})

class MessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=User.objects.all(), label='Recipient', empty_label="Select recipient", widget=forms.Select(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your message here'}))

    class Meta:
        model = Message
        fields = ['recipient', 'content']

    def save(self, commit=True, recipient_private_key=None):
        message = super().save(commit=False)
        if recipient_private_key:
            # Decrypt the message content using the provided private key
            message.decrypt_message(recipient_private_key)
        if commit:
            message.save()
        return message
