## 当前ToDO
- [x] 打包路径判断Bug
- [ ] 增加CUDA支持 cuda_home = os.environ.get('CUDA_HOME') or os.environ.get('CUDA_PATH')
- [ ] 修一下这该死的日志系统吧
- [ ] 问一下360为什么报毒，我可不想交保护费啊啊啊
- [x] Release判断有问题，而且点取消还会继续
- [x] 修复非avx的链接错误
- [ ] 找一下为什么Conda会报dll的问题，尽管这些不会影响到运行（可能是真得加环境变量？）
## 高优优先级
- [ ] 增加图标支持
- [ ] 增加TK支持
- [ ] 终端调试工具

## 一般优先级
- [ ] 重写依赖搜索
- [ ] 杀进程
- [ ] 控制台程序
- [ ] 要不要加个环境变量PYTHONPATH
- [ ] 图标问题可参考
- [ ] .Net在低版本的Win平台需要先请求保证4.0Net"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\NET Framework Setup\NDP
- [ ] 增加MKL深度适配 https://blog.csdn.net/qq_35133971/article/details/100101397
