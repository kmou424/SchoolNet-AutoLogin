import requests
import socket
import uuid

from config import ACCOUNT, PASSWORD


def get_mac_addr() -> str:
    mac_addr = hex(uuid.getnode())[2:]
    return ':'.join(mac_addr[i:i + 2] for i in range(0, len(mac_addr), 2))


IPV4_ADDR = socket.gethostbyname(socket.gethostname())
MAC_ADDR = get_mac_addr()

url = f"http://10.10.11.14/webauth.do?wlanuserip={IPV4_ADDR}&wlanacname=XF_BRAS&mac={MAC_ADDR}&vlan=0" \
      f"&rand=38cf68abb081fe"

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "upgrade-insecure-requests": "1"
}

body = "&".join([
    "loginType=",
    "auth_type=0",
    "isBindMac1=0",
    "pageid=1",
    "templatetype=3",
    "listbindmac=0",
    "recordmac=0",
    "isRemind=0",
    "loginTimes=",
    "groupId=",
    "distoken=",
    "echostr=",
    "url=",
    "isautoauth=",
    "notice_pic_loop2=%2Fportal%2Fuploads%2Fgeneral%2Fdemo1%2Fimage%2Fbanner.jpg",
    "notice_pic_loop2=%2Fportal%2Fuploads%2Fgeneral%2Fdemo1%2Fimage%2Fbanner1.jpg",
    f"userId={ACCOUNT}",
    f"passwd={PASSWORD}"
])

r = requests.post(url=url, headers=headers, data=body)
if r.status_code == 200:
    print("登录成功")
else:
    print("登录失败")
