# QPT - Quick packaging tool 快捷封装工具
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/GT-ZhangAcer/QPT?include_prereleases)
![GitHub forks](https://img.shields.io/github/forks/GT-ZhangAcer/QPT)
![GitHub Repo stars](https://img.shields.io/github/stars/GT-ZhangAcer/QPT)
[![Downloads](https://static.pepy.tech/personalized-badge/qpt?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Pypi%20User)](https://pepy.tech/project/qpt)
![GitHub](https://img.shields.io/github/license/GT-ZhangAcer/QPT)
[![Build](https://github.com/GT-ZhangAcer/QPT/actions/workflows/python-publish.yml/badge.svg)](https://github.com/GT-ZhangAcer/QPT/actions/workflows/python-publish.yml)
[![QQGroup](https://img.shields.io/badge/QQ_Group-1128826410-52B6EF?style=social&logo=tencent-qq&logoColor=000&logoWidth=20)](https://jq.qq.com/?_wv=1027&k=49HB5ymm)

[GitHub主页](https://github.com/GT-ZhangAcer/QPT) | [Gitee主页](https://gitee.com/GT-zhangacer/QPT)

QPT是一款可以“模拟”开发环境的多功能封装工具，一行命令即可将普通的Python脚本打包成EXE可执行程序，与此同时还可轻松引入CUDA等深度学习加速库，
尽可能在用户使用时复现您的开发环境。  

## 版本更新
### 更新日志
当前版本为V1.0a9版本，接下来的版本将会更换为V1.0Beta1。[更新日志](RELEASE.MD)

### EAP - The Early Access Program
EAP邀测版本：当前版本为尝鲜版本，仅具备基本功能和Win10兼容，而且可能会有未测试出的Bug  
> 使用时如发现问题，强烈建议加QQ群1128826410与我们进行交流，当然也可联系QQ：ZhangAcer进行解决[感谢] 

## 相关案例
以下为内测QPT提供支持的开源项目，在此非常感谢这些作者为QPT提供的宝贵建议以及多次的调试与沟通，这也是QPT走向成熟的关键，同时也要感谢各位大佬~~在面对Bug时的不杀之恩。~~  
1. 交互式语义分割标注软件 - [PaddleCV-SIG/iann](https://github.com/PaddleCV-SIG/iann)
2. 景观健康效益辅助评估工具 - [JiehangXie/Landscape-Heath-Score](https://github.com/JiehangXie/Landscape-Heath-Score)

## 快速使用
### 安装/更新QPT到当前环境
#### 安装
通用方式：`python -m pip install qpt`  
国内推荐：`python -m pip install qpt -i https://pypi.tuna.tsinghua.edu.cn/simple`
#### 更新 - 强烈建议先卸载后安装
Step1 卸载`python -m pip uninstall qpt`  
Step2 安装`python -m pip install qpt`
#### 开始打包

##### 方式一、撰写打包脚本[推荐]
首先介绍一下示例项目的目录结构，文件名不可使用__main__等Python关键字，除此之外可随意命名。  
其中`sample_program`就是待打包的**项目文件夹**，里面的`run.py`就是用户点击EXE文件后需要执行的**主程序文件**，
`sample.jpg`这个“配角”就简单充当一下项目中需要的静态文件好了。  
在`sample_sandbox`目录下新建一个名为`create_sample_module.py`的py文件。
```
------------
|-sample_sandbox
   |-sample_program
      |-run.py
      |-sample.jpg
   |-create_sample_module.py
```
撰写以下代码即可完成打包：  
```python
# 导入QPT
from qpt.executor import CreateExecutableModule

if __name__ == '__main__':
    # 实例化Module - 关于路径的部分建议使用绝对路径
    module = CreateExecutableModule(work_dir="./sample_program",                # [项目文件夹]待打包的目录，并且该目录下需要有↓下方提到的py文件
                                    launcher_py_path="./sample_program/run.py", # [主程序文件]用户启动EXE文件后，QPT要执行的py文件
                                    save_path="./out")                          # [输出目录]打包后相关文件的输出目录
                                  # requirements_file="auto"                    # [依赖]此处可填入依赖文件路径，也可设置为auto自动搜索依赖
                                  # hidden_terminal=False                       # [终端窗口]设置为True后，运行时将不会展示黑色终端窗口    
    # 开始打包
    module.make()
```
##### 方式二、使用命令打包[快捷]
注意：使用命令打包的前提是当前**默认Python环境**中使用pip安装了`qpt`，否则可能存在形如`qpt不是内部或外部命令,也不是可运行的程序`的报错信息。此外，若需要自动搜索依赖，强烈建议将QPT安装在开发环境，并且在开发环境中执行QPT，因为QPT会在搜索文件的import和pip list进行比对来确保搜索结果精确。  

打开cmd/终端并输入以下命令即可完成打包：  
`qpt -f ./sample_program -p ./sample_program/run.py -s ./out -h False`  

完整命令列表可使用`qpt --help`获取：
```bash
Options:
  -f, --folder TEXT     待打包的文件夹路径，该目录也应当为整个项目的根目录或工作目录，否则可能会导致出现找不到模块等Python基础
                        报错。  [required]
  -p, --py TEXT         待打包的主要Py脚本文件所在的路径，例如要yyy/xxx.py中xxx.py是需要打包的主要Python文件
                        ，那么该处填写xxx.py即可。  [required]
  -s, --save TEXT       打包后文件保存的路径。  [required]
  -r, --require TEXT    自动检测软件包依赖，填写auto后将会自动查找待打包的文件夹路径中所有py文件的import使用情况，最终生
                        成requirements文件
                        当然，也可传入requirements.txt文件路径，这样即可指定依赖列表进行安装。
  -h, --hidden BOOLEAN  是否隐藏全部终端窗口，若输入true或判定为真则隐藏全部Terminal窗口（适用于使用了PyQT、TK等桌
                        面级可视化程序），输入false或判定为否则不隐藏（适用于Console & 终端程序）。
  --help                Show this message and exit.
```

## 进阶使用QPT
- [x] [1. 更改QPT全局镜像源](examples/advanced/更换镜像源.md)
- [x] [2. 隐藏运行时的终端窗口](examples/advanced/隐藏控制台窗口.md)
- [x] [3. 能够更快定位用户问题的日志系统](examples/advanced/收集用于Debug的用户日志.md)
- [x] [4. 添加无需用户手动安装的CUDA加速模块](examples/advanced/增加CUDA的支持.md)

完整进阶使用文档详见[examples/advanced](examples/advanced)
## 高阶开发手册
还没写
## 设计思想  
仍在编

## ToDO - 计划安排

### 功能支持安排
- [x] 环境在线、离线部署能力 - 封装后包含基本的Python解释器并具备环境部署能力
- [ ] CUDA环境支持 - 提供GPU版本的部署能力支持 - 预计V1.0 Beta版本加入
- [ ] 支持EXE文件自定义图标
- [ ] 支持封装为单个EXE文件
- [ ] QPT拓展名支持
- [ ] 超轻量级在线环境部署能力 - 环境部分完全在线部署，可轻松控制在1M文件大小
- [ ] QPT图形化封装界面
- [ ] 自定义封装算子 - 提供自定义封装OP支持
- [ ] Module集市
- [ ] 模型加密
- [ ] 增加32位操作系统支持

### 发版安排
2021.6上旬    QPT V1.0 Alpha版本发布  
2021.7       QPT V1.0 Release Candidate(RC)版本发布  
2021.8       QPT V1.0 正式版发布  

## 开源协议
本项目使用GNU LESSER GENERAL PUBLIC LICENSE(LGPL)开源协议。  
### Example：
1. 使用QPT简单打包了自己的“强化学习小游戏”，该情况无需申请QPT授权以及更换个人代码仓库完整的开源协议。   
2. 对QPT源代码进行了修改，尽管这些代码非恶意代码，但为了保证开发者和使用者权益和安全，在未取得QPT授权的情况下需要开源完整的源代码等LGPL协议中所要求的内容。
