from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import subprocess
from login import Ui_Dialog as login

class Ui_Dialog(object):
    def __init__(self, username):
        self.findUsername = username

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(269, 335)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-60, 0, 381, 81))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/newPrefix/2024-03-09 16_50_18-Facebook.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 90, 251, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.ChangePasswordButton = QtWidgets.QPushButton(Dialog)
        self.ChangePasswordButton.setGeometry(QtCore.QRect(80, 230, 111, 41))
        self.ChangePasswordButton.setObjectName("ChangePasswordButton")
        self.LogoutButton = QtWidgets.QPushButton(Dialog)
        self.LogoutButton.setGeometry(QtCore.QRect(80, 280, 111, 41))
        self.LogoutButton.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                        "color: rgb(255, 255, 255);")
        self.LogoutButton.setObjectName("LogoutButton")

        # Connect the "Change Password" button to the change_password method
        self.ChangePasswordButton.clicked.connect(self.change_password)
        # Connect the "Logout" button to the close_window method
        self.LogoutButton.clicked.connect(Dialog.close)
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Account Management"))
        self.label_2.setText(_translate("Dialog", f"User: {self.findUsername}"))
        self.ChangePasswordButton.setText(_translate("Dialog", "Change Password"))
        self.LogoutButton.setText(_translate("Dialog", "Logout"))

    def change_password(self):
        # Connect to the SQLite database
        connection = sqlite3.connect('user.db')
        cursor = connection.cursor()

        # Fetch password based on the username
        cursor.execute("SELECT password FROM users WHERE username = ?", (self.findUsername,))
        stored_password = cursor.fetchone()

        # Close the database connection
        connection.close()

        if stored_password is None:
            QtWidgets.QMessageBox.warning(None, "Error", "User not found.")
            return

        # Prompt user for current password
        current_password, ok = QtWidgets.QInputDialog.getText(None, "Current Password", "Enter your current password:", QtWidgets.QLineEdit.Password)
        if not ok:
            return  # User canceled the input

        if current_password != stored_password[0]:
            QtWidgets.QMessageBox.warning(None, "Incorrect Password", "The current password you entered is incorrect.")
            return
        
        # Prompt user for new password
        new_password, ok = QtWidgets.QInputDialog.getText(None, "New Password", "Enter your new password:", QtWidgets.QLineEdit.Password)
        if not ok:
            return  # User canceled the input
        
        # Prompt user to confirm new password
        confirm_new_password, ok = QtWidgets.QInputDialog.getText(None, "Confirm New Password", "Confirm your new password:", QtWidgets.QLineEdit.Password)
        if not ok:
            return  # User canceled the input
        
        # Verify new password and confirmation match
        if new_password != confirm_new_password:
            QtWidgets.QMessageBox.warning(None, "Password Mismatch", "The new passwords you entered do not match.")
            return
        
        # Update the password in the database
        connection = sqlite3.connect('user.db')
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, self.findUsername))
        connection.commit()
        connection.close()

        QtWidgets.QMessageBox.information(None, "Password Changed", "Your password has been successfully changed.")

import account_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    if len(sys.argv) > 1:
        username = sys.argv[1]
        ui = Ui_Dialog(username)
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
