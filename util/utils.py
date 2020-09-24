from django.http import JsonResponse


def result_ok(data=None, message='操作成功'):
    result = {
        'success': True,
        'message': message
    }
    if data:
        result['data'] = data
    return JsonResponse(result)


def result_fail(message='操作失败'):
    result = {
        'success': False,
        'message': message
    }
    return JsonResponse(result)


def check_get_method(request):
    if request.method != 'GET':
        return False, result_fail("需要GET请求！")
    return True, None


def check_post_method(request):
    if request.method != 'POST':
        return False, result_fail("需要POST请求！")
    return True, None

def createfile(path):
    import os

    path = path.strip()
    path = path.rstrip("\\")

    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)

        print(path + '创建成功。')
        return True
    else:
        print(path + '目录已存在')
        return False

def createPy(codeStr):
    code = open('bot.py','w',encoding='utf8')
    code.write(codeStr)
    code.close()