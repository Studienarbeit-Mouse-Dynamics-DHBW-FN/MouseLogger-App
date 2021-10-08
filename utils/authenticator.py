import re

class Authenticator:
    _authenicated = False

    def valid_email(self, mail: str) -> bool:
        """return wheter the give mail matches a mail pattern"""
        return re.match(r"[^@]+@[^@]+\.[^@]+", mail)

    def authenticate(self, mail: str) -> None:
        # url = 'http://localhost:3000/sendmail'
        # try:
        #     res = requests.post(url, json={'email': username})
        #     print(res.text)
        # except:
        #     print('err: no username send')
        pass
    
    def is_authenicated(self) -> bool:
        return self._authenicated