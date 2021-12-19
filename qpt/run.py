import os
import sys


from qpt.memory import QPT_MEMORY

IGNORE_ENV_FIELD = ["conda", "Conda", "Python", "python"]
interpreter_dir = os.path.dirname(sys.executable)
sys_p = sys.path
# ToDo 用户运行时可能sys.path还是旧的
new_sys_p = list()
for sp in sys_p:
    for field in IGNORE_ENV_FIELD:
        if field in sp and interpreter_dir not in sp:
            break
    else:
        new_sys_p.append(sp)

sys.path = new_sys_p
ROOT_PATH = os.path.abspath("./")
os.environ.update(QPT_MEMORY.get_env_vars(ROOT_PATH))
from qpt.executor import RunExecutableModule

module = RunExecutableModule("./")
module.run()
