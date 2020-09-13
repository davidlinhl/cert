import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import os
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import time
import json
import img2pdf


class Index(tornado.web.RequestHandler):
    content_range = {
        "荣誉证书.jpg": [100, 100, 400, 250],
        "聘书.jpg": [80, 110, 430, 280],
        "竖版.jpg": [150, 100, 340, 300],
        "空.jpg": [80, 130, 430, 260],
    }

    def get(self):
        fonts = os.listdir("./font")
        fonts = [n.rstrip(".TTF").rstrip(".ttf").rstrip(".ttc").rstrip(".TTC") for n in fonts]
        certs = os.listdir("./static/certificates")
        certs = [os.path.join("certificates", n) for n in certs]
        self.render("main.html", fonts=fonts, certs=certs)

    def post(self):
        img_path = "./static/certificates"
        time_str = time.time()
        img_paths = []
        for img_name in os.listdir(img_path):
            bk_img = cv2.imread(os.path.join(img_path, img_name))
            height, width, channel = bk_img.shape

            # 读取图片
            img_pil = Image.fromarray(bk_img)
            draw = ImageDraw.Draw(img_pil)

            # 名字
            ll = self.content_range[img_name][:2]
            font_path = "./font/{}.ttf".format(self.get_argument("name-font", "方正字体"))
            name_font_size = int(self.get_argument("name-font-size"))
            print(name_font_size)
            print(font_path)
            font = ImageFont.truetype(font_path, name_font_size)
            name = self.get_argument("name-text", "请输入名字")
            draw.multiline_text((ll[0], ll[1]), name, font=font, fill="black")

            # 内容
            font_path = "./font/{}.ttf".format(self.get_argument("content-font", "方正字体"))
            font = ImageFont.truetype(font_path, int(self.get_argument("content-font-size")))
            text = self.get_argument("content-text", "请输入内容")
            draw.multiline_text((ll[0], ll[1] + 2 * name_font_size), text, font=font, fill="black")

            # 等级
            font_path = "./font/{}.ttf".format(self.get_argument("grade-font", "方正字体"))
            font = ImageFont.truetype(font_path, int(self.get_argument("grade-font-size")))
            text = self.get_argument("grade-content", "请输入内容")
            draw.multiline_text(
                (width / 2 - 32 * len(text) / 2, 200), text, font=font, fill="black"
            )  # TODO: 这里需要知道内容多少个像素

            file_path = "./static/temp/{}-{}-{}".format(time_str, name, img_name)
            cv2.imwrite(file_path, np.array(img_pil))
            img_paths.append(file_path)
        self.write(json.dumps({"status": "ok", "img_paths": img_paths}))


class Pdf(tornado.web.RequestHandler):
    def get(self):
        img_path = self.get_argument("path")
        print(img_path)
        pdf_path = img_path.replace("jpg", "pdf")
        with open(pdf_path, "wb") as f:
            f.write(img2pdf.convert(img_path))
        names = pdf_path.split("/")[-1].split("-")
        name = ""
        for n in names[1:]:
            name += n + "-"
        name = name.rstrip("-")
        self.write(json.dumps({"status": "ok", "path": pdf_path.lstrip("."), "name": name}))


define("port", default=8000, help="run on the given port", type=int)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", Index),
            (r"/pdf", Pdf),
        ],  # 主页
        template_path=os.path.join(
            os.path.dirname(__file__),
            "templates",
        ),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
