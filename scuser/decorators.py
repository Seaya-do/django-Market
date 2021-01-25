from django.shortcuts import redirect
from .models import Scuser


#login하지않으면 자동으로 로그인 화면넘어가기
def login_required(funtion):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        if user is None or not user:
            return redirect('/login')
        print('login_required!')
        return funtion(request, *args, **kwargs)
    return wrap


#관리자(admin)권한이 주어질때
def admin_required(funtion):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        if user is None or not user:
            return redirect('/login')
        user = Scuser.objects.get(email=user)
        if user.level != 'admin':
            return redirect('/')

        print('login_required!')
        return funtion(request, *args, **kwargs)
    return wrap