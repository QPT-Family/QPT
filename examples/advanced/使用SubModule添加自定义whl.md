# 进阶使用 - 使用 SubModule 添加自定义 whl

如果有些包需要构建环境，或者种种原因并不存在于公开源中，但是你已经有一份 whl/gz/zip，那么可以通过 SubModule 来将其添加进来。  

## 示例

```Python
from qpt.executor import CreateExecutableModule as CEM
from qpt.modules.package import CopyWhl2Packages


module = CEM(
    work_dir="./",
    launcher_py_path="./eiseg/exe.py",
    save_path="./dist",
    requirements_file="./requirements.txt",
    sub_modules=[
        CopyWhl2Packages('/path/to/some/whl/xxx.whl')  # 修改这一行
    ]
)

module.make()
```

## 附注

在`qpt.modules.package`里还有很多 SubModule，目前尚无文档，但可读其中注释，随后将继续更新。
