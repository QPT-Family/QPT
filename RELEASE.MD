# Release 更新日志

## V1.0a8 - 2021.6.30
### 重要更新
1. 在打包时增加“是否隐藏终端”的接口，若待打包的程序为PyQT、WxPython等含有可视化界面的程序，在不需要控制台/终端界面时可配置该接口进行隐藏。  
   当然，若本身为控制台/终端界面的程序，这个隐藏就会很令人抓狂，QPT默认该接口为“不隐藏”。[使用文档](https://github.com/GT-ZhangAcer/QPT/blob/main/examples/advanced/%E9%9A%90%E8%97%8F%E6%8E%A7%E5%88%B6%E5%8F%B0%E7%AA%97%E5%8F%A3.md)
2. Kernel中增加copytree忽略文件级别的功能，后续将在开发自定义OP时暴露该接口。
3. 修改了CIL部分的文案，同时增加hidden_terminal的指令。
4. 增加WPF、MFC的进度条
### Fix Bug
1. 修复了打包时传入的源文件路径与保存路径一致但没有报错的情况，当前若打包时两目录为同一目录则会raise一个报错信息，提示用户需要更改路径而不是强制覆盖文件。
2. 修复不同盘符打包可能出现的问题。

### 不兼容更新
1. 进度条部分可能会从PyQT（约150M）更换为TK（25M 需要编译）、CRL+WPF（10M 难度较大）、Win32+MFC（0M 资料较少）三种方案中任一种，在选择hidden_terminal接口为False后将会取消所有依赖
2. 原none_gui接口更名为hidden_terminal，增加了可读性。

### 下个版本ToDO
1. 增加自定义图标接口
2. 增加CUDA支持
4. 取消PyQT作为必须依赖（可能需要重写自动化依赖搜索脚本）
5. 更新README

Tips：在未来两个版本中，仍不会出现V1.0RC版本，待大量测试验证后发布1.0RC
