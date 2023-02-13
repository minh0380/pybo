from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserForm

# Create your views2 here.

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username') # form.cleaned_data.get 함수는 폼의 입력값을 개별적으로 얻고 싶은 경우에 사용하는 함수
            raw_password = form.cleaned_data.get('password1')
            
            # 신규 사용자를 생성한 후 자동 로그인
            user = authenticate(username=username, password=raw_password) # 사용자 인증(사용자명과 비밀번호가 정확한지 검증)
            login(request, user) # 로그인(사용자 세션 생성)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})