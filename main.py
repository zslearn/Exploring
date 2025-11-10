from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QStackedLayout, QFrame, QApplication,
                               QHBoxLayout, QSplashScreen)
from PySide6.QtGui import (QIcon, Qt, QMovie)
import time, sys
from PySide6.QtCore import (QThread, QObject, Signal, QPropertyAnimation)


class OpenMovie(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 300)

        self.movie = QMovie("document/successful.gif")
        self.movie.setScaledSize(self.size())

        self.label = QLabel(self)
        self.label.setMovie(self.movie)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.movie.start()

    def center(self):
        """让启动页居中屏幕"""
        screen_geometry = QApplication.primaryScreen().geometry()
        self.move(
            (screen_geometry.width() - self.width()) // 2,
            (screen_geometry.height() - self.height()) // 2
        )


class SplashWorker(QObject):
    # 定义信号：通知主线程关闭启动动画并显示主窗口
    finished = Signal()

    def run(self):
        # 模拟加载耗时（6秒），子线程中仅做非 UI 操作
        time.sleep(6)
        # 发送信号（触发主线程的槽函数）
        self.finished.emit()


class Windows(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("探索之路")
        self.setWindowIcon(QIcon("document/1.png"))
        self.resize(1000, 800)
        self.stack_layout = QStackedLayout()
        self.nav_buttons = dict()
        self.init_ui()

    def init_ui(self):
        # 顶层导航栏及其布局
        top_navigation_bar = QFrame(self)
        top_navigation_bar.setStyleSheet("background-color:#6A5ACD")
        top_navigation_bar.setFixedHeight(40)
        # 顶层导航栏关联内容区及其布局
        home_page = HomePage()
        self.stack_layout.addWidget(home_page)
        explore_page = ExplorePage()
        self.stack_layout.addWidget(explore_page)
        thought_page = ThoughtPage()
        self.stack_layout.addWidget(thought_page)
        note_page = NotePage()
        self.stack_layout.addWidget(note_page)
        tool_page = ToolPage()
        self.stack_layout.addWidget(tool_page)
        other_layout = OtherPage()
        self.stack_layout.addWidget(other_layout)
        # (在导航栏中添加按钮)
        top_navigation_layout = QHBoxLayout(top_navigation_bar)
        top_navigation_layout.setContentsMargins(0, 0, 0, 0)
        top_navigation_layout.setSpacing(0)
        navigation_btn = [
            ("首页", "home"),
            ("社会探索", "explore"),
            ("思路梳理", "thought"),
            ("笔记整理", "note"),
            ("工具", "tool"),
            ("其他", "other")
        ]
        for text, name in navigation_btn:
            btn = QPushButton(text, flat=True)
            btn.setFixedHeight(40)
            top_navigation_layout.addWidget(btn)
            self.nav_buttons[name] = btn

        self.nav_buttons["home"].clicked.connect(lambda:self.switch_page(0))
        self.nav_buttons["explore"].clicked.connect(lambda: self.switch_page(1))
        self.nav_buttons["thought"].clicked.connect(lambda: self.switch_page(2))
        self.nav_buttons["note"].clicked.connect(lambda: self.switch_page(3))
        self.nav_buttons["tool"].clicked.connect(lambda: self.switch_page(4))
        self.nav_buttons["other"].clicked.connect(lambda: self.switch_page(5))
        top_navigation_layout.addStretch(1)

        # 主窗口主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(top_navigation_bar)
        main_layout.addLayout(self.stack_layout)

    def switch_page(self, index):
        self.stack_layout.setCurrentIndex(index)
        # 高亮当前选中的按钮
        for i, (name, btn) in enumerate(self.nav_buttons.items()):
            if i == index:
                btn.setStyleSheet("background-color: #483D8B")
            else:
                btn.setStyleSheet("background-color: #6A5ACD")


class HomePage(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:white")


class ExplorePage(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:red")


class ThoughtPage(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:blue")


class NotePage(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:green")


class ToolPage(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:white")


class OtherPage(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:grey")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 启动动画
    splash = OpenMovie()
    splash.center()
    splash.show()

    worker = SplashWorker()
    thread = QThread()

    # 3. 连接信号槽：子线程完成后，主线程执行 UI 操作
    worker.finished.connect(splash.close)  # 关闭启动动画（主线程）
    worker.finished.connect(Windows().show)  # 显示主窗口（主线程）
    worker.finished.connect(thread.quit)  # 子线程结束后退出
    worker.finished.connect(worker.deleteLater)  # 释放工作对象
    thread.finished.connect(thread.deleteLater)  # 释放线程

    # 4. 移动工作对象到子线程，启动线程
    worker.moveToThread(thread)
    thread.started.connect(worker.run)  # 线程启动后执行 worker.run
    thread.start()

    sys.exit(app.exec())
