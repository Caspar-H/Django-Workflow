from django.contrib.auth.forms import UserCreationForm

from userlogin.models import User


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

