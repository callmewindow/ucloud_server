import traceback
import os
import subprocess
from bot.models import Bot
from user.models import User
from util.utils import *

# mkpath = "E:\\2020\\pathtest\\"
mkpath = "/home/ucloud/"

def create_bot(request):
    args = request.POST
    bot = Bot()
    bot.botName = args.get('botName')
    bot.botType = args.get('botType')
    bot.botQQ = args.get('botQQ')
    bot.botPwd = args.get('botPassword')
    bot.userId = User.objects.filter(id=args.get('userId')).first()
    if bot.userId is None:
        return result_fail('请输入userId！')
    if Bot.objects.filter(botName=bot.botName):
        return result_fail('该名称已被占用')
    bot.botIntro = args.get('botIntro')
    bot.save()
    path = mkpath + str(bot.id)
    createfile(path)
    os.chdir(path)
    password = open('.password','w',encoding='utf8')
    password.write(bot.botQQ+ ' ' + bot.botPwd)
    password.close()
    code = open('bot.py','w',encoding='utf8')
    code.close()
    createPy('')
    # TODO: python docker
    data = {
        'botId': bot.id
    }
    return result_ok(data)


def bot_info(request):
    bot_id = request.GET.get('botId')
    if bot_id is None:
        return result_fail('请输入botId！')
    bot = Bot.objects.filter(id=bot_id)
    if bot.first() is None:
        return result_fail('机器人不存在！')
    bot = bot.first()
    user = User.objects.filter(id=bot.userId_id)
    if user.first() is None:
        return result_fail()
    user = user.first()
    # TODO: python docker
    data = {
        'botName': bot.botName,
        'botStatus': bot.botStatus,
        'botIntro': bot.botIntro,
        'botType': bot.botType,
        'botQQ': bot.botQQ,
        'botOwner': {
            'userId': user.id,
            'userName': user.username
        },
        # 'botLog': String
        # 'botCode': String
    }
    return result_ok(data)


def upload_code(request):
    try:
        dict = request.POST
        botId = dict.get('botId')
        botCode = dict.get('code')

        qset = Bot.objects.filter(id = botId)
        if qset:
            Bot.objects.filter(id = botId).update(botCode = botCode)
        else:
            return result_fail('不存在该机器人。')

        path = mkpath + str(botId)
        os.chdir(path)
        code = open('bot.py','w',encoding='utf8')
        code.write(botCode)
        code.close()

        res = subprocess.getoutput('pylint bot.py')
        data = {
            'checkResult': res
        }
        return result_ok(data,'代码更新成功。')


    except:
        traceback.print_exc()
        return result_fail('Unexpected Error')




def start_bot(request):
    bot_id = request.POST.get('botId')
    if bot_id is None:
        return result_fail('请输入botId！')
    bot = Bot.objects.filter(id=bot_id)
    if bot.first() is None:
        return result_fail('机器人不存在！')
    bot = bot.first()
    # TODO: python docker
    return result_ok()


def stop_bot(request):
    bot_id = request.POST.get('botId')
    if bot_id is None:
        return result_fail('请输入botId！')
    bot = Bot.objects.filter(id=bot_id)
    if bot.first() is None:
        return result_fail('机器人不存在！')
    bot = bot.first()
    # TODO: python docker
    return result_ok()


def delete_bot(request):
    bot_id = request.POST.get('botId')
    if bot_id is None:
        return result_fail('请输入botId！')
    bot = Bot.objects.filter(id=bot_id)
    if bot.first() is None:
        return result_fail('机器人不存在！')
    bot = bot.first()
    bot.delete()
    # TODO: python docker
    return result_ok()


def get_all_bots(request):
    bots = Bot.objects.all()
    bot_list = []
    for bot in bots:
        user = User.objects.filter(id=bot.userId_id)
        if user.first() is None:
            return result_fail()
        user = user.first()
        bot_data = {
            'botId': bot.id,
            'botStatus': bot.botStatus,
            'botName': bot.botName,
            'botType': bot.botType,
            'botOwner': {
                'userId': user.id,
                'userName': user.username
            }
        }
        bot_list.append(bot_data)
    return result_ok(bot_list)


def fork_bot(request):
    pass
