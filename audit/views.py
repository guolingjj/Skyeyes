from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

from django.contrib.auth import login,authenticate,logout


def acc_login(req):

    error_msg=''
    if req.method=="GET":
        return render(req,"login-page.html")
    else:

        _email=req.POST.get("acc")
        _pwd=req.POST.get("pwd")
        user=authenticate(username=_email,password=_pwd)#验证:返回验证对象,失败则是None
        if user:
            login(req,user)
            next_url = req.GET.get("next", '../web/index')
            return redirect(next_url)
        else:
            print('111')
            error_msg='password or account error'
            return render(req, "login-page.html",{'error_msg':error_msg})
@login_required
def web_ssh(req):
   return render(req,'web_ssh_page.html')
@login_required
def host_mag(req):
    return render(req, 'host_mag.html')
def acc_logout(req):
    logout(req)
    return redirect("/login")