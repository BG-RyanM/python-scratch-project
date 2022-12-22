import matplotlib.pyplot as plt
import numpy as np


class Index(object):
    ind = 0
    figure = None
    TOTAL_CHARTS = 3

    def next(self, event):
        print("next!")
        self.ind += 1
        self.ind = self.ind % Index.TOTAL_CHARTS
        self.do_change(self.ind)

    def prev(self, event):
        print("prev!")
        self.ind -= 1
        self.ind = self.ind % Index.TOTAL_CHARTS
        self.do_change(self.ind)

    def do_change(self, idx):
        Index.figure.clear()
        make_plot(Index.figure, idx)
        plt.draw()


def make_plot(fig, idx):
    global index_object
    ax = fig.add_subplot(111)
    x = np.linspace(0, 2 * np.pi, 1000)
    if idx % 3 == 0:
        ax.plot(x, np.cos(x))
    elif idx % 3 == 1:
        ax.plot(x, np.sin(x))
    else:
        ax.plot(x, np.tan(x))

    names = ["cos", "sin", "tan"]
    fig.suptitle("Trig Function {}".format(names[idx]))
    name = "Plot #{}".format(idx + 1)
    ax.title.set_text(name)  # set title of graph
    ax.set_xlabel("X Axis!")
    ax.set_ylabel("Y Axis!")

    print("making buttons!")
    axprev = plt.axes([0.7, 0.0, 0.1, 0.075])
    axnext = plt.axes([0.81, 0.0, 0.1, 0.075])
    bnext = plt.Button(axnext, "Next")
    bnext.on_clicked(index_object.next)
    index_object.next_button = bnext
    bprev = plt.Button(axprev, "Previous")
    bprev.on_clicked(index_object.prev)
    index_object.prev_button = bprev


def setup_display():
    fig = plt.figure()
    Index.figure = fig
    make_plot(fig, 0)

    plt.show()


index_object = Index()
setup_display()
