import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np

bk_img = cv2.imread("./web/static/certificates/空.jpg")
shape = bk_img.shape
print(shape)
cv2.imshow("test", bk_img)
cv2.waitKey()
# 设置需要显示的字体
fontpath = "./web/font/方正字体.ttf"
font = ImageFont.truetype(fontpath, 15)
img_pil = Image.fromarray(bk_img)
draw = ImageDraw.Draw(img_pil)
# 绘制文字信息
text = u"""艾琳 小姐姐"""
draw.multiline_text((80, 120), text, font=font, fill="black")

font = ImageFont.truetype(fontpath, 16)
text = "人美心善气质佳 "
draw.multiline_text((shape[1] / 2 - 16 * len(text) / 2, 150), text, font=font, fill="black")

font = ImageFont.truetype(fontpath, 32)
text = "一等奖"
print(len(text))
print(shape[1] / 2 - 32 * len(text) / 2)
draw.multiline_text((shape[1] / 2 - 32 * len(text) / 2, 200), text, font=font, fill="black")

bk_img = np.array(img_pil)

cv2.imshow("add_text", bk_img)
cv2.waitKey()
cv2.imwrite("add_text.jpg", bk_img)


# from PIL import Image, ImageDraw, ImageFont
# import textwrap
#
# astr = u'''艾琳小姐姐
# 人美心善气质佳
# 一等奖
# '''
# #这个设置文字个数
# para = textwrap.wrap(astr, width=15)
#
# MAX_W, MAX_H = 200, 200
# im = Image.new('RGB', (MAX_W, MAX_H), (0, 0, 0, 0))
# draw = ImageDraw.Draw(im)
# font = ImageFont.truetype(
#     'FZHTJW.TTF', 18)
#
# current_h, pad = 50, 10
# for line in para:
#     w, h = draw.textsize(line, font=font)
#     draw.text(((MAX_W - w)/2, current_h), line, font=font)
#     current_h += h + pad
#
# im.save('test.png')
