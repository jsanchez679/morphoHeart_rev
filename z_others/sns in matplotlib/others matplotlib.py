
#%%
import sys
import matplotlib
matplotlib.use('QtAgg')
import pandas as pd
from pathlib import Path
import seaborn as sns
import numpy as np

from PyQt6 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        sc = MplCanvas(self, width=5, height=4, dpi=100)

        # dir_df = Path('D:\Documents JSP\Dropbox\Dropbox_Juliana\PhD_Thesis\Data_ongoing\LS_ongoing\A_LS_Analysis\im_morphoHeart2\R_testing4 - Before ThBall - Copy\R_testing4\LS52_F02\csv_all\LS52_F02_dfUnloop_th_i2e[ch1-tiss]_atrium.csv')
        dir_df = Path('D:\Documents JSP\Dropbox\Dropbox_Juliana\PhD_Thesis\Data_ongoing\LS_ongoing\A_LS_Analysis\im_morphoHeart\LS52_F02_V_SR_1029_2A\Results_LS52_F02_V_SR_1029\csv_all\LS52_F02_V_SR_1029_hm_unloopAtr_MyocTh.csv')
        print(dir_df)
        heatmap = pd.read_csv(dir_df)  
        print(heatmap.sample(10))

        b = sns.heatmap(heatmap, cmap='turbo', ax=sc.axes)#, vmin = vmin, vmax = vmax)#, xticklabels=20, yticklabels=550)
        x_pos = sc.axes.get_xticks()
        x_pos_new = np.linspace(x_pos[0], x_pos[-1], 19)
        x_lab_new = np.arange(-180,200,20)
        sc.axes.set_xticks(x_pos_new) 

        y_pos = sc.axes.get_yticks()
        y_pos_new = np.linspace(y_pos[0], y_pos[-1], 11)
        sc.axes.set_yticks(y_pos_new) 

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()

#%%
import sys
import matplotlib
matplotlib.use('QtAgg')
import pandas as pd
from pathlib import Path
import seaborn as sns
import numpy as np

from PyQt6 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        sc = MplCanvas(self, width=5, height=4, dpi=100)

        # dir_df = Path('D:\Documents JSP\Dropbox\Dropbox_Juliana\PhD_Thesis\Data_ongoing\LS_ongoing\A_LS_Analysis\im_morphoHeart2\R_testing4 - Before ThBall - Copy\R_testing4\LS52_F02\csv_all\LS52_F02_dfUnloop_th_i2e[ch1-tiss]_atrium.csv')
        dir_df = Path('D:\Documents JSP\Dropbox\Dropbox_Juliana\PhD_Thesis\Data_ongoing\LS_ongoing\A_LS_Analysis\im_morphoHeart\LS52_F02_V_SR_1029_2A\Results_LS52_F02_V_SR_1029\csv_all\LS52_F02_V_SR_1029_hm_unloopAtr_MyocTh.csv')
        print(dir_df)
        heatmap = pd.read_csv(dir_df)  
        print(heatmap.sample(10))

        b = sns.heatmap(heatmap, cmap='turbo', ax=sc.axes)#, vmin = vmin, vmax = vmax)#, xticklabels=20, yticklabels=550)
        x_pos = sc.axes.get_xticks()
        x_pos_new = np.linspace(x_pos[0], x_pos[-1], 19)
        x_lab_new = np.arange(-180,200,20)
        sc.axes.set_xticks(x_pos_new) 

        y_pos = sc.axes.get_yticks()
        y_pos_new = np.linspace(y_pos[0], y_pos[-1], 11)
        sc.axes.set_yticks(y_pos_new) 

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()

#%%
import sys
import time

import numpy as np

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        # Ideally one would use self.addToolBar here, but it is slightly
        # incompatible between PyQt6 and other bindings, so we just add the
        # toolbar as a plain widget instead.
        layout.addWidget(NavigationToolbar(static_canvas, self))
        layout.addWidget(static_canvas)

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)
        layout.addWidget(NavigationToolbar(dynamic_canvas, self))

        self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        t = np.linspace(0, 10, 101)
        # Set up a Line2D.
        self._line, = self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._timer = dynamic_canvas.new_timer(50)
        self._timer.add_callback(self._update_canvas)
        self._timer.start()

    def _update_canvas(self):
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._line.set_data(t, np.sin(t + time.time()))
        self._line.figure.canvas.draw()


if __name__ == "__main__":
    # Check whether there is already a running QApplication (e.g., if running
    # from an IDE).
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()


# %%

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
import seaborn as sns

tips = sns.load_dataset("tips")

class MainWindow(QtWidgets.QMainWindow):
    send_fig = QtCore.pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()

        self.main_widget = QtWidgets.QWidget(self)

        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122, sharex=self.ax1, sharey=self.ax1)
        self.axes=[self.ax1, self.ax2]
        self.canvas = FigureCanvas(self.fig)

        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, 
                                  QtWidgets.QSizePolicy.Policy.Expanding)
        self.canvas.updateGeometry()

        self.dropdown1 = QtWidgets.QComboBox()
        self.dropdown1.addItems(["sex", "time", "smoker"])
        self.dropdown2 = QtWidgets.QComboBox()
        self.dropdown2.addItems(["sex", "time", "smoker", "day"])
        self.dropdown2.setCurrentIndex(2)

        self.dropdown1.currentIndexChanged.connect(self.update)
        self.dropdown2.currentIndexChanged.connect(self.update)
        self.label = QtWidgets.QLabel("A plot:")

        self.layout = QtWidgets.QGridLayout(self.main_widget)
        self.layout.addWidget(QtWidgets.QLabel("Select category for subplots"))
        self.layout.addWidget(self.dropdown1)
        self.layout.addWidget(QtWidgets.QLabel("Select category for markers"))
        self.layout.addWidget(self.dropdown2)

        self.layout.addWidget(self.canvas)

        self.setCentralWidget(self.main_widget)
        self.show()
        self.update()

    def update(self):

        colors=["b", "r", "g", "y", "k", "c"]
        self.ax1.clear()
        self.ax2.clear()
        cat1 = self.dropdown1.currentText()
        cat2 = self.dropdown2.currentText()
        print (cat1, cat2)

        for i, value in enumerate(tips[cat1].unique().get_values()):
            print ("value ", value)
            df = tips.loc[tips[cat1] == value]
            self.axes[i].set_title(cat1 + ": " + value)
            for j, value2 in enumerate(df[cat2].unique().get_values()):
                print ("value2 ", value2)
                df.loc[ tips[cat2] == value2 ].plot(kind="scatter", x="total_bill", y="tip", 
                                                ax=self.axes[i], c=colors[j], label=value2)
        self.axes[i].legend()   
        self.fig.canvas.draw_idle()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv) 
    ex = MainWindow()
    sys.exit(app.exec_())
# %%
