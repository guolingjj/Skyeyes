from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

from django.contrib.auth import login,authenticate,logout
from backend.multitask import MultiTaskManage
import json

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

def batch_task_mag(req):
    if req.method=='POST':
        task_arguments=json.loads(req.POST.get('task_args'))


        task_obj=MultiTaskManage(req)
        task_id=task_obj.task_id

        return HttpResponse(task_id)