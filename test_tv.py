from tvDatafeed import TvDatafeed, Interval
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import websocket
import ssl
import socket
from datetime import datetime

def print_with_time(*args, **kwargs):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}]', *args, **kwargs)


def on_retry(retry_state):
    print_with_time(f"[尝试第 {retry_state.attempt_number} 次] 调用失败Err,准备重试...")
    #shift_to_next_proxy()  # 假设这是切换代理的函数
    # 调用 tv_client 的方法
    proxy = {
    'http_proxy_host': '172.29.106.29',
    'http_proxy_port': 28888,
    # 如果需要认证
    #'http_proxy_auth': ('proxy_username', 'proxy_password')
    }
    if retry_state.attempt_number == 2:
        tv.set_proxy(proxy) 


@retry(
    stop=stop_after_attempt(3),          # 最多尝试3次
    wait=wait_fixed(3),                  # 每次失败后等待3秒
    retry=retry_if_exception_type((websocket.WebSocketException, TimeoutError, ConnectionError, ssl.SSLError, socket.error)),
    before_sleep=on_retry  # 动态创建 on_retry 并传入 tv_client
)
def test_basic_functionality():
    """测试基本功能是否正常工作"""
    '''
    proxy = {
    'http_proxy_host': '172.18.112.1',
    'http_proxy_port': 7897,
    # 如果需要认证
    #'http_proxy_auth': ('proxy_username', 'proxy_password')
    }
    '''

    data = tv.get_hist(symbol="AAPL", exchange="NASDAQ", interval=Interval.in_daily, n_bars=30)
    
    if data is not None and not data.empty:
        print_with_time("✅ Basic functionality test passed")

    else:
        print("❌ Basic functionality test failed")

import time
if __name__ == "__main__":

    proxy = {
    'http_proxy_host': '127.0.0.1',
    'http_proxy_port': 9981,
    # 如果需要认证
    'http_proxy_auth': ('admin', 'pavilion')
    }
    tv = TvDatafeed()
    while True:
        tv.set_proxy(proxy)
        try:
            test_basic_functionality()
        except Exception as e:
            print_with_time(f"❌ Basic functionality test failed with exception: {e}")

        time.sleep(35)  # 等待5秒后重试
