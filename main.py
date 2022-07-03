from requests import session as sesh
import requests
from requests.adapters import HTTPAdapter
from ssl import PROTOCOL_TLSv1_2
from urllib3 import PoolManager
from collections import OrderedDict
from re import compile
from cryptocode import decrypt
import ctypes
import os


class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block, ssl_version=PROTOCOL_TLSv1_2)

def checker():
    os.system("cls")
    ctypes.windll.kernel32.SetConsoleTitleA("Valorant Skin Checker")
    print("""
  ██████  ██ ▄█▀ ██▓ ███▄    █     ▄████▄   ██░ ██ ▓█████  ▄████▄   ██ ▄█▀▓█████  ██▀███  
▒██    ▒  ██▄█▒ ▓██▒ ██ ▀█   █    ▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
░ ▓██▄   ▓███▄░ ▒██▒▓██  ▀█ ██▒   ▒▓█    ▄ ▒██▀▀██░▒███   ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒
  ▒   ██▒▓██ █▄ ░██░▓██▒  ▐▌██▒   ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
▒██████▒▒▒██▒ █▄░██░▒██░   ▓██░   ▒ ▓███▀ ░░▓█▒░██▓░▒████▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒
▒ ▒▓▒ ▒ ░▒ ▒▒ ▓▒░▓  ░ ▒░   ▒ ▒    ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░▒  ░ ░░ ░▒ ▒░ ▒ ░░ ░░   ░ ▒░     ░  ▒    ▒ ░▒░ ░ ░ ░  ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
░  ░  ░  ░ ░░ ░  ▒ ░   ░   ░ ░    ░         ░  ░░ ░   ░   ░        ░ ░░ ░    ░     ░░   ░ 
      ░  ░  ░    ░           ░    ░ ░       ░  ░  ░   ░  ░░ ░      ░  ░      ░  ░   ░     
                                  ░                       ░                                  """)
    lines = input("Account: ")
    username = lines.split(":")[0].replace('\n', '')
    password = lines.split(":")[1].replace('\n', '')
    headers = OrderedDict({
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "application/json, text/plain, */*",
        'User-Agent': 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)'
    })
    session = sesh()
    session.headers = headers
    session.mount('https://', TLSAdapter())
    data = {
        "client_id": "play-valorant-web-prod",
        "nonce": "1",
        "redirect_uri": "https://playvalorant.com/opt_in",
        "response_type": "token id_token",
        'scope': 'account openid',
    }
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)',
    }
    r = session.post(f'https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers)
    data = {
        'type': 'auth',
        'username': username,
        'password': password
    }
    r2 = session.put('https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers)
    data = r2.json()

    if "access_token" in r2.text:
        pattern = compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
        data = pattern.findall(data['response']['parameters']['uri'])[0]
        token = data[0]
    elif "auth_failure" in r2.text:
        print("banned")

    elif "rate_limited" in r2.text:
        print("Ratelimited")


    headers = {
        'User-Agent': 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)',
        'Authorization': f'Bearer {token}',
    }
    r = session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={})
    entitlement = r.json()['entitlements_token']

    r = session.post('https://auth.riotgames.com/userinfo', headers=headers, json={})
    data = r.json()
    puuid = data['sub']
    sess = requests.Session()
    UrlList = {"AuthUrl":"https://auth.riotgames.com/api/v1/authorization","EntitlementsUrl":"https://entitlements.auth.riotgames.com/api/token/v1","UserInfoUrl":"https://auth.riotgames.com/userinfo"}
    DefaultHeaders1 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko","Pragma": "no-cache","Accept": "*/*","Content-Type": "application/json"}
    Skin = []
    SkinStr = ""
    RankIDtoRank = {"0":"Unranked","1":"Unused1", "2":"Unused2" ,"3":"Iron 1" ,"4":"Iron 2" ,"5":"Iron 3" ,"6":"Bronz 1" ,"7":"Bronz 2" ,"8":"Bronz 3" ,"9":"Silver 1" ,"10":"Silver 2", "11":"Silver 3" ,"12":"Gold 1" ,"13":"Gold 2" ,"14":"Gold 3" ,"15":"Platinum 1" ,"16":"Platinum 2" ,"17":"Plantinum 3" ,"18":"Diamond 1" ,"19":"Diamond 2" ,"20":"Diamond 3" ,"21":"Immortal 1" ,"22":"Immortal 2" ,"23":"Immortal 3" ,"24":"Radiant"}
    DefaultHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko","Pragma": "no-cache","Accept": "*/*","Content-Type": "application/json","Authorization":f"Bearer {token}"}  
    GetUserInfo = sess.post(UrlList["UserInfoUrl"],headers=DefaultHeaders)
    GameName =  GetUserInfo.text.split('game_name":"')[1].split('"')[0]           
    Tag = GetUserInfo.text.split('tag_line":"')[1].split('"')[0]  
    Sub = GetUserInfo.text.split('sub":"')[1].split('"')[0] 
    EmailVerified = GetUserInfo.text.split('email_verified":')[1].split('"')[0]
    GetAccountRegion = sess.get(f"https://api.henrikdev.xyz/valorant/v1/account/{GameName}/{Tag}",headers=DefaultHeaders1)
    if "region" in GetAccountRegion.text:
        Region = GetAccountRegion.json()["data"]["region"]
        AccountLevel = GetAccountRegion.json()["data"]["account_level"]
        Lastupdate = GetAccountRegion.json()["data"]["last_update"]
    else:
        print("Fail")
    PvpNetHeaders = {"Content-Type": "application/json","Authorization": f"Bearer {token}","X-Riot-Entitlements-JWT": entitlement,"X-Riot-ClientVersion": "release-01.08-shipping-10-471230","X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"} 
    try:
        CheckRanked = sess.get(f"https://pd.{Region}.a.pvp.net/mmr/v1/players/{puuid}/competitiveupdates",headers=PvpNetHeaders)

        if '","Matches":[]}' in CheckRanked.text:
            Rank = "UnRanked"
            
        else:
            RankID = CheckRanked.text.split('"TierAfterUpdate":')[1].split(',"')[0]
            Rank = RankIDtoRank[RankID]                  
    except:
        Rank = "Unknow"
    try:
        GetPoints = sess.get(f"https://pd.{Region}.a.pvp.net/store/v1/wallet/{Sub}",headers=PvpNetHeaders)
        ValorantPoints = GetPoints.json()["Balances"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"]
        Radianite = GetPoints.json()["Balances"]["e59aa87c-4cbf-517a-5983-6e81511be9b7"]
    except:
        ValorantPoints = "UnKnow"
        Radianite = "UnKnow"      
    try:
        GetSkins = sess.get(f"https://pd.{Region}.a.pvp.net/personalization/v2/players/{Sub}/playerloadout",headers=PvpNetHeaders) 
        Skins = GetSkins.json()["Guns"]
        SkinsLength = len(Skins)
        SkinRange = range(SkinsLength)
        for xs in SkinRange:
            Skins2 = GetSkins.json()["Guns"][xs]["SkinID"]
            GetSkinName = sess.get(f"https://valorant-api.com/v1/weapons/skins/{Skins2}")
            SkinName = GetSkinName.json()["data"]["displayName"]
            Skin.append(SkinName)
            SkinStr += "| " + SkinName + "\n"   
    except:
        Skin.clear()
        Skin = "UnKnow"
        SkinStr = "| UnKnow \n"
    print(f"{username}:{password} | Region: {Region} | Last played: {Lastupdate}| Level: {AccountLevel} | Email Verified: {EmailVerified} | Rank: {Rank} | VP: {ValorantPoints} | RP: {Radianite} | Total Skins: {len(Skin)}")   
    SaveHits = open("results//Hits.txt", "a+")
    SaveHits.write(f"[--------------[Valorant]--------------]\n| User&Pass: {username}:{password}\n| Region: {Region}\n| Last played: {Lastupdate}\n| Level: {AccountLevel}\n| Email Verified: {EmailVerified}\n| Rank: {Rank}\n| VP: {ValorantPoints} - RP: {Radianite}\n|-------------[Skins({len(Skin)})]-------------]\n{SkinStr}[-------------------------------------]\n\n")
    SaveHits.close()
checker()
