import json


def load_user():
    with open ('users.txt', 'r', encoding='utf-8') as f:
        text = f.read()
        if not text:
            return {}
        return json.loads(text)
    
def save_user(login, user_info):   
    users = load_user()

    if login in users:
        return False
    
    users[login] = user_info

    with open ('users.txt', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)
    return True

def get_user_by_login(login):
    user = load_user() 
    return user.get(login)         
    
