# Author: Acer Zhang
# Datetime: 2022/5/11 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import subprocess

t = subprocess.Popen(
    args=['python tmp.py'],
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    stdin=subprocess.PIPE)

# 持续获取子进程输出
while True:
    line = t.stdout.readline().decode('utf-8', errors="ignore")
    if line:
        # 判断子进程是否发出input()信号
        if "---QPT COMPATIBLE_INPUT_START_FLAG---" in line:
            # 解析约定的写入路径与提示词
            path, pro = line.replace(
                "---QPT COMPATIBLE_INPUT_START_FLAG---", "").replace(
                "---QPT COMPATIBLE_INPUT_END_FLAG---", "").split("---QPT COMPATIBLE_INPUT_SPLIT_FLAG---")
            print("path", path, pro)
            # 在主进程中获取用户输入
            raw = input(pro)
            # 向约定的文件中写入
            with open(path, "wb") as f:
                f.write(raw.encode("utf-8"))
        print(line)
    else:
        break
