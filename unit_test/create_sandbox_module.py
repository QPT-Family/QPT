from qpt.executor import CreateExecutableModule

if __name__ == '__main__':
    module = CreateExecutableModule(work_dir="./sandbox_m",
                                    launcher_py_path="./sandbox_m/run.py",
                                    save_path="./out",
                                    requirements_file="sandbox_m/requirements_with_opt.txt")
    module.make()
