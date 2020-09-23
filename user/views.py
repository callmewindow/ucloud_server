import datetime
import traceback

# from dateutil.tz import gettz
from django.forms.models import model_to_dict
from django.http.response import HttpResponse

from bot.models import Bot as BotCon
from user.models import *
from util.utils import *


def json_raw(dict):
    return str(dict).replace('\'', '\"').replace('None', 'null')


def model_to_dict_fixed(model):
    d = model_to_dict(model)
    for key in d.keys():
        if d[key].__class__ == datetime.datetime:
            d[key] = d[key].strftime('%Y-%m-%d %H:%M:%S')
    return d


def api_format(request):
    try:
        dict = request.POST
        msg = {}


    except:
        traceback.print_exc()
        msg['result'] = 'Unexpected Error'
        return HttpResponse(json_raw(msg))


# Create your views here.
def register(request):
    try:
        dict = request.POST
        msg = {}

        tag = User()
        tag.username = dict.get('userName', None)
        tag.password = dict.get('password', None)
        if tag.username == None or tag.password == None:
            # msg['success'] = 'false'
            # msg['message'] = '用户名或密码不能为空。'
            return result_fail('用户名或密码不能为空。')
        elif tag.username == '' or tag.password == '':
            # msg['success'] = 'false'
            # msg['message'] = '用户名或密码不能为空。'
            return result_fail('用户名或密码不能为空。')
        elif User.objects.filter(username=tag.username):
            # msg['success'] = 'false'
            # msg['message'] = '该用户名已被注册。'
            return result_fail('该用户名已注册。')

        # msg['success'] = 'true'
        # msg['message'] = '注册成功。'
        tag.save()
        return result_ok(None,'注册成功。')
    except:
        traceback.print_exc()
        # msg['success'] = 'false'
        # msg['message'] = 'Unexpected Error'
        return result_fail()


def login(request):
    try:
        dict = request.POST
        msg = {}

        username = dict.get('userName', None)
        password = dict.get('password', None)
        if username == None or password == None:
            # msg['success'] = 'false'
            # msg['message'] = '用户名或密码不能为空。'
            return result_fail('用户名或密码不能为空。')

        qset = User.objects.filter(username=username, password=password)
        if qset:
            # msg['success'] = 'true'
            # msg['result'] = '登录成功。'
            # msg['data'] = model_to_dict(qset.first())
            return result_ok(model_to_dict_fixed(qset.first()),'登录成功。')
        else:
            # msg['success'] = 'false'
            # msg['message'] = '用户不存在或密码错误。'
            return result_fail('用户不存在或密码错误。')

    except:
        traceback.print_exc()
        # msg['success'] = 'false'
        # msg['message'] = 'Unexpected Error'
        return result_fail('Unexpected Error')


def info(request):
    try:
        dict = request.GET
        msg = {}

        id = dict.get('userId', None)
        if id == None:
            # msg['success'] = 'false'
            # msg['message'] = '用户ID不能为空。'
            return result_fail('用户ID不能为空。')

        qsets = BotCon.objects.filter(userId_id=id)
        qset_list = []
        if qsets:
            # msg['success'] = 'true'
            # msg['message'] = '成功获取。'
            for qset in qsets:
                bot_data = {
                    'botId': qset.id,
                    'botQQ': qset.botQQ,
                    'botStatus': qset.botStatus,
                    'botName': qset.botName,
                    'botType': qset.botType,
                    'botIntro': qset.botIntro
                }
                qset_list.append(bot_data)
            # msg['data'] = qset_list
            return result_ok(qset_list,'获取成功。')
        else:
            # msg['success'] = 'true'
            # msg['message'] = '成功获取。'
            # msg['data'] = model_to_dict(qset)
            # return HttpResponse(json_raw(msg))
            # msg['success'] = 'false'
            # msg['message'] = '还未创建任何机器人。'
            return result_fail('还未创建任何机器人')
    except:
        traceback.print_exc()
        # msg['success'] = 'false'
        # msg['message'] = 'Unexpected Error'
        return result_fail('Unexpected Error')
