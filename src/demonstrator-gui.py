#!/usr/bin/python3

import sys, os, subprocess
from time import sleep
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtQml import *

class WorkerSignals(QObject):
    progress = pyqtSignal(int, str)

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    def run(self):
        self.fn(*self.args, **self.kwargs)

class MainWindow(object):
    def __init__(self):
        self.__appEngine = QQmlApplicationEngine()
        self.__appEngine.load("application-window.qml")
        self.__appWindow = self.__appEngine.rootObjects()[0]
        self.__gauge = self.__appWindow.findChild(QObject, "Gauge")
        self.__consoleOutput = self.__appWindow.findChild(QObject, "ConsoleOutput")

        #self.__appWindow.timerSignal.connect(self.update_gui)

        self.threadpool = QThreadPool()

    def update_gui(self, n, text):
        self.__gauge.setProperty("value", n)
        self.__consoleOutput.setProperty("text", text)

    def show(self):
        self.__appWindow.showFullScreen()

    def start(self):
        worker = Worker(self.reader)
        worker.signals.progress.connect(self.update_gui)
        self.threadpool.start(worker)

    def physical_area(self, address):
        return (address >> 12) & 15

    def physical_line(self, address):
        return (address >> 8) & 15

    def physical_device(self, address):
        return address & 255

    def group_main(self, address):
        return (address >> 11) & 31

    def group_middle(self, address):
        return (address >> 8) & 7

    def group_sub(self, address):
        return address & 255

    def reader(self, progress_callback):
        #agent_path = os.path.abspath(sys.path[0] + '/..')
        fifo_path = '/tmp/demo_fifo'

        if not os.path.exists(fifo_path):
            os.mkfifo(fifo_path)

        with subprocess.Popen('agent --demo', shell=True) as agent:
            print("Opening FIFO...")
            sleep(2)
            with open(fifo_path) as fifo:
                print("FIFO opened")
                exporting_flows = False
                while True:
                    data = fifo.readline()
                    if len(data) == 0:
                        print("FIFO closed")
                        break
                    data = data.replace("\\n", "")

                    if "Starting flow export" in data:
                        exporting_flows = True

                    if "Finished flow export" in data:
                        exporting_flows = False

                    # start of telegram
                    if not exporting_flows and "--------------------------------------------" in data:
                        src = fifo.readline().split("Source Address: ")[1]
                        dest = fifo.readline().split("Destination Address: ")[1]
                        time = fifo.readline().split("Start Time: ")[1]
                        fifo.readline() # element not needed
                        apci = fifo.readline().split("APCI: ")[1]
                        fifo.readline() # element not needed
                        payload_size = fifo.readline().split("Byte Count: ")[1] # + 9 = total
                        priority = fifo.readline().split("Priority: ")[1]
                        hop_count = fifo.readline().split("Hop Count: ")[1]
                        is_group_address = fifo.readline().split("Is Group Address: ")[1]
                        fifo.readline() # element not needed
                        fifo.readline() # end of telegram
                        src_addr = repr(self.physical_area(int(src, 16))) + '.' + repr(self.physical_line(int(src, 16))) + '.' + repr(self.physical_device(int(src, 16)))
                        dest_addr = repr(self.group_main(int(dest, 16))) + '/' + repr(self.group_middle(int(dest, 16))) + '/' + repr(self.group_sub(int(dest, 16)))
                        output = "{0} ----- {2} Byte(s) ----> {1}".format(src_addr, dest_addr, int(payload_size))
                        progress_callback.emit(int(payload_size) + 9, output)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.start()
    sys.exit(app.exec_())
