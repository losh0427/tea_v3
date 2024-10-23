import sys
import time
import ui2model
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLineEdit,
    QHBoxLayout,
    QProgressBar,
    QMessageBox,
)
from PyQt6.QtGui import QPixmap, QImage, QFont, QDoubleValidator
from PyQt6.QtCore import Qt, QTimer
from os import getcwd


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.CURRENT_PATH = getcwd().replace("\\", "/")

        self.setWindowTitle("茶葉計畫")

        self.FONT = QFont("微軟正黑體", 14)
        self.SMALL_FONT = QFont("微軟正黑體", 10)
        ENTRY_WIDTH = 10

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        self.global_layout = QHBoxLayout()
        main_widget.setLayout(self.global_layout)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.global_layout.addLayout(self.layout)

        # logo
        logo_frame = QHBoxLayout()
        self.layout.addLayout(logo_frame)
        logo_frame.addStretch()
        img = QImage(self.CURRENT_PATH + "/logo.png")
        pixmap = QPixmap(img.scaled(80, 240, Qt.AspectRatioMode.KeepAspectRatio))
        self.logo_label = QLabel()
        self.logo_label.setPixmap(pixmap)
        logo_frame.addWidget(self.logo_label)
        logo_frame.addStretch()

        # limit

        bound_setting_layout = QHBoxLayout()
        self.layout.addLayout(bound_setting_layout)
        bound_setting_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        bound_setting_layout_left = QVBoxLayout()
        bound_setting_layout.addLayout(bound_setting_layout_left)
        bound_setting_layout_mid = QVBoxLayout()
        bound_setting_layout.addLayout(bound_setting_layout_mid)
        bound_setting_layout_right = QVBoxLayout()
        bound_setting_layout.addLayout(bound_setting_layout_right)

        bound_setting_layout_left.addWidget(QLabel("變量", font=self.FONT))
        bound_setting_layout_mid.addWidget(QLabel("上界", font=self.FONT))
        bound_setting_layout_right.addWidget(QLabel("下界", font=self.FONT))

        data_name = [
            "Power",
            "Position",
        ]
        self.upper_bound_entry = []
        self.lower_bound_entry = []
        data_default = [[500, 900], [-100, 100]]
        for i in range(2):
            bound_setting_layout_left.addWidget(QLabel(data_name[i], font=self.FONT))
            self.upper_bound_entry.append(QLineEdit())
            self.upper_bound_entry[i].setText(str(data_default[i][0]))
            self.upper_bound_entry[i].setFont(self.FONT)
            self.upper_bound_entry[i].setFixedWidth(ENTRY_WIDTH * 15)
            self.upper_bound_entry[i].setValidator(QDoubleValidator())
            bound_setting_layout_mid.addWidget(self.upper_bound_entry[i])
            self.lower_bound_entry.append(QLineEdit())
            self.lower_bound_entry[i].setText(str(data_default[i][1]))
            self.lower_bound_entry[i].setFont(self.FONT)
            self.lower_bound_entry[i].setFixedWidth(ENTRY_WIDTH * 15)
            self.lower_bound_entry[i].setValidator(QDoubleValidator())
            bound_setting_layout_right.addWidget(self.lower_bound_entry[i])

        # 材料
        material_frame = QHBoxLayout()
        self.layout.addLayout(material_frame)
        material_frame.addWidget(QLabel("材料係數設定:", font=self.FONT))
        self.material_entry = QLineEdit()
        self.material_entry.setText("0.95")
        self.material_entry.setFont(self.FONT)
        self.material_entry.setFixedWidth(ENTRY_WIDTH * 15)
        self.material_entry.setValidator(QDoubleValidator())
        material_frame.addWidget(self.material_entry)
        material_frame.addWidget(QLabel("熱電轉換係數:", font=self.FONT))
        self.ETconvert_entry = QLineEdit()
        self.ETconvert_entry.setText("100000")
        self.ETconvert_entry.setFont(self.FONT)
        self.ETconvert_entry.setFixedWidth(ENTRY_WIDTH * 15)
        self.ETconvert_entry.setValidator(QDoubleValidator())
        material_frame.addWidget(self.ETconvert_entry)

        # 輸入
        input_frame = QHBoxLayout()
        self.layout.addLayout(input_frame)
        input_frame.addWidget(QLabel("秒數:", font=self.FONT))
        self.seconds_entry = QLineEdit()
        self.seconds_entry.setText("3")
        self.seconds_entry.setFont(self.FONT)
        self.seconds_entry.setFixedWidth(ENTRY_WIDTH * 15)
        self.seconds_entry.setValidator(QDoubleValidator())
        input_frame.addWidget(self.seconds_entry)
        input_frame.addWidget(QLabel("搜索次數:", font=self.FONT))
        self.runs_entry = QLineEdit()
        self.runs_entry.setText("5")
        self.runs_entry.setFont(self.FONT)
        self.runs_entry.setFixedWidth(ENTRY_WIDTH * 15)
        self.runs_entry.setValidator(QDoubleValidator())
        input_frame.addWidget(self.runs_entry)

        # 計算按鈕
        self.calculate_button = QPushButton("計算")
        self.calculate_button.setFont(self.FONT)
        self.layout.addWidget(self.calculate_button)
        self.calculate_button.clicked.connect(self.calculate)

        # 確認按鈕
        self.confirm_button = QPushButton("確認", self)
        self.confirm_button.setFont(self.FONT)
        self.layout.addWidget(self.confirm_button)
        self.confirm_button.clicked.connect(self.show_message_and_hide_button)
        self.confirm_button.setVisible(False)

        # 進度條
        style = """
            QProgressBar {
                text-align:center;
            }
        """
        self.progress_bar = QProgressBar()
        self.progress_bar.setFormat("%v/%m")
        self.progress_bar.setStyleSheet(style)
        self.layout.addWidget(self.progress_bar)
        self.progress_bar.hide()
        self.eta_label = QLabel()
        self.layout.addWidget(self.eta_label)

        # Objective Value Trend
        self.obj_val_label = QLabel("Objective Value Trend")
        self.obj_val_label.setFont(self.FONT)
        self.layout.addWidget(self.obj_val_label)
        self.obj_val_trend_figure = QLabel()
        self.obj_val_trend_figure.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.obj_val_trend_figure)
        self.obj_val_trend_figure_path = QLabel()
        self.obj_val_trend_figure_path.setFont(self.SMALL_FONT)
        self.layout.addWidget(self.obj_val_trend_figure_path)

        self.obj_val_label.setVisible(False)
        self.obj_val_trend_figure.setVisible(False)
        self.obj_val_trend_figure_path.setVisible(False)

        # 右半邊
        output_layout = QVBoxLayout()
        self.global_layout.addLayout(output_layout)

        # 輸出數值
        self.output_text_layout = QVBoxLayout()
        output_layout.addLayout(self.output_text_layout)

        output_label = QLabel("輸出數值:")
        output_label.setFont(self.FONT)
        self.output_text_layout.addWidget(output_label)
        self.output_label = QLabel()
        self.output_label.setFont(self.SMALL_FONT)
        self.output_text_layout.addWidget(self.output_label)

        for i in range(self.output_text_layout.count()):
            widget = self.output_text_layout.itemAt(i).widget()
            if widget is not None:
                widget.setVisible(False)

        # 圖表
        self.figure_layout = QVBoxLayout()
        output_layout.addLayout(self.figure_layout)

        self.electric_figure_text_layout = QHBoxLayout()
        self.figure_layout.addLayout(self.electric_figure_text_layout)

        self.electric_figure_label_title = QLabel("電場")
        self.electric_figure_label_title.setFont(self.FONT)
        self.electric_figure_text_layout.addWidget(self.electric_figure_label_title)

        self.electric_figure_label_path = QLabel()
        self.electric_figure_label_path.setFont(self.SMALL_FONT)
        self.electric_figure_text_layout.addWidget(self.electric_figure_label_path)
        self.electric_figure_label_path.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.electric_figure_label = QLabel()
        self.figure_layout.addWidget(self.electric_figure_label)

        self.heat_figure_text_layout = QHBoxLayout()
        self.figure_layout.addLayout(self.heat_figure_text_layout)

        self.heat_figure_label_title = QLabel("熱場")
        self.heat_figure_label_title.setFont(self.FONT)
        self.heat_figure_text_layout.addWidget(self.heat_figure_label_title)

        self.heat_figure_label_path = QLabel()
        self.heat_figure_label_path.setFont(self.SMALL_FONT)
        self.heat_figure_text_layout.addWidget(self.heat_figure_label_path)
        self.heat_figure_label_path.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.heat_figure_label = QLabel()
        self.figure_layout.addWidget(self.heat_figure_label)

        self.electric_figure_label_title.setVisible(False)
        self.electric_figure_label.setVisible(False)
        self.heat_figure_label_title.setVisible(False)
        self.heat_figure_label.setVisible(False)
        self.electric_figure_label_path.setVisible(False)
        self.heat_figure_label_path.setVisible(False)

        window_size = self.size()
        self.init_width = window_size.width()
        self.init_height = window_size.height()

    def show_message_and_hide_button(self):
        self.confirm_button.setVisible(False)
        self.calculate_button.setEnabled(True)
        self.eta_label.setVisible(False)
        for i in range(self.output_text_layout.count()):
            widget = self.output_text_layout.itemAt(i).widget()
            if widget is not None:
                widget.setVisible(False)
        self.electric_figure_label_title.setVisible(False)
        self.electric_figure_label.setVisible(False)
        self.heat_figure_label_title.setVisible(False)
        self.heat_figure_label.setVisible(False)
        self.electric_figure_label_path.setVisible(False)
        self.heat_figure_label_path.setVisible(False)

    def doUpdateProgressBar(self, i):
        # update trend
        self.obj_val_label.setVisible(True)
        self.obj_val_trend_figure.setVisible(True)
        self.obj_val_trend_figure_path.setVisible(True)

        trend_figure_path = ui2model.getTrendFigurePath(self.CURRENT_PATH)
        self.obj_val_trend_figure_path.setText(trend_figure_path)

        pixmap = QPixmap()
        pixmap.load(trend_figure_path)
        pixmap = pixmap.scaled(388, 300)

        self.obj_val_trend_figure.setPixmap(pixmap)

        # update progress bar
        self.progress_bar.setValue(i + 1)
        elapsed_time = time.time() - self.start_time
        eta_seconds = (elapsed_time / (i + 1)) * (self.iteration - i - 1)
        hours, remainder = divmod(eta_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        eta_str = f"預計完成時間: {int(hours)}小時 {int(minutes)}分 {int(seconds)}秒            "
        self.eta_label.setText(eta_str)

        QApplication.processEvents()

    def doOutputResult(
        self, heat_path, electric_path, e_avg, h_avg, e_std, h_std, max_id
    ):
        self.eta_label.setText("已完成")
        self.output_label.setText(
            f"電場平均:{e_avg}\t熱場平均:{h_avg}\tmax_id:{max_id}\n電場標準差:{e_std}\t熱場標準差:{h_std}"
        )
        self.heat_figure_label_path.setText(heat_path)
        self.electric_figure_label_path.setText(electric_path)
        self.progress_bar.hide()

        pixmap = QPixmap()
        pixmap.load(electric_path)
        pixmap = pixmap.scaled(388, 300)
        self.electric_figure_label.setPixmap(pixmap)

        pixmap = QPixmap()
        pixmap.load(heat_path)
        pixmap = pixmap.scaled(388, 300)

        self.heat_figure_label.setPixmap(pixmap)

        self.electric_figure_label_title.setVisible(True)
        self.electric_figure_label.setVisible(True)
        self.heat_figure_label_title.setVisible(True)
        self.heat_figure_label.setVisible(True)
        self.electric_figure_label_path.setVisible(True)
        self.heat_figure_label_path.setVisible(True)

        self.confirm_button.setVisible(True)
        for i in range(self.output_text_layout.count()):
            widget = self.output_text_layout.itemAt(i).widget()
            if widget is not None:
                widget.setVisible(True)

    def calculate(self):
        self.calculate_button.setEnabled(False)

        iter_txt = self.runs_entry.text()
        seconds_need = self.seconds_entry.text()
        seconds_need = 3 if seconds_need == "" else round(float(seconds_need))
        material_coefficient = self.material_entry.text()
        material_coefficient = (
            0.95 if material_coefficient == "" else float(material_coefficient)
        )
        ETconvert_coefficient = self.ETconvert_entry.text()
        ETconvert_coefficient = (
            100000 if ETconvert_coefficient == "" else float(ETconvert_coefficient)
        )

        if iter_txt == "":
            iter_txt = "5"
        self.iteration = int(iter_txt)

        data_limit = []
        for i in range(2):
            data_limit.append(
                [
                    float(self.upper_bound_entry[i].text()),
                    float(self.lower_bound_entry[i].text()),
                ]
            )

        self.progress_bar.show()
        self.progress_bar.setValue(0)
        self.progress_bar.setRange(0, self.iteration)
        self.eta_label.setVisible(True)

        self.start_time = time.time()

        # running
        ui2model.run(
            self.iteration,
            material_coefficient,
            ETconvert_coefficient,
            seconds_need,
            data_limit,
            self.doUpdateProgressBar,
        )
        ui2model.getResult(self.doOutputResult, self.CURRENT_PATH)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()

    sys.exit(app.exec())
