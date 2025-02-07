from Crypto.Cipher import AES
import base64


# 填充函数，将数据填充到16字节的倍数
def pad(data):
    while len(data) % 16 != 0:
        data += b' '
    return data


# 移除填充函数
def unpad(data):
    return data.rstrip(b' ')


# AES 加密
def aes_encrypt(data):
    data = data.encode('utf-8')
    # 使用固定密钥字符串并将其编码为字节类型
    key = "qwertyuiopasdfgh".encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_data = cipher.encrypt(pad(data))
    return base64.b64encode(iv + encrypted_data).decode('utf-8')


# AES 解密
def aes_decrypt(encrypted_data):
    # 使用固定密钥字符串并将其编码为字节类型
    key = "qwertyuiopasdfgh".encode('utf-8')
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data[16:]))
    return decrypted_data.decode('utf-8')

# 示例数据
# data = "Hello, World!"
#
#
# # 加密数据
# encrypted_data = aes_encrypt(data)
# print(f"Encrypted: {encrypted_data}")
#
# # 解密数据
# decrypted_data = aes_decrypt(encrypted_data)
# print(f"Decrypted: {decrypted_data}")
