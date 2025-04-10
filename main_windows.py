import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QDesktopWidget

from extractXML import extract_xml, save_csv

'''
#1、使用以下代码中的文件拖拽功能，只需将文件或文件夹拖拽到文本编辑框中即可。如果文件是本地文件，它们将以文件路径的形式显示在文本编辑框中。
#2、如果你想要进一步处理这些文件路径，比如复制、移动、读取或执行其他操作，你可以在 processFiles 方法中添加你的自定义代码，该方法在用户点击提交按钮后被调用。在该方法中，你可以访问文本编辑框的内容，将其拆分成文件路径，并执行相应的操作。
'''


# 使用子类来继承父类的方法，这里的’DragDropTextEdit‘，继承自  ’QTextEdit‘ ，并且添加了文件拖拽的支持。
# 这使得你可以将它用作拖拽文件的目标，以便在应用程序中方便地处理文件路径。
class DragDropTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(DragDropTextEdit, self).__init__(parent)
        self.setAcceptDrops(True)  # 启用拖拽
        self.setPlaceholderText("拖拽文件到此处，或粘贴文件路径后按 Enter")  # 提示信息

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if len(urls) == 1:
            file_path = urls[0].toLocalFile()
            if os.path.isfile(file_path):
                self.clear()
                self.append(file_path)
                self.process_file(file_path)  # 直接处理文件（可选）
        else:
            print("警告：仅支持拖入单个文件！")

    def keyPressEvent(self, event):
        # 如果按下 Enter 键，则处理当前文本（文件路径）
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            file_path = self.toPlainText().strip()
            if file_path:
                self.process_file(file_path)
        else:
            super().keyPressEvent(event)  # 其他按键正常处理

    def process_file(self, file_path):
        """处理文件路径（提取数据并保存 CSV）"""
        try:
            # 去除 file:// 前缀（如果存在）
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
        self.setWindowTitle('文件拖拽窗口')  # 设置主窗口的标题为 "文件拖拽窗口"。
        # 获取屏幕的宽度和高度
        screen = QDesktopWidget().screenGeometry()
        screenWidth = screen.width()
        screenHeight = screen.height()
        # 计算窗口居中的坐标
        x = (screenWidth - self.width()) // 2
        y = (screenHeight - self.height()) // 2
        # 设置窗口大小已经出现在屏幕的什么位置
        self.setGeometry(x, y, 600, 400)  # 设置主窗口的初始位置和大小。 (x, y)是设置窗口出现的位置。窗口的宽度为 600 像素，高度为 400 像素。

        # 初始化窗口排版模式
        central = QWidget(self)  # 创建一个名为 central 的 QWidget（窗口中央部件），用于将其他小部件添加到主窗口的中央区域。
        self.setCentralWidget(central)  # 将 central 部件设置为主窗口的中央部分。这意味着所有其他小部件将放置在 central 部件中，以确保它们在窗口中间显示。
        display = QVBoxLayout(central)  # 创建一个垂直布局管理器 display，它将用于管理 central 部件中的小部件的位置和大小。垂直布局意味着小部件将按垂直方向排列。

        # 窗口
        self.textEdit = DragDropTextEdit()  #####这里来实例化上面子类继承的内容DragDropTextEdit 的实例，并将其赋值给 self.textEdit 属性。这个文本编辑框支持文件拖拽功能。
        display.addWidget(self.textEdit)  # 将 self.textEdit 添加到垂直布局管理器 display 中
        # 按钮
        self.submit_Button = QPushButton('提交文件', self)  # 创建提交按钮的名称
        self.submit_Button.clicked.connect(self.processFiles)  # 给提交按钮绑定事件函数processFiles
        display.addWidget(self.submit_Button)  # 展示出提交按钮

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