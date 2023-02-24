from PyQt5.QtWidgets import *
from AutoShutdown_python import Ui_MainWindow
import datetime, os
from datetime import timedelta


class Otomasyon(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.ApplyBtn.clicked.connect(self.BtnApply)

    def BtnApply(self):
        if self.ui.radioButtonReboot.isChecked():
            time = self.ui.timeEdit.time()
            times = time.toString().split(":")
            nowTimes = str(datetime.datetime.now().time()).split(":")
            time1 = timedelta(hours=int(nowTimes[0]), minutes=int(nowTimes[1]))
            time2 = timedelta(hours=int(times[0]), minutes=int(times[1]))
            result = str(time2 - time1)
            if "-" in result:
                self.ui.lblStat.setStyleSheet("color: red;")
                self.ui.lblStat.setText("İleri bir saat giriniz")
            else:
                result = result.split(":")
                total = 0
                total += int(result[0])*3600
                total += int(result[1])*60
                try:
                    os.system(f"reboot /s /t {str(total)}")
                    self.ui.lblStat.setStyleSheet("color: green;")
                    self.ui.lblStat.setText(f"{time.toString()}'da yeniden başlatılıcak")
                except:
                    self.ui.lblStat.setStyleSheet("color: red;")
                    self.ui.lblStat.setText("Hata Oluştu")
        else:
            time = self.ui.timeEdit.time()
            times = time.toString().split(":")
            nowTimes = str(datetime.datetime.now().time()).split(":")
            time1 = timedelta(hours=int(nowTimes[0]), minutes=int(nowTimes[1]))
            time2 = timedelta(hours=int(times[0]), minutes=int(times[1]))
            result = str(time2 - time1)
            if "-" in result:
                self.ui.lblStat.setStyleSheet("color: red;")
                self.ui.lblStat.setText("İleri bir saat giriniz")
            else:
                result = result.split(":")
                total = 0
                total += int(result[0])*3600
                total += int(result[1])*60
                try:
                    os.system(f"shutdown /s /t {str(total)}")
                    self.ui.lblStat.setStyleSheet("color: green;")
                    self.ui.lblStat.setText(f"{time.toString()}'da kapanıcak")
                except:
                    self.ui.lblStat.setStyleSheet("color: red;")
                    self.ui.lblStat.setText("Hata Oluştu")


if __name__ == "__main__":
    app = QApplication([])
    window = Otomasyon()
    window.show()
    app.exec_()