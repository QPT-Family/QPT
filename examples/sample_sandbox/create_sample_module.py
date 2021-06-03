from qpt.executor import CreateExecutableModule

if __name__ == '__main__':
    module = CreateExecutableModule(work_dir="./sample_program",
                                    launcher_py_path="./sample_program/run.py",
                                    save_path="./out")
    module.make()
