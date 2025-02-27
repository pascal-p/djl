from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', ) # 'created_at', 'updated_at' => automatically excluded?
