from qpt.executor import CreateExecutableModule

if __name__ == '__main__':
    module = CreateExecutableModule(launcher_py_path="./sample_program/run.py",
                                    work_dir="./sample_program",
                                    save_path="./out")
    module.make()
