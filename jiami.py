#!/usr/bin/env python
#AES-demo
import os
import base64
import time
from Crypto.Cipher import AES

'''
采用AES对称加密算法
'''


# str不是16的倍数那就补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes

# 加密方法
def encrypt_oracle(key):
    try:
        # 一次性读取文本内容
        with open('mima.txt', 'r') as banks:
            # print(text) 测试打印读取的数据
            # 待加密文本
            mystr = banks.read()
        text = base64.b64encode(mystr.encode('utf-8')).decode('ascii')
        # 初始化加密器
        aes = AES.new(add_to_16(key), AES.MODE_ECB)
        # 先进行aes加密
        encrypt_aes = aes.encrypt(add_to_16(text))
        # 用base64转成字符串形式
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
        # print(encrypted_text) 测试打印加密数据
        # 写入加密数据到文件
        with open("bankmima.txt","w") as bankdata:
            bankdata.write(encrypted_text)
            print("加密完成")
    except:
        print("加密失败")

# 解密方法
def decrypt_oralce(key):
    try:
        # 密文
        with open('bankmima.txt', 'r', encoding='utf-8') as banks:
            # print(text) 测试打印读取的加密数据
            # 待解密文本
            text = banks.read()
        # 初始化加密器
        aes = AES.new(add_to_16(key), AES.MODE_ECB)
        # 优先逆向解密base64成bytes
        base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
        # bytes解密
        decrypted_text = str(aes.decrypt(base64_decrypted),encoding='utf-8') # 执行解密密并转码返回str
        decrypted_text = base64.b64decode(decrypted_text.encode('utf-8')).decode('utf-8')
        #写入解密数据到文件
        with open("mima.txt","w") as bankdata:
            bankdata.write(decrypted_text)
            print("解密完成")
        return decrypted_text
    except:
        print("解密失败")

def main():
    #提供选择
    print("1.加密")
    print("2.解密")
    print("3.退出")
    while True:
        choose = input("请选择:")
        if choose == "1":
            #判断是否有bankmima.txt
            if os.path.exists("bankmima.txt"):
                print("文件已存在,请输入解密密匙")
                #输入私钥
                key = input("请输入私钥(请记好你的私钥，忘了那就凉凉，别找作者，作者也没有办法):")
                #解密
                str = decrypt_oralce(key)
                #判断是否解密成功
                if str == None:
                    print("解密失败")
                    #等待3秒
                    time.sleep(3)
                    return
                #创建mima.txt文件
                with open("mima.txt","w") as f:
                    f.write(str)
                #加密
                print("请重新输入密匙(你可以重新输入一个新的密匙,也可以输入原来的密匙)")
                key = input("请输入私钥(请记好你的私钥，忘了那就凉凉，别找作者，作者也没有办法):")
                encrypt_oracle(key)
                #删除mima.txt文件
                os.remove("mima.txt")
            else:
                #输入私钥
                key = input("请输入私钥(请记好你的私钥，忘了那就凉凉，别找作者，作者也没有办法):")
                #加密
                encrypt_oracle(key)
                #判断是否加密成功
                if os.path.exists("bankmima.txt") == False:
                    print("加密失败")
                    #等待3秒
                    time.sleep(3)
                    return
                #删除mima.txt文件
                os.remove("mima.txt")
        elif choose == "2":
            #输入私钥
            key = input("请输入私钥:")
            #解密
            str = decrypt_oralce(key)
            #判断是否解密成功
            if str == None:
                print("解密失败")
                #等待3秒
                time.sleep(3)
                return
            #删除bankmima.txt文件
            os.remove("bankmima.txt")
        elif choose == "3":
            break
        else:
            print("输入错误")
