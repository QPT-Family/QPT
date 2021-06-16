# QPT - Quick packaging tool 快捷封装工具
![GitHub forks](https://img.shields.io/github/forks/GT-ZhangAcer/QPT)
![GitHub Repo stars](https://img.shields.io/github/stars/GT-ZhangAcer/QPT)
[![Downloads](https://static.pepy.tech/personalized-badge/qpt?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Pypi%20User)](https://pepy.tech/project/qpt)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/GT-ZhangAcer/QPT?include_prereleases)
![GitHub](https://img.shields.io/github/license/GT-ZhangAcer/QPT)
[![Upload Python Package](https://github.com/GT-ZhangAcer/QPT/actions/workflows/python-publish.yml/badge.svg)](https://github.com/GT-ZhangAcer/QPT/actions/workflows/python-publish.yml)
> EAP: 当前版本为尝鲜版本，仅具备基本功能，该项目将长期维护  
> Alpha发布前待解决问题：1. .Net运行库兼容性 2. 增加控制台脚本选择开关 3. 添加GPU支持

QPT是一款可以“模拟”开发环境的多功能封装工具，一行命令即可将普通的Python脚本打包成EXE可执行程序，与此同时还可轻松引入CUDA等深度学习加速库，
尽可能在用户使用时复现您的开发环境。  
  

## 相关案例
> 刚刚开始，案例较少 先凑合一下吧~

## 快速使用QPT
#### 安装QPT到当前环境
> Warning!当前版本暂未发版，预计6月15日之前完成最终封装测试
> 不好意思，再次咕咕咕，尽量本周发版！  

`pip install qpt -i https://pypi.tuna.tsinghua.edu.cn/simple`    
或  
`pip install qpt`  

#### 目录结构
首先介绍一下示例项目的目录结构，其中`sample_program`就是待打包的**项目文件夹**，里面的`run.py`就是用户点击EXE文件后需要执行的**主程序文件**，
`sample.jpg`这个“配角”就简单充当一下项目中需要的静态文件好了。  

```
------------
|-sample_sandbox
   |-sample_program
      |-run.py
      |-sample.jpg
```

#### 开始打包

##### [推荐]方式一、撰写打包脚本
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
    # 实例化Module
    module = CreateExecutableModule(work_dir="./sample_program",                # [项目文件夹]待打包的目录，并且该目录下需要有↓下方提到的py文件
                                    launcher_py_path="./sample_program/run.py", # [主程序文件]用户启动EXE文件后，QPT要执行的py文件
                                    save_path="./out")                          # [输出目录]打包后相关文件的输出目录
    # 开始打包
    module.make()
```
#### [快捷]方式二、使用命令打包
注意：使用命令打包的前提是当前**默认Python环境**中使用pip安装了`qpt`，否则可能存在形如`qpt不是内部或外部命令,也不是可运行的程序`的报错信息。  

打开cmd/终端并输入以下命令即可完成打包：  
`qpt -f ./sample_program -p ./sample_program/run.py -s ./out`  

完整命令列表可使用`qpt --help`获取：
```bash
Options:
  -f, --folder TEXT   待打包的文件夹路径，该目录也应当为整个项目的根目录或工作目录，否则可能会导致出现找不到模块等Python基础报错
                      。  [必须]
  -p, --py TEXT       待打包的主要Py脚本文件所在的路径，例如要yyy/xxx.py中xxx.py是需要打包的主要Python文件，那
                      么该处填写xxx.py即可。  [必须]
  -s, --save TEXT     打包后文件保存的路径。  [必须]
  -r, --require TEXT  自动检测软件包依赖，默认/填写auto后将会自动查找待打包的文件夹路径中所有py文件的import使用情况，最终生成r
                      equirements文件。当然，也可传入requirements.txt文件路径，这样即可指定依赖列表进行安装。
  --help              查看帮助.
```

## 进阶使用QPT
太多了，捋一捋
## 高阶文档手册
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
2021.6       QPT V1.0 Release Candidate(RC)版本发布  
2021.7       QPT V1.0 正式版发布  

## 开源协议
本项目使用GNU LESSER GENERAL PUBLIC LICENSE(LGPL)开源协议。  
### Example：
1. 小张使用QPT简单打包了自己的“强化学习小游戏”，该情况无需申请QPT授权以及更换个人代码仓库完整的开源协议。   
2. 小王QPT源代码进行了修改，尽管这些代码非恶意代码，但为了保证开发者和使用者权益和安全，在未取得QPT授权的情况下需要开源完整的源代码等LGPL协议中所要求的内容。
