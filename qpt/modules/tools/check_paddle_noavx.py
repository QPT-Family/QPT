# Author: Acer Zhang
# Datetime:2021/7/7 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import traceback
from qpt.kernel.qos import Logging

SUPPORT_AVX = None
try:
    from paddle.fluid.core_avx import *
    SUPPORT_AVX = True
except Exception as e:
    Logging.warning(str(e))
    info = traceback.format_exc()
    if "cv2" in info:
        # ToDo 实际上还是不能确定，但Paddle这块不知道为什么要这样测cv2是否存在
        SUPPORT_AVX = True
    else:
        SUPPORT_AVX = False
