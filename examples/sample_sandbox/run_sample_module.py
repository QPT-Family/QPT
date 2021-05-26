from qpt.executor import RunExecutableModule

ROOT_PATH = r"./"
if __name__ == '__main__':
    module = RunExecutableModule(ROOT_PATH + "out")
    module.run()
