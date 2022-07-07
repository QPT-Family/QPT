from qpt.executor import CreateExecutableModule

module = CreateExecutableModule(work_dir="./",
                                launcher_py_path="./main.py",
                                save_path="./../out")
module.make()
