from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLabel, QCheckBox, QSpinBox, QPushButton,
                               QGroupBox, QScrollArea, QGridLayout, QAbstractSpinBox)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap
import os

class DetailWidget(QWidget):
    data_changed = Signal(object)

    def __init__(self):
        super().__init__()
        self.current_ship = None
        self.setup_ui()

    def setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

        content = QWidget()
        scroll.setWidget(content)
        layout = QVBoxLayout(content)

        # ---- 立绘区域 ----
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(200)
        self.image_label.setStyleSheet("border: 1px solid gray;")
        layout.addWidget(self.image_label)

        # ---- 基本信息 ----
        basic_group = QGroupBox("基本信息")
        form = QFormLayout(basic_group)
        self.id_label = QLabel()
        self.name_label = QLabel()
        self.faction_label = QLabel()
        self.class_label = QLabel()
        self.rarity_label = QLabel()
        form.addRow("编号:", self.id_label)
        form.addRow("名称:", self.name_label)
        form.addRow("阵营:", self.faction_label)
        form.addRow("舰种:", self.class_label)
        form.addRow("稀有度:", self.rarity_label)
        layout.addWidget(basic_group)

        # ---- 状态操作 ----
        state_group = QGroupBox("状态")
        state_layout = QHBoxLayout(state_group)

        self.owned_cb = QCheckBox("已获得")
        #self.owned_cb.stateChanged.connect(self.on_owned_changed)
        self.owned_cb.clicked.connect(self.on_owned_clicked)

        self.breakthrough_layout = QHBoxLayout()
        self.breakthrough_spin = QSpinBox()
        self.breakthrough_spin.setRange(0, 3)
        self.breakthrough_spin.setSuffix(" 破")
        self.breakthrough_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.breakthrough_spin.valueChanged.connect(self.on_breakthrough_changed)
        self.breakthrough_minus = QPushButton("-")
        self.breakthrough_plus = QPushButton("+")
        self.breakthrough_minus.clicked.connect(lambda: self.breakthrough_spin.setValue(self.breakthrough_spin.value()-1))
        self.breakthrough_plus.clicked.connect(lambda: self.breakthrough_spin.setValue(self.breakthrough_spin.value()+1))
        self.breakthrough_layout.addWidget(self.breakthrough_minus)
        self.breakthrough_layout.addWidget(self.breakthrough_spin)
        self.breakthrough_layout.addWidget(self.breakthrough_plus)

        self.oath_cb = QCheckBox("已誓约")
        #self.oath_cb.stateChanged.connect(self.on_oath_changed)
        self.oath_cb.clicked.connect(self.on_oath_clicked)

        self.level120_cb = QCheckBox("120级")
        #self.level120_cb.stateChanged.connect(self.on_level120_changed)
        self.level120_cb.clicked.connect(self.on_level120_clicked)

        state_layout.addWidget(self.owned_cb)
        state_layout.addLayout(self.breakthrough_layout)
        state_layout.addWidget(self.oath_cb)
        state_layout.addWidget(self.level120_cb)
        state_layout.addStretch()
        layout.addWidget(state_group)

        # ---- 科技点 (动态计算总和) ----
        tech_group = QGroupBox("科技点总和 (获得+满破+120级)")
        tech_layout = QGridLayout(tech_group)

        self.tech_labels = {}  # 存储每个科技项的QLabel

        tech_list = [
            ("耐久", "tech_durability"),
            ("炮击", "tech_firepower"),
            ("雷击", "tech_torpedo"),
            ("防空", "tech_aa"),
            ("航空", "tech_aviation"),
            ("命中", "tech_accuracy"),
            ("装填", "tech_reload"),
            ("机动", "tech_mobility"),
            ("反潜", "tech_antisub")
        ]

        for i, (display_name, base_name) in enumerate(tech_list):
            row = i // 3
            col = (i % 3) * 2
            label_name = QLabel(display_name + ":")
            label_value = QLabel("0")
            label_value.setAlignment(Qt.AlignRight)
            tech_layout.addWidget(label_name, row, col)
            tech_layout.addWidget(label_value, row, col+1)
            self.tech_labels[base_name] = label_value

        layout.addWidget(tech_group)

        # ---- 获取方式 ----
        acquire_group = QGroupBox("获取方式")
        acquire_form = QFormLayout(acquire_group)
        self.acquire_main_label = QLabel()
        self.acquire_detail_label = QLabel()
        self.build_time_label = QLabel()
        self.drop_locations_label = QLabel()
        self.shop_exchange_label = QLabel()
        self.permanent_label = QLabel()
        acquire_form.addRow("主要获取:", self.acquire_main_label)
        acquire_form.addRow("详细信息:", self.acquire_detail_label)
        acquire_form.addRow("建造时间:", self.build_time_label)
        acquire_form.addRow("打捞地点:", self.drop_locations_label)
        acquire_form.addRow("商店兑换:", self.shop_exchange_label)
        acquire_form.addRow("是否常驻:", self.permanent_label)
        layout.addWidget(acquire_group)

        # ---- 实装活动 ----
        event_group = QGroupBox("实装活动")
        event_form = QFormLayout(event_group)
        self.debut_label = QLabel()
        self.release_date_label = QLabel()
        self.notes_label = QLabel()
        event_form.addRow("首次登场:", self.debut_label)
        event_form.addRow("实装时间:", self.release_date_label)
        event_form.addRow("备注:", self.notes_label)
        layout.addWidget(event_group)

        # 编辑按钮（简化）
        self.edit_btn = QPushButton("编辑详细信息")
        self.edit_btn.clicked.connect(self.open_edit_dialog)
        layout.addWidget(self.edit_btn)

        layout.addStretch()

    def set_ship(self, ship):
        self.current_ship = ship
        self.update_display()

    def clear(self):
        self.current_ship = None
        self.id_label.clear()
        self.name_label.clear()
        self.faction_label.clear()
        self.class_label.clear()
        self.rarity_label.clear()
        self.owned_cb.setChecked(False)
        self.oath_cb.setChecked(False)
        self.level120_cb.setChecked(False)
        self.breakthrough_spin.setValue(0)
        for label in self.tech_labels.values():
            label.setText("0")
        self.acquire_main_label.clear()
        self.acquire_detail_label.clear()
        self.build_time_label.clear()
        self.drop_locations_label.clear()
        self.shop_exchange_label.clear()
        self.permanent_label.clear()
        self.debut_label.clear()
        self.release_date_label.clear()
        self.notes_label.clear()
        self.image_label.clear()

    def update_display(self):
        if not self.current_ship:
            return
        s = self.current_ship
        print(f"update_display: ship {s.id}, owned={s.owned}, oath={s.oath}, level120={s.level_120}, bt={s.breakthrough}")

        self.id_label.setText(str(s.id))
        self.name_label.setText(s.name)
        self.faction_label.setText(s.faction)
        self.class_label.setText(s.ship_class)
        self.rarity_label.setText(s.rarity)

        # 状态
        self.owned_cb.setChecked(s.owned)
        self.oath_cb.setChecked(s.oath)
        self.level120_cb.setChecked(s.level_120)
        self.breakthrough_spin.setValue(s.breakthrough)

        # 科技点：动态计算总和
        tech_bases = [
            "tech_durability", "tech_firepower", "tech_torpedo", "tech_aa",
            "tech_aviation", "tech_accuracy", "tech_reload", "tech_mobility", "tech_antisub"
        ]
        for base in tech_bases:
            total = s.get_tech_total(base)
            self.tech_labels[base].setText(str(total))

        # 获取方式
        self.acquire_main_label.setText(s.acquire_main)
        self.acquire_detail_label.setText(s.acquire_detail)
        self.build_time_label.setText(s.build_time)
        self.drop_locations_label.setText(", ".join(s.drop_locations))
        self.shop_exchange_label.setText(s.shop_exchange)
        self.permanent_label.setText("是" if s.is_permanent else "否")

        # 实装活动
        self.debut_label.setText(s.debut_event)
        self.release_date_label.setText(s.release_date)
        self.notes_label.setText(s.notes)

        # 立绘
        if s.image_path and os.path.exists(s.image_path):
            pixmap = QPixmap(s.image_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_label.setPixmap(pixmap)
            else:
                self.image_label.setText("图片无法加载")
        else:
            self.image_label.setText("无立绘")

    def on_owned_clicked(self, checked):
        if not self.current_ship:
            return
        #print(f"on_owned_clicked: ship {self.current_ship.id}, checked={checked}")
        self.current_ship.owned = checked
        if not checked:  # 取消拥有时清零突破
            # 临时阻塞突破数信号，避免触发 on_breakthrough_changed
            self.breakthrough_spin.blockSignals(True)
            self.current_ship.breakthrough = 0
            self.breakthrough_spin.setValue(0)
            self.breakthrough_spin.blockSignals(False)
        self.data_changed.emit(self.current_ship)

    def on_breakthrough_changed(self, value):
        if self.current_ship:
            self.current_ship.breakthrough = value
            #print(f"on_breakthrough_changed: ship {self.current_ship.id}, breakthrough={value}")
            self.data_changed.emit(self.current_ship)

    def on_oath_clicked(self, checked):
        if self.current_ship:
            self.current_ship.oath = checked
            self.data_changed.emit(self.current_ship)

    def on_level120_clicked(self, checked):
        if self.current_ship:
            self.current_ship.level_120 = checked
            self.data_changed.emit(self.current_ship)

    def open_edit_dialog(self):
        # 可以扩展为编辑科技点等详细信息的对话框
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "提示", "编辑功能可通过直接修改 JSON 文件实现。")