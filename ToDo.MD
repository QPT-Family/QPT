## b2 ToDO
- [x] 用户表示会有QPT找不到模块的情况，初步判断可能是环境变量的问题
- [ ] 支持Conda版本的CUDA
- [x] 重写依赖搜索 - Requirements里加QPT 过滤掉的包除去依赖后加入上去
- [x] 修改依赖的文案
- [ ] 使用TK进度条
- [x] 高兼容版本编译入口
- [x] 增加37、39编译方案
- [ ] 增加CUDA选择
- [x] 提升路径判断机制，避免在特殊路径下解压
- [x] 统一输出函数为Logging
- [ ] 文件夹重复问题还是没解决 - 以后统一迁移吧顺便支持个中文路径
- [ ] BS多次安装
- [x] 统一终端环境为UTF-8而非GBK
- [x] 增加跨应用调用支持
- [ ] 增加自定义图标
## 下版本ToDo
- [ ] 增加图标支持 SFX+Configs+Win32Copy
- [ ] 增加个多入口支持
- [ ] 试一下重新编译360还会不会误报
- [ ] 增加DML支持
- [ ] 关键部分增加Callback
- [ ] 增加多程序入口
- [ ] 修一下日志系统在GUI模式
- [ ] 开发整体工具包迁移至smart_opt
- [ ] sys_info更改为sys_swap并增加warmup和mem
- [ ] Debug状态文件删除，借助环境变量统一在sys_info注册
- [ ] 增加进程锁
- [ ] 加个网络链接测试，增加链接池
- [ ] 增加可选编译安装
- [ ] 给用户UA选择权
## Other
- [ ] 增加跨应用CLI
- [ ] Pyd支持
- [ ] 增加防修改部分 - 增加安装状态文件+状态文件增加GUID+哈希校验
- [ ] 增加跨平台需求
- [ ] Requirements类缺乏前瞻性考虑，或增加互斥Module概念
- [ ] 要不要杀进程 - PID互斥锁
- [ ] 增加MKL深度适配（或许直接加环境变量？） https://blog.csdn.net/qq_35133971/article/details/100101397
- [ ] EXE、txt、cmd加入QPT元素
- [ ] QPT拓展名支持
- [ ] 超轻量级在线环境部署能力 - 环境部分完全在线部署，可轻松控制在1M文件大小
- [ ] QPT图形化封装界面
- [ ] 自定义封装算子 - 提供自定义封装OP支持
- [ ] Module集市
- [ ] 模型加密
- [ ] 增加32位操作系统支持
- [ ] 用户测PIP增加测速，避开国内源无法在国外使用

git config --global --unset url.https://hub.fastgit.org/.insteadof
git config --global url."https://hub.fastgit.org/".insteadOf "https://github.com/"

    NVIDIA Kepler (GTX 600 series) and above
    AMD GCN 1st Gen (Radeon HD 7000 series) and above
    Intel Haswell (4th-gen core) HD Integrated Graphics and above

