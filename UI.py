import MetaTrader5 as mt5
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QCheckBox
from PyQt5.QtCore import Qt
import sys
from UI_helper_functions import place_trade, exit_all_trades


def on_dax_buy_click():
    place_trade("DE40", mt5.ORDER_TYPE_BUY)


def on_dax_sell_click():
    place_trade("DE40", mt5.ORDER_TYPE_SELL)


def on_ndx_buy_click():
    place_trade("USTEC", mt5.ORDER_TYPE_BUY)


def on_ndx_sell_click():
    place_trade("USTEC", mt5.ORDER_TYPE_SELL)


def on_exit_all_trades_click():
    exit_all_trades()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.exit_trade_button = None
        self.exit_all_trades_button = None
        self.enable_exit_all_trades_button = None
        self.enable_exit_all_trades_checkbox = None
        self.enable_ndx_sell_checkbox = None
        self.enable_ndx_buy_checkbox = None
        self.enable_dax_sell_checkbox = None
        self.enable_dax_buy_checkbox = None
        self.ndx_buy_button = None
        self.ndx_sell_button = None
        self.dax_buy_button = None
        self.dax_sell_button = None
        self.setWindowTitle('Stock Trading Panel')
        self.init_UI()

    def init_UI(self):

        self.setGeometry(300, 300, 560, 100)

        self.ndx_buy_button, self.ndx_sell_button = self.create_buy_sell_buttons()
        self.ndx_buy_button.clicked.connect(on_ndx_buy_click)
        self.ndx_buy_button.setFixedSize(70, 30)
        self.ndx_sell_button.clicked.connect(on_ndx_sell_click)
        self.ndx_sell_button.setFixedSize(70, 30)

        ndx_layout = self.set_button_layout('NDX', (2, 4), self.ndx_buy_button, self.ndx_sell_button)

        self.dax_buy_button, self.dax_sell_button = self.create_buy_sell_buttons()
        self.dax_buy_button.clicked.connect(on_dax_buy_click)
        self.dax_buy_button.setFixedSize(70, 30)
        self.dax_sell_button.clicked.connect(on_dax_sell_click)
        self.dax_sell_button.setFixedSize(70, 30)

        dax_layout = self.set_button_layout('DAX', (2, 4), self.dax_buy_button, self.dax_sell_button)

        dax_button_checkbox_layout = QVBoxLayout()
        self.enable_dax_buy_checkbox = QCheckBox('Enable DAX Buy', self)  # Checkbox to enable buying on DAX
        self.enable_dax_buy_checkbox.stateChanged.connect(lambda state: self.on_checkbox_dax_buy_state_changed(state))
        dax_button_checkbox_layout.insertWidget(0, self.enable_dax_buy_checkbox)

        self.enable_dax_sell_checkbox = QCheckBox('Enable Dax Sell', self)  # Checkbox to enable selling on DAX
        self.enable_dax_sell_checkbox.stateChanged.connect(lambda state: self.on_checkbox_dax_sell_state_changed(state))
        dax_button_checkbox_layout.insertWidget(1, self.enable_dax_sell_checkbox)

        ndx_button_checkbox_layout = QVBoxLayout()
        self.enable_ndx_buy_checkbox = QCheckBox('Enable NDX Buy', self)  # Checkbox to enable buying on Nasdaq
        self.enable_ndx_buy_checkbox.stateChanged.connect(lambda state: self.on_checkbox_ndx_buy_state_changed(state))
        ndx_button_checkbox_layout.insertWidget(0, self.enable_ndx_buy_checkbox)

        self.enable_ndx_sell_checkbox = QCheckBox('Enable NDX Sell', self)  # Checkbox to enable selling on Nasdaq
        self.enable_ndx_sell_checkbox.stateChanged.connect(lambda state: self.on_checkbox_ndx_sell_state_changed(state))
        ndx_button_checkbox_layout.insertWidget(1, self.enable_ndx_sell_checkbox)

        exit_trade_button_checkbox_layout = QHBoxLayout()  # Checkbox to exit all trades
        self.enable_exit_all_trades_checkbox = QCheckBox('Enable ability to exit all trades', self)
        self.enable_exit_all_trades_checkbox.stateChanged.connect(lambda state: self.on_checkbox_exit_all_trades_state_changed(state))
        exit_trade_button_checkbox_layout.insertWidget(0, self.enable_exit_all_trades_checkbox)
        self.exit_trade_button = QPushButton('Exit all trades', self)
        self.exit_trade_button.clicked.connect(on_exit_all_trades_click)
        exit_trade_button_checkbox_layout.insertWidget(1, self.exit_trade_button)

        self.exit_all_trades_button = QHBoxLayout()

        self.disable_all_buttons()

        self.set_ndx_style()
        self.set_dax_style()
        hbox = QHBoxLayout()

        hbox.addLayout(ndx_layout)
        hbox.addLayout(ndx_button_checkbox_layout)
        hbox.addLayout(dax_layout)
        hbox.addLayout(dax_button_checkbox_layout)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(exit_trade_button_checkbox_layout)
        self.setLayout(vbox)
        self.show()

    def create_buy_sell_buttons(self):
        buy_button = QPushButton('Buy', self)
        sell_button = QPushButton('Sell', self)
        return buy_button, sell_button

    def on_checkbox_exit_all_trades_state_changed(self, state):
        if state == Qt.Checked:
            self.dax_buy_button.setEnabled(True)
        else:
            self.dax_buy_button.setEnabled(False)

    def on_checkbox_dax_buy_state_changed(self, state):
        if state == Qt.Checked:
            self.dax_buy_button.setEnabled(True)
        else:
            self.dax_buy_button.setEnabled(False)

    def on_checkbox_dax_sell_state_changed(self, state):
        if state == Qt.Checked:
            self.dax_sell_button.setEnabled(True)
        else:
            self.dax_sell_button.setEnabled(False)

    def on_checkbox_ndx_buy_state_changed(self, state):
        if state == Qt.Checked:
            self.ndx_buy_button.setEnabled(True)
        else:
            self.ndx_buy_button.setEnabled(False)

    def on_checkbox_ndx_sell_state_changed(self, state):
        if state == Qt.Checked:
            self.ndx_sell_button.setEnabled(True)
        else:
            self.ndx_sell_button.setEnabled(False)

    def disable_all_buttons(self):
        self.dax_buy_button.setEnabled(False)
        self.dax_sell_button.setEnabled(False)
        self.ndx_buy_button.setEnabled(False)
        self.ndx_sell_button.setEnabled(False)

    def set_button_layout(self, market, location_numbers, buy_button, sell_button):
        layout = QVBoxLayout()
        label = QLabel(market, self)
        label.setStyleSheet("""
          QLabel {
              font-size: 20px;
              font-weight: bold;
              color: #333;
          }
        """)
        layout.addWidget(label)
        layout.addWidget(buy_button)
        layout.addWidget(sell_button)
        layout.setAlignment(Qt.AlignCenter)
        layout.insertSpacerItem(location_numbers[0], QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))
        layout.insertSpacerItem(location_numbers[1], QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        return layout

    def set_ndx_style(self):
        self.ndx_buy_button.setStyleSheet(
            """
            QPushButton {
               background-color: #007BFF;
               color: white;
               border-radius: 5px;
               padding: 5px;
            }
            QPushButton:hover {
               background-color: #0056b3;
            }
            QPushButton:pressed {
               background-color: #004085;
            }
            """)

        self.ndx_sell_button.setStyleSheet(
            """
            QPushButton {
               background-color: #DC3545;
               color: white;
               border-radius: 5px;
               padding: 5px;
            }
            QPushButton:hover {
               background-color: #c82333;
            }
            QPushButton:pressed {
               background-color: #bd2130;
            }
            """)

    def set_dax_style(self):
        self.dax_buy_button.setStyleSheet(
            """
            QPushButton {
               background-color: #007BFF;
               color: white;
               border-radius: 5px;
               padding: 5px;
            }
            QPushButton:hover {
               background-color: #0056b3;
            }
            QPushButton:pressed {
               background-color: #004085;
            }
            """)

        self.dax_sell_button.setStyleSheet(
            """
            QPushButton {
               background-color: #DC3545;
               color: white;
               border-radius: 5px;
               padding: 5px;
            }
            QPushButton:hover {
               background-color: #c82333;
            }
            QPushButton:pressed {
               background-color: #bd2130;
            }
            """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
