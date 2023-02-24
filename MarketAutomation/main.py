from PyQt5.QtWidgets import *
from market_python import Ui_MainWindow
import sys, sqlite3, datetime



class Otomasyon(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.LoadData()

        self.ui.btnGoPage1.clicked.connect(self.GoPage1)
        self.ui.btnGoPage2.clicked.connect(self.GoPage2)
        self.ui.btnGoPage3.clicked.connect(self.GoPage3)
        self.ui.btnGoPage4.clicked.connect(self.GoPage4)
        self.ui.btnGoPage5.clicked.connect(self.GoPage5)
        self.ui.btnGoPage6.clicked.connect(self.GoPage6)
        self.ui.btnGoMenu.clicked.connect(self.GoMenu)
        self.ui.btnGoMenu_2.clicked.connect(self.GoMenu)
        self.ui.btnGoMenu_3.clicked.connect(self.GoMenu)
        self.ui.btnGoMenu_4.clicked.connect(self.GoMenu)
        self.ui.btnGoMenu_5.clicked.connect(self.GoMenu)
        self.ui.btnGoMenu_6.clicked.connect(self.GoMenu)
        self.ui.btnCloseCase.clicked.connect(self.CloseCase)
        self.ui.btnBasketInAddProduct.clicked.connect(self.BasketInAddProduct)


    def LoadData(self):
        self.DbName = "MarketAutomation/data.db"
        db = sqlite3.connect(self.DbName)
        cur = db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS brands(name)")
        cur.execute("CREATE TABLE IF NOT EXISTS categories(name)")
        cur.execute("CREATE TABLE IF NOT EXISTS products(id integer primary key, name, stock, price, brand, category, expiryDate)")
        cur.execute("CREATE TABLE IF NOT EXISTS salesHistory(totalPrice, date)")
        cur.execute("CREATE TABLE IF NOT EXISTS dailyTurnover(Price, date)")
        cur.execute("CREATE TABLE IF NOT EXISTS weeklyTurnover(Price, date)")
        cur.execute("CREATE TABLE IF NOT EXISTS monthlyTurnover(Price, date)")
        db.close()

    def GoMenu(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def msgBox(self, title, content):
        return QMessageBox.question(self, title, content, QMessageBox.Yes | QMessageBox.No)
    
    def CloseCase(self):
        sys.exit()

    # ! ////////////////////////////////////////// Page 1 //////////////////////////////////////////
    def GoPage1(self):
        self.ui.tblBasketList.setColumnCount(4)
        self.ui.tblBasketList.setHorizontalHeaderLabels(("id", "ürün", "adet", "fiyat"))
        self.ui.tblBasketList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ui.cmbBrands_4.clear()
        self.ui.cmbCategories_5.clear()
        if self.ui.tableWidget_4.rowCount() > 0:
            for i in reversed(range(self.ui.tableWidget_4.rowCount())):
                self.ui.tableWidget_4.removeRow(i)
        db = sqlite3.connect(self.DbName)
        cur = db.cursor()
        cur.execute("select * from brands")
        brands = cur.fetchall()
        for brand in brands:
            self.ui.cmbBrands_4.addItem(brand[0])

        cur.execute("select * from categories")
        categories = cur.fetchall()
        for category in categories:
            self.ui.cmbCategories_5.addItem(category[0])
        
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        db.close()

        self.ui.tableWidget_4.setColumnCount(7)
        self.ui.tableWidget_4.setHorizontalHeaderLabels(("id", "ürün", "stok", "fiyat", "marka", "kategori", "stt"))
        self.ui.tableWidget_4.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for product in products:
            rowCount = self.ui.tableWidget_4.rowCount()
            self.ui.tableWidget_4.insertRow(rowCount)
            self.ui.tableWidget_4.setItem(rowCount, 0, QTableWidgetItem(str(product[0])))
            self.ui.tableWidget_4.setItem(rowCount, 1, QTableWidgetItem(str(product[1])))
            self.ui.tableWidget_4.setItem(rowCount, 2, QTableWidgetItem(str(product[2])))
            self.ui.tableWidget_4.setItem(rowCount, 3, QTableWidgetItem(str(product[3])))
            self.ui.tableWidget_4.setItem(rowCount, 4, QTableWidgetItem(str(product[4])))
            self.ui.tableWidget_4.setItem(rowCount, 5, QTableWidgetItem(str(product[5])))
            self.ui.tableWidget_4.setItem(rowCount, 6, QTableWidgetItem(str(product[6])))

        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.btnDeleteBasket.clicked.connect(self.DeleteBasket)
        self.ui.btnSell.clicked.connect(self.ReadTabel)

    def BasketInAddProduct(self):
        productId = self.ui.spnProductId.value()
        productPiece = self.ui.spnProductStock.value()
        if productId > 0 and productPiece > 0:
            db = sqlite3.connect(self.DbName)
            cur = db.cursor()
            command = f"SELECT * FROM products WHERE id = {productId}"
            cur.execute(command)
            productDetail = cur.fetchall()
            db.close()
            if len(productDetail) > 0:
                if productPiece > int(productDetail[0][2]):
                    print("Maalesef Stok miktarımız yetersiz")
                else:
                    rowCount = self.ui.tblBasketList.rowCount()
                    self.ui.tblBasketList.insertRow(rowCount)
                    self.ui.tblBasketList.setItem(rowCount, 0, QTableWidgetItem(str(productDetail[0][0])))
                    self.ui.tblBasketList.setItem(rowCount, 1, QTableWidgetItem(str(productDetail[0][1])))
                    self.ui.tblBasketList.setItem(rowCount, 2, QTableWidgetItem(str(productPiece)))
                    self.ui.tblBasketList.setItem(rowCount, 3, QTableWidgetItem(str(productDetail[0][3])))
            else:
                pass

    def ReadTabel(self):
        rowCount = self.ui.tblBasketList.rowCount()
        columnCount = self.ui.tblBasketList.columnCount()
        for row in range(rowCount):
            rowData = []
            for column in range(columnCount):
                widgetItem = self.ui.tblBasketList.item(row, column)
                if widgetItem and widgetItem.text():
                    rowData.append(widgetItem.text())
                else:
                    rowData.append("NULL")
            self.Sell(rowData)

    def DeleteBasket(self):
        if self.ui.tblBasketList.rowCount() > 0:
            for i in reversed(range(self.ui.tblBasketList.rowCount())):
                self.ui.tblBasketList.removeRow(i)

    def Sell(self, data):
        print(data)
        db = sqlite3.connect(self.DbName)
        cur = db.cursor()
        command = f"SELECT * FROM products WHERE id = '{data[0]}'"
        cur.execute(command)
        productDetail = cur.fetchall()
        print(productDetail[0][2])
        print(data[2])
        stock = int(productDetail[0][2]) - int(data[2])
        print(stock)
        command = f"UPDATE products SET stock = '{stock}' WHERE id = {data[0]}"
        cur.execute(command)
        db.commit()
        db.close()
        self.DeleteBasket()
        self.GoPage1()


    # ! ////////////////////////////////////////// Page 2 //////////////////////////////////////////
    def GoPage2(self):
        self.ui.cmbBrands.clear()
        self.ui.cmbCategories.clear()
        if self.ui.tableWidget_2.rowCount() > 0:
            for i in reversed(range(self.ui.tableWidget_2.rowCount())):
                self.ui.tableWidget_2.removeRow(i)
        db = sqlite3.connect(self.DbName)
        cur = db.cursor()
        cur.execute("select * from brands")
        brands = cur.fetchall()
        for brand in brands:
            self.ui.cmbBrands.addItem(brand[0])

        cur.execute("select * from categories")
        categories = cur.fetchall()
        for category in categories:
            self.ui.cmbCategories.addItem(category[0])
        
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        db.close()

        self.ui.tableWidget_2.setColumnCount(7)
        self.ui.tableWidget_2.setHorizontalHeaderLabels(("id", "ürün", "stok", "fiyat", "marka", "kategori", "stt"))
        self.ui.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for product in products:
            rowCount = self.ui.tableWidget_2.rowCount()
            self.ui.tableWidget_2.insertRow(rowCount)
            self.ui.tableWidget_2.setItem(rowCount, 0, QTableWidgetItem(str(product[0])))
            self.ui.tableWidget_2.setItem(rowCount, 1, QTableWidgetItem(str(product[1])))
            self.ui.tableWidget_2.setItem(rowCount, 2, QTableWidgetItem(str(product[2])))
            self.ui.tableWidget_2.setItem(rowCount, 3, QTableWidgetItem(str(product[3])))
            self.ui.tableWidget_2.setItem(rowCount, 4, QTableWidgetItem(str(product[4])))
            self.ui.tableWidget_2.setItem(rowCount, 5, QTableWidgetItem(str(product[5])))
            self.ui.tableWidget_2.setItem(rowCount, 6, QTableWidgetItem(str(product[6])))

        self.ui.lblStatMessage.clear()

        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.btnAddProduct.clicked.connect(self.AddProduct)
        self.ui.btnUpdateProduct.clicked.connect(self.UpdateProduct)

    def AddProduct(self):
        productName = self.ui.lneProductName.text()
        stock = self.ui.spnStock.value()
        price = self.ui.spnPrice.value()
        brand = self.ui.cmbBrands.currentText()
        category = self.ui.cmbCategories.currentText()
        stt = self.ui.dateEditStt.date()

        today = str(datetime.datetime.today())
        today = today.split(" ")[0].split("-")

        date1 = datetime.datetime(int(today[0]), int(today[1]), int(today[2]))
        date2 = datetime.datetime(stt.getDate()[0], stt.getDate()[1], stt.getDate()[2])
        day = (date2 - date1)

        if len(productName) == 0 or not stock > 0 or not price > 0 or len(brand) == 0 or len(category) == 0:
            self.ui.lblStatMessage.setStyleSheet("color: red;")
            self.ui.lblStatMessage.setText("Lütfen tüm Boşlukları Doldurun.")
        elif not day.days > 0:
            self.ui.lblStatMessage.setStyleSheet("color: red;")
            self.ui.lblStatMessage.setText("Son kullanma tarihi geçmiş bir ürün girdiniz")
        else:
            try:
                db = sqlite3.connect(self.DbName)
                cur = db.cursor()
                command = f"INSERT INTO products (name, stock, price, brand, category, expiryDate) VALUES('{productName}', '{stock}', '{price}', '{brand}', '{category}', '{stt.getDate()[0]}.{stt.getDate()[1]}.{stt.getDate()[2]}')"
                cur.execute(command)
                db.commit()
                db.close()
                self.ui.lneProductName.clear()
                self.ui.spnPrice.setValue(0)
                self.ui.spnStock.setValue(0)
                self.ui.lblStatMessage.setStyleSheet("color: green;")
                self.ui.lblStatMessage.setText("Ürün Eklendi")
                self.GoPage2()
            except:
                self.ui.lblStatMessage.setStyleSheet("color: red;")
                self.ui.lblStatMessage.setText("Bir Hata Oluştu")

    def UpdateProduct(self):
        productName = self.ui.lneProductName.text()
        stock = self.ui.spnStock.value()
        price = self.ui.spnPrice.value()
        brand = self.ui.cmbBrands.currentText()
        category = self.ui.cmbCategories.currentText()
        stt = self.ui.dateEditStt.date()
        productId = self.ui.spnId.value()

        today = str(datetime.datetime.today())
        today = today.split(" ")[0].split("-")

        date1 = datetime.datetime(int(today[0]), int(today[1]), int(today[2]))
        date2 = datetime.datetime(stt.getDate()[0], stt.getDate()[1], stt.getDate()[2])
        day = (date2 - date1)

        if len(productName) == 0 or not stock > 0 or not price > 0 or not productId > 0 or len(brand) == 0 or len(category) == 0:
            self.ui.lblStatMessage.setStyleSheet("color: red;")
            self.ui.lblStatMessage.setText("Lütfen tüm Boşlukları Doldurun.")
        elif not day.days > 0:
            self.ui.lblStatMessage.setStyleSheet("color: red;")
            self.ui.lblStatMessage.setText("Son kullanma tarihi geçmiş bir ürün girdiniz")
        else:
            db = sqlite3.connect(self.DbName)
            cur = db.cursor()
            command = f"UPDATE products SET name = '{productName}', stock = '{stock}', price = '{price}', brand = '{brand}', category = '{category}', expiryDate = '{stt.getDate()[0]}.{stt.getDate()[1]}.{stt.getDate()[2]}' WHERE id = {productId}"
            cur.execute(command)
            db.commit()
            db.close()
            self.ui.lblStatMessage.setStyleSheet("color: green;")
            self.ui.lblStatMessage.setText("Ürün Güncellendi")
            self.GoPage2()
    # ! ////////////////////////////////////////// Page 3 //////////////////////////////////////////

    def GoPage3(self):
        self.ui.cmbBrands_2.clear()
        self.ui.cmbBrands_3.clear()
        self.ui.cmbCategories_3.clear()
        self.ui.cmbCategories_4.clear()
        if self.ui.tableWidget.rowCount() > 0:
            for i in reversed(range(self.ui.tableWidget.rowCount())):
                self.ui.tableWidget.removeRow(i)

        self.ui.lblStatMessage_2.clear()

        db = sqlite3.connect(self.DbName)
        cur = db.cursor()
        cur.execute("select * from brands")
        brands = cur.fetchall()
        for brand in brands:
            self.ui.cmbBrands_3.addItem(brand[0])
            self.ui.cmbBrands_2.addItem(brand[0])

        cur.execute("select * from categories")
        categories = cur.fetchall()
        for category in categories:
            self.ui.cmbCategories_3.addItem(category[0])
            self.ui.cmbCategories_4.addItem(category[0])

        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        db.close()

        self.ui.tableWidget.setColumnCount(7)
        self.ui.tableWidget.setHorizontalHeaderLabels(("id", "ürün", "stok", "fiyat", "marka", "kategori", "stt"))
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for product in products:
            rowCount = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowCount)
            self.ui.tableWidget.setItem(rowCount, 0, QTableWidgetItem(str(product[0])))
            self.ui.tableWidget.setItem(rowCount, 1, QTableWidgetItem(str(product[1])))
            self.ui.tableWidget.setItem(rowCount, 2, QTableWidgetItem(str(product[2])))
            self.ui.tableWidget.setItem(rowCount, 3, QTableWidgetItem(str(product[3])))
            self.ui.tableWidget.setItem(rowCount, 4, QTableWidgetItem(str(product[4])))
            self.ui.tableWidget.setItem(rowCount, 5, QTableWidgetItem(str(product[5])))
            self.ui.tableWidget.setItem(rowCount, 6, QTableWidgetItem(str(product[6])))

        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.btnDeleteCategories.clicked.connect(self.DeleteFilterCategories)
        self.ui.btnDeleteBrands.clicked.connect(self.DeleteFilterBrands)
        self.ui.btnBrandsProductList.clicked.connect(self.BrandsInProducts)
        self.ui.btnCategoriesProductList.clicked.connect(self.CategoriesInProducts)
    
    def DeleteFilterCategories(self):
        category = self.ui.cmbCategories_4.currentText()
        if not len(category) == 0:
            ret = self.msgBox('Uyarı', f"{category} Kategorisindeki tüm ürünleri silmek istediğine eminmisin ?")
            if ret == QMessageBox.Yes:
                try:
                    db = sqlite3.connect(self.DbName)
                    cur = db.cursor()
                    command = f"DELETE FROM products WHERE category = '{category}'"
                    cur.execute(command)
                    db.commit()
                    db.close()
                    self.ui.lblStatMessage_2.setStyleSheet("color: green;")
                    self.ui.lblStatMessage_2.setText("Silindi.")
                    self.GoPage3()
                except:
                    self.ui.lblStatMessage_2.setStyleSheet("color: red;")
                    self.ui.lblStatMessage_2.setText("Bir hata oluştu.")
            else:
                pass
        else:
            self.ui.lblStatMessage_2.setStyleSheet("color: red;")
            self.ui.lblStatMessage_2.setText("Lütfen tüm Boşlukları Doldurun.")

    def DeleteFilterBrands(self):
        brand = self.ui.cmbBrands_2.currentText()
        if not len(brand) == 0:
            ret = self.msgBox('Uyarı', f"{brand} markasına ait tüm ürünleri silmek istediğine eminmisin ?")
            if ret == QMessageBox.Yes:
                try:
                    db = sqlite3.connect(self.DbName)
                    cur = db.cursor()
                    command = f"DELETE FROM products WHERE brand = '{brand}'"
                    cur.execute(command)
                    db.commit()
                    db.close()
                    self.ui.lblStatMessage_2.setStyleSheet("color: green;")
                    self.ui.lblStatMessage_2.setText("Silindi.")
                    self.GoPage3()
                except:
                    self.ui.lblStatMessage_2.setStyleSheet("color: red;")
                    self.ui.lblStatMessage_2.setText("Bir hata oluştu.")
            else:
                pass
        else:
            self.ui.lblStatMessage_2.setStyleSheet("color: red;")
            self.ui.lblStatMessage_2.setText("Lütfen tüm Boşlukları Doldurun.")

    def BrandsInProducts(self):
        brand = self.ui.cmbBrands_3.currentText()
        if not len(brand) == 0:
            if self.ui.tableWidget.rowCount() > 0:
                for i in reversed(range(self.ui.tableWidget.rowCount())):
                    self.ui.tableWidget.removeRow(i)
            db = sqlite3.connect(self.DbName)
            cur = db.cursor()
            command = f"SELECT * FROM products WHERE brand = '{brand}'"
            cur.execute(command)
            products = cur.fetchall()
            db.close()

            self.ui.tableWidget.setColumnCount(7)
            self.ui.tableWidget.setHorizontalHeaderLabels(("id", "ürün", "stok", "fiyat", "marka", "kategori", "stt"))
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            for product in products:
                rowCount = self.ui.tableWidget_2.rowCount()
                self.ui.tableWidget.insertRow(rowCount)
                self.ui.tableWidget.setItem(rowCount, 0, QTableWidgetItem(str(product[0])))
                self.ui.tableWidget.setItem(rowCount, 1, QTableWidgetItem(str(product[1])))
                self.ui.tableWidget.setItem(rowCount, 2, QTableWidgetItem(str(product[2])))
                self.ui.tableWidget.setItem(rowCount, 3, QTableWidgetItem(str(product[3])))
                self.ui.tableWidget.setItem(rowCount, 4, QTableWidgetItem(str(product[4])))
                self.ui.tableWidget.setItem(rowCount, 5, QTableWidgetItem(str(product[5])))
                self.ui.tableWidget.setItem(rowCount, 6, QTableWidgetItem(str(product[6])))
        else:
            self.ui.lblStatMessage_2.setStyleSheet("color: red;")
            self.ui.lblStatMessage_2.setText("Lütfen tüm Boşlukları Doldurun.")

    def CategoriesInProducts(self):
        category = self.ui.cmbCategories_3.currentText()
        if not len(category) == 0:
            if self.ui.tableWidget.rowCount() > 0:
                for i in reversed(range(self.ui.tableWidget.rowCount())):
                    self.ui.tableWidget.removeRow(i)
            db = sqlite3.connect(self.DbName)
            cur = db.cursor()
            command = f"SELECT * FROM products WHERE category = '{category}'"
            cur.execute(command)
            products = cur.fetchall()
            db.close()

            self.ui.tableWidget.setColumnCount(7)
            self.ui.tableWidget.setHorizontalHeaderLabels(("id", "ürün", "stok", "fiyat", "marka", "kategori", "stt"))
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            for product in products:
                rowCount = self.ui.tableWidget_2.rowCount()
                self.ui.tableWidget.insertRow(rowCount)
                self.ui.tableWidget.setItem(rowCount, 0, QTableWidgetItem(str(product[0])))
                self.ui.tableWidget.setItem(rowCount, 1, QTableWidgetItem(str(product[1])))
                self.ui.tableWidget.setItem(rowCount, 2, QTableWidgetItem(str(product[2])))
                self.ui.tableWidget.setItem(rowCount, 3, QTableWidgetItem(str(product[3])))
                self.ui.tableWidget.setItem(rowCount, 4, QTableWidgetItem(str(product[4])))
                self.ui.tableWidget.setItem(rowCount, 5, QTableWidgetItem(str(product[5])))
                self.ui.tableWidget.setItem(rowCount, 6, QTableWidgetItem(str(product[6])))
        else:
            self.ui.lblStatMessage_2.setStyleSheet("color: red;")
            self.ui.lblStatMessage_2.setText("Lütfen tüm Boşlukları Doldurun.")

    # ! ////////////////////////////////////////// Page 4 //////////////////////////////////////////

    def GoPage4(self):
        self.ui.cmbCategories_2.clear()
        self.ui.cmbBrands_6.clear()
        if self.ui.tableWidget_3.rowCount() > 0:
            for i in reversed(range(self.ui.tableWidget_3.rowCount())):
                self.ui.tableWidget_3.removeRow(i)

        db = sqlite3.connect(self.DbName)
        cur = db.cursor()
        cur.execute("select * from brands")
        brands = cur.fetchall()
        for brand in brands:
            self.ui.cmbBrands_6.addItem(brand[0])

        cur.execute("select * from categories")
        categories = cur.fetchall()
        for category in categories:
            self.ui.cmbCategories_2.addItem(category[0])
        
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        db.close()

        self.ui.tableWidget_3.setColumnCount(7)
        self.ui.tableWidget_3.setHorizontalHeaderLabels(("id", "ürün", "stok", "fiyat", "marka", "kategori", "stt"))
        self.ui.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        totalStock = 0
        totalPrice = 0

        for product in products:
            totalStock += int(product[2])
            totalPrice += float(product[3])
            rowCount = self.ui.tableWidget_3.rowCount()
            self.ui.tableWidget_3.insertRow(rowCount)
            self.ui.tableWidget_3.setItem(rowCount, 0, QTableWidgetItem(str(product[0])))
            self.ui.tableWidget_3.setItem(rowCount, 1, QTableWidgetItem(str(product[1])))
            self.ui.tableWidget_3.setItem(rowCount, 2, QTableWidgetItem(str(product[2])))
            self.ui.tableWidget_3.setItem(rowCount, 3, QTableWidgetItem(str(product[3])))
            self.ui.tableWidget_3.setItem(rowCount, 4, QTableWidgetItem(str(product[4])))
            self.ui.tableWidget_3.setItem(rowCount, 5, QTableWidgetItem(str(product[5])))
            self.ui.tableWidget_3.setItem(rowCount, 6, QTableWidgetItem(str(product[6])))
        self.ui.lblStock.setText(f"Toplam Stok : {totalStock}       Toplam Fiyat : {totalPrice}")
        totalStock = 0
        totalPrice = 0

        self.ui.btnFiltersBrandProducts.clicked.connect(self.ByBrands)
        self.ui.btnFiltersCategoryProducts.clicked.connect(self.ByCategories)
        self.ui.btnAllProducts.clicked.connect(self.GoPage4)
        self.ui.stackedWidget.setCurrentIndex(4)

    def ByBrands(self):
        brand = self.ui.cmbBrands_6.currentText()
        if not len(brand) == 0:
            if self.ui.tableWidget_3.rowCount() > 0:
                for i in reversed(range(self.ui.tableWidget_3.rowCount())):
                    self.ui.tableWidget_3.removeRow(i)
            db = sqlite3.connect(self.DbName)
            cur = db.cursor()
            command = f"SELECT * FROM products WHERE brand = '{brand}'"
            cur.execute(command)
            products = cur.fetchall()
            db.close()

            self.ui.tableWidget_3.setColumnCount(7)
            self.ui.tableWidget_3.setHorizontalHeaderLabels(("id", "ürün", "stok", "fiyat", "marka", "kategori", "stt"))
            self.ui.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            totalStock = 0
            totalPrice = 0

            for product in products:
                totalStock += int(product[2])
                totalPrice += float(product[3])
                rowCount = self.ui.tableWidget_2.rowCount()
                self.ui.tableWidget_3.insertRow(rowCount)
                self.ui.tableWidget_3.setItem(rowCount, 0, QTableWidgetItem(str(product[0])))
                self.ui.tableWidget_3.setItem(rowCount, 1, QTableWidgetItem(str(product[1])))
                self.ui.tableWidget_3.setItem(rowCount, 2, QTableWidgetItem(str(product[2])))
                self.ui.tableWidget_3.setItem(rowCount, 3, QTableWidgetItem(str(product[3])))
                self.ui.tableWidget_3.setItem(rowCount, 4, QTableWidgetItem(str(product[4])))
                self.ui.tableWidget_3.setItem(rowCount, 5, QTableWidgetItem(str(product[5])))
                self.ui.tableWidget_3.setItem(rowCount, 6, QTableWidgetItem(str(product[6])))
            self.ui.lblStock.setText(f"Toplam Stok : {totalStock}       Toplam Fiyat : {totalPrice}")
            totalStock = 0
            totalPrice = 0
        else:
            pass

    def ByCategories(self):
        category = self.ui.cmbCategories_2.currentText()
        if not len(category) == 0:
            if self.ui.tableWidget_3.rowCount() > 0:
                for i in reversed(range(self.ui.tableWidget_3.rowCount())):
                    self.ui.tableWidget_3.removeRow(i)
            db = sqlite3.connect(self.DbName)
            cur = db.cursor()
            command = f"SELECT * FROM products WHERE category = '{category}'"
            cur.execute(command)
            products = cur.fetchall()
            db.close()

            self.ui.tableWidget_3.setColumnCount(7)
            self.ui.tableWidget_3.setHorizontalHeaderLabels(("id", "ürün", "stok", "fiyat", "marka", "kategori", "stt"))
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            totalStock = 0
            totalPrice = 0

            for product in products:
                totalStock += int(product[2])
                totalPrice += float(product[3])
                rowCount = self.ui.tableWidget_3.rowCount()
                self.ui.tableWidget_3.insertRow(rowCount)
                self.ui.tableWidget_3.setItem(rowCount, 0, QTableWidgetItem(str(product[0])))
                self.ui.tableWidget_3.setItem(rowCount, 1, QTableWidgetItem(str(product[1])))
                self.ui.tableWidget_3.setItem(rowCount, 2, QTableWidgetItem(str(product[2])))
                self.ui.tableWidget_3.setItem(rowCount, 3, QTableWidgetItem(str(product[3])))
                self.ui.tableWidget_3.setItem(rowCount, 4, QTableWidgetItem(str(product[4])))
                self.ui.tableWidget_3.setItem(rowCount, 5, QTableWidgetItem(str(product[5])))
                self.ui.tableWidget_3.setItem(rowCount, 6, QTableWidgetItem(str(product[6])))
            self.ui.lblStock.setText(f"Toplam Stok : {totalStock}       Toplam Fiyat : {totalPrice}")
            totalStock = 0
            totalPrice = 0
        else:
            pass
    # ! ////////////////////////////////////////// Page 5 //////////////////////////////////////////

    def GoPage5(self):
        self.ui.BrandsList.clear()
        self.ui.lblBrandStatMessage.clear()
        self.ui.lneBrandName.clear()
        self.ui.stackedWidget.setCurrentIndex(5)

        db = sqlite3.connect(self.DbName)
        cur = db.cursor()
        cur.execute("SELECT * FROM brands")
        brands = cur.fetchall()
        db.close()

        for brand in brands:
            self.ui.BrandsList.addItem(brand[0])
        self.ui.btnAddBrand.clicked.connect(self.AddBrand)
        self.ui.btnDeleteBrand.clicked.connect(self.DeleteBrand)
        self.ui.BrandsList.itemClicked.connect(self.BrandsListClicked)

    def AddBrand(self):
        brandName = self.ui.lneBrandName.text()
        db = sqlite3.connect(self.DbName)
        cur = db.cursor()
        if len(brandName) > 0:
            command = f"SELECT * FROM brands WHERE name = '{brandName}'"
            cur.execute(command)
            brands = cur.fetchall()
            if len(brands) == 0:
                command = f"INSERT INTO brands ('name') VALUES ('{brandName}')"
                cur.execute(command)
                db.commit()
                db.close()
                self.ui.lblBrandStatMessage.setStyleSheet("color: green;")
                self.ui.lblBrandStatMessage.setText("Eklendi")
                self.GoPage5()
            else:
                self.ui.lblBrandStatMessage.setStyleSheet("color: red;")
                self.ui.lblBrandStatMessage.setText("Bu marka zaten var")  
        else:
            self.ui.lblBrandStatMessage.setStyleSheet("color: red;")
            self.ui.lblBrandStatMessage.setText("Lütfen marka yazınız")  

    def DeleteBrand(self):
        brand = self.ui.lneBrandName.text()
        if len(brand) > 0:
            db = sqlite3.connect(self.DbName)
            cur = db.cursor()
            command = f"SELECT * FROM brands WHERE name = '{brand}'"
            cur.execute(command)
            brands = cur.fetchall()
            if len(brands) > 0:
                command = f"DELETE FROM brands WHERE name = '{brand}'"
                cur.execute(command)
                db.commit()
                db.close()
                self.ui.lblBrandStatMessage.setStyleSheet("color: green;")
                self.ui.lblBrandStatMessage.setText("Silindi")
                self.GoPage5()
            else:
                self.ui.lblBrandStatMessage.setStyleSheet("color: red;")
                self.ui.lblBrandStatMessage.setText("Marka Bulunamadı")  
        else:
            self.ui.lblBrandStatMessage.setStyleSheet("color: red;")
            self.ui.lblBrandStatMessage.setText("Marka Yazınız")  
    
    def BrandsListClicked(self, item):
        self.ui.lneBrandName.setText(item.text())

    # ! ////////////////////////////////////////// Page 6 //////////////////////////////////////////
    
    def GoPage6(self):
        self.ui.CategoryList.clear()
        self.ui.lblCategoryStatMessage.clear()
        self.ui.lneCategoryName.clear()
        self.ui.stackedWidget.setCurrentIndex(6)

        db = sqlite3.connect(self.DbName)
        cur = db.cursor()
        cur.execute("SELECT * FROM categories")
        categories = cur.fetchall()
        db.close()

        for category in categories:
            self.ui.CategoryList.addItem(category[0])
        self.ui.btnAddCategory.clicked.connect(self.AddCategory)
        self.ui.btnDeleteCategory.clicked.connect(self.DeleteCategory)
        self.ui.CategoryList.itemClicked.connect(self.CategoryListClicked)
    
    def AddCategory(self):
        categoryName = self.ui.lneCategoryName.text()
        db = sqlite3.connect(self.DbName)
        cur = db.cursor()
        if len(categoryName) > 0:
            command = f"SELECT * FROM categories WHERE name = '{categoryName}'"
            cur.execute(command)
            categories = cur.fetchall()
            if len(categories) == 0:
                command = f"INSERT INTO categories ('name') VALUES ('{categoryName}')"
                cur.execute(command)
                db.commit()
                db.close()
                self.ui.lblCategoryStatMessage.setStyleSheet("color: green;")
                self.ui.lblCategoryStatMessage.setText("Eklendi")
                self.GoPage6()
            else:
                self.ui.lblCategoryStatMessage.setStyleSheet("color: red;")
                self.ui.lblCategoryStatMessage.setText("Bu kategori zaten var")  
        else:
            self.ui.lblCategoryStatMessage.setStyleSheet("color: red;")
            self.ui.lblCategoryStatMessage.setText("Lütfen kategori yazınız")  

    def DeleteCategory(self):
        category = self.ui.lneCategoryName.text()
        if len(category) > 0:
            db = sqlite3.connect(self.DbName)
            cur = db.cursor()
            command = f"SELECT * FROM categories WHERE name = '{category}'"
            cur.execute(command)
            categories = cur.fetchall()
            if len(categories) > 0:
                command = f"DELETE FROM categories WHERE name = '{category}'"
                cur.execute(command)
                db.commit()
                db.close()
                self.ui.lblBrandStatMessage.setStyleSheet("color: green;")
                self.ui.lblBrandStatMessage.setText("Silindi")
                self.GoPage6()
            else:
                self.ui.lblCategoryStatMessage.setStyleSheet("color: red;")
                self.ui.lblCategoryStatMessage.setText("Kategori bulunamadı")  
        else:
            self.ui.lblBrandStatMessage.setStyleSheet("color: red;")
            self.ui.lblBrandStatMessage.setText("Marka seçiniz")

    def CategoryListClicked(self, item):
        self.ui.lneCategoryName.setText(item.text())

if __name__ == "__main__":
    app = QApplication([])
    window = Otomasyon()
    window.show()
    app.exec_()