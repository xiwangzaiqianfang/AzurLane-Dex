from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class StatDialog(QDialog):
    def __init__(self, stats_dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("统计结果")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"总计舰船数: {stats_dict['total']}"))
        layout.addWidget(QLabel(f"已获得: {stats_dict['owned']}"))
        layout.addWidget(QLabel(f"未获得: {stats_dict['not_owned']}"))
        layout.addWidget(QLabel(f"已满破: {stats_dict['max_break']}"))
        layout.addWidget(QLabel(f"未满破: {stats_dict['not_max']}"))
        layout.addWidget(QLabel(f"已誓约: {stats_dict['oath']}"))
        layout.addWidget(QLabel(f"已改造: {stats_dict['remodeled']}"))
        layout.addWidget(QLabel(f"可改造未改造: {stats_dict['can_remodel_not']}"))
        layout.addWidget(QLabel(f"120级: {stats_dict['level120']}"))
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)