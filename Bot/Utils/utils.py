from PIL.ImageDraw import ImageDraw
from vk_api import VkUpload


def load_class(full_class_string: str):
    """
    dynamically load a class from a string
    """
    from importlib import import_module
    class_data = full_class_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = import_module(module_path)
    # Finally, we retrieve the Class
    return getattr(module, class_str)


def uploadImg(self, path):
    """
    :param self: класс бота или че там я хз
    :param path: путь к фалу
    :return: строку для аттачмента
    """
    upload = VkUpload(self.bot.vk)
    photo = upload.photo_messages(path)[0]

    return f"photo{photo['owner_id']}_{photo['id']},"


def downloadImg(url):
    import requests
    from PIL import Image
    from random import randint
    img_r = requests.get(url, stream=True)
    img_r.raw.decode_content = True
    img: Image = Image.open(img_r.raw)
    path = f"avatar{randint(0, 100)}"
    img.save(path, "PNG")
    return path


def rounded_rectangle(self: ImageDraw, xy, corner_radius, fill=None, outline=None):
    upper_left_point = xy[0]
    bottom_right_point = xy[1]
    self.rectangle(
        [
            (upper_left_point[0], upper_left_point[1] + corner_radius),
            (bottom_right_point[0], bottom_right_point[1] - corner_radius)
        ],
        fill=fill,
        outline=outline
    )
    self.rectangle(
        [
            (upper_left_point[0] + corner_radius, upper_left_point[1]),
            (bottom_right_point[0] - corner_radius, bottom_right_point[1])
        ],
        fill=fill,
        outline=outline
    )
    self.pieslice(
        [upper_left_point, (upper_left_point[0] + corner_radius * 2, upper_left_point[1] + corner_radius * 2)],
        180,
        270,
        fill=fill,
        outline=outline
    )
    self.pieslice(
        [(bottom_right_point[0] - corner_radius * 2, bottom_right_point[1] - corner_radius * 2), bottom_right_point],
        0,
        90,
        fill=fill,
        outline=outline
    )
    self.pieslice([(upper_left_point[0], bottom_right_point[1] - corner_radius * 2),
                   (upper_left_point[0] + corner_radius * 2, bottom_right_point[1])],
                  90,
                  180,
                  fill=fill,
                  outline=outline
                  )
    self.pieslice([(bottom_right_point[0] - corner_radius * 2, upper_left_point[1]),
                   (bottom_right_point[0], upper_left_point[1] + corner_radius * 2)],
                  270,
                  360,
                  fill=fill,
                  outline=outline
                  )


ImageDraw.rounded_rectangle = rounded_rectangle
