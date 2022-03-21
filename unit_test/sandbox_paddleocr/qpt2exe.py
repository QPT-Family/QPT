from qpt.executor import CreateExecutableModule

module = CreateExecutableModule(work_dir="./",
                                launcher_py_path="./run.py",
                                save_path="./../out",
                                requirements_file="./requirements_with_opt.txt")
module.make()
