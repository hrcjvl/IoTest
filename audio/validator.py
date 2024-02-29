#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
用于测试结果校验的代码
"""
import json as js
import re
import os
from .testresult import STATUS


import sys

# add audio process
# import librosa
# import sys
# import numpy as np



def json(output):
    """ 将output字符串加载为json方式的dict """
    return js.loads(output)


def element(obj, key, default=None):
    """ 获得obj的数据成员，如果key不存在，则返回default内容 """
    if key in obj:
        return obj[key]
    else:
        return default


def strcut_element(output, xpath):
    """ 获得格式化二进制报文xpath对应的基本数据，例如strcut_element(output, "/a/b") """
    try:
        data = js.loads(output)
        splits = xpath.split('/') 
        for s in splits:
            if len(s)>0:
                data = data[s]
        for key in data:
            if key.startswith('@'):
                return data[key]            
    except:
        raise Exception('无法从%s读取成员%s'%(output, xpath))
    return None


def hex2bytes(hex):
    """ 将hex方式的字符串转变为byte数组 """
    a_bytes = bytes.fromhex(hex)
    return a_bytes


def validate(results: list) -> STATUS:
    """ 综合各个测试步骤的结果，获得有个综合结果。如果有一个步骤失败/未知，则总体结果失败/未知；否则测试结果为成功 """
    failed = 0
    unknown = 0
    passed = 0
    for o in results:
        if o.status == STATUS.FAILED:
            failed = failed + 1
        elif o.status == STATUS.UNKNOWN:
            unknown = unknown + 1
        elif o.status == STATUS.PASSED:
            passed = passed + 1

    if failed > 0:
        return STATUS.FAILED

    if unknown > 0:
        return STATUS.UNKNOWN

    return STATUS.PASSED


def read_txt(file, encoding='utf-8'):
    """ 读取文本文件，返回全部文本内容 """
    if not os.path.exists(file):
        raise Exception("File not found: " + file)

    with open(file, "r", encoding=encoding) as f:
        content = f.read()
    return content


def read_json(file, encoding='utf-8'):
    """ 读取JSON文件，返回JSON对象 """
    content = read_txt(file, encoding)
    return json(content)


def grep(str, pattern):
    """ 从字符串中找出匹配正则表达式的所有内容，并按数组返回 """
    match = re.findall(pattern, str, re.I)
    return match


def grep_file(file, pattern, encoding='utf-8'):
    """ 从文件中找出匹配正则表达式的所有内容，并按数组返回 """
    content = read_txt(file, encoding) 
    return grep(content, pattern)


def cmp_audio(src, dest):
    sys.exec("/tmp/xxx /tmp/yyy -v")



# def process_audio(src, dest):
#     print("exec audio.py")
#     print(os.getcwd())
#     path = os.getcwd()
#     os.execlp('python/python.exe','python', 'src/python/iotest/audio.py', src, dest)


import subprocess

# def process_audio(src, dest):
#     print("exec audio.py")
#     print(os.getcwd())
#     path = os.getcwd()
#     # 构建Python脚本的绝对路径
#     script_path = os.path.join(path, 'src', 'python', 'iotest', 'audio.py')
#     python_path = os.path.join(path, 'python', 'python.exe')
#     # 使用完整路径运行Python解释器
#     subprocess.Popen(['python', script_path, src, dest])

def process_audio(src, dest, threshold=0.6):
    # print("exec audio.py")
    path = os.getcwd()
    
    script_path = os.path.join(path, 'src', 'python', 'iotest', 'audio.py')
    
    # 240229
    src_path = os.path.join(path, 'resource', 'audio', 'srcAudio.wav')
    dest_path = os.path.join(path, 'resource', 'audio', 'destAudio.wav')
    
    
    # end 240229
    
    process = subprocess.Popen(['python', script_path, src_path, dest_path],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               creationflags=subprocess.CREATE_NO_WINDOW)
    # 等待程序完成并获取输出结果
    stdout, stderr = process.communicate()
    similarity = 0;
    if process.returncode == 0:
        print("audio script executed successfully")
        print(stdout.decode())  # 打印标准输出
        match = re.search(r"Similarity: (\d+\.\d{1,2})", stdout.decode())
        if match:
            similarity = float(match.group(1)) 
            print(similarity)
    else:
        print("Script execution failed")
        print(stderr.decode())
    
    result = False
    if similarity >= threshold:
        result = True
        
    # return stdout.decode(), stderr.decode(), process.returncode
    return result

