# Author: Acer Zhang
# Datetime:2021/7/3 
# Copyright belongs to the author.
# Please indicate the source for reprinting.


from qpt.executor import RunExecutableModule

if __name__ == '__main__':
    module = RunExecutableModule("./unit_out/paddle-cpu/Release")
    module.run()
