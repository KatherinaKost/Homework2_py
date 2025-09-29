import re

def chek_name(name):
    if re.fullmatch(r'^[А-Яа-яЁё]+$', name):
        return True
    return False

def chek_log(log):
    if re.fullmatch('^[A-Za-z_]{6,20}$', log):
        return True
    return False

def chek_pass(pas):
    if re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,15}$', pas):
        return True
    return False

def chek_email(email):
    if re.fullmatch( r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return True
    return False

def chek_age(age):
    if re.fullmatch(r'\d+', age) and 12 <= int(age) <=100:
        return True
    return False