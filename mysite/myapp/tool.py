
from django.core.files.storage import FileSystemStorage
from mysite import settings
import hashlib, os

def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

class ImageStorage(FileSystemStorage):
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):

        super(ImageStorage, self).__init__(location, base_url)
    # 重写 _save方法
    def _save(self, name, content):
        import os, time, random
        ext = os.path.splitext(name)[1]
        # 文件目录
        d = os.path.dirname(name)
        # 定义文件名，年月日时分秒随机数
        fn = time.strftime('%Y%m%d%H%M%S')
        fn = fn + '_%d' %       random.randint(0,100)
        # 重写合成文件名
        name = os.path.join(d, fn + ext)
        # 调用父类方法
        return super(ImageStorage, self)._save(name, content)

class FigureImageStorage(FileSystemStorage):

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 初始化
        self.user_id = ''
        super(FigureImageStorage, self).__init__(location, base_url)

    # 重写 _save方法
    def _save(self, name, content):
        # name为上传文件名称
        # 文件扩展名
        ext = os.path.splitext(name)[1]
        # 文件目录
        dir = os.path.dirname(name)
        # 重写合成文件名
        name = os.path.join(dir, 'user_id' + ext)
        # 调用父类方法
        return super(FigureImageStorage, self)._save(name, content)