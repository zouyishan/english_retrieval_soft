from PySide2.QtWidgets import *
import re


class EnglishSoft(QWidget):
    def __init__(self, parent=None):
        super(EnglishSoft, self).__init__(parent)
        self.window = QMainWindow()
        # 单选框
        self.btn1 = QRadioButton("词汇", self.window)
        self.btn2 = QRadioButton("短语", self.window)
        self.btn3 = QRadioButton("句式", self.window)
        self.btn4 = QRadioButton("语步", self.window)
        self.btn1.setChecked(1)
        self.bg = QButtonGroup(self.window)
        self.bg.addButton(self.btn1)
        self.bg.addButton(self.btn2)
        self.bg.addButton(self.btn3)
        self.bg.addButton(self.btn4)
        # 文本内容
        self.textEdit = QPlainTextEdit(self.window)
        # 搜索框
        self.checkBox = QLineEdit(self.window)
        # 打开文件
        self.op = QPushButton('打开文件', self.window)
        # 保存文件
        self.save = QPushButton('保存文件', self.window)
        # 检索键
        self.button = QPushButton('检索', self.window)
        # 搜索结果
        self.res = QPlainTextEdit(self.window)

        self.initUI()

    # 展示UI
    def initUI(self):
        self.btn1.move(310, 20)
        self.btn2.move(365, 20)
        self.btn3.move(420, 20)
        self.btn4.move(475, 20)

        self.window.resize(540, 390)
        self.window.setWindowTitle('学术写作辅助软件')

        self.textEdit.setPlaceholderText("请输入文章")
        self.textEdit.move(10, 28)
        self.textEdit.resize(300, 361)

        self.res.setPlaceholderText("检索结果")
        self.res.setReadOnly(1)
        self.res.resize(220, 310)
        self.res.move(310, 80)

        self.checkBox.setPlaceholderText("查询的关键词")
        self.checkBox.resize(150, 23)
        self.checkBox.move(312, 51)

        self.button.resize(80, 30)
        self.button.move(460, 48)
        self.save.move(90, 0)
        self.op.move(2, 0)
        self.button.clicked.connect(self.find)
        self.op.clicked.connect(self.openFile)
        self.save.clicked.connect(self.saveFile)
        self.window.show()

    def handleCalc(self):
        info = self.textEdit.toPlainText()

        # 薪资20000 以上 和 以下 的人员名单
        salary_above_20k = ''
        salary_below_20k = ''
        for line in info.splitlines():
            if not line.strip():
                continue
            parts = line.split(' ')
            # 去掉列表中的空字符串内容
            parts = [p for p in parts if p]
            name, salary, age = parts
            if int(salary) >= 20000:
                salary_above_20k += name + '\n'
            else:
                salary_below_20k += name + '\n'

        QMessageBox.about(self.window,
                          '统计结果',
                          f'''以上的有：\n{salary_above_20k}
                    \n以下的有：\n{salary_below_20k}'''
                          )

    def openFile(self):
        file_path = QFileDialog.getOpenFileName(self, '选择文件', './', '*.txt')
        f = open(file_path[0], "r", encoding="utf-8")
        data = f.read()
        f.close()
        self.textEdit.setPlainText(data)

    def saveFile(self):
        data = self.textEdit.toPlainText()
        file_path = QFileDialog.getSaveFileName(self, '文件保存', './', '*.txt')
        f = open(file_path[0], "w", encoding="utf-8")
        f.write(data)
        f.close()

    def find(self):
        data = self.checkBox.text()
        src = self.textEdit.toPlainText()
        if data == '':
            QMessageBox.about(self.window, '提示', '检索框为空')
        if src == '':
            QMessageBox.about(self.window, '提示', '输入框为空')

        obj = re.search(data, src, re.M | re.I)
        text = ''
        if obj is None:
            text = '匹配失败'
            self.res.setPlainText(text)
            return
        text = '匹配成功, 相关字符为: '
        tup = obj.span()
        start = tup[0]
        end = tup[1]
        if start - 2 >= 0:
            start -= 2
        if end + 2 < len(src):
            end += 2
        text += '...'
        text += src[start:end]
        text += '..., 字符位于: '
        text += str(tup[0])
        text += '-'
        text += str(tup[1])
        self.res.setPlainText(text)


if __name__ == '__main__':
    app = QApplication([])
    tx = EnglishSoft()
    app.exec_()
