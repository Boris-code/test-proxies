import threading
import time

import requests


def get_proxies(proxies_url):
    response = requests.get(proxies_url)
    proxies = response.text.split("\n")[:1000]
    print("共获取到 {} 个代理".format(len(proxies)))
    for proxy in proxies:
        proxy = proxy.strip().replace("<br />", "")
        if not proxy:
            continue
        proxy = {"http": "http://{}".format(proxy), "https": "https://{}".format(proxy)}
        yield proxy


def test(*, proxies_name, proxies_url):
    total_count = 0
    success_count = []
    exception_count = []
    avg_spend_time = []

    def start_request(proxies):
        start_time = time.time()
        try:
            response = requests.get(
                "https://www.baidu.com", proxies=proxies, timeout=20
            )
            print(proxies, response)
            # response = requests.get('http://icanhazip.com', proxies=proxies, timeout=20)
            # print(proxies, response.text)
            spend_time = time.time() - start_time
            success_count.append(1)
            avg_spend_time.append(spend_time)

        except Exception as e:
            print("{} 请求异常".format(proxy), e)
            exception_count.append(1)

            spend_time = time.time() - start_time
            avg_spend_time.append(spend_time)

    threads = []
    for proxy in get_proxies(proxies_url):
        total_count += 1
        thread = threading.Thread(target=start_request, args=(proxy,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(
        f"""
        代理 {proxies_name} 请求百度测试
        代理总数 = {total_count}
        请求成功 = {sum(success_count)}
        请求异常 = {sum(exception_count)}
        平均耗时 = {sum(avg_spend_time) / total_count}
    """
    )


if __name__ == "__main__":
    # proxies_url 提取的代理使用\r\n分割
    test(
        proxies_name="shenlong",
        proxies_url="http://api.shenlongip.com/ip?key=7y63d77w&pattern=txt&count=50&protocol=2",
    )
