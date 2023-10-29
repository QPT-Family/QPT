# QPT - Python程序模块化封装工具（Py转EXE）
[![Downloads](https://static.pepy.tech/personalized-badge/qpt?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Pypi%20User)](https://pepy.tech/project/qpt)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/GT-ZhangAcer/QPT?include_prereleases)
![GitHub forks](https://img.shields.io/github/forks/GT-ZhangAcer/QPT)
![GitHub Repo stars](https://img.shields.io/github/stars/GT-ZhangAcer/QPT)
![GitHub](https://img.shields.io/github/license/GT-ZhangAcer/QPT)
![](https://img.shields.io/badge/%E6%B7%B1%E5%BA%A6%E9%80%82%E9%85%8D-Win10_1806+-9cf)
[![QQGroup](https://img.shields.io/badge/QQ群-1128826410-9cf?logo=tencent-qq&logoColor=000&logoWidth=15)](https://jq.qq.com/?_wv=1027&k=49HB5ymm)
![](https://img.shields.io/badge/%E5%8F%91%E8%B5%B7%E4%BA%BA-GTZhangAcer-9cf)

<p align="center">
 <img src="https://cdn.jsdelivr.net/gh/QPT-Family/QPT/ext/rc/2023.png" width="128" />

[国产Gitee](https://gitee.com/GT-zhangacer/QPT) | [GitHub主页](https://github.com/GT-ZhangAcer/QPT) | [快速使用](https://github.com/QPT-Family/QPT#%E5%BF%AB%E9%80%9F%E4%BD%BF%E7%94%A8) | [进阶教程](https://github.com/QPT-Family/QPT#%E8%BF%9B%E9%98%B6%E4%BD%BF%E7%94%A8qpt) | [社区&捐赠支持](https://github.com/QPT-Family/QPT#%E7%A4%BE%E5%8C%BA%E6%94%AF%E6%8C%81) | [开发进度 GitHub Project](https://github.com/orgs/QPT-Family/projects/3/views/3?layout=board) | [踩坑笔记](https://github.com/QPT-Family/QPT/tree/开发分支/informal_essay)
<p align="center">



# 项目不定期更新
> ~~因工作原因、个人健康状态，再加上硬盘坏了导致拓展Python环境的源码完全丢失（未开源是因为体积太大），项目恢复更新成本过高，故无法进行更新。~~    
> 换工作了，有时间了，可更！

QPT是一款致力于让**开源项目**更好通往互联网世界的Python项目打包工具，以此期望更多计算机用户能够分享开源的乐趣与价值。  
在设计之初，我们发现较多深度学习开源项目仅能够在专业开发者手中运行，想要让普通人参与其中并非易事（CUDA支持、MKL、NoAVX支持等），故在灵活性和易用性上做出额外设计，使其更利于高阶开发者定制封装策略，也能够满足入门开发者基础封装需要。

**QPT并非一天建成，涉及编译、性能的项目通常需要长时间建设，考虑到当前建设进度，建议使用时在指导下投入生产环境，以此避免被老板暴打hhh~**

<sup>如果对您有帮助，欢迎来点个⭐Star吧</sup>

### 版本说明
#### EAP - The Early Access Program  [更新日志](https://github.com/QPT-Family/QPT/releases) | [开发进度](https://github.com/orgs/QPT-Family/projects/3/views/3?layout=board)    

当前版本为V1.0b5，该版本已放弃对Python3.7及更低版本支持，同时我们仍仅支持Windows10 1806+的适配（不支持MAC和Linux纯粹是维护不过来，不支持低版本Windows是因为真的太难）

`如在Win7中不能运行，可考虑在cmd中输入sfc/scannow修复系统进行解决，Win7+系统在输入前需添加DISM/Online/Cleanup-Image/RestoreHealth 或许还能有抢救的机会`

* 使用QPT的优势
  ```
  【打包逻辑自由】默认打包不及预期，可通过自定义SubModule来让QPT来捕捉你的封装需求。 可参考 [进阶教程](https://github.com/QPT-Family/QPT#%E8%BF%9B%E9%98%B6%E4%BD%BF%E7%94%A8qpt)
  【图形化/代码/命令打包】图形化界面是最易于使用的方式，同时支持代码控制打包逻辑，以及属于一行命令进行打包。（图形化打包方式正在建设中，预计V1.0a版本发布）  
  【源码形态自由】默认打包后源码可见，也可编译为pyd以保护源码内容。（源码可见也意味着可以使用git来帮助用户更新你的源代码）
  【内置CUDA打包逻辑】深度学习项目有福了。（AMD的ROCm如果支持Windows，可及时通知我来加入适配）  
  【Debug与日志】提供几个实用的Debug工具以及日志系统，方便用户使用出现问题时更快追踪异常情况。  
  【EXE的体积/速度可定制】支持三种打包方式：秒安装、首次安装、在线安装三种方式，对应了三种：普通、较小、Mini三种打包体积，未来还将支持1M+大小的在线部署模块。
  ```  
* QPT的缺陷  
  ```
  【环境模拟】由于是“模拟”开发环境，所以相较传统打包对项目的规范程度有一定要求，越规范的项目越不容易出问题。（在努力想办法增加容错率了，在努力了，在努力了，打包中弹出的提示信息一定要多看几眼，每个字符都是血汗啊）  
  【依赖处理】QPT只会打包源码中出现的Python包，但如果该包的依赖部分书写不规范（当然，大部分Python包是规范的）则可能会出现依赖缺失的问题。若您没有Requirements文件，那么在QPT自动生成Requirements.txt文件后需要您确认依赖是否完备，否则可能会有依赖漏掉的情况。  
  【踩坑继承】您搭建项目时所踩下的坑，QPT在模拟时可能并不会自动打包进去，极端情况下仍需要您手动撰写SubModule来保证用户可以正常使用。 
  【仍在测试】当前版本并非正式版，所以会有坑，放心吧。
  【兼容性】仅兼容Windows10 1806+，低版本Windows只能碰运气，Linux和MAC的适配还没新建文件夹。
  ``` 

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
- [x] [7. 打包PaddleOCR、PaddleX等业务程序](https://aistudio.baidu.com/aistudio/projectdetail/3571518)
- [x] [8. PaddleOCR和QPT的落地实战 via:@ITerydh](https://github.com/ITerydh/OCRandQPTandIS)

完整进阶使用文档详见[examples/advanced](examples/advanced)

## 高阶开发手册/项目贡献指南
预计V1.0RC版本发布
## 设计思想  
还没来得及写，和Pyinstaller、Nutika、Czfreeze等打包工具思路不太一样。（他们几个的思路本来也不太一样哈哈哈）

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
| 上海大学 曾老师 | 200 .00 RMB | 银牌赞助席位 |赞助席位 |
| [Viggo(wxbool)](https://github.com/wxbool) | 100 .00 RMB | 银牌赞助席位
| [YaoFANGUK](https://github.com/YaoFANGUK) | 100 .00 RMB | 银牌赞助席位
| 社区ID \*头 | 66 .00 RMB | 支持赞助席位 |
| 社区ID iterhui | 50 .00 RMB | 支持赞助席位 |
| 社区ID LFeightyFour | 23 .33 RMB | 支持赞助席位 |
| 社区ID \*猪 | 20 .00 RMB | 支持赞助席位 |
| 社区ID super松 | 20 .00 RMB | 支持赞助席位 |
| 社区ID \*\*辉 | 20 .00 RMB | 支持赞助席位 |
| 社区ID jerrychoices | 20 .00 RMB | 支持赞助席位 |
| 社区ID 14\*\*\*\*650 | 10 .00 RMB | 支持赞助席位 |
| 社区ID yangy996 | 10 .00 RMB | 支持赞助席位 |
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
