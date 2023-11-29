import sys
from PyQt5.QtWidgets import QApplication
from app_window import AppWindow

def main():
    app = QApplication(sys.argv) 
    main_window = AppWindow()    
    main_window.show()           
    sys.exit(app.exec_())        

if __name__ == '__main__':
    main()
