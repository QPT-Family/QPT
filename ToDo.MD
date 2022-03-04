## b1.dev5 ToDO
- [x] 用户表示会有QPT找不到模块的情况，初步判断可能是环境变量的问题
- [x] 重写依赖搜索 - Requirements里加QPT 过滤掉的包除去依赖后加入上去
- [x] 修改依赖的文案
- [x] 高兼容版本编译入口
- [x] 增加37、39编译方案
- [x] 提升路径判断机制，避免在特殊路径下解压
- [x] 统一输出函数为Logging
- [x] 统一终端环境为UTF-8而非GBK
- [x] 增加跨应用调用支持
- [x] 增加自定义图标
- [x] Python部分解压到临时目录
## b1.dev6ToDo
- [x] 使用TK进度条，完全取消PyQT5依赖
- [x] 内部更换CMD为PowerShell（外部下个版本更新）
- [x] configs文件保存为二进制，360实在太笨了，文件里加base64就算是病毒也是服了，误报率不算KPI这是？
- [x] 【实验性】解决多进程输出卡死
- [x] Conda中打包可能存在~情况 https://github.com/QPT-Family/QPT/issues/22
- [x] multiprocessing无限循环情况 https://github.com/QPT-Family/QPT/issues/23
- [x] UA统一使用cmd开启
- 
## b2.dev3
- [x] 增强pwsh兼容性
- [ ] 支持Conda版本的CUDA
- [ ] 增加CUDA选择
- [ ] 简单加密
- [ ] 文件夹重复问题还是没解决 - 以后统一迁移吧顺便支持个中文路径
- [ ] BS多次安装以及为什么wget还需要安装
- [ ] 增加PaddleOCR部署的文档/依赖列表的适配

## 下版本可能的ToDo
- [ ] 增加多程序入口
- [ ] 开发整体工具包迁移至smart_opt
- [x] sys_info更改为sys_swap并增加warmup和mem
- [ ] Debug状态文件删除，借助环境变量统一在sys_info注册
- [ ] 增加进程锁
- [ ] 加个网络链接测试，增加链接池
- [ ] 增加可选编译安装
- [ ] 给用户UA选择权
- [ ] 重构Module管理器，增加互斥Module - 初步考虑按主键+name去判定是否互斥
## Other
- [ ] 增加跨应用CLI的文档
- [ ] Pyd支持
- [ ] 增加防修改部分 - 增加安装状态文件+状态文件增加GUID+哈希校验
- [ ] 增加跨平台需求
- [ ] Requirements类缺乏前瞻性考虑，或增加互斥Module概念
- [ ] 要不要杀进程 - PID互斥锁
- [ ] EXE、txt、cmd加入QPT元素
- [ ] QPT拓展名支持
- [ ] 超轻量级在线环境部署能力 - 环境部分完全在线部署，可轻松控制在1M文件大小
- [ ] QPT图形化封装界面
- [ ] 自定义封装算子 - 提供自定义封装OP支持
- [ ] Module集市
- [ ] 分区加密

- [ ] 用户测PIP增加测速，避开国内源无法在国外使用

## 二次验证优先级
- [ ] 增加MKL深度适配（或许直接加环境变量？） https://blog.csdn.net/qq_35133971/article/details/100101397
- [ ] 增加32位操作系统支持
- [ ] 看一下egg格式的包搜索问题

git config --global --unset url.https://hub.fastgit.org/.insteadof
git config --global url."https://hub.fastgit.org/".insteadOf "https://github.com/"

    NVIDIA Kepler (GTX 600 series) and above
    AMD GCN 1st Gen (Radeon HD 7000 series) and above
    Intel Haswell (4th-gen core) HD Integrated Graphics and above

Start-Process powershell -Verb runAs -NoNewWindow
