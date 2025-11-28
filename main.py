import sys
from PyQt5 import QtWidgets
from crm_app.ui.login_window import LoginWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())