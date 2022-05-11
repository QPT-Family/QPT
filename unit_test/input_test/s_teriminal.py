# Author: Acer Zhang
# Datetime: 2022/5/11 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import subprocess

t = subprocess.Popen(
    args=['python "/Users/zhanghongji/Library/Application Support/JetBrains/PyCharmCE2021.2/scratches/tmp.py"'],
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    stdin=subprocess.PIPE)

while True:
    line = t.stdout.readline().decode('utf-8', errors="ignore")
    if line:
        if "---QPT COMPATIBLE_INPUT_START_FLAG---" in line:
            path, pro = line.replace(
                "---QPT COMPATIBLE_INPUT_START_FLAG---", "").replace(
                "---QPT COMPATIBLE_INPUT_END_FLAG---", "").split("---QPT COMPATIBLE_INPUT_SPLIT_FLAG---")
            print("path", path, pro)
            raw = input(pro)
            f = open(path, "wb")
            f.write(raw.encode("utf-8"))
            f.flush()
            f.close()
        print(line)
    else:
        break
