import sys
import os

ROOT_PATH = os.path.abspath("./")
sys.path.append("./Python/Lib/site-packages")
sys.path.append("./Python/Lib/ext")
sys.path.append("./Python")
sys.path.append("./Python/Scripts")

from qpt.executor import RunExecutableModule

module = RunExecutableModule("./")
module.run()
