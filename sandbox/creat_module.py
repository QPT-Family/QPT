import os
from qpt.executor import CreateExecutableModule

ROOT_PATH = r"D:/Python_Projects/QPT/sandbox/"
if __name__ == '__main__':
    module = CreateExecutableModule(launcher_py_path=os.path.join(ROOT_PATH, "sample_program/run.py"),
                                    work_dir=os.path.join(ROOT_PATH, "sample_program"),
                                    save_path=os.path.join(ROOT_PATH, "out"))
    module.make()
