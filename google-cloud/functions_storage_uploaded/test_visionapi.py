# pip install google-cloud-vision
# pip install pillow

from PIL import Image, ImageDraw

# Imports the Google Cloud client library
from google.cloud import vision


def view_results(path, objects):
    # 画像表示
    im = Image.open(path)
    (im_w, im_h) = im.size
    draw = ImageDraw.Draw(im)

    for object_ in objects:
        poly_xy = []
        for vertex in object_.bounding_poly.normalized_vertices:
            poly_xy.append((vertex.x * im_w, vertex.y * im_h))

        # 対象物の周辺に多角形を描画
        draw.polygon(poly_xy, outline=(255, 0, 0))
        text_x = poly_xy[0][0] + (im_w * 0.05)
        text_y = poly_xy[0][1] - (im_h * 0.03)
        # ラベル付与
        draw.text((text_x, text_y), object_.name, fill=(255, 0, 0))
    # 画像保存
    save_path = "result.png"
    im.save(save_path)


# Instantiates a client
client = vision.ImageAnnotatorClient()

# The URI of the image file to annotate
file_name = "./test_baby.png"

# Loads the image into memory
with open(file_name, "rb") as image_file:
    content = image_file.read()

image = vision.Image(content=content)
objects = client.object_localization(image=image).localized_object_annotations

# 辞書型に整形
localize_object_di = {}
for object_ in objects:
    vertex_li = []
    for vertex in object_.bounding_poly.normalized_vertices:
        vertex_li.append({"x": vertex.x, "y": vertex.y})
    localize_object_di[object_.name] = {"score": object_.score, "vertex": vertex_li}

print(objects)
view_results(file_name, objects)

# Performs label detection on the image file
# response = client.label_detection(image=image)
# labels = response.label_annotations

# print(labels)
# for label in labels:
#     print(label.description)
