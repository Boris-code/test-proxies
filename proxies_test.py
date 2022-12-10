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
    spend_time = []
    one_proxy_test_times = 1  # 每个代理请求的次数

    def start_request(proxies):
        for i in range(one_proxy_test_times):
            start_time = time.time()
            try:
                response = requests.get(
                    "https://www.baidu.com", proxies=proxies, timeout=20
                )
                print(proxies, response)
                # response = requests.get('http://icanhazip.com', proxies=proxies, timeout=20)
                # print(proxies, response.text)
                success_count.append(1)
                spend_time.append(time.time() - start_time)

            except Exception as e:
                print("{} 请求异常".format(proxy), e)
                exception_count.append(1)
                spend_time.append(time.time() - start_time)

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
        并发总请求次数 = {total_count * one_proxy_test_times}
        请求成功 = {sum(success_count)}
        请求异常 = {sum(exception_count)}
        平均耗时 = {sum(spend_time) / total_count * one_proxy_test_times}
    """
    )


if __name__ == "__main__":
    # proxies_url 提取的代理使用\r\n分割
    # test(
    #     proxies_name="shenlong",
    #     proxies_url="http://api.shenlongip.com/ip?key=7y63d77w&pattern=txt&count=50&protocol=2",
    # )
    test(
        proxies_name="品赞",
        proxies_url="https://service.ipzan.com/core-extract?num=50&no=20211015780077026986&minute=1&repeat=1&pool=ordinary&mode=whitelist&secret=f2fqhitk8",
    )
