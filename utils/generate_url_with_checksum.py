import hashlib
import urllib.parse


def generate_url_with_checksum(action, query_string):
    shared_secret = 'J5ZkhvCnDYmfIE9gzuBhwdRmI0nfXUrUTRdrjmk0'
    url = action + query_string + shared_secret
    checksum = hashlib.sha1(url.encode()).hexdigest()
    return urllib.parse.quote_plus(query_string + '&checksum=%s' % checksum)
