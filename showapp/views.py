from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from showapp.models import Msg
from django.core.paginator import Paginator
from public_fun import Log
@Log
def menu(request):  # 列表
    # request.session['c_number'] = 1
    city = request.GET.get('city')
    job_type = request.GET.get('type')
    # print(city,job_type,'number')
    if city == 'bj':
        city = '北京'
    elif city == 'sh':
        city = '上海'
    elif city == 'gz':
        city = '广州'
    elif city == 'sz':
        city = '深圳'
    if job_type == 'web':
        job_type = 'web'
    elif job_type == 'spider':
        job_type = '爬虫'
    elif job_type == 'bigdata':
        job_type = '大数据'
    elif job_type == 'AI':
        job_type = '人工智能'
    msgs = Msg.objects.filter(ideal_city__icontains=city).filter(ideal_position__icontains=job_type).order_by('name')
    paginator = Paginator(msgs,per_page=8)
    page = paginator.page(number=1)
    resp = render(request,'groupapp/menu.html',{'page':page,'city':city,'job_type':job_type,'number':'1'})
    resp.set_cookie('hh','1')  # 存cookies
    return resp
@Log
def main(request):  # 主页
    return render(request,'groupapp/main.html')


def introduce(request):  # 介绍
    return render(request,'groupapp/introduce.html')


def changePage(request):  # 换页
    meta = request.META
    print(meta,'metaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    # c_number = request.session.get('c_number')  # 当前在多少页
    c_number= int(request.COOKIES['hh'])  # 当前在多少页
    city = request.GET.get('city')  # 当前城市
    job_type = request.GET.get('job_type')  # 当前工作类型
    number = request.GET.get('v')   #  对页数的操作
    msgs = Msg.objects.filter(ideal_city__icontains=city).filter(ideal_position__icontains=job_type).order_by('name')
    paginator = Paginator(msgs,per_page=8)
    count = paginator.num_pages  # 当前城市,职位共有多少页
    if number == 'f12543451254':  # 加一操作
        number = c_number+1
        if number < count:  # 页码小于上限还可以加
            msgs = msgs[int(number) * 8 - 8:int(number) * 8 - 1].values()  # 返回的数据
            resp = JsonResponse({'msgs': list(msgs),'nextstate':'nextok','previousstate':'previousok','number':number})
            resp.set_cookie('hh',str(number))  # 存回cookie
            return resp
        elif number == count: # 页码到上限 把上一页去掉
            msgs = msgs[int(number) * 8 - 8:int(number) * 8 - 1].values()  # 返回的数据
            resp = JsonResponse({'msgs': list(msgs), 'previousstate': 'previousok','nextstate':'nextno','number':number})
            resp.set_cookie('hh', str(number))  # 存回cookie
            return resp
    elif number == 'f12543541254':  # 减一操作
        number = c_number-1
        print(number,'72行')
        if number > 1:  # 大于下限,
            print(msgs,'74 行')
            msgs = msgs[int(number) * 8 - 8:int(number) * 8 - 1].values()  # 返回的数据
            resp = JsonResponse({'msgs': list(msgs), 'nextstate':'nextok','previousstate':'previousok','number':number})
            resp.set_cookie('hh', str(number))  # 存回cookie
            return resp
        elif number == 1: # 等于下限,把下一页去掉
            msgs = msgs[int(number) * 8 - 8:int(number) * 8 - 1].values()  # 返回的数据
            resp = JsonResponse({'msgs': list(msgs), 'nextstate':'nextok','previousstate':'previousno','number':number})
            resp.set_cookie('hh', str(number))  # 存回cookie
            return resp
    elif number == 'f':  # 展示第一页的数据
        number = 1
        msgs = msgs[int(number) * 8 - 8:int(number) * 8 - 1].values()  # 返回的数据
        resp = JsonResponse({'msgs': list(msgs), 'nextstate':'nextok','previousstate':'previousno','number':number})
        resp.set_cookie('hh', str(number))  # 存回cookie
        return resp
    elif number == 'l':
        number = count  # 等于最后一页
        msgs = msgs[int(number) * 8 - 8:int(number) * 8 - 1].values()  # 返回的数据
        resp = JsonResponse({'msgs': list(msgs), 'nextstate':'nextno','previousstate':'previousok','number':number})
        resp.set_cookie('hh', str(number))  # 存回cookie
        return resp
    else:
        return HttpResponse('')




def jumpPage(request):  # 跳页 试着把参数加密
    number = request.GET.get('number') # number是数字,number是特殊字符
    c_number = int(request.COOKIES.get('hh'))
    city = request.GET.get('city')  # 当前城市
    job_type = request.GET.get('job_type')  # 当前工作类型
    msgs = Msg.objects.filter(ideal_city__icontains=city).filter(ideal_position__icontains=job_type).order_by('name')
    try:
        number = int(number)
        paginator = Paginator(msgs,per_page=8)
        if 1 < number < paginator.num_pages:  # 大于1 小于最大页码
            msgs = msgs[int(number) * 8 - 8:int(number) * 8 - 1].values()  # 返回的数据
            resp = JsonResponse({'msgs': list(msgs), 'nextstate': 'nextok', 'previousstate': 'previousok', 'number': number})
            resp.set_cookie('hh', str(number))  # 存回cookie
            return resp
        elif number == 1:
            msgs = msgs[int(number) * 8 - 8:int(number) * 8 - 1].values()  # 返回的数据
            resp = JsonResponse(
                {'msgs': list(msgs), 'nextstate': 'nextok', 'previousstate': 'previousno', 'number': number})
            resp.set_cookie('hh', str(number))  # 存回cookie
            return resp
        elif number == paginator.num_pages:
            msgs = msgs[int(number) * 8 - 8:int(number) * 8 - 1].values()  # 返回的数据
            resp = JsonResponse({'msgs': list(msgs), 'nextstate': 'nextno', 'previousstate': 'previousok', 'number': number})
            resp.set_cookie('hh', str(number))  # 存回cookie
            return resp
        else:
            number = c_number
            msgs = msgs[int(number) * 8 - 8:int(number) * 8 - 1].values()  # 返回的数据
            resp = JsonResponse({'msgs': list(msgs), 'nextstate': 'next', 'previousstate': 'previous', 'number': number})
            resp.set_cookie('hh', str(number))  # 存回cookie
            return resp
    except:
        number = c_number
        msgs = msgs[int(number) * 8 - 8:int(number) * 8 - 1].values()  # 返回的数据
        resp = JsonResponse({'msgs': list(msgs), 'nextstate': 'next', 'previousstate': 'previous', 'number': number})
        resp.set_cookie('hh', str(number))  # 存回cookie
        return resp


def searchMsg(request):   # 搜索
    index = request.POST.get('index')
    msg = request.POST.get('msg')
    print(index, msg, 'sssssssssssssssssss')
    if index == 0:
        return HttpResponse('no')
    elif index == 1:  # 按城市查找,if 拼音 else 汉字
        for i in msg.lower():
            pass
        # elif msg.lower() in 'shanghai':
        # pass

    elif index == 2:  # 按职位查找
        pass

    return HttpResponse('qwe')