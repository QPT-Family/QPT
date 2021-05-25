from qpt.executor import RunExecutableModule

ROOT_PATH = r"D:/Python_Projects/QPT/sandbox/"
if __name__ == '__main__':
    module = RunExecutableModule(ROOT_PATH + "out")
    module.run()