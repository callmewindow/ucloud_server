import traceback
import os
import subprocess
import string
from django.http import FileResponse
from bot.models import Bot
from user.models import User
from util.utils import *
from bot.uDocker import *


# mkpath = "E:\\2020\\pathtest\\"
mkpath = "/home/ucloud/"
init()

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
    password = open('.passwd','w',encoding='utf8')
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
    if bot.botStatus == False:
        res = 'null'
    else:
        os.system('docker cp {}:/home/mirai/main.out /home/main.out'.format(bot_id))
        #file = open('/home/main.out','r')
        #res = file.read()
        res = get_last_n_lines('/home/main.out',100)
    # TODO: python docker
    data = {
        'botName': bot.botName,
        'botStatus': bot.botStatus,
        'botIntro': bot.botIntro,
        'botType': bot.botType,
        'botQQ': bot.botQQ,
        'botCode': bot.botCode,
        'botLog': res,
        'botOwner': {
            'userId': user.id,
            'userName': user.username
        }
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
    try:
        bot_id = request.POST.get('botId')
        if bot_id is None:
            return result_fail('请输入botId！')
        bot = Bot.objects.filter(id=bot_id)
        if bot.first() is None:
            return result_fail('机器人不存在！')
        bot = bot.first()
        if bot.botStatus == 1:
            return result_fail('机器人已启动')

        createContainer(bot_id)
        Bot.objects.filter(id = bot.id).update(botStatus=1)

        return result_ok()
    except:
        traceback.print_exc()
        return result_fail('Unexpected Error')


def stop_bot(request):
    bot_id = request.POST.get('botId')
    if bot_id is None:
        return result_fail('请输入botId！')
    bot = Bot.objects.filter(id=bot_id)
    if bot.first() is None:
        return result_fail('机器人不存在！')
    bot = bot.first()

    if bot.botStatus == 0:
        return result_fail('机器人未启动')

    # TODO: python docker

    removeContainer(bot_id)
    Bot.objects.filter(id = bot.id).update(botStatus=0)

    return result_ok('机器人已停止。')


def delete_bot(request):
    bot_id = request.POST.get('botId')
    if bot_id is None:
        return result_fail('请输入botId！')
    bot = Bot.objects.filter(id=bot_id)
    if bot.first() is None:
        return result_fail('机器人不存在！')
    bot = bot.first()
    if bot.botStatus == 1:
        removeContainer(bot_id)
    Bot.objects.filter(id = bot_id).delete()
    # TODO: python docker
    return result_ok('')


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
    dict = request.POST

    userId = dict.get('userId')
    botName = dict.get('botName')
    botId = dict.get('botId')
    botQQ = dict.get('botQQ')
    botPwd = dict.get('botPassword')

    if botName == None or botName == '':
        return result_fail('机器人名称为空。')
    if userId == None or userId == '':
        return result_fail('用户ID为空。')
    if botId == None or botId == '':
        return result_fail('机器人ID为空')
    if Bot.objects.filter(botName=botName):
        return result_fail('该名称已被占用')
    qset = Bot.objects.filter(id = botId).first()
    if qset:
        bot = Bot()
        bot.botName = botName
        bot.botStatus = 0
        bot.botIntro = qset.botIntro
        bot.botType = qset.botType
        bot.botQQ = botQQ
        bot.botPwd = botPwd
        bot.botPermission = qset.botPermission
        bot.botCode = qset.botCode
        user = User.objects.filter(id = userId).first()
        if not user:
            return result_fail('不存在该用户')
        bot.userId = user
        bot.save()
        path = mkpath + str(bot.id)
        createfile(path)
        os.chdir(path)
        password = open('.passwd', 'w', encoding='utf8')
        password.write(bot.botQQ + ' ' + bot.botPwd)
        password.close()
        code = open('bot.py', 'w', encoding='utf8')
        code.write(bot.botCode)
        code.close()
        data = {
            'botId': bot.id
        }
        return result_ok(data,'复制成功。')
    else:
        return result_fail('不存在该机器人。')

def downloadCode(request):
    dict = request.GET
    botId = dict.get('botId')
    path = mkpath + str(botId)+"/bot.py"
    print("1"+path)
    file = open(path,'rb')
    print(path)
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="bot.py"'
    return response


def get_last_n_lines(logfile, n):
    n = int(n)
    blk_size_max = 4096
    n_lines = []
    with open(logfile, 'r',encoding='utf8') as fp:
        fp.seek(0, os.SEEK_END)
        cur_pos = fp.tell()
        while cur_pos > 0 and len(n_lines) < n:
            blk_size = min(blk_size_max, cur_pos)
            fp.seek(cur_pos - blk_size, os.SEEK_SET)
            blk_data = fp.read(blk_size)
            assert len(blk_data) == blk_size
            #blk_data = str(blk_data,encoding='utf8')
            lines = blk_data.split('\n')

            # adjust cur_pos
            if len(lines) > 1 and len(lines[0]) > 0:
                n_lines[0:0] = lines[1:]
                cur_pos -= (blk_size - len(lines[0]))
            else:
                n_lines[0:0] = lines
                cur_pos -= blk_size

            fp.seek(cur_pos, os.SEEK_SET)

    if len(n_lines) > 0 and len(n_lines[-1]) == 0:
        del n_lines[-1]
    return n_lines[-n:]