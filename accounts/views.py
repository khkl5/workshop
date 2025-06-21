from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.conf import settings

# تسجيل مستخدم جديد
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # حفظ المستخدم
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()

                # تحديث بيانات الملف الشخصي
                profile = user.profile
                profile.phone_number = form.cleaned_data.get('phone_number', '')
                profile.address = form.cleaned_data.get('address', '')
                profile.save()

                # إرسال الإيميل للمستخدم
                send_mail(
                    subject='🎉 مرحباً بك! تم إنشاء حسابك',
                    message=(
                        f'مرحباً {user.first_name or user.username}!\n\n'
                        f'بيانات حسابك:\n'
                        f'اسم المستخدم: {user.username}\n'
                        f'البريد الإلكتروني: {user.email}\n'
                        f'رقم الجوال: {profile.phone_number}\n'
                        f'العنوان: {profile.address}\n\n'
                        'نتمنى لك يوماً سعيداً 🌷'
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                # تسجيل دخول المستخدم
                login(request, user)

            # تحويل لصفحة النجاح
            return redirect('register_success')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

# تسجيل دخول المستخدم
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # بعد تسجيل الدخول يروح للصفحة الرئيسية
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

# صفحة نجاح التسجيل
def register_success(request):
    return render(request, 'accounts/register_success.html')
