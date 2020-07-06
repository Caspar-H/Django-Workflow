from django.contrib.auth.forms import UserCreationForm
from django import forms

from userlogin.models import User, UserSetting


class RFSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_rf = True
        if commit:
            user.save()
        return user


class EMESignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_eme = True
        if commit:
            user.save()
        return user


class ManagerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_manager = True
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserSettingForm(forms.ModelForm):
    class Meta:
        model = UserSetting
        fields = ('email_notification', )
