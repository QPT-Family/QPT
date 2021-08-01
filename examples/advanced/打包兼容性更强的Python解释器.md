# 打包兼容性更强的Python解释器 - 跨Python版本编译

由于QPT采用的是前项式模拟方式进行打包，若您想要打包一个兼容性更强的软件包，那么跨Python版本编译则尤为重要。

## 兼容性

举例当前已知的Python版本在Windows版本上的兼容情况如下：

| Python版本 | WinXP | Win7 | Win8 | Win8.1 | Win10 | Win11 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| 3.4 | √ | √ | √ | √ | √ | - |
| 3.5 | X | √ | √ | √ | √ | - |
| 3.6 | X | √ | √ | √ | √ | - |
| 3.7 | X | √ | √ | √ | √ | - |
| 3.8 | X | √ | X | - | √ | - |
| 3.9 | X | X | X | - | √ | - |
| 3.10 | X | X | X | - | √ | - |

## QPT推荐的版本

由于当前（2021.8.2）WinXP以及Win8.0用户市场占有量极低，而Win7、Win10操作系统则为主力。  
为了最大的操作系统兼容性，QPT推荐您在打包时使用Python3.7（照顾部分Win8.1用户）或使用Python3.8（相较于3.7引入了较多新特性）。

> QPT默认在找不到镜像时采用Python3.8进行打包，也推荐使用该版本进行打包。

## 如何指定解释器版本进行打包

### 方案一、在对应解释器版本下使用QPT

由于QPT会预先判断当前解释器版本号，以当前解释器版本号来下载Python解释器镜像。  
举例：GT想让用户在Python3.7环境下运行他的程序，那么打包时需要将QPT安装在Python3.7的环境中，并且在该环境下执行QPT的打包工作。

### 方案二、跨Python版本编译

在使用代码打包时，可通过以下方式引入其它Python解释器镜像来达到跨Python版本编译目的。  
举例：GT的电脑只有Python3.10，但GT想打包一个Python3.7版本的软件包，那么他需要插入以下代码

```python
from qpt.executor import CreateExecutableModule as CEM

# 此处导入Python37镜像
from qpt.modules.python_env import Python37

if __name__ == '__main__':
    module = CEM(work_dir="./sample_program",
                 launcher_py_path="./sample_program/run.py",
                 save_path="./out",
                 # 下方指定Python镜像
                 interpreter_module=Python37())
    module.make()
```
这样GT就在Python3.10的解释器环境下打包出支持Python3.7的软件包，但仍需要注意的是：
1. 需考虑待打包的代码是否兼容该Python版本。
2. 该Python版本是否可以在目标用户操作系统上执行。