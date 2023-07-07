"""图片文件Cache"""
from PIL import Image
from pathlib import Path
import requests
from io import BytesIO

URL_PREFIX = "https://www.bungie.net/"
ASSETS_DIRNAME = "assets"


def get_image(path: str) -> Image:
    """获取图片文件,若本地不存在则访问网络

    Args:
        path (str): 文件路径和名称

    Returns:
        Image: PIL.Image 对象
    """
    local_file = local_check(path)

    if local_file is not None:
        return local_file
    else:
        download_from_server(path)


def local_check(path: str) -> Image:
    """查询本地是否存储图片

    Args:
        path (str): 图片路径

    Returns:
        Image: 若存在则返回文件
    """
    image_path = Path().cwd().parent / ASSETS_DIRNAME / path

    if image_path.exists():
        return Image.open(image_path)

    return None


def download_from_server(path: str) -> None:
    """从Bungie服务器上下载到本地

    Args:
        path (str): 图片路径
    """

    resp = requests.get(URL_PREFIX + path)
    image_path = Path().cwd().parent / ASSETS_DIRNAME / path

    image_path.parent.mkdir(parents=True, exist_ok=True)

    with open(image_path, "wb") as f:
        f.write(BytesIO(resp.content).getbuffer())
        f.close()


# r = local_check("common/destiny2_content/screenshots/1084190509.jpg")
# print(r)

# download_from_server(
#     "common/destiny2_content/icons/d9ba41fd5e27b1021e2ec66db4ed361e.jpg"
# )
