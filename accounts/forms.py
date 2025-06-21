from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(
        max_length=30,
        label="اسم المستخدم",
        help_text=None
    )
    first_name = forms.CharField(label='الاسم', max_length=50)
    email = forms.EmailField(label='البريد الإلكتروني')
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تأكيد كلمة المرور', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("هذا البريد الإلكتروني مستخدم من قبل")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("اسم المستخدم مستخدم من قبل")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise ValidationError("كلمتا المرور غير متطابقتين")
