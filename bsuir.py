import requests
import json


class ApiError(Exception):
    pass


class AuthError(Exception):
    pass


class AuthRequired(Exception):
    def __init__(self, method):
        self._method = method


    def try_method(self):
        return self._method()


class IISBsuirApi():
    def __init__(self, username, password):
        self._session = requests.Session()
        self._username = username
        self._password = password
        
        
    def auth(self, ):
        payload = json.dumps({'username': self._username, 'password': self._password})
        headers = {'Content-Type': 'application/json'}
        r = self._session.post('https://journal.bsuir.by/api/v1/auth/login', data=payload, headers=headers)
        if r.json()['loggedIn'] == False:
            raise AuthError
        if r.status_code != 200:
            raise requests.exceptions.HTTPError
            
        
    def getGradebook(self):
        r = self._session.get('https://journal.bsuir.by/api/v1/portal/schedule/gradebook')
        if r.status_code == 500:
            raise AuthError
        if r.status_code == 401:
            self.auth()
            return self.getGradebook()    
        return r.json()