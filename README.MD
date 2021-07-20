# QPT - Quick packaging tool 快捷封装工具
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/GT-ZhangAcer/QPT?include_prereleases)
![GitHub forks](https://img.shields.io/github/forks/GT-ZhangAcer/QPT)
![GitHub Repo stars](https://img.shields.io/github/stars/GT-ZhangAcer/QPT)
[![Downloads](https://static.pepy.tech/personalized-badge/qpt?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Pypi%20User)](https://pepy.tech/project/qpt)
![GitHub](https://img.shields.io/github/license/GT-ZhangAcer/QPT)
[![Build](https://github.com/GT-ZhangAcer/QPT/actions/workflows/python-publish.yml/badge.svg)](https://github.com/GT-ZhangAcer/QPT/actions/workflows/python-publish.yml)
![](https://img.shields.io/badge/%E6%B7%B1%E5%BA%A6%E9%80%82%E9%85%8D-Win7+-9cf)
[![QQGroup](https://img.shields.io/badge/QQ群-1128826410-52B6EF?logo=tencent-qq&logoColor=000&logoWidth=15)](https://jq.qq.com/?_wv=1027&k=49HB5ymm)

[GitHub主页](https://github.com/GT-ZhangAcer/QPT) | [Gitee主页](https://gitee.com/GT-zhangacer/QPT)

QPT是一款可以“模拟”开发环境的多功能封装工具，最短只需一行命令即可将普通的Python脚本打包成EXE可执行程序，并选择性添加CUDA和NoAVX的支持，尽可能兼容更多用户环境。    
当然，由于QPT设计思想与其他打包工具有着较大差异，极力推荐您在使用时简略了解设计思想来更好使用QPT。 

> 感觉还可以的话，求求了，点个Star吧

用QPT打包EXE的优势
1. 可定制兼容方案，在打包形如PaddlePaddle深度学习Python库时也可流畅打包。
2. 支持命令式打包，同时也支持通过Python语句打包。
3. 轻松引入CUDA库，用户使用时无需显式安装CUDA也可获得GPU加速能力。
4. 兼容大部分NoAVX平台，10年前的台式机也有机会体验来自深度学习的乐趣。
5. 提供大量Debug工具以及日志系统，使用出现问题也可更快追踪异常情况。
6. 打包后体积较小，未来还将支持30M+大小的在线部署方案。

## 相关案例
以下为内测QPT提供支持的开源项目，在此非常感谢这些作者为QPT提供的宝贵建议以及多次的调试与沟通，这也是QPT走向成熟的关键，同时也要感谢各位大佬~~在面对Bug时的不杀之恩。~~  
1. 交互式语义分割标注软件 - [PaddleCV-SIG/iann](https://github.com/PaddleCV-SIG/iann)
2. 景观健康效益辅助评估工具 - [JiehangXie/Landscape-Heath-Score](https://github.com/JiehangXie/Landscape-Heath-Score)
3. 团子翻译器-OCR部分 - [PantsuDango/Dango-Translator](https://github.com/PantsuDango/Dango-Translator)

## 版本更新
### 更新日志
当前版本为V1.0a9版本，接下来的版本将会更换为V1.0Beta1。[更新日志](RELEASE.MD)

### EAP - The Early Access Program
EAP邀测：当前版本为尝鲜版本，仅具备基本功能，而且可能会有未测试出的Bug，建议在指导下投入生产环境。  
> 使用时如发现问题，强烈建议加QQ群1128826410与我们进行交流，当然也可联系QQ：ZhangAcer进行解决[感谢] 


## 快速使用
### 安装/更新QPT到当前环境
#### 安装
通用方式：`python -m pip install qpt`  
国内推荐：`python -m pip install qpt -i https://pypi.tuna.tsinghua.edu.cn/simple`
#### 更新 - 强烈建议先卸载后安装
Step1 卸载：`python -m pip uninstall qpt`  
Step2 安装：`python -m pip install qpt`
### 开始打包

#### 方式一、撰写打包脚本[推荐]
撰写以下代码即可完成打包：  
```python
# 导入QPT
from qpt.executor import CreateExecutableModule

# 实例化Module - 关于路径的部分建议使用绝对路径
module = CreateExecutableModule(work_dir="./sample_program",                # [项目文件夹]待打包的目录，并且该目录下需要有↓下方提到的py文件
                                launcher_py_path="./sample_program/run.py", # [主程序文件]用户启动EXE文件后，QPT要执行的py文件
                                save_path="./out")                          # [输出目录]打包后相关文件的输出目录
                              # requirements_file="auto"                    # [依赖]此处可填入依赖文件路径，也可设置为auto自动搜索依赖
                              # hidden_terminal=False                       # [终端窗口]设置为True后，运行时将不会展示黑色终端窗口    
# 开始打包
module.make()
```
#### 方式二、使用命令打包[快捷]
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
- [x] [4. 增加CUDA加速模块](examples/advanced/增加CUDA的支持.md)

完整进阶使用文档详见[examples/advanced](examples/advanced)
## 高阶开发手册
预计V1.0RC版本发布
## 设计思想  


### 发版安排 - 随时可能咕咕咕
- [x] 2021.6上旬    QPT V1.0 Alpha版本发布  
- [ ] 2021.7       QPT V1.0 Release Candidate(RC)版本发布  
- [ ] 2021.8       QPT V1.0 正式版发布  

## 与其他打包工具对比
基准为对PaddlePaddle2.1.0版本的CPU与GPU版本以及其相关依赖进行打包，以下为与其他打包工具的对比情况。（\*为省略了部分软件包名）
| 工具名称 | 打包方案 | 离线部署体积CPU/GPU |  在线部署 |是否支持CUDA加速 | 是否对NoAVX兼容 | 运行速度 | 加密 |
|  ----  | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: |
| QPT  | 前向式模拟   | 100M+/1.2GB+ | 30M+ | 支持打包CUDA | 兼容 | 快速 | 在做了 |
| Pyin*  | 反向推理 | 高于QPT | 不支持 | 需用户安装 | 不支持 | 一般 | Pyd |
| CxFr*  | 反向推理 | 暂未测试 | 不支持 | 需用户安装 | 不支持 | 一般 | Pyd |
| Nuit*  | 源码编译 | 暂未测试 | 不支持 | 需用户安装 | 不支持 | 快速 | 编译加密 |

其他说明
1. QPT会在用户第一次运行时会有环境兼容性适配步骤，与其他打包工具相比会显得耗时，但随后的运行速度可接近原生开发环境。
2. 已知Pyin\*在打包时默认打包命令在打包PaddlePaddle时会有较大可能性打包失败，需要用户额外添加相关动态链接库并屏蔽部分Python包方可运行。
3. 除QPT外，更推荐Nuit\*来打包深度学习相关库，性能好且打包难度较低。
4. NoAVX支持非常重要，当前仍有大量桌面级用户使用NoAVX平台。


## 开源协议
本项目使用GNU LESSER GENERAL PUBLIC LICENSE(LGPL)开源协议。  
### Example：
1. 使用QPT简单打包了自己的“强化学习小游戏”，该情况无需申请QPT授权以及更换个人代码仓库完整的开源协议。   
2. 对QPT源代码进行了修改，尽管这些代码非恶意代码，但为了保证开发者和使用者权益和安全，在未取得QPT授权的情况下需要开源完整的源代码等LGPL协议中所要求的内容。
