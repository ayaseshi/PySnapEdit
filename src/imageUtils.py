from PyQt5.QtGui import QImage, QPixmap
import numpy as np

class ImageUtils():
    def pixmapToImage(self, pixmap):
        image = pixmap.toImage()
        buffer = image.bits().asstring(image.byteCount())
        img = np.frombuffer(buffer, dtype=np.uint8).reshape((image.height(), image.width(), 4))
        return img
    
    def imageToPixmap(self, img):
        h, w, ch = img.shape
        bytesPerLine = ch * w
        image = QImage(img.data, w, h, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        return pixmap