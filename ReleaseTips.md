# 发版贴士

## 版本号
### 版本命名
正式版直接`x.y`数字命名，概念版为`x.ya`，测试版为`x.yb`，预览版`x.yrc`，开发版在后缀中增加.dev+数字。  
必要时需要做pre-release。
### 版本写入
在`qpt.version`下写入最新版本号
## 第三方Check
### PaddlePaddle
#### 1.NoAVX
据说可能会修订地址，需要额外关注该情况，在预修改时通知全体开发者。
#### 2.CUDA适配
1. 每次PaddlePaddle发版后需要第一时间确定默认版本号的CUDA版本，避免`modules.paddle_family.PaddlePaddlePackage`中发生异常
2。 CUDA目前只搜索到9-12+0-4版本，请注意最新CUDA驱动适配情况