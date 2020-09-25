from django.conf.urls import url

from bot.views import *

urlpatterns = [
    url(r'create', create_bot),
    url(r'info', bot_info),
    url(r'uploadCode', upload_code),
    url(r'start', start_bot),
    url(r'stop', stop_bot),
    url(r'delete', delete_bot),
    url(r'getAll', get_all_bots),
    url(r'fork', fork_bot),
    url(r'uploadCode',upload_code),
    url(r'download',downloadCode)
]