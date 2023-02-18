import argparse
import requests
import uuid

from netifaces import interfaces, ifaddresses, AF_INET
from config import ACCOUNT, PASSWORD


def get_mac_addr() -> str:
    mac_addr = hex(uuid.getnode())[2:]
    return ':'.join(mac_addr[i:i + 2] for i in range(0, len(mac_addr), 2))


def get_ip_by_interface(interface: str) -> list:
    addresses = ifaddresses(interface)
    if AF_INET not in addresses.keys():
        return [None]
    ret = list()
    for i in addresses[AF_INET]:
        if 'addr' in i.keys():
            ret.append(i['addr'])
    return ret


USER_AGENT_PRESETS = {
    "GooglePixel6": "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.023; wv) AppleWebKit/537.36 (KHTML, "
                    "like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "iPhone13ProMax": "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, "
                      "like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
    "Windows10Edge": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "MacOSXSafari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) "
                    "Version/9.0.2 Safari/601.3.9",
    "LinuxFirefox": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
}

body = "loginType=&auth_type=0&isBindMac1=1&pageid=1&templatetype=1&listbindmac=1&recordmac=0&isRemind=0&loginTimes" \
       "=&groupId=&distoken=&echostr=&url=http://edge-http.microsoft.com&isautoauth=&notice_pic_loop1=/portal" \
       "/uploads/pc/demo3/images/logo.jpg&notice_pic_loop2=/portal/uploads/pc/demo3/images/rrs_bg.jpg&" \
       f"userId={ACCOUNT}&passwd={PASSWORD}"


def action_list(args):
    if args.ua_preset:
        print('\n'.join(USER_AGENT_PRESETS.keys()))
    elif args.interface:
        print('\n\n'.join([f"Interface:\t {it}\nIP(s):\t\t {', '.join([str(name) for name in get_ip_by_interface(it)])}"
                           for it in interfaces()]))


def action_login(args):
    assert args.ua_preset in USER_AGENT_PRESETS.keys(), f"User-Agent preset: \"{args.ua_preset}\" is not found"
    interface_args = args.interface.split(':')
    assert len(interface_args) == 2, f"Interface: \"{args.interface}\" must like \"[Interface Name]:[n-st IP]\" type"
    interface, ip_st = interface_args
    assert interface in interfaces(), f"Interface: \"{interface}\" is not found"
    assert ip_st.isdigit(), f"Interface n-st IP parse error: \"{ip_st}\" is not a digit number"
    ip_st = int(ip_st)
    ips = get_ip_by_interface(interface)
    assert 1 <= ip_st <= len(ips), f"Interface n-st IP number is invalid: All of IP(s) count is {len(ips)}" \
                                   f", but {ip_st} by given"

    url = f"http://10.10.11.14/webauth.do" \
          f"?wlanacip=10.10.11.101" \
          f"&wlanacname=XF_BRAS" \
          f"&wlanuserip={ips[ip_st - 1]}" \
          f"&mac={get_mac_addr()}" \
          f"&vlan=0" \
          f"&url=http://edge-http.microsoft.com"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "DNT": "1",
        "Host": "10.10.11.14",
        "Origin": "http://10.10.11.14",
        "Referer": f"{url}",
        "Upgrade-Insecure-Requests": "1",
        'User-Agent': USER_AGENT_PRESETS[args.ua_preset]
    }
    print(f"Requesting(Post): {url}")
    r = requests.post(url=url, headers=headers, data=body)

    print()
    print(f"Status Code: {r.status_code}")
    print(f"Request Body: {r.request.body}")
    print(f"Request Headers: {r.request.headers}")
    print()

    print("Result: ", end="")
    if r.status_code == 200:
        print("Login Succeed")
    else:
        print("Login Failed")


def arguments():
    arg_parser = argparse.ArgumentParser(description="SchoolNet login for SCITC")
    action_subparser = arg_parser.add_subparsers(dest="action", title="action options")
    login_action_subparser = action_subparser.add_parser("login", help="login SchoolNet")
    login_action_subparser.set_defaults(func=action_login)
    login_action_subparser.add_argument(
        '-u', '--ua-preset',
        required=True,
        type=str,
        metavar='[User-Agent Preset Name]',
        help='set user-agent to login SchoolNet'
    )
    login_action_subparser.add_argument(
        '-i', '--interface',
        required=True,
        type=str,
        metavar='[Network Interface Name with n-st IP]',
        help='set network interface to login SchoolNet(eg. eth0:1/wlan:2/[Interface Name]:[n-st IP])'
    )
    help_action_subparser = action_subparser.add_parser("list", help="show some available arguments")
    help_action_subparser.set_defaults(func=action_list)
    help_action_subparser_mutually_exclusive_group = help_action_subparser.add_mutually_exclusive_group()
    help_action_subparser_mutually_exclusive_group.add_argument(
        '-u', '--ua-preset',
        action='store_true',
        help='User-Agent presets'
    )
    help_action_subparser_mutually_exclusive_group.add_argument(
        '-i', '--interface',
        action='store_true',
        help='Network Interfaces'
    )
    args = arg_parser.parse_args()
    if not args.action:
        arg_parser.print_help()
    else:
        args.func(args)


if __name__ == '__main__':
    arguments()
