from django.contrib.auth.forms import UserCreationForm
from django import forms

from userlogin.models import User, UserSetting


class VHARFSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_vha_rf = True
        if commit:
            user.save()
        return user


class TPGRFSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_tpg_rf = True
        if commit:
            user.save()
        return user


class TPGSAEDSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_tpg_saed = True
        if commit:
            user.save()
        return user


class TPGPMSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_tpg_pm = True
        if commit:
            user.save()
        return user


class TPGEMESignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_tpg_eme = True
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
        fields = ('email_notification',)
