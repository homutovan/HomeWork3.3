import requests
from pprint import pprint
import webbrowser

try:
    from secret import TOKEN
except ModuleNotFoundError:
    print('Файл с секретным ключом отсутствует, требуется ключ')

#TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'

class User:
           
    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token
        
    def get_params(self):         
        return dict(
            access_token = self.token,
            user_id = self.user_id,
            user_ids = self.user_id,
            fields = 'domain',
            v='5.103'
        )
        
    def get_friends(self):
        params = self.get_params()
        response = requests.get('https://api.vk.com/method/friends.get', params)
        return response.json()['response']['items']
    
    def friends_set(self):
        return set(friend['id'] for friend in User.get_friends(self))
    
    def get_info(self):
        params = self.get_params()
        response = requests.get('https://api.vk.com/method/users.get', params)
        return response.json()['response'][0]
        
    def __and__(self, other):
        return list(User(friend, TOKEN) for friend in (User.friends_set(self) & User.friends_set(other)))
    
    def __str__(self):
        return f"https://vk.com/{User.get_info(self)['domain']}"
    
    def __repr__(self):
        return f"https://vk.com/{User.get_info(self)['domain']}"

USER_ID = '2453810'
USER_ID2 = '160117406'

user1 = User(USER_ID, TOKEN)
user2 = User(USER_ID2, TOKEN)

###############################################
#########Ищем и выводим общих друзей###########
###############################################
print(user1 & user2)

for friend in user1 & user2:
    print(friend, friend.get_info()['first_name'], friend.get_info()['last_name'])