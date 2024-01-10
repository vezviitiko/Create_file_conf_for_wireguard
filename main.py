import subprocess

def generate_key():
    # Генерация ключа
    genkey_process = subprocess.Popen(["wg", "genkey"], stdout=subprocess.PIPE)
    genkey_output, _ = genkey_process.communicate()
    private_key = genkey_output.decode().strip()

    # Публичный ключ из приватного
    pubkey_process = subprocess.Popen(["wg", "pubkey"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    pubkey_output, _ = pubkey_process.communicate(input=private_key.encode())
    public_key = pubkey_output.decode().strip()

    print("Приватный ключ:", private_key)
    print("Публичный ключ:", public_key)
    return(private_key, public_key)

def create_wireguard_config(port_num, key_pri):
    file_content = f"""[Interface]
PrivateKey = {key_pri}
Address = 10.66.66.{port_num}/24, fd42:42:42::{port_num}/64
DNS = 8.8.8.8, 8.8.4.4
        
[Peer]
PublicKey = ##your public key server
AllowedIPs = 0.0.0.0/0, ::/0 
Endpoint = ##your ip:##your port 
PersistentKeepalive = 30"""

    with open(f"""wire{port_num}.conf""", 'w') as file:
        file.write(file_content)

def append_to_file(file_name, text_to_append):
    with open(file_name, 'a') as file:
        file.write(text_to_append)

port_num = input("Введите номер свободного порта: ")

key_pri,key_pub = generate_key()

create_wireguard_config(port_num, key_pri)
print(f"""Файл wire{port_num}.conf создан успешно""")

file_name = "wg0.conf"
text_to_append = f"""

[Peer]
#new conn mobily {port_num}
PublicKey = {key_pub}
AllowedIPs = 10.66.66.{port_num}/32, fd42:42:42::{port_num}/128"""

append_to_file(file_name, text_to_append)
print("Файл "+file_name+" успешно дополнен")
