import img2pdf

with open("name.pdf", "wb") as f:
    f.write(img2pdf.convert("bk.jpg"))
