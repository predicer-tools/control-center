# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QProgressBar, QSizePolicy,
    QSpacerItem, QSpinBox, QStatusBar, QTabWidget,
    QTextBrowser, QToolButton, QTreeView, QVBoxLayout,
    QWidget)
from . import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(942, 722)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ApplicationExit))
        self.actionQuit.setIcon(icon)
        self.actionQuit.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_16 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_5 = QVBoxLayout(self.tab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_2 = QGroupBox(self.tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_21 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.toolButton_start_master_loop = QToolButton(self.groupBox_2)
        self.toolButton_start_master_loop.setObjectName(u"toolButton_start_master_loop")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart))
        self.toolButton_start_master_loop.setIcon(icon1)
        self.toolButton_start_master_loop.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.horizontalLayout_21.addWidget(self.toolButton_start_master_loop)

        self.toolButton_stop_master_loop = QToolButton(self.groupBox_2)
        self.toolButton_stop_master_loop.setObjectName(u"toolButton_stop_master_loop")
        self.toolButton_stop_master_loop.setEnabled(False)
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStop))
        self.toolButton_stop_master_loop.setIcon(icon2)
        self.toolButton_stop_master_loop.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolButton_stop_master_loop.setArrowType(Qt.ArrowType.NoArrow)

        self.horizontalLayout_21.addWidget(self.toolButton_stop_master_loop)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_2)

        self.label_current_task = QLabel(self.groupBox_2)
        self.label_current_task.setObjectName(u"label_current_task")

        self.horizontalLayout_21.addWidget(self.label_current_task)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_4)


        self.verticalLayout_5.addWidget(self.groupBox_2)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.groupBox_4 = QGroupBox(self.tab)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.toolButton_start_hertta_server = QToolButton(self.groupBox_4)
        self.toolButton_start_hertta_server.setObjectName(u"toolButton_start_hertta_server")
        self.toolButton_start_hertta_server.setIcon(icon1)

        self.horizontalLayout_5.addWidget(self.toolButton_start_hertta_server)

        self.progressBar_hertta_status = QProgressBar(self.groupBox_4)
        self.progressBar_hertta_status.setObjectName(u"progressBar_hertta_status")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar_hertta_status.sizePolicy().hasHeightForWidth())
        self.progressBar_hertta_status.setSizePolicy(sizePolicy)
        self.progressBar_hertta_status.setMaximum(1)
        self.progressBar_hertta_status.setValue(-1)
        self.progressBar_hertta_status.setTextVisible(False)
        self.progressBar_hertta_status.setInvertedAppearance(False)

        self.horizontalLayout_5.addWidget(self.progressBar_hertta_status)

        self.label_hertta_server_status = QLabel(self.groupBox_4)
        self.label_hertta_server_status.setObjectName(u"label_hertta_server_status")

        self.horizontalLayout_5.addWidget(self.label_hertta_server_status)


        self.verticalLayout_7.addLayout(self.horizontalLayout_5)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_10 = QLabel(self.groupBox_4)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_8.addWidget(self.label_10)

        self.spinBox_time_line_step = QSpinBox(self.groupBox_4)
        self.spinBox_time_line_step.setObjectName(u"spinBox_time_line_step")
        self.spinBox_time_line_step.setFrame(False)
        self.spinBox_time_line_step.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.spinBox_time_line_step.setMaximum(999)

        self.horizontalLayout_8.addWidget(self.spinBox_time_line_step)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_12 = QLabel(self.groupBox_4)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_16.addWidget(self.label_12)

        self.spinBox_time_line_duration = QSpinBox(self.groupBox_4)
        self.spinBox_time_line_duration.setObjectName(u"spinBox_time_line_duration")
        self.spinBox_time_line_duration.setFrame(False)
        self.spinBox_time_line_duration.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.spinBox_time_line_duration.setMaximum(999)

        self.horizontalLayout_16.addWidget(self.spinBox_time_line_duration)


        self.verticalLayout_3.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_15 = QLabel(self.groupBox_4)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_17.addWidget(self.label_15)

        self.lineEdit_location_country = QLineEdit(self.groupBox_4)
        self.lineEdit_location_country.setObjectName(u"lineEdit_location_country")

        self.horizontalLayout_17.addWidget(self.lineEdit_location_country)


        self.verticalLayout_3.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_16 = QLabel(self.groupBox_4)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_18.addWidget(self.label_16)

        self.lineEdit_location_place = QLineEdit(self.groupBox_4)
        self.lineEdit_location_place.setObjectName(u"lineEdit_location_place")

        self.horizontalLayout_18.addWidget(self.lineEdit_location_place)


        self.verticalLayout_3.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.toolButton_open_hertta_settings_file = QToolButton(self.groupBox_4)
        self.toolButton_open_hertta_settings_file.setObjectName(u"toolButton_open_hertta_settings_file")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen))
        self.toolButton_open_hertta_settings_file.setIcon(icon3)

        self.horizontalLayout_20.addWidget(self.toolButton_open_hertta_settings_file)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_3)

        self.toolButton_query_hertta_settings = QToolButton(self.groupBox_4)
        self.toolButton_query_hertta_settings.setObjectName(u"toolButton_query_hertta_settings")
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.HelpFaq))
        self.toolButton_query_hertta_settings.setIcon(icon4)

        self.horizontalLayout_20.addWidget(self.toolButton_query_hertta_settings)

        self.toolButton_update_hertta_settings = QToolButton(self.groupBox_4)
        self.toolButton_update_hertta_settings.setObjectName(u"toolButton_update_hertta_settings")
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
        self.toolButton_update_hertta_settings.setIcon(icon5)

        self.horizontalLayout_20.addWidget(self.toolButton_update_hertta_settings)


        self.verticalLayout_3.addLayout(self.horizontalLayout_20)


        self.verticalLayout_7.addLayout(self.verticalLayout_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)


        self.horizontalLayout_11.addWidget(self.groupBox_4)

        self.groupBox_6 = QGroupBox(self.tab)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.toolButton_run_building_optimization = QToolButton(self.groupBox_6)
        self.toolButton_run_building_optimization.setObjectName(u"toolButton_run_building_optimization")
        self.toolButton_run_building_optimization.setIcon(icon1)
        self.toolButton_run_building_optimization.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout_8.addWidget(self.toolButton_run_building_optimization)

        self.toolButton_run_weather_forecast = QToolButton(self.groupBox_6)
        self.toolButton_run_weather_forecast.setObjectName(u"toolButton_run_weather_forecast")
        self.toolButton_run_weather_forecast.setIcon(icon1)
        self.toolButton_run_weather_forecast.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout_8.addWidget(self.toolButton_run_weather_forecast)

        self.toolButton_run_electricity_prices = QToolButton(self.groupBox_6)
        self.toolButton_run_electricity_prices.setObjectName(u"toolButton_run_electricity_prices")
        self.toolButton_run_electricity_prices.setIcon(icon1)
        self.toolButton_run_electricity_prices.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout_8.addWidget(self.toolButton_run_electricity_prices)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer)


        self.horizontalLayout_11.addWidget(self.groupBox_6)


        self.verticalLayout_9.addLayout(self.horizontalLayout_11)

        self.groupBox_10 = QGroupBox(self.tab)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_10)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.treeView_tasks = QTreeView(self.groupBox_10)
        self.treeView_tasks.setObjectName(u"treeView_tasks")
        self.treeView_tasks.setHeaderHidden(True)
        self.treeView_tasks.header().setVisible(False)

        self.verticalLayout_6.addWidget(self.treeView_tasks)


        self.verticalLayout_9.addWidget(self.groupBox_10)


        self.horizontalLayout_10.addLayout(self.verticalLayout_9)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_3 = QGroupBox(self.tab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy1)
        self.groupBox_3.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.toolButton_fetch_total_records = QToolButton(self.groupBox_3)
        self.toolButton_fetch_total_records.setObjectName(u"toolButton_fetch_total_records")
        self.toolButton_fetch_total_records.setIcon(icon5)

        self.horizontalLayout_7.addWidget(self.toolButton_fetch_total_records)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")
        font = QFont()
        font.setBold(True)
        font.setUnderline(False)
        self.label_11.setFont(font)

        self.horizontalLayout_14.addWidget(self.label_11)

        self.toolButton_play_weather = QToolButton(self.groupBox_3)
        self.toolButton_play_weather.setObjectName(u"toolButton_play_weather")
        self.toolButton_play_weather.setIcon(icon1)

        self.horizontalLayout_14.addWidget(self.toolButton_play_weather)

        self.toolButton_play_weather_backwards = QToolButton(self.groupBox_3)
        self.toolButton_play_weather_backwards.setObjectName(u"toolButton_play_weather_backwards")
        icon6 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaSkipBackward))
        self.toolButton_play_weather_backwards.setIcon(icon6)

        self.horizontalLayout_14.addWidget(self.toolButton_play_weather_backwards)

        self.toolButton_stop_weather = QToolButton(self.groupBox_3)
        self.toolButton_stop_weather.setObjectName(u"toolButton_stop_weather")
        icon7 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.SystemShutdown))
        self.toolButton_stop_weather.setIcon(icon7)

        self.horizontalLayout_14.addWidget(self.toolButton_stop_weather)


        self.verticalLayout_2.addLayout(self.horizontalLayout_14)

        self.label_weather_total_records = QLabel(self.groupBox_3)
        self.label_weather_total_records.setObjectName(u"label_weather_total_records")

        self.verticalLayout_2.addWidget(self.label_weather_total_records)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.spinBox_limit_weather = QSpinBox(self.groupBox_3)
        self.spinBox_limit_weather.setObjectName(u"spinBox_limit_weather")
        self.spinBox_limit_weather.setProperty(u"showGroupSeparator", True)
        self.spinBox_limit_weather.setMaximum(1000000)

        self.horizontalLayout_2.addWidget(self.spinBox_limit_weather)

        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.spinBox_page_weather = QSpinBox(self.groupBox_3)
        self.spinBox_page_weather.setObjectName(u"spinBox_page_weather")
        self.spinBox_page_weather.setProperty(u"showGroupSeparator", True)
        self.spinBox_page_weather.setMaximum(1000000)

        self.horizontalLayout_2.addWidget(self.spinBox_page_weather)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_13 = QLabel(self.groupBox_3)
        self.label_13.setObjectName(u"label_13")
        font1 = QFont()
        font1.setBold(True)
        self.label_13.setFont(font1)

        self.horizontalLayout_15.addWidget(self.label_13)

        self.toolButton_play_electricity_consumption = QToolButton(self.groupBox_3)
        self.toolButton_play_electricity_consumption.setObjectName(u"toolButton_play_electricity_consumption")
        self.toolButton_play_electricity_consumption.setIcon(icon1)

        self.horizontalLayout_15.addWidget(self.toolButton_play_electricity_consumption)

        self.toolButton_play_electricity_consumption_backwards = QToolButton(self.groupBox_3)
        self.toolButton_play_electricity_consumption_backwards.setObjectName(u"toolButton_play_electricity_consumption_backwards")
        self.toolButton_play_electricity_consumption_backwards.setIcon(icon6)

        self.horizontalLayout_15.addWidget(self.toolButton_play_electricity_consumption_backwards)

        self.toolButton_stop_electricity_consumption = QToolButton(self.groupBox_3)
        self.toolButton_stop_electricity_consumption.setObjectName(u"toolButton_stop_electricity_consumption")
        self.toolButton_stop_electricity_consumption.setIcon(icon7)

        self.horizontalLayout_15.addWidget(self.toolButton_stop_electricity_consumption)


        self.verticalLayout_2.addLayout(self.horizontalLayout_15)

        self.label_elec_total_records = QLabel(self.groupBox_3)
        self.label_elec_total_records.setObjectName(u"label_elec_total_records")

        self.verticalLayout_2.addWidget(self.label_elec_total_records)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_6.addWidget(self.label_4)

        self.spinBox_limit_elec = QSpinBox(self.groupBox_3)
        self.spinBox_limit_elec.setObjectName(u"spinBox_limit_elec")
        self.spinBox_limit_elec.setProperty(u"showGroupSeparator", True)
        self.spinBox_limit_elec.setMaximum(1000000)

        self.horizontalLayout_6.addWidget(self.spinBox_limit_elec)

        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_6.addWidget(self.label_3)

        self.spinBox_page_elec = QSpinBox(self.groupBox_3)
        self.spinBox_page_elec.setObjectName(u"spinBox_page_elec")
        self.spinBox_page_elec.setProperty(u"showGroupSeparator", True)
        self.spinBox_page_elec.setMaximum(1000000)

        self.horizontalLayout_6.addWidget(self.spinBox_page_elec)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_14 = QLabel(self.groupBox_3)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font1)

        self.horizontalLayout_13.addWidget(self.label_14)

        self.toolButton_play_heat_consumption = QToolButton(self.groupBox_3)
        self.toolButton_play_heat_consumption.setObjectName(u"toolButton_play_heat_consumption")
        self.toolButton_play_heat_consumption.setIcon(icon1)

        self.horizontalLayout_13.addWidget(self.toolButton_play_heat_consumption)

        self.toolButton_play_heat_consumption_backwards = QToolButton(self.groupBox_3)
        self.toolButton_play_heat_consumption_backwards.setObjectName(u"toolButton_play_heat_consumption_backwards")
        self.toolButton_play_heat_consumption_backwards.setIcon(icon6)

        self.horizontalLayout_13.addWidget(self.toolButton_play_heat_consumption_backwards)

        self.toolButton_stop_heat_consumption = QToolButton(self.groupBox_3)
        self.toolButton_stop_heat_consumption.setObjectName(u"toolButton_stop_heat_consumption")
        self.toolButton_stop_heat_consumption.setIcon(icon7)

        self.horizontalLayout_13.addWidget(self.toolButton_stop_heat_consumption)


        self.verticalLayout_2.addLayout(self.horizontalLayout_13)

        self.label_heat_total_records = QLabel(self.groupBox_3)
        self.label_heat_total_records.setObjectName(u"label_heat_total_records")

        self.verticalLayout_2.addWidget(self.label_heat_total_records)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_9.addWidget(self.label_6)

        self.spinBox_limit_heat = QSpinBox(self.groupBox_3)
        self.spinBox_limit_heat.setObjectName(u"spinBox_limit_heat")
        self.spinBox_limit_heat.setWrapping(False)
        self.spinBox_limit_heat.setProperty(u"showGroupSeparator", True)
        self.spinBox_limit_heat.setMaximum(1000000)

        self.horizontalLayout_9.addWidget(self.spinBox_limit_heat)

        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_9.addWidget(self.label_5)

        self.spinBox_page_heat = QSpinBox(self.groupBox_3)
        self.spinBox_page_heat.setObjectName(u"spinBox_page_heat")
        self.spinBox_page_heat.setProperty(u"showGroupSeparator", True)
        self.spinBox_page_heat.setMaximum(1000000)

        self.horizontalLayout_9.addWidget(self.spinBox_page_heat)


        self.verticalLayout_2.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_3.addWidget(self.label_9)

        self.comboBox_timeframe = QComboBox(self.groupBox_3)
        self.comboBox_timeframe.setObjectName(u"comboBox_timeframe")

        self.horizontalLayout_3.addWidget(self.comboBox_timeframe)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_17 = QLabel(self.groupBox_3)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font1)

        self.horizontalLayout_19.addWidget(self.label_17)

        self.toolButton_play_live_frequency = QToolButton(self.groupBox_3)
        self.toolButton_play_live_frequency.setObjectName(u"toolButton_play_live_frequency")
        self.toolButton_play_live_frequency.setIcon(icon1)

        self.horizontalLayout_19.addWidget(self.toolButton_play_live_frequency)

        self.toolButton_stop_live_frequency = QToolButton(self.groupBox_3)
        self.toolButton_stop_live_frequency.setObjectName(u"toolButton_stop_live_frequency")
        self.toolButton_stop_live_frequency.setIcon(icon7)

        self.horizontalLayout_19.addWidget(self.toolButton_stop_live_frequency)


        self.verticalLayout_2.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_12.addWidget(self.label_8)

        self.spinBox_limit_freq = QSpinBox(self.groupBox_3)
        self.spinBox_limit_freq.setObjectName(u"spinBox_limit_freq")
        self.spinBox_limit_freq.setProperty(u"showGroupSeparator", True)
        self.spinBox_limit_freq.setMaximum(1000000)

        self.horizontalLayout_12.addWidget(self.spinBox_limit_freq)

        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_12.addWidget(self.label_7)

        self.spinBox_page_freq = QSpinBox(self.groupBox_3)
        self.spinBox_page_freq.setObjectName(u"spinBox_page_freq")
        self.spinBox_page_freq.setMaximum(1000000)

        self.horizontalLayout_12.addWidget(self.spinBox_page_freq)


        self.verticalLayout_2.addLayout(self.horizontalLayout_12)


        self.verticalLayout_4.addWidget(self.groupBox_3)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        self.groupBox.setMinimumSize(QSize(0, 0))
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.comboBox_bucket = QComboBox(self.groupBox)
        self.comboBox_bucket.setObjectName(u"comboBox_bucket")

        self.horizontalLayout_4.addWidget(self.comboBox_bucket)

        self.toolButton_delete_data_from_influxdb = QToolButton(self.groupBox)
        self.toolButton_delete_data_from_influxdb.setObjectName(u"toolButton_delete_data_from_influxdb")
        icon8 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.toolButton_delete_data_from_influxdb.setIcon(icon8)

        self.horizontalLayout_4.addWidget(self.toolButton_delete_data_from_influxdb)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayout_4.addWidget(self.groupBox)


        self.horizontalLayout_10.addLayout(self.verticalLayout_4)


        self.verticalLayout_5.addLayout(self.horizontalLayout_10)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout = QHBoxLayout(self.tab_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 3, 0, 0)
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.groupBox_8 = QGroupBox(self.tab_2)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_12 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(3, 3, 3, 3)
        self.textBrowser_hertta_output = QTextBrowser(self.groupBox_8)
        self.textBrowser_hertta_output.setObjectName(u"textBrowser_hertta_output")

        self.verticalLayout_12.addWidget(self.textBrowser_hertta_output)


        self.verticalLayout_13.addWidget(self.groupBox_8)

        self.groupBox_5 = QGroupBox(self.tab_2)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(3, 3, 3, 3)
        self.textBrowser_hertta_client_output = QTextBrowser(self.groupBox_5)
        self.textBrowser_hertta_client_output.setObjectName(u"textBrowser_hertta_client_output")

        self.verticalLayout_10.addWidget(self.textBrowser_hertta_client_output)


        self.verticalLayout_13.addWidget(self.groupBox_5)


        self.horizontalLayout.addLayout(self.verticalLayout_13)

        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.groupBox_7 = QGroupBox(self.tab_2)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(3, 3, 3, 3)
        self.textBrowser_freq = QTextBrowser(self.groupBox_7)
        self.textBrowser_freq.setObjectName(u"textBrowser_freq")

        self.verticalLayout_11.addWidget(self.textBrowser_freq)


        self.verticalLayout_15.addWidget(self.groupBox_7)

        self.groupBox_9 = QGroupBox(self.tab_2)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.verticalLayout_14 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(3, 3, 3, 3)
        self.textBrowser_log = QTextBrowser(self.groupBox_9)
        self.textBrowser_log.setObjectName(u"textBrowser_log")

        self.verticalLayout_14.addWidget(self.textBrowser_log)


        self.verticalLayout_15.addWidget(self.groupBox_9)


        self.horizontalLayout.addLayout(self.verticalLayout_15)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_16.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 942, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Control Center", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
#if QT_CONFIG(shortcut)
        self.actionQuit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Task master", None))
        self.toolButton_start_master_loop.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.toolButton_stop_master_loop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.label_current_task.setText(QCoreApplication.translate("MainWindow", u"Press Start", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Hertta Server", None))
        self.label_hertta_server_status.setText(QCoreApplication.translate("MainWindow", u"Offline", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"time_line[step]", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"time_line[duration]", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"location[country]", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"location[place]", None))
        self.toolButton_update_hertta_settings.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Hertta Client", None))
        self.toolButton_run_building_optimization.setText(QCoreApplication.translate("MainWindow", u"Building opt.", None))
        self.toolButton_run_weather_forecast.setText(QCoreApplication.translate("MainWindow", u"Weather forec.", None))
        self.toolButton_run_electricity_prices.setText(QCoreApplication.translate("MainWindow", u"Electr. prices", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"Tasks", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Fetch from Data Lake to InfluxDb", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Weather", None))
        self.toolButton_play_weather.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.toolButton_stop_weather.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_weather_total_records.setText(QCoreApplication.translate("MainWindow", u"Click refresh", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"limit", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"page", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Electricity Consumption", None))
        self.toolButton_play_electricity_consumption.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.toolButton_stop_electricity_consumption.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_elec_total_records.setText(QCoreApplication.translate("MainWindow", u"Click refresh", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"limit", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"page", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Heat Consumption", None))
        self.toolButton_play_heat_consumption.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.toolButton_stop_heat_consumption.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_heat_total_records.setText(QCoreApplication.translate("MainWindow", u"Click refresh", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"limit", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"page", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Time frame", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Live frequency", None))
        self.toolButton_play_live_frequency.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.toolButton_stop_live_frequency.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"limit", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"page", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Delete data from InfluxDb", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Controls", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"Hertta server log", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Hertta client log", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"Live frequency log", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"Log", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Logs", None))
    # retranslateUi

