from django import forms
from .models import User


class RegistrationForm(forms.ModelForm):  # Форма для регистрации пользователей
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  # Указываем поля: имя, фамилия и email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User .objects.filter(email=email).exists():
            raise forms.ValidationError("Этот адрес электронной почты уже используется.")
        return email

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Имя"
        self.fields['last_name'].label = "Фамилия"
        self.fields['email'].label = "Электронная почта"