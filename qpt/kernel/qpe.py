# Author: Acer Zhang
# Datetime:2021/8/29 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os

import qpt
from qpt.kernel.qos import get_qpt_tmp_path

QPT_SFX_ICON_SIZE = 128


def make_icon(ico_path, pe_path, save_path=None, img_save_path=None):
    if not img_save_path:
        img_save_path = os.path.join(get_qpt_tmp_path("icon"), "make_icon.ico")

    if save_path is None:
        save_path = pe_path

    import PIL.Image as Image
    # 处理图像
    img = Image.open(ico_path).resize((QPT_SFX_ICON_SIZE, QPT_SFX_ICON_SIZE))
    img.save(img_save_path, sizes=[(QPT_SFX_ICON_SIZE, QPT_SFX_ICON_SIZE)])

    # 读取图像
    assert os.path.exists(img_save_path), f"{os.path.abspath(img_save_path)}图像文件不存在，请检查路径拼写是否正确！"
    with open(img_save_path, "rb") as f:
        img_b = f.read()

    # 这也使得只能在QPT项目中用，不是很方便，等后面完全模块化了，一起重构
    with open(os.path.join(os.path.dirname(qpt.__file__), "ext/ico/Logo.ico"), "rb") as f:
        img_mask = f.read()

    with open(pe_path, "rb") as f:
        pe_data = f.read()
        offset = pe_data.index(img_mask[22:])

    from pefile import PE

    pe = PE(pe_path)

    rva = pe.get_rva_from_offset(offset)
    pe.set_bytes_at_rva(rva, img_b[22:])
    final = pe.write()
    with open(save_path, 'wb') as final_f:
        final_f.write(final)


if __name__ == '__main__':
    test1 = r'D:\QPTProgram\QPT\unit_test\sandbox_paddleocr\favicon.ico'
    pe_test = r"D:\QPTProgram\QPT\QPTSFX\Release\QPTSFX.exe"
    save_1 = r"J:\QPT_UT_OUT_CACHE\new.exe"
    make_icon(test1, pe_test, save_path=save_1)
