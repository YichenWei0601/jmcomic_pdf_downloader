"""
This script is used to download the PDF of a specific album from jmcomic.com
Directly run this script and enter the album ID to download the PDF.
"""

import jmcomic
import os
import glob


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
    print("PDF Downloaded: ", latest_pdf)

index = input("Enter the album ID: ")
get_jm(int(index))