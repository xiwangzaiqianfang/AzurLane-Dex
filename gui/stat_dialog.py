from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class StatDialog(QDialog):
    def __init__(self, not_owned, not_max, parent=None):
        super().__init__(parent)
        self.setWindowTitle("统计结果")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"未获得舰船数: {not_owned}"))
        layout.addWidget(QLabel(f"已获得未满破舰船数: {not_max}"))
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)