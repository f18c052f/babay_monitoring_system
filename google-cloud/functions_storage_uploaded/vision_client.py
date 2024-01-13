import io
from google.cloud import vision
from PIL import Image, ImageDraw, ImageFont


class Vision:
    def __init__(self, image_data: bytes):
        self.client = vision.ImageAnnotatorClient()
        self.image = vision.Image(content=image_data)

    def get_detection_labels(self):
        response = self.client.label_detection(image=self.image)
        return response.label_annotations

    def isBabyExist(self, labels) -> bool:
        flag = False
        for label in labels:
            if label.description == "Baby":
                flag = True
        return flag

    def draw_detect_text(self, image_data: bytes):
        text = "### Baby is detected ###"
        position = (10, 10)

        font = ImageFont.truetype("./MPLUS1p-Light.ttf", size=40)

        image = Image.open(io.BytesIO(image_data))
        draw = ImageDraw.Draw(image)
        draw.text(position, text, font=font, fill="white")
        image.save("test_result.png")

        img_bytes = io.BytesIO()
        return img_bytes.getvalue()
