## 当前ToDO
- [ ] 高兼容版本编译
- [ ] 增加图标支持
- [ ] 增加TK支持
- [ ] 加个CUDA版本选择
- [x] 临时目录改名
- [ ] 嵌入式版本-拜拜！
- [ ] BatchInstall想办法优化
- [ ] 检查一下完整包Python，是否能得到正确的Paddle版本
- [ ] 注册/反注册dll
- [ ] 增加跨平台需求
- [ ] 通过ctypes判定是否需要修漏洞
- [ ] 增加DML支持
- [ ] Debug状态文件删除，借助环境变量统一在sys_info注册
- [ ] SubModule对op文件加判断
- [ ] 有必要对Win32的dll做个注册了
## 高优优先级
- [ ] 增加图标支持
- [x] 增加TK支持
- [ ] Pyd支持
- [ ] 增加防修改部分 - 增加安装状态文件+状态文件增加GUID+哈希校验

## 一般优先级
- [ ] 重写依赖搜索
- [ ] Requirements类缺乏前瞻性考虑，或增加互斥Module概念
- [ ] requirements里加QPT
- [ ] 增加翻新脚本
- [ ] 杀进程
- [ ] 控制台程序
- [ ] 要不要加个环境变量PYTHONPATH
- [ ] 图标问题可参考
- [ ] .Net在低版本的Win平台需要先请求保证4.0Net"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\NET Framework Setup\NDP
- [ ] 增加MKL深度适配 https://blog.csdn.net/qq_35133971/article/details/100101397
- [ ] EXE、txt、cmd加入QPT元素

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

git config --global --unset url.https://hub.fastgit.org/.insteadof
git config --global url."https://hub.fastgit.org/".insteadOf "https://github.com/"


    NVIDIA Kepler (GTX 600 series) and above
    AMD GCN 1st Gen (Radeon HD 7000 series) and above
    Intel Haswell (4th-gen core) HD Integrated Graphics and above

