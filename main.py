import requests
import json
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import datetime

# 假设 user_tokens 是一个公共的模块，它被两个脚本都使用
import user_tokens

# 第一个脚本的代码
def script1():
    def send_request(data, token):
        url = "https://xxyx-client-api.xiaoxiaoyouxuan.com/sign_up"
        headers = {"xx-token": token}
        response = requests.post(url, headers=headers, json=data)
        return "success" in response.text

    def main_script1(token):
        task_id = input("请输入目标id：")
        data = {"task_id": task_id}
        try:
            start_time_str = input("请输入开始时间（英文状态下输入，格式：YYYY-MM-DD HH:MM:SS）：")
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
            preset_run_time = int(start_time.timestamp())
            current_time = time.time()
            remaining_time = preset_run_time - current_time
        except ValueError:
            print("输入有误，请检查是否为英文状态下输入")
            return

        while remaining_time > 0:
            time.sleep(1)
            current_time = time.time()
            remaining_time = preset_run_time - current_time
            if remaining_time > 0:
                hours = int(remaining_time / 3600)
                minutes = int((remaining_time % 3600) / 60)
                seconds = int((remaining_time % 3600) % 60)

                #print(f"当前系统时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}，距离抢购时间还有：{hours}小时{minutes}分钟{seconds}秒")
                print(f"\r当前系统时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}，距离抢购时间还有：{hours}小时{minutes}分钟{seconds}秒", end="")



        print(" ")
        print("抢购中.....")
        results = []
        with ThreadPoolExecutor(max_workers=50) as executor:
            results = list(executor.map(lambda data: send_request(data, token), [data for _ in range(1000)]))

        if any(results):
            print("************抢购成功************")
        else:
            print("************抢购失败************")

        print(f"当前系统时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        print("注: 仅供学习交流，违法使用后果自负")
        print("*" * 40)

    print("*" * 100)
    print("\n欢迎使用FUCK-晓晓\n")

    while True:
        choice = input("请输入选项＞＞\n1 - 使用内置token\n2 - 使用活动token\n3 - 说明\n4 - 退出\n")

        if choice == "2":
            token = input("请输入xx-token的值：")
            main_script1(token) 
        elif choice == "1":
            name_choice = input("请选择：\n" + "\n".join([f"{k} - {v['name']}" for k, v in user_tokens.tokens.items()]))  # Adjusting token selection
            token = user_tokens.tokens.get(name_choice, {}).get("token", "")
            if token:
                main_script1(token)
            else:
                print("无效选项，请重新输入。")
        elif choice == "3":
            print("*" * 100)
            print("时间设置：默认1000发，50并发，耗时0.5s，即每秒100发，共执行10s，所以务必将程序开始时间卡在此10秒内。")
            print("\n获取id：打开plus.web.xxyx.ltd，提取对应活动页面网址结尾处的id")
            print("\n时间格式：YYYY-MM-DD HH:MM:SS 如2023-8-20 8:59:57 纯英文输入")
            print("\n获取token：打开plus.web.xxyx.ltd，短信验证码登录，随便打开一个活动页面，抓包'xx-token的值'")
            print("*" * 100)
        elif choice == "4":
            break
        else:
            print("无效选项，请重新输入。")

# 第二个脚本的代码
def script2():
    def query_orders(token):
        url = 'https://xxyx-client-api.xiaoxiaoyouxuan.com/order_list?limit=10&page=1&status=1'
        headers = {
            "xx-token": token
        }

        response = requests.get(url, headers=headers)
        response_data = json.loads(response.text)
        order_list = response_data['data']['list']

        for order in order_list:
            platform = order['platform']
            store_name = order['store_name']
            create_time = order['create_time']
            rule = order['rule']
            name = order['status']['name']
            praise_demand_info = order['praise_demand_info']

            print(f"\n{platform}\n{store_name}\n{create_time}\n{rule}\n{name}\n{praise_demand_info}\n")

    while True:
        print("*" * 100)
        print("\n欢迎使用订单查询\n")
        choice = input("请选择查询方式：\n1. 查询内置\n2. 查询指定token\n3. 退出\n")

        if choice == '1':
            for key, data in user_tokens.tokens.items():
                print(f"{key}: {data['name']}")

            selected_key = input("请选择token编号（或输入B返回上一步）：")
            if selected_key == 'B':
                continue
            if selected_key in user_tokens.tokens:
                selected_token = user_tokens.tokens[selected_key]['token']
                query_orders(selected_token)
            else:
                print("无效的token编号")
        elif choice == '2':
            token_value = input("请输入xx-token的值（或输入B返回上一步）：")
            if token_value == 'B':
                continue
            query_orders(token_value)
        elif choice == '3':
            print("谢谢使用，再见！")
            break
        else:
            print("无效的选择")

# 主选择功能
def main():
    while True:
        print("*" * 100)
        print("\n功能选择:\n")
        print("1. 抢单")
        print("2. 查询")
        print("3. 退出程序")

        choice = input("\n请选择一个选项: ")

        if choice == "1":
            script1()
        elif choice == "2":
            script2()
        elif choice == "3":
            print("谢谢使用，再见！")
            break
        else:
            print("无效的选择，请重新输入。")

if __name__ == "__main__":
    main()
