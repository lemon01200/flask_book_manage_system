# from lzx
import os

"""
获取对应深度的父目录的路径
"""

def get_parent_path(file, deep):
    """
    :param file: 当前文件路径
    :param deep: 当前文件到对应文件父目录的深度
    :return:
    """
    # 获取当前文件所在目录
    filename = os.path.realpath(file)
    # 获取当前文件父目录
    file_path = os.path.dirname(filename)
    # 获取文件实际目录
    for i in range(0, deep):
        # 获取父目录的绝对路径
        tmp_parent_path = os.path.abspath(os.path.join(file_path, os.path.pardir))
        file_path = tmp_parent_path
    return file_path


