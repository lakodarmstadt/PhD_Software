import pyqtgraph as pg
import numpy as np
from scipy import interpolate
scaler = None


class ScaleHandler():
    def __init__(self, lines):
        xs = [float(line.name()) for line in lines]
        ys = [float(line.x()) for line in lines]
        self.interp = interpolate.interp1d(xs, ys, assume_sorted=False, bounds_error=False, fill_value='extrapolate')
        self.inv_interp = interpolate.interp1d(ys, xs, assume_sorted=False, bounds_error=False, fill_value='extrapolate')
        self.markers = ys

    def get_scaled_time(self, input_t):
        return self.interp(input_t)

    def get_unscaled_time(self, input_scaled_t):
        return self.inv_interp(input_scaled_t)


def resample():
    print('Resample!')


def update_nonlinear(object=None):
    global lines
    global scaler
    start_time = 0
    stop_time = 30
    last_time = start_time

    lines = sorted(lines, key=lambda x: x.name())
    old_scaler = scaler
    if object is not None and old_scaler is not None:
        delta_t = 0
        for i, line in enumerate(lines):
            line.blockSignals(True)
            line.setValue(line.x() + delta_t)
            line.blockSignals(False)
            if line == object:
                moved_t = line.x()
                prior_t = old_scaler.markers[i]
                delta_t = moved_t - prior_t

    for i, line in enumerate(lines):
        if i + 1 < len(lines):
            next_time = lines[i + 1].x()
        else:
            next_time = stop_time
        line.setBounds([last_time + 1e-9 if last_time != 0 else last_time, None])
        last_time = line.x()

    old_scaler = scaler
    scaler = ScaleHandler(lines)
    plots = [p2]
    for plot in plots:
        for item in plot.items:
            if isinstance(item, pg.PlotDataItem):
                if old_scaler is not None:
                    # get old unscaled time and set the data as this time.
                    item.setData(scaler.get_scaled_time(old_scaler.get_unscaled_time(item.xData)), item.yData)

            elif isinstance(item, pg.InfiniteLine):
                if old_scaler is not None:
                    item.setValue(scaler.get_scaled_time(old_scaler.get_unscaled_time(item.x())))


app = pg.QtGui.QApplication([])
win = pg.GraphicsWindow()
# def onClick(event):
# if event.double():
# items = win.scene().items(event.scenePos())
# for x in items:
# if isinstance(x, pg.PlotItem):
# coord_pos = x.vb.mapSceneToView(event.scenePos())
# line=x.addLine(x=coord_pos.x(), name=scaler.get_unscaled_time(coord_pos.x()), movable=True)
# lines.append(line)
# line.sigPositionChanged.connect(update_nonlinear)
# update_nonlinear()

# win.scene().sigMouseClicked.connect(onClick)
p1 = win.addPlot(y=[])
lines = []
for i in range(10):
    line = p1.addLine(x=i * 2, name=i * 2, movable=True)
    lines.append(line)
    line.sigPositionChanged.connect(update_nonlinear)
    line.sigPositionChangeFinished.connect(resample)
win.nextRow()
data = np.sin(np.linspace(0, 2 * np.pi, 20000)) + np.random.rand(20000)
p2 = win.addPlot(x=np.linspace(0, 20, 20000), y=data)
p2.addLine(x=2, movable=False)
p2.setXLink(p1)
p1.disableAutoRange(axis=pg.ViewBox.XAxis)
update_nonlinear()

pg.QtGui.QApplication.instance().exec_()
