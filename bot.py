import json
from urllib.parse import parse_qs, unquote, quote
import requests
import time
from datetime import datetime

headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://pixelfarm.app',
        'referer': 'https://pixelfarm.app/',
    }

def load_credentials():
    # Membaca token dari file dan mengembalikan daftar token
    try:
        with open('query_id.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        # print("Token berhasil dimuat.")
        return queries
    except FileNotFoundError:
        print("File query_id.txt tidak ditemukan.")
        return 
    except Exception as e:
        print("Terjadi kesalahan saat memuat query:", str(e))
        return 

def load_token():
    try:
        with open('token.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print("File token.txt tidak ditemukan.")
        return 
    except Exception as e:
        print("Terjadi kesalahan saat memuat token:", str(e))
        return 

def getuseragent(index):
    try:
        with open('useragent.txt', 'r') as f:
            useragent = [line.strip() for line in f.readlines()]
        if index < len(useragent):
            return useragent[index]
        else:
            return "Index out of range"
    except FileNotFoundError:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
    except Exception as e:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'


def auth(query):
    url =f'https://api.pixelfarm.app/user/login?auth_data={query}'
    try:
        response = requests.get(url)
        if response.status_code >= 500:
            print_(f"Status Code : {response.status_code}")
            return None
        elif response.status_code >= 400:
            print_(f"Status Code : {response.status_code} | Msg {response.text}")
            return None
        else:
            return response.json()
    except requests.exceptions.ConnectionError as e:
        print_(f"Connection Error: {e}")
    except Exception as e:
        print_(f"Error: {e}")

def get_user_data(auth_token):
    url = "https://api.pixelfarm.app/user"
    headers['Authorization'] = f'Bearer {auth_token}'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code >= 500:
            print_(f"Status Code : {response.status_code}")
            return None
        elif response.status_code >= 400:
            print_(f"Status Code : {response.status_code} | Msg {response.text}")
            return None
        else:
            return response.json()
    except requests.exceptions.ConnectionError as e:
        print_(f"Connection Error: {e}")
    except Exception as e:
        print_(f"Error: {e}")

def claim(auth_token):
    url = "https://api.pixelfarm.app/user/claim"
    headers['Authorization'] = f'Bearer {auth_token}'
    try:
        response = requests.post(url, headers=headers)
        if response.status_code >= 500:
            print_(f"Status Code : {response.status_code}")
            return None
        elif response.status_code >= 400:
            print_(f"Status Code : {response.status_code} | Msg {response.text}")
            return None
        else:
            return response.json()
    except requests.exceptions.ConnectionError as e:
        print_(f"Connection Error: {e}")
    except Exception as e:
        print_(f"Error: {e}")

def sell(auth_token, payload):
    url = "https://api.pixelfarm.app/user/sell-fruit"
    headers['Authorization'] = f'Bearer {auth_token}'
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code >= 500:
            print_(f"Status Code : {response.status_code}")
            return None
        elif response.status_code >= 400:
            print_(f"Status Code : {response.status_code} | Msg {response.text}")
            return None
        else:
            return response.json()
    except requests.exceptions.ConnectionError as e:
        print_(f"Connection Error: {e}")
    except Exception as e:
        print_(f"Error: {e}")

def parse_query(query: str):
    parsed_query = parse_qs(query)
    parsed_query = {k: v[0] for k, v in parsed_query.items()}
    user_data = json.loads(unquote(parsed_query['user']))
    parsed_query['user'] = user_data
    return parsed_query


def printdelay(delay):
    now = datetime.now().isoformat(" ").split(".")[0]
    hours, remainder = divmod(delay, 3600)
    minutes, sec = divmod(remainder, 60)
    print(f"[{now}] | Waiting Time: {hours} hours, {minutes} minutes, and {round(sec)} seconds")

def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] {word}")

def get_token(username):
        tokens = json.loads(open("tokens.json").read())
        if str(username) not in tokens.keys():
            return None
        return tokens[str(username)]

def set_token(username, token):
        tokens = json.loads(open("tokens.json").read())
        tokens[str(username)] = token
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))

def get_quest(id):
    url =f'https://api.pixelfarm.app/user/{id}/quests'
    try:
        response = requests.get(url)
        if response.status_code >= 500:
            print_(f"Status Code : {response.status_code}")
            return None
        elif response.status_code >= 400:
            print_(f"Status Code : {response.status_code} | Msg {response.text}")
            return None
        else:
            return response.json()
    except requests.exceptions.ConnectionError as e:
        print_(f"Connection Error: {e}")
    except Exception as e:
        print_(f"Error: {e}")

def done_quest(auth_token, payload):
    url = 'https://api.pixelfarm.app/user/user-quest'
    headers['Authorization'] = f'Bearer {auth_token}'
    try:
        response = requests.put(url, headers=headers, json=payload)
        if response.status_code >= 500:
            print_(f"Status Code : {response.status_code}")
            return None
        elif response.status_code >= 400:
            print_(f"Status Code : {response.status_code} | Msg {response.text}")
            return None
        else:
            return response.json()
    except requests.exceptions.ConnectionError as e:
        print_(f"Connection Error: {e}")
    except Exception as e:
        print_(f"Error: {e}")

def clear_quest(id, token):
    data_quest = get_quest(id)
    if data_quest is not None:
        list_quest = data_quest.get('data')
        for quest in list_quest:
            if quest['done_at'] is None:
                payload = {"quest_id":quest.get('id')}
                time.sleep(2)
                data_done = done_quest(token, quest)
                if data_done is not None:
                    data = data_done.get('data')
                    if data == True:
                        print_(f"Quest {quest.get('name')} completed")
            else:
                print_(f"Quest {quest.get('name')} Done")

def main():
    fruit_total = 2000
    while True:
        queries = load_credentials()
        delay = 3600*4
        start_time = time.time()
        for index, query in enumerate(queries):
            useragent = getuseragent(index)
            headers['User-Agent'] = useragent
            encoded_query = quote(query)
            data_parse = parse_query(query)
            user = data_parse.get('user')
            print_(f"============ [Account {index+1} | {user.get('username')}] ===========")
            auth_token = get_token(user.get('id'))
            if auth_token is None:
                data_auth = auth(encoded_query)
                if data_auth is not None:
                    print_("Set Token")
                    auth_token = data_auth.get('data')
                    set_token(user.get('id'), auth_token)
            time.sleep(2)
            clear_quest(user.get('id'), auth_token)
            time.sleep(2)
            claim_response = claim(auth_token)
            if claim_response['data']:
                time.sleep(2)
                user_data = get_user_data(auth_token)
                print_(f"[ Username     ]  : {user_data['data']['telegram_username']}")
                print_(f"[ Gem Amount   ]  : {user_data['data']['gem_amount']}")
                print_(f"[ Total Fruit  ]  : {user_data['data']['crops'][0]['fruit_total']}")
                print_(f"[ Tipe Tree    ]  : {user_data['data']['crops'][0]['tree_type']}")
                total_fruit = user_data['data']['crops'][0]['fruit_total']
                if user_data['data']['crops'][0]['fruit_total'] >= fruit_total:
                    payload = {
                        "tree_type": user_data['data']['crops'][0]['tree_type'],
                        "amount": int(total_fruit)
                    }
                    response = sell(auth_token, payload)
                    if response:
                        print_("Sell fruit successfully")
                        print_("="*46)
                    else:
                        print_("Sell fruit failed")
                        print_("="*46)
                else:
                    print_(f"Total Fruits : {total_fruit}")
                    print_(f"Minimum Sell Fruits   : {fruit_total}")
                    print_("="*46)
            else:
                print_("\nClaim Response: Failed Claim")
                print_("="*46)

        end_time = time.time()
        total_time = delay - (end_time - start_time)
        print_("========= All Account Done =========")
        print()
        printdelay(total_time)
        time.sleep(total_time)
        

        

if __name__ == "__main__":
    main()