from PySide6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QCheckBox, QPushButton, QLabel
from PySide6.QtCore import Signal

class FilterBar(QWidget):
    filter_changed = Signal(dict)
    reset_clicked = Signal()
    stat_clicked = Signal()
    add_ship_clicked = Signal()
    switch_file_clicked = Signal()
    export_clicked = Signal()
    import_clicked = Signal()
    update_online_clicked = Signal()

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # 阵营
        layout.addWidget(QLabel("阵营:"))
        self.faction_combo = QComboBox()
        self.faction_combo.addItems(["全部", "白鹰", "皇家", "重樱", "铁血", "东煌", "撒丁", "北方联合", "鸢尾", "维希教廷", "META"])
        self.faction_combo.currentTextChanged.connect(self.on_filter_changed)
        layout.addWidget(self.faction_combo)

        # 舰种
        layout.addWidget(QLabel("舰种:"))
        self.class_combo = QComboBox()
        self.class_combo.addItems(["全部", "驱逐", "轻巡", "重巡", "超巡", "战巡", "战列", "航母", "轻航", "航战", "重炮", "维修", "潜艇", "潜母", "工作舰"])
        self.class_combo.currentTextChanged.connect(self.on_filter_changed)
        layout.addWidget(self.class_combo)

        # 稀有度
        layout.addWidget(QLabel("稀有度:"))
        self.rarity_combo = QComboBox()
        self.rarity_combo.addItems(["全部", "普通", "稀有", "精锐", "超稀有", "海上传奇"])
        self.rarity_combo.currentTextChanged.connect(self.on_filter_changed)
        layout.addWidget(self.rarity_combo)

        # 复选框
        self.remodel_cb = QCheckBox("可改造")
        self.remodel_cb.stateChanged.connect(self.on_filter_changed)
        layout.addWidget(self.remodel_cb)

        self.oath_cb = QCheckBox("已誓约")
        self.oath_cb.stateChanged.connect(self.on_filter_changed)
        layout.addWidget(self.oath_cb)

        self.owned_cb = QCheckBox("已获得")
        self.owned_cb.stateChanged.connect(self.on_filter_changed)
        layout.addWidget(self.owned_cb)

        self.max_cb = QCheckBox("已满破")
        self.max_cb.stateChanged.connect(self.on_filter_changed)
        layout.addWidget(self.max_cb)

        self.level120_cb = QCheckBox("120级")
        self.level120_cb.stateChanged.connect(self.on_filter_changed)
        layout.addWidget(self.level120_cb)

        # 按钮
        self.reset_btn = QPushButton("重置")
        self.reset_btn.clicked.connect(self.reset_clicked)
        layout.addWidget(self.reset_btn)

        self.stat_btn = QPushButton("一键统计")
        self.stat_btn.clicked.connect(self.stat_clicked)
        layout.addWidget(self.stat_btn)

        self.add_btn = QPushButton("新增舰船")
        self.add_btn.clicked.connect(self.add_ship_clicked)
        layout.addWidget(self.add_btn)

        self.switch_btn = QPushButton("切换账号")
        self.switch_btn.clicked.connect(self.switch_file_clicked)
        layout.addWidget(self.switch_btn)

        self.export_btn = QPushButton("导出")
        self.export_btn.clicked.connect(self.export_clicked)
        layout.addWidget(self.export_btn)

        self.import_btn = QPushButton("导入")
        self.import_btn.clicked.connect(self.import_clicked)
        layout.addWidget(self.import_btn)

        self.update_btn = QPushButton("网络更新")
        self.update_btn.clicked.connect(self.update_online_clicked)
        layout.addWidget(self.update_btn)

        layout.addStretch()

        #print("复选框互斥状态：")
        #for cb in [self.remodel_cb, self.oath_cb, self.owned_cb, self.max_cb, self.level120_cb]:
        # print(f"{cb.text()}: autoExclusive={cb.autoExclusive()}")

    def on_filter_changed(self):
        criteria = {}
        if self.faction_combo.currentText() != "全部":
            criteria['faction'] = self.faction_combo.currentText()
        if self.class_combo.currentText() != "全部":
            criteria['ship_class'] = self.class_combo.currentText()
        if self.rarity_combo.currentText() != "全部":
            criteria['rarity'] = self.rarity_combo.currentText()
        if self.remodel_cb.isChecked():
            criteria['can_remodel'] = True
        if self.oath_cb.isChecked():
            criteria['oath'] = True
        if self.owned_cb.isChecked():
            criteria['owned'] = True
        if self.max_cb.isChecked():
            criteria['max_breakthrough'] = True
        if self.level120_cb.isChecked():
            criteria['level_120'] = True
        self.filter_changed.emit(criteria)

    def reset(self):
        self.faction_combo.setCurrentText("全部")
        self.class_combo.setCurrentText("全部")
        self.rarity_combo.setCurrentText("全部")
        self.remodel_cb.setChecked(False)
        self.oath_cb.setChecked(False)
        self.owned_cb.setChecked(False)
        self.max_cb.setChecked(False)
        self.level120_cb.setChecked(False)

    def get_criteria(self):
        # 返回当前筛选条件字典，用于刷新时重新应用
        criteria = {}
        if self.faction_combo.currentText() != "全部":
            criteria['faction'] = self.faction_combo.currentText()
        if self.class_combo.currentText() != "全部":
            criteria['ship_class'] = self.class_combo.currentText()
        if self.rarity_combo.currentText() != "全部":
            criteria['rarity'] = self.rarity_combo.currentText()
        if self.remodel_cb.isChecked():
            criteria['can_remodel'] = True
        if self.oath_cb.isChecked():
            criteria['oath'] = True
        if self.owned_cb.isChecked():
            criteria['owned'] = True
        if self.max_cb.isChecked():
            criteria['max_breakthrough'] = True
        if self.level120_cb.isChecked():
            criteria['level_120'] = True
        return criteria