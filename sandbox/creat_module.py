from qpt.executor import CreateExecutableModule

if __name__ == '__main__':
    a = CreateExecutableModule(main_py_path=r"D:\Python_Projects\QPT\sandbox\sample_program\run.py",
                               workdir=r"D:\Python_Projects\QPT\sandbox\sample_program",
                               save_dir=r"D:\Python_Projects\QPT\sandbox\out")
    a.make()
