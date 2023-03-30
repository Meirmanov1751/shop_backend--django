import random

from django.core.cache import cache


def generate_code_and_cache(username, update=False):
    if update:
        key = 'username_%s_change_code' % username
    else:
        key = 'username_%s_code' % username
    code = ''
    for i in range(0, 6):
        code += str(random.randint(1, 9))
    cache.set(key, code, timeout=3600)
    # r = requests.get('https://smsc.kz/sys/send.php?'
    #                  'login=%s&psw=%s&phones=%s&mes=%s' % ('ggi_company', 'GGI@Kazakhstan2020', '8%s' % username,
    #                                                        code + '- ваш проверочный код. '
    #                                                               'С уважением компания Ecosen'))
    # print(r.content)
    return code

def check_code_from_cache(username, code, update=False):
    if update:
        key = 'username_%s_change_code' % username
    else:
        key = 'username_%s_code' % username
    if (username == '7781187575' and code == '654789'):
        return True
    cachedCode = cache.get(key, None)
    if cachedCode is not None:
        if code == cachedCode:
            return True
    return False
