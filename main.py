from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
import sys

# Charger UI
qtcreator_file = "design3.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class DesignWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(DesignWindow, self).__init__()
        self.setupUi(self)

        self.image = None
        self.gray = None
        self.mag = None

        # Connexions
        self.Browse.clicked.connect(self.get_image)
        self.Validate_1.clicked.connect(self.apply_first_derivative)
        self.Validate_2.clicked.connect(self.compute_gradient_edges)

        self.Lapbtn.clicked.connect(self.apply_laplacian)
        self.Logbtn.clicked.connect(self.apply_log)
        self.Cannybtn.clicked.connect(self.apply_canny)

    # ---------------------------
    # Charger image
    # ---------------------------
    def get_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.image = cv2.imread(path)
            self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

            self.display_image(self.gray, self.GrayImg)

    # ---------------------------
    # Affichage image
    # ---------------------------
    def display_image(self, img, label):
        pixmap = self.cvToPixmap(img)
        label.setPixmap(pixmap)
        label.setScaledContents(True)

    # ---------------------------
    # Conversion OpenCV → QPixmap
    # ---------------------------
    def cvToPixmap(self, img):
        if len(img.shape) == 2:
            h, w = img.shape
            q_img = QtGui.QImage(img.data, w, h, w, QtGui.QImage.Format_Grayscale8)
        else:
            h, w, ch = img.shape
            q_img = QtGui.QImage(img.data, w, h, w * ch, QtGui.QImage.Format_RGB888)

        return QPixmap.fromImage(q_img)

    # ---------------------------
    # Prewitt / Sobel
    # ---------------------------
    def apply_first_derivative(self):
        if self.gray is None:
            print("Image non chargée")
            return

        if self.radioPrewitt.isChecked():
            print("Prewitt choisi")
            Hx = np.array([[-1, 0, 1],
                           [-1, 0, 1],
                           [-1, 0, 1]])

            Hy = np.array([[-1, -1, -1],
                           [0, 0, 0],
                           [1, 1, 1]])

        elif self.radioSobel.isChecked():
            print("Sobel choisi")
            Hx = np.array([[-1, 0, 1],
                           [-2, 0, 2],
                           [-1, 0, 1]])

            Hy = np.array([[-1, -2, -1],
                           [0, 0, 0],
                           [1, 2, 1]])
        else:
            print("Aucune méthode sélectionnée ❌")
            return

        gx = cv2.filter2D(self.gray, cv2.CV_64F, Hx)
        gy = cv2.filter2D(self.gray, cv2.CV_64F, Hy)

        mag = np.sqrt(gx ** 2 + gy ** 2)

        self.mag = cv2.normalize(
            mag, None, 0, 255, cv2.NORM_MINMAX
        ).astype(np.uint8)

        self.display_image(self.mag, self.FilteredImg)

    # ---------------------------
    # Seuillage
    # ---------------------------
    def compute_gradient_edges(self):
        if self.mag is None:
            print("Appliquer gradient d'abord")
            return

        try:
            t1 = int(self.Threshold_1.toPlainText().strip())
            t2 = int(self.Threshold_2.toPlainText().strip())
        except:
            print("Erreur seuil → valeurs par défaut")
            t1, t2 = 100, 255

        print("Seuils:", t1, t2)

        _, thresh = cv2.threshold(self.mag, t1, t2, cv2.THRESH_BINARY)

        self.display_image(thresh, self.SegmentedImg)
    # ---------------------------
    # Laplacien
    # ---------------------------
    def apply_laplacian(self):
        if self.gray is None:
            return

        lap = cv2.Laplacian(self.gray, cv2.CV_64F)
        lap = cv2.convertScaleAbs(lap)

        self.display_image(lap, self.LaplacianImg)

    # ---------------------------
    # LoG
    # ---------------------------
    def apply_log(self):
        if self.gray is None:
            return

        blur = cv2.GaussianBlur(self.gray, (5, 5), 0)
        log = cv2.Laplacian(blur, cv2.CV_64F)
        log = cv2.convertScaleAbs(log)

        self.display_image(log, self.LoGImg)

    # ---------------------------
    # Canny
    # ---------------------------
    def apply_canny(self):
        if self.gray is None:
            return

        canny = cv2.Canny(self.gray, 100, 200)

        self.display_image(canny, self.CannyImg)


# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DesignWindow()
    window.show()
    sys.exit(app.exec_())