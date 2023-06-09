from os import path

from PyQt5.QtWidgets import QFileDialog, QGraphicsPixmapItem, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QPainter
import cv2

from config import showAlert

FILE_EX = "Image Files (*.png *.jpg *.webp)"

class File:
    def __init__(self):
        self.image_path = None
        self.loaded = False

    def openFile(self):
        file_name, _ = QFileDialog.getOpenFileName(None, "Otwórz plik", "", FILE_EX)

        try:
            if file_name:
                self.image_path = file_name
                pixmap = QPixmap(file_name)
                height = pixmap.height()
                width = pixmap.width()

                item = QGraphicsPixmapItem(pixmap)
                return item, height, width, file_name
        except: return None, None, None, None

    def saveToOriginal(self, scene):
        if not self.image_path and not self.loaded:
            showAlert("Błąd!", "Nie wczytano jeszcze żadnego pliku.", QMessageBox.Warning)
            print("Nie wczytano jeszcze żadnego pliku")
            return

        if self.loaded:
            self.saveFileAs(None, scene)
            return

        if not path.exists(self.image_path):
            showAlert("Błąd!", "Podana ścieżka do pliku nie istnieje.", QMessageBox.Critical)
            print("Podana ścieżka do pliku nie istnieje")
            return

        image = QImage(scene.graphicsScene.sceneRect().size().toSize(), QImage.Format_ARGB32)

        painter = QPainter(image)
        scene.graphicsScene.render(painter)
        painter.end()

        image.save(self.image_path)
        print("Zapisano")

    def saveFileAs(self, parent, scene):
        if scene.checkEmpty():
            showAlert("Błąd!", "Brak zdjęcia, dodaj zdjęcie aby wykonać na nim operacje.", QMessageBox.Warning)
            print("Brak zdjęcia, dodaj zdjęcie aby wykonać na nim operacje.")
            return

        try:
            file_name, _ = QFileDialog.getSaveFileName(parent, "Zapisz plik", "", FILE_EX)

            if file_name:
                image = QImage(scene.graphicsScene.sceneRect().size().toSize(), QImage.Format_ARGB32)

                painter = QPainter(image)
                scene.graphicsScene.render(painter)
                painter.end()

                image.save(file_name)
        except: pass
    
    def saveCompressed(self, encimg, format_filter):
        try:
            file_name, _ = QFileDialog.getSaveFileName(None, "Zapisz plik", "", format_filter)

            if file_name:
                image = QImage.fromData(encimg)
                image.save(file_name)
        except Exception as e:
            print("Błąd: ", str(e))

    def isImageFile(self, file_name):
        try:
            image = cv2.imread(file_name)
            return image is not None
        except:
            return False

    def restartImage(self):
        self.image_path = None