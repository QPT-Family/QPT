from qpt.executor import CreateExecutableModule
from qpt.modules.package import PaddlePaddlePackage

if __name__ == '__main__':
    # module = CreateExecutableModule(launcher_py_path="./paddle_program/run.py",
    #                                 work_dir="./paddle_program",
    #                                 save_path="./out",
    #                                 sub_modules=[PaddlePaddlePackage()])
    module = CreateExecutableModule(work_dir="./paddle_program",
                                    launcher_py_path="./paddle_program/run.py",
                                    save_path="./out", dependency_file=True)
    module.make()
