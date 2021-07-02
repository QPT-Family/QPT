# 细节性ToDO
- [x] 只留exe在文件夹外面
- [ ] 打包前对路径做判断，避免出现.和空格路径，运行时检测导入模块是否从相对路径导入，需要设置为相对路径保证导入的安全性|测试带有空格和.以及中文的路径情况，即使不是相对路径
- [ ] 加入PaddleHub、PaddleNLP、PaddleOCR深度适配方案，保证用户在使用中文用户名时可以读取参数
- [ ] 增加对AVX的支持

## 高优优先级
- [ ] 窗口化
- [ ] 取消PyQT依赖
- [ ] 增加图标支持
- [ ] 增加CUDA支持
- [ ] 增加非AVX的支持
## 一般优先级
- [ ] 重写依赖搜索
- [ ] 杀进程
- [ ] 控制台程序
- [ ] 要不要加个环境变量PYTHONPATH
- [ ] 图标问题可参考
- [ ] .Net在低版本的Win平台需要先请求保证4.0Net"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\NET Framework Setup\NDP
