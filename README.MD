# QPT - Quick packaging tool Python快捷封装工具 Alpha
![GitHub forks](https://img.shields.io/github/forks/GT-ZhangAcer/QPT)
![GitHub Repo stars](https://img.shields.io/github/stars/GT-ZhangAcer/QPT)
[![Downloads](https://static.pepy.tech/personalized-badge/qpt?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Pypi%20User)](https://pepy.tech/project/qpt)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/GT-ZhangAcer/QPT?include_prereleases)
![GitHub](https://img.shields.io/github/license/GT-ZhangAcer/QPT)
[![Upload Python Package](https://github.com/GT-ZhangAcer/RIFLE_Module/actions/workflows/python-publish.yml/badge.svg)](https://github.com/GT-ZhangAcer/RIFLE_Module/actions/workflows/python-publish.yml)
> EAP: 当前版本为尝鲜版本，仅具备基本功能，该项目将长期维护

将Python打包为EXE文件虽然是一种很非主流的事情，但不可否认的是Cz_freeze、Pyinstaller等优秀的打包工具在这些看似极端的场景下也可以脱颖而出。
虽然这些打包工具在正常情况下可以满足开发者使用需求，但其封装逻辑决定了其在某种意义上是在复原打包时的开发环境，而QPT采用的策略是通过模拟配置开发环境来在用户使用时“复现”开发环境。  
例如使用Pyinstaller打包需要CUDA的Python程序时往往需要开发者手动去安置CUDA文件才在执行EXE文件时也能够使用上CUDA，但在QPT中这部分只需要添加1行甚至无需额外的代码配置即可在用户使用时自动安装CUDA相关依赖。    
听起来QPT很像是为深度学习准备的打包工具，实际上它可以完成大部分打包任务，而非仅深度学习。QPT作为一个快捷的封装工具，其目的是在打包后也能提供常规的开发环境来执行Python脚本，必要时也可提供简单的GUI来提高灵活性。

## 相关案例
> 刚刚开始，案例较少 先凑合一下吧~

## QPT环境配置
没看错，安装就是如此简单  
`pip install qpt -i https://pypi.tuna.tsinghua.edu.cn/simple`  
当然，在国外的话可以使用下方命令直接从Pypi镜像源中拉取QPT  
`pip install qpt` 

## 快速使用QPT
接下来将会以仓库中examples文件夹下的sample_sandbox为例，简简单单介绍一下常规使用方式。  
当然，高阶玩法同样会有文档，详情可见[文档手册](https://github.com/GT-ZhangAcer/QPT#%E6%96%87%E6%A1%A3%E6%89%8B%E5%86%8C) 一节。
### Step1 准备待打包的文件
#### 目录结构
首先介绍一下目录结构，假设`sample_program`就是你待打包的“程序文件夹”，里面的`run.py`就是用户点击EXE文件后需要执行的“主程序”，
`sample.jpg`就当作是程序运行时所需的其他文件就好。
接下来我们就要去打包`sample_program`啦~

```
------------
|-sample_sandbox
   |-sample_program
      |-run.py
      |-sample.jpg
```

### Step2 撰写打包脚本并进行打包
#### 创建create_sample_module.py
我们需要撰写一个py文件来操作打包，当然后续也会提供类似Cz_freeze、Pyinstaller的命令版本教程（在做了在做了）。  
比较推荐的是在`sample_program`同级别目录下构建一个py文件用于打包，当然也可以在`sample_program`目录下进行打包，虽然不妨碍打包进度，但这样也会将用于打包的py文件打包进去。  
```
------------
|-sample_sandbox
   |-sample_program
      |-run.py
      |-sample.jpg
   |-create_sample_module.py
```
#### 撰写打包脚本
```python
# 导入QPT
from qpt.executor import CreateExecutableModule

if __name__ == '__main__':
    # 实例化Module
    module = CreateExecutableModule(launcher_py_path="./sample_program/run.py", # 用户启动EXE文件后，QPT要执行的py文件
                                    work_dir="./sample_program",                # 待打包的目录，并且该目录下需要有↑上方提到的py文件
                                    save_path="./out")                          # 打包后相关文件的输出目录
    # 开始打包
    module.make()
```
关于CreateExecutable Module用法可见[文档手册](https://github.com/GT-ZhangAcer/QPT#%E6%96%87%E6%A1%A3%E6%89%8B%E5%86%8C)
### Step3 调试 - 测试在当前环境下是否可以正常执行/达到预期
```python
from qpt.executor import RunExecutableModule

if __name__ == '__main__':
    module = RunExecutableModule("./out")   # "./out"就是刚刚打包后相关文件的输出目录
    module.run()
```
常见Debug教程详见：还没写

### Step4 实测程序是否可以正常执行
此处晚上在写
## 文档手册
还没写
## 设计思想  
仍在编

## ToDO - 计划安排

### 功能支持安排
- [x] 环境离线部署能力 - 封装后包含基本的Python解释器并具备环境部署能力
- [ ] QPT拓展名支持
- [ ] CUDA环境支持 - 提供GPU版本的部署能力支持
- [ ] 支持封装为单个EXE文件
- [ ] 超轻量级在线环境部署能力 - 仅需提供Python文件即可封装，环境部分在线部署
- [ ] QPT图形化封装界面
- [ ] 自定义封装算子 - 提供自定义封装OP支持
- [ ] Module集市
- [ ] 模型加密

### 发版安排
还没整完

## 开源协议
本项目使用GNU LESSER GENERAL PUBLIC LICENSE(LGPL)开源协议。  
###补充内容：
1. 在“未修改QPT本体源码”且“仅使用QPT对个人软件进行打包”的情况时可认定该类项目是“借助了QPT的作品”，该情况下可像正常的自由软件一样使用，并且无需申请QPT授权以及更换个人代码仓库完整的开源协议。  
2. 相反，若对QPT本体进行了修改等操作会被认为该项目是QPT的“衍生品”，此时需要向本仓库进行申请许可并在QPT部分保留LGPL开源协议副本等LGPL开源协议中要求的内容。

###Example：
1. 小张使用QPT打包了自己的“强化学习小游戏”，仅仅使用了QPT代码，并未对QPT本体进行进行修改，那么小张可像正常的自由软件一样使用，并且无需申请QPT授权以及更换个人代码仓库完整的开源协议。   
2. 小王clone了QPT代码，并修改了"executor.py"文件且增加了少许代码进行发布。尽管这些代码非恶意代码，但为了保证开发者和使用者权益和安全，在未取得QPT授权的情况下需要开源完整的源代码等LGPL协议中所要求的内容。