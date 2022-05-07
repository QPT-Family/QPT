# Author: Acer Zhang
# Datetime:2021/6/26 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from paddleocr import PaddleOCR

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
img_path = './1.jpg'
result = ocr.ocr(img_path, cls=True)
for line in result:
    print(line)
