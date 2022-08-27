

import requests
import rsa
import pickle
import base64
from threading import Thread
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

url = "http://127.0.0.1:5000/"

def generate_rsa_key():
    publicKey, privateKey = rsa.newkeys(512)
    return publicKey, privateKey

def encrypt_message(publicKey, message):
    encMessage = rsa.encrypt(message.encode(),publicKey)
    return encMessage
def decrypt_message(privateKey, message):
    decMessage = rsa.decrypt(message, privateKey).decode()
    return decMessage

def generate_keys(username_own):
    public,private = generate_rsa_key()
    f = open(".keys/self_keys.dat","wb")
    d = {
        "public_own" : public,
        "private_own" : private,
        "chat_id" : 0
        }
    pickle.dump(d,f)
    f.close()
    data = {
        "username": username_own,
        "public_n": public.n,
        "public_e":public.e}
    response = requests.post(url+"/send_public_key", json= data)
          
def check_exist():
    try:
        f = open(".keys/self_keys.dat", "rb")
        f.close()
        return True
    except:
        return False
    

def send_message(to_username,from_username):
    message = input("Enter Your Message (0 - Change User) : ")
    if message == "0":
        __init__()
    f = open(".keys/user_keys.dat", "rb+")
    while True:
            data = pickle.load(f)
            if data["username_target"] == to_username:
                public_key =  data["public_key"]
                break
    a = encrypt_message(public_key, message)
    enc_message = base64.b64encode(a)
    data = {
            "username":to_username,
            "message":enc_message.decode("utf-8"),
            "from_username":from_username
            }
    response = requests.post(url,json = data)

def __init__():
    username_target = input("Enter Username Of Your Friend : ")
    if check_exist():
        if have_key(username_target):
            while True:
                send_message(username_target, username_own)
        else:
            ask_key(username_target)
            while True:
                send_message(username_target, username_own)
    else:
        generate_keys(username_own)
        __init__()

def have_key(username_target):
    try:
        f = open(".keys/user_keys.dat","rb")
        while True:
            data=pickle.load(f)
            if data["username"] == username_target:
                return True
            f.close()
    except:
        return False
               

def ask_key(username_target):
    response = requests.get(url+"/ask_key",params={"username":username_target})
    data = response.json()
    public_n = data["public_n"]
    public_e = data["public_e"]
    f = open(".keys/user_keys.dat","ab")
    d = {
        "username_target" : username_target,
        "public_key":rsa.PublicKey(public_n, public_e)
        }
    pickle.dump(d,f)
    f.close()
                            
    
def receive_message(username_own):
    f = open(".keys/self_keys.dat", "rb+")
    data = pickle.load(f)
    public_own = data["public_own"]
    private_own =  data["private_own"]
    last_chat_id = data["chat_id"]
    f.close()
    response = requests.get(url+"/check_message",params={"username":username_own,"last_chat_id":
                                                    last_chat_id})
    try:
        data = response.json()
        messages = data["message"]
        users = data["username"]
        chat_id = data["chat_id"]
        a = zip(messages,users,chat_id)
        for message,user,chat in a:
            message = base64.b64decode(message.encode("utf-8"))
            message = decrypt_message(private_own,message)
            print("\n"+bcolors.FAIL + user + " : " + message + bcolors.ENDC)
            last_chat_id = chat
    except:
        pass
        
    f = open(".keys/self_keys.dat","wb")
    d = {
        "public_own" : public_own,
        "private_own" : private_own,
        "chat_id" : last_chat_id
        }
    pickle.dump(d,f)
    f.close()
    
        
def loop():
    while True:
        receive_message(username_own)
        time.sleep(1)
def create_bg_thread():
    t1 = Thread(target = loop)
    t2 = Thread(target = __init__)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()

def begin_texting():
    a = input("Are you a new user (y/n) : ")
    global username_own
    username_own = input("Enter You Username : ")
    if (a == "y"):
        generate_keys(username_own)
        create_bg_thread()
        while True:
            pass
    else:
       create_bg_thread()
       while True:
           pass
       
begin_texting()        

