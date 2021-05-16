import base64, uuid
from django.core.files.base import ContentFile

def get_report_image(data):
    _, str_img = data.split(';base64')
    decoded_img = base64.b64decode(str_img)
    img_name = str(uuid.uuid4())[:10] + '.png'
    return ContentFile(decoded_img, name=img_name)
