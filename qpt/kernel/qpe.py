# Author: Acer Zhang
# Datetime:2021/8/29 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os

from qpt.kernel.qos import get_qpt_tmp_path


def make_icon(ico_path, pe_path, save_path=None, img_save_path=None):
    if img_save_path:
        img_save_path = os.path.join(get_qpt_tmp_path("icon"), "make_icon.ico")

    if save_path is None:
        save_path = pe_path

    # Todo 后期加warmup
    import pefile
    import PIL.Image as Image
    # 处理图像
    img = Image.open(ico_path).resize((128, 128))
    img.save(img_save_path, sizes=[(128, 128)])

    # 读取图像
    assert os.path.exists(img_save_path), f"{os.path.abspath(img_save_path)}图像文件不存在，请检查路径拼写是否正确！"
    with open(img_save_path, "rb") as f:
        img_b = f.read()

    # PE
    pe = pefile.PE(pe_path)
    # offset 可从ExeScope中获取
    rva = pe.get_rva_from_offset(0x1D6E8)
    pe.set_bytes_at_rva(rva, img_b[22:])
    f = pe.write()
    with open(save_path, 'wb') as final_f:
        final_f.write(f)


if __name__ == '__main__':
    test1 = r'M:\ICON\i.ico'
    pe_test = r"M:\ICON\o2.exe"
    save_1 = r"M:\ICON\new1.exe"
    make_icon(test1, pe_test, save_path=save_1)
