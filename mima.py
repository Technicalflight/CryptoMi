# -*- coding:UTF-8 -*-
import hashlib
import os
import re
import time
import requests
import random
import string
#导入jiami.py
import jiami
#导入tijiao.py
import tijiao
def main():
    #清空数据
    os.system("cls")
    #输入密码
    str = input("请输入密码：")
    #输入使用该密码的网站
    str1 = input("请输入使用该密码的网站：")
    #判断网站是否为空
    if str1 == "":
        print("网站不能为空")
        #等待3秒
        time.sleep(3)
        #返回主函数,重新输入
        main()
    #正则判断网站是否合法
    if not re.match(r'^[a-zA-Z0-9]+([\-\.][a-zA-Z0-9]+)*\.[a-zA-Z]{2,5}$',str1):
        print("网站不合法")
        #等待3秒
        time.sleep(3)
        #返回主函数
        main()
    #判断网站是否已经存在
    if str1 in open("mima.txt","r").read():
        print("网站已存在,3秒后将返回")
        #等待3秒
        time.sleep(3)
        #返回主函数
        main()
    #判断密码是否为空
    if str == "":
        print("密码不能为空")
        #等待3秒
        time.sleep(3)
        #返回主函数
        main()
    sc = hashlib.sha1(str.encode("utf-8")).hexdigest()
    print("sha1加密前为 ：",str)
    print("sha1加密前后 ：",sc.upper())

    #生成145位随机字符串
    def getRandomString(length=145):
        import random
        import string
        str_list = [random.choice(string.ascii_letters + string.digits) for i in range(length)]
        random_str = ''.join(str_list)
        return random_str

    #调用kaspersky的api
    url = "https://api.pwnedpasswords.com/range/"+sc.upper()[0:5] #前五位
    payload={}
    headers = {
      'Cookie': '__cf_bm=' + getRandomString()
    }
    response = requests.request("GET", url, headers=headers, data=payload)


    #判断密码是否在数据库中
    if sc.upper()[5:] in response.text:
        print("密码已经被泄露")
        #判断密码在数据库中出现的次数
        for i in response.text.split('\n'):
            if i.split(':')[0] == sc.upper()[5:]:
                print("密码在数据库中出现的次数为:",i.split(':')[1])
        #提出选择
        print("是否继续使用该密码？")
        print("1.是")
        print("2.否")
        #输入选择
        str2 = input("请输入选择：")
        #判断选择是否为空
        if str2 == "":
            print("选择不能为空")
            #等待3秒
            time.sleep(3)
            #返回主函数
            main()
        #判断选择是否为1或2
        if str2 != "1" and str2 != "2":
            print("选择错误")
            #等待3秒
            time.sleep(3)
            #返回主函数
            main()
        #判断选择是否为1
        if str2 == "1":
            #with打开文件
            with open("mima.txt","a") as f:
                #写入密码
                f.write(str1+":"+str+"---->该密码有点危险哟!!!它的泄露次数为:"+i.split(':')[1]+"请忽略(---->)""\r")
                #输出提示,密码已写入文件
                print("密码已写入文件")
        #判断选择是否为2
        if str2 == "2":
            #输出提示,程序将随机生成一个密码
            print("程序将随机生成一个密码")
            #生成随机密码
            #输入要生成的密码长度
            str4 = input("请输入要生成的密码长度(不得低于8位,默认生成16位)：")
            #判断密码长度是否为空
            if str4 == "":
                #默认生成16位密码
                str4 = '16'
            #判断密码长度是否为数字
            if str4.isdigit() == False:
                print("密码长度必须为数字")
                #等待3秒
                time.sleep(3)
                #返回主函数
                main()
            #判断密码长度是否小于8
            if int(str4) < 8:
                print("密码长度不能小于8")
                #等待3秒
                time.sleep(3)
                #返回主函数
                main()
            seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
            sa = []
            for i in range(int(str4)):
              sa.append(random.choice(seed))
            str3 = ''.join(sa)
            print("随机生成的密码为：",str3)
            #判断生成的密码是否在数据库中
            sc1 = hashlib.sha1(str3.encode("utf-8")).hexdigest()
            url1 = "https://api.pwnedpasswords.com/range/"+sc1.upper()[0:5] #前五位
            payload1={}
            headers1 = {
                'Cookie': '__cf_bm=' + getRandomString()
            }
            response1 = requests.request("GET", url1, headers=headers1, data=payload1)
            if sc1.upper()[5:] in response1.text:
                for i in response1.text.split('\n'):
                    if i.split(':')[0] == sc1.upper()[5:]:
                        print("生成的密码在数据库中出现的次数为:",i.split(':')[1])
                        print("生成的密码已经被泄露,但是比你输入的密码安全,我就是要你用这个密码")
                        #with打开文件
                        with open("mima.txt","a") as f:
                            #写入密码
                            f.write(str1+":"+str3+"\r")
                        #输出提示,密码已写入文件
                        print("密码已写入文件")
            else:
                print("生成的密码未被泄露,开始写入文件")
                #with打开文件
                with open("mima.txt","a") as f:
                    #写入密码
                    f.write(str1+":"+str3+"\r")
                    #输出提示,密码已写入文件
                    print("密码已写入文件")
    else:
        print("密码未被泄露")
        #with打开文件
        with open("mima.txt","a") as f:
            #写入密码
            f.write(str1+":"+str+"\r")
            #输出提示,密码已写入文件
            print("密码已写入文件")

#查询密码方法
def chaxun():
    #输入要查询密码的网站域名
    str1 = input("请输入要查询密码的网站域名：")
    #判断网站域名是否为空
    if str1 == "":
        print("网站域名不能为空")
        #等待3秒
        time.sleep(3)
        #返回主菜单
        return
    #正则判断网站域名是否合法
    if re.match(r"^[a-zA-Z0-9]+([\-\.][a-zA-Z0-9]+)*\.[a-zA-Z]{2,5}$",str1) == None:
        print("网站域名不合法")
        #等待3秒
        time.sleep(3)
        #返回主菜单
        return
    #打开文件
    with open("mima.txt","r") as f:
        #读取文件
        str2 = f.read()
        #判断文件是否为空
        if str2 == "":
            print("文件为空")
            #等待3秒
            time.sleep(3)
            #返回主菜单
            return
        #判断文件中是否有该网站域名
        if str1 in str2:
            print("该网站域名已存在")
            #判断是否为查询密码
            if str1+":" in str2:
                print("该网站域名的密码为:" + str2.split(str1+":")[1].split("---->")[0])
                return str2.split(str1+":")[1].split("---->")[0]
            #判断是否为生成密码
            if str1+":" not in str2:
                print("该网站域名的密码为:" + str2.split(str1+":")[1].split("\r")[0])
                return str2.split(str1+":")[1].split("\r")[0]
        else:
            print("该网站域名在文件中不存在,请重新选择")
            #等待3秒
            time.sleep(3)
            #返回主菜单
            return















#主函数初始化
if __name__ == '__main__':
    #判断文件是否存在
    if os.path.exists("mima.txt"):
        print("文件已存在")
    else:
        #创建文件
        with open("mima.txt","w") as f:
            pass
    #死循环
    while True:
        #提示生成和查询密码
        print("1.生成密码(会使用kaspersky的api来进行密码泄露查询)")
        print("2.查询本地保存的密码")
        print("3.roboform本地测试密码(本地)")
        print("4.roboform本地生成密码(本地)")
        print("5.【谨慎使用该功能,该功能会删除明文txt,如果私钥忘了,那就基本上凉凉,别找作者,作者不知道怎么办】使用AES加密密码(本地)")
        print("6.退出")
        #输入选择
        xuanze = input("请输入选择：")
        #判断选择是否为空
        if xuanze == "":
            print("选择不能为空")
            #返回循环
            continue
        #判断选择是否为1或2
        if xuanze != "1" and xuanze != "2" and xuanze != "3" and xuanze != "4" and xuanze != "5" and xuanze != "6":
            print("选择错误")
            #返回循环
            continue
        #判断选择是否为1
        if xuanze == "1":
            #调用主函数
            main()
        #判断选择是否为2
        if xuanze == "2":
            #调用查询密码函数
            chaxun()
        #判断选择是否为3
        if xuanze == "3":
            str = chaxun()
            #调用本地测试密码函数
            tijiao.tijiao(str)
        #判断选择是否为4
        if xuanze == "4":
            #输入密码长度
            changdu = input("请输入密码长度：")
            #判断密码长度是否为空
            if changdu == "":
                print("密码长度不能为空")
                #返回循环
                continue
            #判断密码长度是否为数字
            if changdu.isdigit() == False:
                print("密码长度必须为数字")
                #返回循环
                continue
            #调用本地生成密码函数
            robo = tijiao.scpassword(changdu)
            #等待2秒
            time.sleep(2)
            #请输入要使用该密码的网站域名
            str1 = input("请输入要使用该密码的网站域名：")
            #判断网站域名是否为空
            if str1 == "":
                print("网站域名不能为空")
                #返回循环
                continue
            #正则^[a-zA-Z0-9]+([\-\.][a-zA-Z0-9]+)*\.[a-zA-Z]{2,5}$匹配网站域名
            if re.match("^[a-zA-Z0-9]+([\-\.][a-zA-Z0-9]+)*\.[a-zA-Z]{2,5}$",str1) == None:
                print("网站域名格式错误")
                #返回循环
                continue
            #写入文件
            with open("mima.txt","a") as f:
                f.write(str1+":"+ robo +"\r")
                #输出提示
                print("密码已保存")
            #关闭文件
            f.close()
        #判断选择是否为5
        if xuanze == "5":
            #调用加密函数
            jiami.main()
        #判断选择是否为6
        if xuanze == "6":
            #退出程序
            exit()


