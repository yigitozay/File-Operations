from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout
from tab_pdf import PdfTab
class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'File Handler App'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600

        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        pdf_tab = PdfTab()
        self.tab_widget.addTab(pdf_tab, 'PDF')