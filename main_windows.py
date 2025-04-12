import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QDesktopWidget

from extractXML import extract_xml, save_csv



class DragDropTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(DragDropTextEdit, self).__init__(parent)
        self.setAcceptDrops(True)  # 启用拖拽
        self.setPlaceholderText("拖拽文件到此处，或粘贴文件路径后按 Enter")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            event.accept()
        else:
            event.ignore()

    #通过拖拽文件的方式运行
    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if len(urls) == 1:
            file_path = urls[0].toLocalFile()
            if os.path.isfile(file_path):
                self.clear()
                self.append(file_path)
                self.process_file(file_path)
        else:
            print("警告：仅支持拖入单个文件！")

    #复制文件路径后，使用回车运行
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            file_path = self.toPlainText().strip()
            if file_path:
                self.process_file(file_path)
        else:
            super().keyPressEvent(event)

    #将xml文件中的弹幕提取并保存成csv
    def process_file(self, file_path):
        """处理文件路径（提取数据并保存 CSV）"""
        try:
            # 去除 file:// 前缀
            if file_path.startswith("file:///"):
                file_path = file_path[8:]  # 去除前8个字符（file://）

            # 检查文件是否存在
            if not os.path.exists(file_path):
                print(f"错误：文件不存在 - {file_path}")
                return

            csv_path = ".//output//danmu.csv"
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)

            text_list = extract_xml(file_path)
            save_csv(text_list, csv_path)

            print(f"处理完成！源文件: {file_path}")
            print(f"CSV保存到: {csv_path}")

        except Exception as e:
            print(f"处理失败: {str(e)}")


class MainApp(QMainWindow):  # 创建实例化类
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('文件拖拽窗口')
        # 获取屏幕的宽度和高度
        screen = QDesktopWidget().screenGeometry()
        screenWidth = screen.width()
        screenHeight = screen.height()
        # 计算窗口居中的坐标
        x = (screenWidth - self.width()) // 2
        y = (screenHeight - self.height()) // 2


        self.setGeometry(x, y, 600, 400)
        # 初始化窗口排版模式
        central = QWidget(self)
        self.setCentralWidget(central)
        display = QVBoxLayout(central)

        # 窗口
        self.textEdit = DragDropTextEdit()
        display.addWidget(self.textEdit)
        # 按钮
        self.submit_Button = QPushButton('提交文件', self)
        self.submit_Button.clicked.connect(self.processFiles)
        display.addWidget(self.submit_Button)

    def processFiles(self):
        file_path = self.textEdit.toPlainText().strip()
        if file_path:
            self.textEdit.process_file(file_path)



def main():
    app = QApplication(sys.argv)
    ex = MainApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()