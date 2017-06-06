#/usr/bin/env python
#!_*_coding:utf-8_*_


from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from models import context
import traceback
import datetime
from django.utils import timezone
import json


# Create your views here.

def Login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    data = {'loginstatus':'','user':''}
    if request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            data['user'] = user
            return HttpResponseRedirect('/')
        data['loginstatus'] = 'your username or password id uncorrect!'
    return  render(request,'login/login.html',data)


def Logout(request):
    auth.logout(request)
    return render(request,'login/login.html')


@login_required
def Index(request):
    return render_to_response('web/index.html',{'user':request.user})


@login_required
def Overview(request):
    context_obj = context.objects.all().order_by('-id')
    return render_to_response('web/overview.html',{'context_obj':context_obj,'user':request.user})


@csrf_exempt
@login_required
def Deltails(request,id):
    record = context.objects.get(id=id)
    if request.method == 'POST':
        record.status = 1
        record.save()
        return HttpResponse("ok")
    return render_to_response('web/details.html',{'record':record,'user':request.user})


@login_required
def Record(request):
    return render_to_response('web/record.html',{'user':request.user})

@csrf_exempt
@login_required
def Counts(request):
    title,time,details= request.POST.get('title'),request.POST.get('time'),request.POST.get('details')
    try:
        obj = context.objects.create(title=title,time=time,details=details,auther=request.user)
        return render_to_response('web/record.html', {'user': request.user})
    except:
        traceback.print_exc()

@csrf_exempt
@login_required
def Search(request):
    if request.method == 'POST':
        datas = {}
        str = ""
        get_data = request.POST
        context_obj = None

        for re in get_data:
            if get_data.get(re):
                if re == "Type":
                    if get_data.get(re) == "All":
                        datas['status'] = 2
                    elif get_data.get(re) == "Solved":
                        datas['status'] = 1
                    elif get_data.get(re) == "Unsolved":
                        datas['status'] = 0
                    else:
                        pass
                else:
                    datas[re] = get_data.get(re)

        if len(datas.keys()) == 1 :
            if 'Auther' in datas.keys():
                try:
                    context_obj  = context.objects.filter(auther = datas['Auther']).order_by("-id")
                except:
                    traceback.print_exc()
            elif 'StartTime' in datas.keys():
                try:
                    st = datetime.datetime.strptime(datas['StartTime'], "%Y-%m-%d").date()
                    no = timezone.localtime(timezone.now()).strftime("%Y-%m-%d")
                    et = datetime.datetime.strptime(no,"%Y-%m-%d").date()
                    context_obj = context.objects.filter(time__range=(st, et)).order_by("-id")
                except:
                    traceback.print_exc()
            elif 'EndTime' in datas.keys():
                try:
                    st = datetime.datetime.strptime('2017-01-01', "%Y-%m-%d").date()
                    et = datetime.datetime.strptime(datas['EndTime'],"%Y-%m-%d").date()
                    context_obj = context.objects.filter(time__range=(st, et)).order_by("-id")
                except:
                    traceback.print_exc()
            elif 'status' in datas.keys():
                if datas['status'] == 2:
                    try:
                        context_obj = context.objects.all().order_by("-id")
                    except:
                        traceback.print_exc()
                else:
                    try:
                        context_obj = context.objects.filter(status=datas['status']).order_by("-id")
                    except:
                        traceback.print_exc()
            else:
                pass
        elif len(datas.keys()) == 2:
            if 'Auther' in datas.keys():
                if 'StartTime' in datas.keys():
                    st = datetime.datetime.strptime(datas['StartTime'], "%Y-%m-%d").date()
                    no = timezone.localtime(timezone.now()).strftime("%Y-%m-%d")
                    et = datetime.datetime.strptime(no, "%Y-%m-%d").date()
                    try:
                        context_obj = context.objects.filter(auther=datas['Auther'],time__range=(st, et)).order_by("-id")
                    except:
                        traceback.print_exc()
                elif 'EndTime' in datas.keys():
                    try:
                        st = datetime.datetime.strptime('2017-01-01', "%Y-%m-%d").date()
                        et = datetime.datetime.strptime(datas['EndTime'], "%Y-%m-%d").date()
                        context_obj = context.objects.filter(auther=datas['Auther'],time__range=(st, et)).order_by("-id")
                    except:
                        traceback.print_exc()
                elif 'status' in datas.keys():
                    if datas['status'] ==2:
                        try:
                            context_obj = context.objects.filter(auther=datas['Auther']).order_by("-id")
                        except:
                            traceback.print_exc()
                    else:
                        try:
                            context_obj = context.objects.filter(auther=datas['Auther']).filter(status=datas['status']).order_by("-id")
                        except:
                            traceback.print_exc()
                else:
                    pass

            elif 'StartTime' in datas.keys():
                if 'EndTime' in datas.keys():
                    try:
                        st = datetime.datetime.strptime(datas['StartTime'], "%Y-%m-%d").date()
                        et = datetime.datetime.strptime(datas['EndTime'], "%Y-%m-%d").date()
                        context_obj = context.objects.filter(time__range=(st, et)).order_by("-id")
                    except:
                        traceback.print_exc()
                elif 'status' in datas.keys():
                    if datas['status'] == 2:
                        try:
                            st = datetime.datetime.strptime(datas['StartTime'], "%Y-%m-%d").date()
                            no = timezone.localtime(timezone.now()).strftime("%Y-%m-%d")
                            et = datetime.datetime.strptime(no, "%Y-%m-%d").date()
                            context_obj = context.objects.filter(time__range=(st, et)).order_by("-id")
                        except:
                            traceback.print_exc()
                    else:
                        try:
                            st = datetime.datetime.strptime(datas['StartTime'], "%Y-%m-%d").date()
                            no = timezone.localtime(timezone.now()).strftime("%Y-%m-%d")
                            et = datetime.datetime.strptime(no, "%Y-%m-%d").date()
                            context_obj = context.objects.filter(time__range=(st, et)).filter(status=datas['status']).order_by("-id")
                        except:
                            traceback.print_exc()
            elif 'EndTime' in datas.keys():
                if datas['status'] == 2:
                    try:
                        st = datetime.datetime.strptime('2017-01-01', "%Y-%m-%d").date()
                        et = datetime.datetime.strptime(datas['EndTime'], "%Y-%m-%d").date()
                        context_obj = context.objects.filter(time__range=(st, et)).order_by("-id")
                    except:
                        traceback.print_exc()
                else:
                    try:
                        st = datetime.datetime.strptime('2017-01-01', "%Y-%m-%d").date()
                        et = datetime.datetime.strptime(datas['EndTime'], "%Y-%m-%d").date()
                        context_obj = context.objects.filter(time__range=(st, et)).filter(status=datas['status']).order_by("-id")
                    except:
                        traceback.print_exc()
            else:
                pass
        elif len(datas.keys()) == 3:
            if 'Auther' in datas.keys():
                if 'StartTime' in datas.keys():
                    if 'EndTime' in datas.keys():
                        try:
                            st = datetime.datetime.strptime(datas['StartTime'], "%Y-%m-%d").date()
                            et = datetime.datetime.strptime(datas['EndTime'], "%Y-%m-%d").date()
                            context_obj = context.objects.filter(time__range=(st, et),auther=datas['Auther']).order_by("-id")
                        except:
                            traceback.print_exc()
                    elif 'status' in datas.keys():
                        if datas['status'] == 2:
                            try:
                                st = datetime.datetime.strptime(datas['StartTime'], "%Y-%m-%d").date()
                                no = timezone.localtime(timezone.now()).strftime("%Y-%m-%d")
                                et = datetime.datetime.strptime(no, "%Y-%m-%d").date()
                                context_obj = context.objects.filter(time__range=(st, et)).filter(auther=datas['Auther']).order_by("-id")
                            except:
                                traceback.print_exc()
                        else:
                            try:
                                st = datetime.datetime.strptime(datas['StartTime'], "%Y-%m-%d").date()
                                no = timezone.localtime(timezone.now()).strftime("%Y-%m-%d")
                                et = datetime.datetime.strptime(no, "%Y-%m-%d").date()
                                context_obj = context.objects.filter(time__range=(st, et)).filter(status=datas['status'],auther=datas['Auther']).order_by("-id")
                            except:
                                traceback.print_exc()
                    else:
                        pass
                elif 'EndTime' in datas.keys():
                    if 'status' in datas.keys():
                        if datas['status'] == 2:
                            try:
                                st = datetime.datetime.strptime('2017-01-01', "%Y-%m-%d").date()
                                et = datetime.datetime.strptime(datas['EndTime'], "%Y-%m-%d").date()
                                context_obj = context.objects.filter(time__range=(st, et),auther=datas['auther']).order_by("-id")
                            except:
                                traceback.print_exc()
                        else:
                            try:
                                st = datetime.datetime.strptime('2017-01-01', "%Y-%m-%d").date()
                                et = datetime.datetime.strptime(datas['EndTime'], "%Y-%m-%d").date()
                                context_obj = context.objects.filter(time__range=(st, et)).filter(status=datas['status'],auther=datas['auther']).order_by("-id")
                            except:
                                traceback.print_exc()
            elif 'StartTime' in datas.keys():
                if 'EndTime' in datas.keys():
                    if 'status' in datas.keys():
                        if datas['status'] ==2:
                            try:
                                st = datetime.datetime.strptime(datas['StartTime'], "%Y-%m-%d").date()
                                et = datetime.datetime.strptime(datas['EndTime'], "%Y-%m-%d").date()
                                context_obj = context.objects.filter(time__range=(st, et)).order_by("-id")
                            except:
                                traceback.print_exc()
                        else:
                            try:
                                st = datetime.datetime.strptime(datas['StartTime'], "%Y-%m-%d").date()
                                et = datetime.datetime.strptime(datas['EndTime'], "%Y-%m-%d").date()
                                context_obj = context.objects.filter(time__range=(st, et),status=datas['status']).order_by("-id")
                            except:
                                traceback.print_exc()
                    else:
                        pass
                else:
                    pass
            else:
                pass
        elif len(datas.keys()) == 4:
            if datas['status'] == 2:
                try:
                    st = datetime.datetime.strptime(datas['StartTime'], "%Y-%m-%d").date()
                    et = datetime.datetime.strptime(datas['EndTime'], "%Y-%m-%d").date()
                    context_obj = context.objects.filter(time__range=(st, et),auther=datas['Auther']).order_by("-id")
                except:
                    traceback.print_exc()
            else:
                try:
                    st = datetime.datetime.strptime(datas['StartTime'], "%Y-%m-%d").date()
                    et = datetime.datetime.strptime(datas['EndTime'], "%Y-%m-%d").date()
                    context_obj = context.objects.filter(time__range=(st, et), status=datas['status'],auther=datas['Auther']).order_by("-id")
                except:
                    traceback.print_exc()
        else:
            pass

        for re in context_obj:
            if re.status:
                str += "<tr>"
            else:
                str += "<tr style=\"color:red;\">"
            str += "<th><a href='/deltails/%d'>%d</a> </th>" % (re.id, re.id)
            str += "<th>%s</th>" % (re.title)
            str += "<th>%s</th>" % (re.auther)
            str += "<th>%s</th>" % (re.time)
            str += "<th>%s</th>" % (re.status)
            str += "</tr>"
        return HttpResponse(str)
    else:
        return render_to_response("web/search.html", {'user': request.user})


@csrf_exempt
@login_required
def Changpwd(request):
    if request.method == 'POST':
        oldpassword = request.POST.get('orgp')
        username = request.user
        user = auth.authenticate(username=username, password=oldpassword)
        if user is not None and user.is_active:
            newpassword = request.POST.get('newp')
            user.set_password(newpassword)
            user.save()
            return HttpResponse(json.dumps({'error_code':0}))
        else:
            return HttpResponse(json.dumps({'error_code':1}))

