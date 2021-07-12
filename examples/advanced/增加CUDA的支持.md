# 增加CUDA模块 - 无需用户手动安装CUDA也可使用GPU加速

QPT相对于其它打包工具而言，技术方案更偏爱兼容深度学习领域，在使用深度学习工具包时难免会接触到CUDA等加速组件。  
不要担心，QPT可以轻松让你打包的程序具备无需安装也能使用的CUDA模块！

## 使用方法 - PaddlePaddle为例
### 前置条件
1. 【安装PaddlePaddle】当前Python环境下需要具备`paddlepaddle-gpu`这一Python库。
2. 【安装能用的CUDA】当前系统中安装了`paddlepaddle-gpu`所对应的CUDA组件。  
   例如你安装了`paddlepaddle-gpu.post110`，而在PaddlePaddle官网中可以查询到其支持CUDA11.0的深度学习包。   
   因此在你的操作系统中需要安装CUDA11.0以及对应的CUDNN，以保障`paddlepaddle-gpu`可以运行。
3. 【一切照旧】按正常步骤来打包吧~，但需要注意的是，在确定Requirements文件时可以检查`paddlepaddle-gpu`版本号是否正确，同时屏幕上也会提示`搜索到PaddlePaddle-GPU版本信息：2.1.1，所需CUDA版本：10.2"`的字样
请务必核对版本号是否符合预期。