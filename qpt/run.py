import sys

sys.path.append("./Python/Lib/site-packages")

from qpt.executor import RunExecutableModule

# out\Python\Lib\site-packages\qpt
# module = RunExecutableModule("./../../../../")
module = RunExecutableModule("./")
module.run()
