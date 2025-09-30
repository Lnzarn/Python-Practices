from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QPixmap, QIntValidator
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QStackedWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QMainWindow, QWidget
import os
from banklogic.banklogic import (
    get_connection, create_table, admin_panel, verify_user, get_userid, check_balance, deposit_money, update_money)


class MainWindow(QMainWindow):
    # ----Init and Main Setup----
    def __init__(self, received_username, receieved_user_id, connectiondb):
        super().__init__()
        # Initializing Variables
        self.username = received_username
        self.user_id = receieved_user_id
        self.connection = connectiondb
        # GUI
        self.setWindowTitle("Smile Bank")
        self.setupUi()
        self.setStyleSheet("""
            QMainWindow{
                background-color: #f4f3ee;
                           }
            QLabel {
                color: #000000;
                font-family: Lato;
                           }
            QPushButton#cancel {
                color: #000000;
                font-size: 16px;
                font-family: Helvetica;
                font-weight: 600;
                border-radius: 27px;
                padding: 10px;
                margin-left: 40px;
                margin-top: 0;
                background-color: #ffd500;
                min-width: 150px;
                min-height: 35px;
            }
            QPushButton#proceed {
                color: #000000;
                font-size: 16px;
                font-family: Helvetica;
                font-weight: 600;
                border-radius: 27px;
                padding: 10px;
                margin-left: 40px;
                margin-top: 0;
                background-color: #ffd500;
                min-width: 150px;
                min-height: 35px;
            }
            
            /* MAIN PAGE DESIGNS */
            QWidget#header{
                background-color: #f7de63;
                border-bottom-right-radius: 25px;
                border-bottom-left-radius: 25px;    
                min-height: 50px;    
                           }
            QLabel#welcome {
                font-size: 30px;
                padding: 0;
                           }
            QLabel#choose {
                color: #919191;
                padding: 0;
                font-size: 12px;
                margin-top: 10px;
                margin-bottom: 0;
                           }
            QLabel#icon{
                margin-left: 15px;
                margin-bottom: 5px;
                margin-right: 20px;
                           }     
            QLabel#appname{
                color: #000000;
                font-size: 18px;
                font-family: Helvetica;
                font-weight: 600;
                min-width: 60px;
                           }           
            QPushButton#content {
                text-align: left;
                color: #000000;
                font-size: 16px;
                font-family: Helvetica;
                font-weight: 600;
                border-radius: 27px;
                padding: 10px;
                padding-left: 45px;
                margin-top: 0;
                background-color: #ffd500;
                min-width: 100px;
                min-height: 35px;
                max-width: 600px;
            }
            QPushButton#logoutbtn {
                color: #ffd500;
                font-size: 12px;
                font-family: Helvetica;
                font-weight: 600;
                border-radius: 17px;
                padding: 10px;
                margin-top: 0;
                background-color: #333333;
            }
            QPushButton#detailsbtn {
                color: #ffd500;
                font-size: 12px;
                font-family: Helvetica;
                font-weight: 600;
                border-radius: 17px;
                padding: 10px;
                margin-top: 0;
                margin-right: 10px;
                background-color: #333333;
            }
                           
            /* INQUIRY PAGE DESIGNS */
            QLabel#balanceimg {
                padding: 0;
                margin-top: 55px;
                margin-bottom: 30px;
                           }  
            QLabel#balanceamount {
                font-size: 50px;
                font-family: Lato;
                font-weight: 500;
                margin: 0;  
                margin-bottom: 10px;
                padding: 0;
                           }  
            QLabel#balancedescription {
                color: #756c6c;
                font-size: 22px;
                font-family: Lato;
                font-weight: 400;
                margin: 0;
                margin-bottom: 30px;
                padding: 0;
                }
            /* WITHDRAW PAGE DESIGNS */
            QLabel#withdrawaltitle {
                font-size: 50px;
                font-family: Lato;
                font-weight: 600;
                margin: 0;
                margin-top: 60px;  
                margin-bottom: 70px;
                margin-left: 20px;
                padding: 0;
                           }  
            QLabel#withdrawalinstruct {
                color: #756c6c;
                font-size: 14px;
                font-family: Lato;
                font-weight: 500;
                margin: 0;
                margin-left: 35px;     
                margin-bottom: 10px;     
                padding: 0;        
                           }
            QLineEdit#transactionamount {
                background-color: #dedcd2;
                color: #756c6c;
                border: 0;
                padding: 10px;
                padding-left: 25px;
                border-radius: 25px;
                margin-left: 40px;
                margin-bottom: 120px;
                min-height: 30px;
                min-width: 400px;
                           }

            /* DEPOSIT PAGE DESIGNS */
            QLabel#deposittitle {
                font-size: 50px;
                font-family: Lato;
                font-weight: 600;
                margin: 0;
                margin-top: 60px;  
                margin-bottom: 70px;
                margin-left: 20px;
                padding: 0;
                           }  
            QLabel#depositinstruct {
                color: #756c6c;
                font-size: 14px;
                font-family: Lato;
                font-weight: 500;
                margin: 0;
                margin-left: 35px;     
                margin-bottom: 10px;     
                padding: 0;        
                           }
            
            /* TRANSFER PAGE DESIGNS */      
            QLabel#transfertitle {
                font-size: 50px;
                font-family: Lato;
                font-weight: 600;
                margin: 0;
                margin-top: 60px;  
                margin-bottom: 70px;
                margin-left: 20px;
                padding: 0;
                           }  
            QLabel#transferinstruct {
                color: #756c6c;
                font-size: 14px;
                font-family: Lato;
                font-weight: 500;
                margin: 0;
                margin-left: 35px;     
                margin-bottom: 10px;     
                padding: 0;        
                           }
                           """)

    def setupUi(self):
        self.centerwidget = QWidget()
        self.resize(900, 600)
        self.setMinimumSize(QSize(600, 550))
        self.setMaximumSize(QSize(1100, 700))

        # Main vertical container
        self.mainVBoxlayout = QVBoxLayout(self.centerwidget)
        self.mainVBoxlayout.setContentsMargins(0, 0, 0, 0)

        # Header
        self.setup_header()

        # Stacked widget for main content
        self.mainStackedWidget = QStackedWidget(parent=self.centerwidget)

        # Main Page
        self.setup_mainpage()

        # Action Pages
        self.setup_balanceinquiry()
        self.setup_withdrawpage()
        self.setup_depositpage()
        self.setup_transfernumberpage()
        self.setup_transferpage()

        self.mainVBoxlayout.addWidget(self.mainStackedWidget)
        window = QWidget()
        window.setLayout(self.mainVBoxlayout)
        self.setCentralWidget(window)

    # ----UI Setup Pages----
    def setup_header(self):
        header = QWidget()
        headerHboxlayout = QHBoxLayout(header)
        headerHboxlayout.setContentsMargins(10, 10, 10, 10)
        headerHboxlayout.setSpacing(0)
        header.setObjectName("header")

        # Left side. This is the icon and app name
        icon_path = os.path.join(os.path.dirname(__file__), "Bankicon.png")
        header_icon = QLabel()
        # Ensuring that if the icon failed to load, there would be an icon.
        try:
            header_iconpixmap = QPixmap(icon_path)
            if not header_iconpixmap.isNull():
                scaled_pixmap = header_iconpixmap.scaled(
                    40, 40,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                header_icon.setPixmap(scaled_pixmap)
            else:
                header_icon.setText(":)")
        except Exception as e:
            print(f"Error loading logo: {e}")

        header_icon.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        header_icon.setObjectName("icon")
        headerHboxlayout.addWidget(header_icon)

        header_appname = QLabel("Smile Bank")
        header_appname.setObjectName("appname")
        headerHboxlayout.addWidget(header_appname)

        # adding a space inbetween
        headerHboxlayout.addStretch()

        # Profile/Detail Button
        header_detailsbtn = QPushButton("Details")
        header_detailsbtn.setObjectName("detailsbtn")
        headerHboxlayout.addWidget(header_detailsbtn)

        # Logout button
        header_logoutbtn = QPushButton("Log Out")
        header_logoutbtn.setObjectName("logoutbtn")
        headerHboxlayout.addWidget(header_logoutbtn)

        self.mainVBoxlayout.addWidget(header)

    def setup_mainpage(self):
        self.mainPage = QWidget()
        mainPagelayout = QHBoxLayout(self.mainPage)
        mainPagelayout.setContentsMargins(0, 0, 0, 0)
        mainPagelayout.setSpacing(0)

        # Left Side
        mainPage_leftwidget = QWidget()
        mainPage_leftlayout = QVBoxLayout(mainPage_leftwidget)
        mainPage_leftlayout.setContentsMargins(50, 20, 50, 20)
        mainPage_leftlayout.setSpacing(22)

        # Welcome Texts
        mainPageWelcomeText = QLabel(f"Welcome, {self.username}!")
        mainPageWelcomeText.setObjectName("welcome")
        mainPageWelcomeText.setGeometry(QRect(0, 0, 100, 200))
        mainPage_leftlayout.addWidget(mainPageWelcomeText)

        mainPageChooseText = QLabel(
            "Please choose an action")
        mainPageChooseText.setObjectName("choose")
        mainPage_leftlayout.addWidget(mainPageChooseText)

        # Action Buttons
        buttons = [
            ("Check Balance", self.on_balance),
            ("Deposit", self.on_deposit),
            ("Withdraw", self.on_withdraw),
            ("Transfer", self.on_transfer_bank_no)
        ]

        # Makes the button
        for text, callback in buttons:
            btn = QPushButton(text)
            btn.setObjectName("content")
            btn.clicked.connect(callback)
            mainPage_leftlayout.addWidget(btn)

        mainPage_leftlayout.addStretch()
        mainPagelayout.addWidget(mainPage_leftwidget, stretch=3)

        # Right Side (White Space)
        mainPage_rightwidget = QWidget()
        mainPagelayout.addWidget(mainPage_rightwidget, stretch=1)

        self.mainStackedWidget.addWidget(self.mainPage)

    def setup_balanceinquiry(self):
        # GUI SETUP
        self.balancewidget = QWidget()
        balancelayout = QVBoxLayout(self.balancewidget)
        balancelayout.setContentsMargins(10, 10, 10, 10)
        balancelayout.setSpacing(5)

        # Loading the Smile Image
        img_path = os.path.join(os.path.dirname(__file__), "smiley.png")
        balance_img = QLabel()
        try:
            balance_imgpixmap = QPixmap(img_path)
            if not balance_imgpixmap.isNull():
                scaled_img = balance_imgpixmap.scaled(
                    130, 130,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                balance_img.setPixmap(scaled_img)
            else:
                balance_img.setText(":)")
        except Exception as e:
            print(f"Image Failed to load: {e}")

        balance_img.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        balance_img.setObjectName("balanceimg")
        balancelayout.addWidget(balance_img)

        self.balance_amount = QLabel("PHP 0.00")
        self.balance_amount.setObjectName("balanceamount")
        balancelayout.addWidget(
            self.balance_amount, alignment=Qt.AlignmentFlag.AlignHCenter)

        balance_description = QLabel("Cash Balance")
        balance_description.setObjectName("balancedescription")
        balancelayout.addWidget(balance_description,
                                alignment=Qt.AlignmentFlag.AlignHCenter, )

        balance_backbtn = QPushButton("Back")
        balance_backbtn.setObjectName("cancel")
        balancelayout.addWidget(
            balance_backbtn, alignment=Qt.AlignmentFlag.AlignLeft)

        balancelayout.addStretch()

        balance_backbtn.clicked.connect(self.back_main)

        self.mainStackedWidget.addWidget(self.balancewidget)

    def setup_depositpage(self):
        # GUI SETUP
        self.depositpage = QWidget()
        depositPageLayout = QVBoxLayout(self.depositpage)
        depositPageLayout.setContentsMargins(10, 10, 10, 10)

        # UI
        depositTitle = QLabel("Deposit")
        depositTitle.setObjectName("deposittitle")
        depositPageLayout.addWidget(
            depositTitle, alignment=Qt.AlignmentFlag.AlignLeft)

        depositInstruct = QLabel("Please enter an amount to deposit")
        depositInstruct.setObjectName("depositinstruct")
        depositPageLayout.addWidget(
            depositInstruct, alignment=Qt.AlignmentFlag.AlignLeft)

        self.deposittextbox = QLineEdit()
        self.deposittextbox.setPlaceholderText("Amount")
        self.deposittextbox.setValidator(QIntValidator(1, 1000000))
        self.deposittextbox.setObjectName("transactionamount")
        depositPageLayout.addWidget(
            self.deposittextbox, alignment=Qt.AlignmentFlag.AlignLeft)

        # Action buttons
        actionBoxWidget = QWidget()
        actionBoxlayout = QHBoxLayout(actionBoxWidget)
        actionBoxlayout.setContentsMargins(0, 0, 0, 0)
        actionBoxlayout.setSpacing(2)

        cancelbtn = QPushButton("Cancel")
        cancelbtn.setObjectName("cancel")
        actionBoxlayout.addWidget(cancelbtn)

        proceedbtn = QPushButton("Proceed")
        proceedbtn.setObjectName("proceed")
        actionBoxlayout.addWidget(proceedbtn)
        actionBoxlayout.addStretch()
        depositPageLayout.addWidget(actionBoxWidget)

        depositPageLayout.addStretch()
        self.mainStackedWidget.addWidget(self.depositpage)

        cancelbtn.clicked.connect(self.back_main)
        proceedbtn.clicked.connect(self.validated_deposit)

    def setup_withdrawpage(self):
        self.withdrawpage = QWidget()
        withdrawPageLayout = QVBoxLayout(self.withdrawpage)
        withdrawPageLayout.setContentsMargins(10, 10, 10, 10)

        withdrawaltitle = QLabel("Withdrawal")
        withdrawaltitle.setObjectName("withdrawaltitle")
        withdrawPageLayout.addWidget(
            withdrawaltitle, alignment=Qt.AlignmentFlag.AlignLeft)

        withdrawalInstruct = QLabel("Please enter an amount to withdraw")
        withdrawalInstruct.setObjectName("withdrawalinstruct")
        withdrawPageLayout.addWidget(
            withdrawalInstruct, alignment=Qt.AlignmentFlag.AlignLeft)

        self.withdrawtextbox = QLineEdit()
        self.withdrawtextbox.setValidator(QIntValidator(1, 1000000))
        self.withdrawtextbox.setPlaceholderText("Amount")
        self.withdrawtextbox.setObjectName("transactionamount")
        withdrawPageLayout.addWidget(
            self.withdrawtextbox, alignment=Qt.AlignmentFlag.AlignLeft)

        actionBoxWidget = QWidget()
        actionBoxlayout = QHBoxLayout(actionBoxWidget)
        actionBoxlayout.setContentsMargins(0, 0, 0, 0)
        actionBoxlayout.setSpacing(2)

        cancelbtn = QPushButton("Cancel")
        cancelbtn.setObjectName("cancel")
        actionBoxlayout.addWidget(cancelbtn)

        proceedbtn = QPushButton("Proceed")
        proceedbtn.setObjectName("proceed")
        actionBoxlayout.addWidget(proceedbtn)

        actionBoxlayout.addStretch()
        withdrawPageLayout.addWidget(actionBoxWidget)
        withdrawPageLayout.addStretch()

        self.mainStackedWidget.addWidget(self.withdrawpage)

        cancelbtn.clicked.connect(self.back_main)
        proceedbtn.clicked.connect(self.validated_withdraw)

    def setup_transferpage(self):

        self.transferpage = QWidget()
        transferPageLayout = QVBoxLayout(self.transferpage)
        transferPageLayout.setContentsMargins(10, 10, 10, 10)

        transferTitle = QLabel("Bank Transfer")
        transferTitle.setObjectName("transfertitle")
        transferPageLayout.addWidget(
            transferTitle, alignment=Qt.AlignmentFlag.AlignLeft)

        transferInstruct = QLabel("Please enter an amount to deposit")
        transferInstruct.setObjectName("depositinstruct")
        transferPageLayout.addWidget(
            transferInstruct, alignment=Qt.AlignmentFlag.AlignLeft)

        transfertextbox = QLineEdit()
        transfertextbox.setPlaceholderText("Amount")
        transfertextbox.setObjectName("transactionamount")
        transferPageLayout.addWidget(
            transfertextbox, alignment=Qt.AlignmentFlag.AlignLeft)

        actionBoxWidget = QWidget()
        actionBoxlayout = QHBoxLayout(actionBoxWidget)
        actionBoxlayout.setContentsMargins(0, 0, 0, 0)
        actionBoxlayout.setSpacing(2)

        cancelbtn = QPushButton("Cancel")
        cancelbtn.setObjectName("cancel")
        actionBoxlayout.addWidget(cancelbtn)

        proceedbtn = QPushButton("Proceed")
        proceedbtn.setObjectName("proceed")
        actionBoxlayout.addWidget(proceedbtn)

        actionBoxlayout.addStretch()
        transferPageLayout.addWidget(actionBoxWidget)

        transferPageLayout.addStretch()

        cancelbtn.clicked.connect(self.on_transfer_bank_no)
        self.mainStackedWidget.addWidget(self.transferpage)

    def setup_transfernumberpage(self):

        self.transfernumberpage = QWidget()
        transferPageLayout = QVBoxLayout(self.transfernumberpage)
        transferPageLayout.setContentsMargins(10, 10, 10, 10)

        transferTitle = QLabel("Bank Transfer")
        transferTitle.setObjectName("transfertitle")
        transferPageLayout.addWidget(
            transferTitle, alignment=Qt.AlignmentFlag.AlignLeft)

        transferInstruct = QLabel("Please enter the Bank No. to transfer to")
        transferInstruct.setObjectName("depositinstruct")
        transferPageLayout.addWidget(
            transferInstruct, alignment=Qt.AlignmentFlag.AlignLeft)

        transfertextbox = QLineEdit()
        transfertextbox.setPlaceholderText("Bank No.")
        transfertextbox.setObjectName("transactionamount")
        transferPageLayout.addWidget(
            transfertextbox, alignment=Qt.AlignmentFlag.AlignLeft)

        actionBoxWidget = QWidget()
        actionBoxlayout = QHBoxLayout(actionBoxWidget)
        actionBoxlayout.setContentsMargins(0, 0, 0, 0)
        actionBoxlayout.setSpacing(2)

        cancelbtn = QPushButton("Cancel")
        cancelbtn.setObjectName("cancel")
        actionBoxlayout.addWidget(cancelbtn)

        proceedbtn = QPushButton("Proceed")
        proceedbtn.setObjectName("proceed")
        actionBoxlayout.addWidget(proceedbtn)

        actionBoxlayout.addStretch()
        transferPageLayout.addWidget(actionBoxWidget)

        transferPageLayout.addStretch()

        cancelbtn.clicked.connect(self.back_main)
        proceedbtn.clicked.connect(self.on_transfer)
        self.mainStackedWidget.addWidget(self.transfernumberpage)
    # ----Page Logic / Action Handlers----

    def on_balance(self):
        print("Balance button clicked")
        self.check_amount_balance()
        self.mainStackedWidget.setCurrentWidget(self.balancewidget)

    def on_deposit(self):
        print("Deposit button clicked")
        self.mainStackedWidget.setCurrentWidget(self.depositpage)

    def on_withdraw(self):
        print("Withdraw button clicked")
        self.mainStackedWidget.setCurrentWidget(self.withdrawpage)

    def on_transfer(self):
        print("Transfer button clicked")
        self.mainStackedWidget.setCurrentWidget(self.transferpage)

    def on_transfer_bank_no(self):
        print("Transfer Bank No button clicked")
        self.mainStackedWidget.setCurrentWidget(self.transfernumberpage)

    def back_main(self):
        print("Back Button Pressed")
        self.mainStackedWidget.setCurrentWidget(self.mainPage)

    # ----Transaction Logic----

    def validated_deposit(self):
        clean_amount = self.deposittextbox.text().strip()

        if not clean_amount:  # Safety check
            print("No amount entered.")
            return
        converted_amount = int(clean_amount)
        successful = deposit_money(
            self.connection, self.user_id, converted_amount)

        if successful:
            print("Deposit Successful")
            self.deposittextbox.clear()
            self.check_amount_balance()
            self.mainStackedWidget.setCurrentWidget(self.mainPage)
        else:
            print("Deposit Unsuccessful")

    def validated_withdraw(self):
        clean_amount = self.withdrawtextbox.text().strip()
        if not clean_amount:
            print("No amount entered.")
            return

        converted_amount = int(clean_amount)
        current_amount = check_balance(self.connection, self.user_id)

        if converted_amount > current_amount:
            print("Withdrawal Unsuccessful: Not enough balance")
            return

        # Calculate new balance
        new_amount = current_amount - converted_amount
        update_money(self.connection, new_amount, self.user_id)

        print("Withdrawal Successful")
        self.withdrawtextbox.clear()
        self.check_amount_balance()
        self.mainStackedWidget.setCurrentWidget(self.mainPage)

    def validated_bankno(self):
        pass

    # ----Helpers / Utility----

    def check_amount_balance(self):
        current_amount = check_balance(self.connection, self.user_id)
        self.balance_amount.setText(f"PHP {current_amount:.2f}")


def main():
    app = QApplication([])
    connection = get_connection("./bankdb.db")

    try:
        create_table(connection)

        while True:
            username = input("Enter name: ")
            password = input("Enter password: ")

            if username == 'admin' and password == 'admin':
                admin_panel(connection)
                login_status = False
            else:
                login_status = verify_user(connection, username, password)

            if login_status:
                user_id = get_userid(connection, username)
                window = MainWindow(username, user_id, connection)
                break

        window.show()
        app.exec()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
