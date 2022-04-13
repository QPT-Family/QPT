# QPT - Quick packaging tool 快捷封装工具
[![Downloads](https://static.pepy.tech/personalized-badge/qpt?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Pypi%20User)](https://pepy.tech/project/qpt)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/GT-ZhangAcer/QPT?include_prereleases)
![GitHub forks](https://img.shields.io/github/forks/GT-ZhangAcer/QPT)
![GitHub Repo stars](https://img.shields.io/github/stars/GT-ZhangAcer/QPT)
![GitHub](https://img.shields.io/github/license/GT-ZhangAcer/QPT)
![](https://img.shields.io/badge/%E6%B7%B1%E5%BA%A6%E9%80%82%E9%85%8D-Win10_1607+-9cf)
[![QQGroup](https://img.shields.io/badge/QQ群-1128826410-9cf?logo=tencent-qq&logoColor=000&logoWidth=15)](https://jq.qq.com/?_wv=1027&k=49HB5ymm)


[国产Gitee](https://gitee.com/GT-zhangacer/QPT) | [GitHub主页](https://github.com/GT-ZhangAcer/QPT) | [快速使用](https://github.com/QPT-Family/QPT#%E5%BF%AB%E9%80%9F%E4%BD%BF%E7%94%A8) | [进阶教程](https://github.com/QPT-Family/QPT#%E8%BF%9B%E9%98%B6%E4%BD%BF%E7%94%A8qpt) | [社区&捐赠支持](https://github.com/QPT-Family/QPT#%E8%BF%9B%E9%98%B6%E4%BD%BF%E7%94%A8qpt) | [开发进度 GitHub Project](https://github.com/orgs/QPT-Family/projects/3/views/3?layout=board)

QPT是一款可以“模拟”开发环境的多功能封装工具，最短只需一行命令即可将普通的Python脚本打包成EXE可执行程序，并选择性添加CUDA和NoAVX的支持，尽可能兼容更多的用户环境。 

<sup>如果对您有帮助，欢迎来点个⭐Star吧</sup>

### 版本说明
#### EAP - The Early Access Program  [更新日志](RELEASE.MD) | [开发进度](https://github.com/orgs/QPT-Family/projects/3/views/3?layout=board)    

`当前版本为V1.0b3尝鲜版本，仅具备基本功能，而且可能会有未测试出的Bug，建议在指导下投入生产环境。`  

`当前仅深度适配Windows10、Windows11系统环境，如您的系统环境为盗版Win7且核心组件被篡改，那么将不能保证QPT可以在Win7上正常运行。`  

* QPT的便利
  ```
  【可定制兼容方案】在打包形如PaddlePaddle深度学习Python库时也可流畅打包，通过自定义SubModule来让QPT来捕捉你的习惯。  
  【解释/命令双模式】不喜欢用命令打包也木有问题，Python语句照样可以轻松打包。  
  【轻松引入CUDA库】还担心用户不会安装CUDA吗？放心，这些QPT在打包时也考虑到了，无需用户安装也能用起CUDA。  
  【兼容大部分NoAVX平台】没有AVX慢是慢了点，但10年前的台式机就没有机会体验来自深度学习的乐趣吗？  
  【简单实用的Debug组件】QPT提供了几个实用的Debug工具以及日志系统，用户使用出现问题也可更快追踪异常情况。  
  【简约不简单的EXE】支持三种打包方式：秒安装、首次安装、在线安装三种方式，对应了三种：普通、较小、Mini三种打包体积，未来还将支持1M+大小的在线部署模块。
  ```  
* QPT的缺陷  
  ```
  【环境模拟】由于是“模拟”开发环境，所以相较传统打包对项目的规范程度有一定要求，越规范的项目越不容易踩坑，但也提升了使用成本。  
  【依赖处理】QPT只会打包源码中出现的Python包，但如果该包的依赖部分书写不规范（当然，大部分Python包是规范的）则可能会出现依赖缺失的问题。若您没有Requirements文件，那么在QPT自动生成Requirements.txt文件后需要您确认依赖是否完备，否则可能会有依赖漏掉的情况。  
  【踩坑继承】您搭建项目时所踩下的坑，QPT在模拟时可能并不会自动打包进去，极端情况下仍需要您手动撰写SubModule来保证用户可以正常使用。 
  ``` 

> *以上均以PaddlePaddle为基准，其他深度学习框架在测试版本中可能需要手动添加Module。

## 快速使用
### 安装/更新QPT到当前环境
#### 安装
* 通用方式：`python -m pip install qpt`  
* 国内推荐：`python -m pip install qpt -i https://mirrors.bfsu.edu.cn/pypi/web/simple`
#### 更新 - 强烈建议先卸载后安装
* Step1 卸载：`python -m pip uninstall qpt`  
* Step2 安装：`python -m pip install qpt`
### 开始打包

#### 方式一、撰写打包脚本[推荐]
* 撰写以下代码即可完成打包：  

  ```python
  # 导入QPT
  from qpt.executor import CreateExecutableModule as CEM

  #                                                        -----关于路径的部分，强烈建议使用绝对路径避免出现问题-----
  module = CEM(work_dir="./sample_program",                # [项目文件夹]待打包的目录，并且该目录下需要有↓下方提到的py文件
               launcher_py_path="./sample_program/run.py", # [主程序文件]用户启动EXE文件后，QPT要执行的py文件
               save_path="./out")                          # [输出目录]打包后相关文件的输出目录
             # requirements_file="auto"                    # [Python依赖]此处可填入依赖文件路径，也可设置为auto自动搜索依赖
             # hidden_terminal=False                       # [终端窗口]设置为True后，运行时将不会展示黑色终端窗口  
             # interpreter_module=Python37()               # [跨版本编译]需要预先from qpt.modules.python_env import Python37
                                                           # 好奇什么时候需要跨版本编译？可参考下方"进阶使用QPT"一节的《打包兼容性更强的Python解释器》
             # icon="your_ico.ico"                         # [自定义图标文件]支持将exe文件设置为ico/JPG/PNG等格式的自定义图标
  # 开始打包
  module.make()
  ```
#### 方式二、使用命令打包[快捷]
注意：使用命令打包的前提是当前**默认Python环境**中使用pip安装了`qpt`，否则可能存在形如`qpt不是内部或外部命令,也不是可运行的程序`的报错信息。此外，若需要自动搜索依赖，强烈建议将QPT安装在开发环境，并且在开发环境中执行QPT，因为QPT会在搜索文件的import和pip list进行比对来确保搜索结果精确。  

* 打开cmd/终端并输入以下命令即可完成打包：  
  ```pwsh
  chcp 65001
  qpt.exe -f ./sample_program -p ./sample_program/run.py -s ./out -h False
  ``` 
  > `chcp 65001` 命令可使得终端转为utf-8形式，避免出现编码问题

* 完整命令列表可使用`qpt --help`获取：
  ```python
  Options:
    -f, --folder TEXT     [项目文件夹]待打包的文件夹路径，该目录也应当为整个项目的根目录或工作目录，否则可能会导致出现找不到模块等P
                          ython基础报错。  [required]
    -p, --py TEXT         [主程序文件]待打包的主要Py脚本文件所在的路径，例如要yyy/xxx.py中xxx.py是需要打包的主要P
                          ython文件，那么该处填写xxx.py即可。  [required]
    -s, --save TEXT       [输出目录]打包后文件保存的路径。  [required]
    -r, --require TEXT    [Python依赖]自动检测软件包依赖，填写auto后将会自动查找待打包的文件夹路径中所有py文件的impo
                          rt使用情况，最终生成requirements文件
                          当然，也可传入requirements.txt文件路径，这样即可指定依赖列表进行安装。
    -h, --hidden BOOLEAN  [终端窗口]是否隐藏全部终端窗口，若输入true或判定为真则隐藏全部Terminal窗口（适用于使用了PyQ
                          T、TK等桌面级可视化程序），输入false或判定为否则不隐藏（适用于Console & 终端程序）。
    -i, --icon TEXT       [自定义图标文件]传入自定义图标文件路径，为EXE设置属于你的图标样式，支持将exe文件设置为ico/JPG/PNG等格式的自定义图标。
    --help                Show this message and exit.
  ```

## 进阶使用QPT/FAQ
- [x] [1. 更改QPT全局镜像源](examples/advanced/更换镜像源.md)
- [x] [2. 隐藏运行时的终端窗口](examples/advanced/隐藏控制台窗口.md)
- [x] [3. 能够更快定位用户问题的日志系统](examples/advanced/收集用于Debug的用户日志.md)
- [x] [4. 增加CUDA加速模块](examples/advanced/增加CUDA的支持.md)
- [x] [5. 打包兼容性更强的Python解释器](examples/advanced/打包兼容性更强的Python解释器.md)
- [x] [6. 使用 SubModule 添加自定义 whl](examples/advanced/使用SubModule添加自定义whl.md)
- [ ] [7. 打包PaddleOCR、PaddleX等业务程序](https://aistudio.baidu.com/aistudio/projectdetail/3571518)

完整进阶使用文档详见[examples/advanced](examples/advanced)

## 高阶开发手册/项目贡献指南
预计V1.0RC版本发布
## 设计思想  


### 发版安排 - 随时可能咕咕咕

`!!!本项目并不是大团队维护的项目，没有组织，没有纪律，如有特殊需求可考虑PR代码，维护者并不会按照计划外的意愿进行维护，随时可能咕咕咕，故入坑需谨慎!!!。`

- [x] 2021.6上旬    QPT V1.0 Alpha版本发布 - 确定初始架构，保证可以凑合用   
- [x] 2021.8       QPT V1.0 Beta版本发布 - 调整架构，完善兼容性   
- [ ] 2021.10       QPT V1.0 RC版本发布 - 增加更多基础功能  
- [ ] 2021.12       QPT V1.0 正式发布 - 完事了，开始正常发版  

其他说明
1. QPT会在用户第一次运行时会有环境兼容性适配步骤，与其他打包工具相比会显得耗时，但随后的运行速度可接近原生开发环境。
2. 已知Pyin\*在打包时默认打包命令在打包PaddlePaddle时会有较大可能性打包失败，需要用户额外添加相关动态链接库并屏蔽部分Python包方可运行。
3. 除QPT外，更推荐Nuit\*来打包深度学习相关库，性能好且打包难度较低。
4. NoAVX支持非常重要，当前仍有大量桌面级用户使用NoAVX平台。

## 社区相关
### 这些项目也在用
以下为内测初期QPT提供支持的开源项目，在此非常感谢这些作者与测试组用户为QPT提供的宝贵建议以及多次的调试与沟通，这也是QPT走向成熟的关键，同时也要感谢各位大佬~~在面对Bug时的不杀之恩。~~   
1. 交互式语义分割标注软件 - [PaddleCV-SIG/iann](https://github.com/PaddleCV-SIG/iann)
2. 景观健康效益辅助评估工具 - [JiehangXie/Landscape-Heath-Score](https://github.com/JiehangXie/Landscape-Heath-Score)
3. 团子翻译器-OCR部分 - [PantsuDango/Dango-Translator](https://github.com/PantsuDango/Dango-Translator)

### 社区支持

#### 来一杯咖啡☕
一杯咖啡提神醒脑，代码更新会更快更好！捐赠部分资金将用于社区维护，如您参与项目日常开发，也将会获得相关社区激励。    
（不介意的话可以在捐赠时加个备注，例如QPT项目+昵称，后续将更新至[捐赠致谢](https://github.com/QPT-Family/.github/blob/%E5%BC%80%E5%8F%91%E5%88%86%E6%94%AF/%E6%8D%90%E8%B5%A0%E8%87%B4%E8%B0%A2.MD)中）  

| 捐赠者 | 累计捐赠金额 | 赞助席位 |
| --- | --- | --- |
| <a href="https://cloud.stariver.org"><img width="100" src="https://user-images.githubusercontent.com/46156734/156889607-ad230ff1-47bf-416a-b7b7-7f4067dcf99a.png"> </a> | 5,000 .00 RMB | 金牌赞助席位 |
| 社区ID 23\*\*\*\*770 | 200 .00 RMB | 银牌赞助席位 |
| 社区ID iterhui | 50 .00 RMB | 支持赞助席位 |
| 社区ID \*猪 | 20 .00 RMB | 支持赞助席位 |
| 社区ID super松 | 20 .00 RMB | 支持赞助席位 |
| 社区ID 14\*\*\*\*650 | 10 .00 RMB | 支持赞助席位 |
| 社区ID 未知 | 1 .00 RMB | 兴趣赞助席位 |

完整捐赠名单&规则详见[捐赠致谢.MD](https://github.com/QPT-Family/.github/blob/%E5%BC%80%E5%8F%91%E5%88%86%E6%94%AF/%E6%8D%90%E8%B5%A0%E8%87%B4%E8%B0%A2.MD)

<div align=center><img width="490" alt="图片" src="https://cdn.jsdelivr.net/gh/GT-ZhangAcer/GT-ZhangAcer/d.jpg"></div>  

#### Jetbrains 全家桶支持
本项目开发所使用的IDE由[Jetbrains](https://jb.gg/OpenSource)支持。
<div align=center><img alt="https://jb.gg/OpenSource" src="ext/img/jetbrains.png" width="80" /></div>

### 开源协议
本项目使用GNU LESSER GENERAL PUBLIC LICENSE(LGPL)开源协议。  
#### Other情况
1. 形如使用QPT简单打包了自己的“强化学习小游戏”等操作，该情况无需申请QPT授权以及更换个人代码仓库完整的开源协议。   
2. 若对QPT源代码进行了修改，尽管这些代码非恶意代码，但为了保证开发者和使用者权益和安全，在未取得QPT授权的情况下需要开源完整的源代码等LGPL协议中所要求的内容。
