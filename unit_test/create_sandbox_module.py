from qpt.executor import CreateExecutableModule

from qpt.kernel.tools.interpreter import set_default_pip_source

set_default_pip_source("https://mirror.baidu.com/pypi/simple")

M_MODULE = True
if __name__ == '__main__':
    if M_MODULE:
        module = CreateExecutableModule(work_dir="./sandbox_m",
                                        launcher_py_path="./sandbox_m/run.py",
                                        save_path="./out",
                                        requirements_file="sandbox_m/requirements_with_opt.txt",
                                        with_debug=True,
                                        hidden_terminal=False)
    else:
        module = CreateExecutableModule(work_dir="./sandbox",
                                        launcher_py_path="./sandbox/run.py",
                                        save_path="./out",
                                        with_debug=True,
                                        hidden_terminal=False)
    module.make()
