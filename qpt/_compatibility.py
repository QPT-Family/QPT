os = "windows"

windows_configs = dict()

# 相对解释器路径的包安装路径，使用时通常与解释器路径拼接
windows_configs["RELATIVE_INTERPRETER_SITE_PACKAGES_PATH"] = "lib/site-packages"

com_configs = None
if os == "windows":
    com_configs = windows_configs

