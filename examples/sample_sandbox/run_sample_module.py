import os
from qpt.executor import RunExecutableModule

if __name__ == '__main__':
    module = RunExecutableModule("./out/Debug")
    module.run()
