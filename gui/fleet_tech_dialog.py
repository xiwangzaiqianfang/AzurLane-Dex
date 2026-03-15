from PySide6.QtWidgets import (QDialog, QVBoxLayout, QTabWidget, QTableWidget,
                               QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout)

class FleetTechDialog(QDialog):
    def __init__(self, camp_tech, global_bonuses, parent=None):
        super().__init__(parent)
        self.setWindowTitle("舰队科技")
        self.resize(600, 500)

        layout = QVBoxLayout(self)
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # 阵营科技点表格
        camp_tab = QTableWidget()
        camp_tab.setColumnCount(2)
        camp_tab.setHorizontalHeaderLabels(["阵营", "科技点总和"])
        camp_tab.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        camps = list(camp_tech.keys())
        camp_tab.setRowCount(len(camps))
        for row, camp in enumerate(camps):
            camp_tab.setItem(row, 0, QTableWidgetItem(camp))
            camp_tab.setItem(row, 1, QTableWidgetItem(str(camp_tech[camp])))
        tabs.addTab(camp_tab, "阵营科技点")

        # 全舰队属性加成表格
        bonus_tab = QTableWidget()
        bonus_tab.setColumnCount(2)
        bonus_tab.setHorizontalHeaderLabels(["加成项", "总值"])
        bonus_tab.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        items = [(f"{sc}-{attr}", value) for (sc, attr), value in global_bonuses.items()]
        bonus_tab.setRowCount(len(items))
        for row, (label, value) in enumerate(items):
            bonus_tab.setItem(row, 0, QTableWidgetItem(label))
            bonus_tab.setItem(row, 1, QTableWidgetItem(str(value)))
        tabs.addTab(bonus_tab, "全舰队加成")

        # 关闭按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)