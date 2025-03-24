import jmcomic
import os
import glob
from wcferry import Wcf
import time
from time import sleep
from threading import Thread
from queue import Empty

print("Start demo...")
wcf = Wcf(debug=True)  # 默认连接本地服务

sleep(5)  # 等微信加载好，以免信息显示异常
print(f"已经登录: {True if wcf.is_login() else False}")
print(f"wxid: {wcf.get_self_wxid()}")

def get_jm(album_id: int):
    # 创建 option 对象
    option = jmcomic.create_option_by_file('op.yml')

    # 下载本子
    option.download_album(album_id)

    # 获取下载路径
    download_path = '.'

    # 查找最新生成的 PDF 文件
    pdf_files = glob.glob(os.path.join(download_path, '*.pdf'))
    latest_pdf = max(pdf_files, key=os.path.getctime)

    # 返回最新生成的 PDF 文件的绝对路径
    return os.path.abspath(latest_pdf)

def handle_message(msg):
    if msg['type'] == 'Text' and msg['content'].startswith('\\jm '):
        try:
            album_id = int(msg['content'][4:].strip())
            pdf_path = get_jm(album_id)
            wcf.send_file(msg['from_group'], pdf_path)
        except ValueError:
            wcf.send_text(msg['from_group'], 'Invalid album ID.')

def process_msg(wcf: Wcf):
    """处理接收到的消息"""
    while wcf.is_receiving_msg():
        try:
            msg = wcf.get_msg()
            print(msg)  # 简单打印
            # 处理消息
            if msg['type'] == 'Text' and msg['content'].startswith('\\jm '):
                try:
                    album_id = int(msg['content'][4:].strip())
                    pdf_path = get_jm(album_id)
                    # 发送文件到指定群聊
                    wcf.send_file('test', pdf_path)
                except ValueError:
                    wcf.send_text('test', 'Invalid album ID.')
        except Empty:
            continue  # Empty message
        except Exception as e:
            print(f"Receiving message error: {e}")

# 监听群聊消息
wcf.enable_receiving_msg(pyq=False)
Thread(target=process_msg, name="GetMessage", args=(wcf,), daemon=True).start()

# 保持程序运行
wcf.keep_running()