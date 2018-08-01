#!/usr/bin/env python3

import sys, os, subprocess, time
from time import sleep
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtQml import *

class Telegram(object):
    def __init__(self, timestamp, source_address, destination_address, is_group_address, payload_size):
        self.timestamp = timestamp
        self.source_address = source_address
        self.destination_address = destination_address
        self.is_group_address = is_group_address
        self.payload_size = payload_size

class WorkerSignals(QObject):
    progress = pyqtSignal(int, str, bool, int, int, int)

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

class AgentQueue(object):
    fifo_path = '/tmp/demo_fifo'
    telegram_list = []
    last_minute_tps = [] # Telegrams per second
    minute_start = 0

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

    def calc_usage(self, tlist):
        knx_header_size = 9
        total_bytes = 0
        knx_maximum_load = 9600/8 # in bytes
        for t in tlist:
            total_bytes += knx_header_size + int(t.payload_size)
        return int(100 * (total_bytes / knx_maximum_load))

    def reader(self, progress_callback):
        if not os.path.exists(self.fifo_path):
            os.mkfifo(self.fifo_path)

        #live: agent --type 1 --input 0 --demo
        #dev: agent --type 3 --input /home/max/sindabus-demonstrator/src/knxlog_21_01_2017_to_21_02_2017.txt --demo
        with subprocess.Popen('agent --type 1 --input 0 --demo', shell=True) as agent:
            print("Opening FIFO...")
            sleep(2)
            with open(self.fifo_path) as fifo:
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
                        timestamp = fifo.readline().split("Start Time: ")[1]
                        fifo.readline() # element not needed
                        apci = fifo.readline().split("APCI: ")[1]
                        fifo.readline() # element not needed
                        payload_size = fifo.readline().split("Byte Count: ")[1] # + 9 = total
                        priority = fifo.readline().split("Priority: ")[1]
                        hop_count = fifo.readline().split("Hop Count: ")[1]
                        is_group_address = fifo.readline().split("Is Group Address: ")[1]
                        fifo.readline() # element not needed
                        fifo.readline() # end of telegram

                        # formatting
                        src_addr = repr(self.physical_area(int(src, 16))) + '.' + repr(self.physical_line(int(src, 16))) + '.' + repr(self.physical_device(int(src, 16)))
                        dest_addr = repr(self.group_main(int(dest, 16))) + '/' + repr(self.group_middle(int(dest, 16))) + '/' + repr(self.group_sub(int(dest, 16)))
                        output = "{0} ----- {2} Byte(s) ----> {1}".format(src_addr, dest_addr, int(payload_size))

                        telegram = Telegram(timestamp, src, dest, is_group_address, payload_size)
                        list_length = len(self.telegram_list)
                        self.telegram_list.append(telegram)
                        self.telegram_list = list(filter(lambda a: a.timestamp == telegram.timestamp, self.telegram_list)) # keep only telegrams from current second

                        bus_usage = self.calc_usage(self.telegram_list)
                        if list_length != len(self.telegram_list):
                            self.last_minute_tps.append(list_length)
                        minute_changed = False
                        average = 0
                        maximum = 0
                        minimum = 0
                        print(output)
                        if self.minute_start == 0:
                            self.minute_start = int(time.time())
                        if len(self.last_minute_tps) >= 60 or int(time.time()) - self.minute_start >= 60:
                            if len(self.last_minute_tps) > 0:
                                average = int(sum(self.last_minute_tps) / len(self.last_minute_tps))
                                maximum = int(max(self.last_minute_tps))
                                minimum = int(min(self.last_minute_tps))
                                minute_changed = True
                                self.minute_start = int(time.time())
                                self.last_minute_tps.clear()
                            else:
                                minute_changed = True
                                self.minute_start = int(time.time())

                        progress_callback.emit(bus_usage, output, minute_changed, average, maximum, minimum)

class MainWindow(object):
    def __init__(self):
        self.initInterface()
        self.initBackgroundThread()

    def initInterface(self):
        self.__appEngine = QQmlApplicationEngine()
        scriptPath = os.path.dirname(os.path.realpath(__file__))
        self.__appEngine.load(os.path.join(scriptPath, "application-window.qml"))
        self.__appWindow = self.__appEngine.rootObjects()[0]
        self.__gauge = self.__appWindow.findChild(QObject, "Gauge")
        self.__chart = self.__appWindow.findChild(QObject, "Chart")
        self.__consoleOutput = self.__appWindow.findChild(QObject, "ConsoleOutput")
        self.__appWindow.showFullScreen()

    def initBackgroundThread(self):
        self.threadpool = QThreadPool()
        q = AgentQueue()
        worker = Worker(q.reader)
        worker.signals.progress.connect(self.onTelegram)
        self.threadpool.start(worker)

    def onTelegram(self, n, text, changed, average, maximum, minimum):
        self.__gauge.setProperty("value", n)
        lines = self.__consoleOutput.property("text").split('\n')
        lines.insert(0, text) # insert at the beginning
        if len(lines) == 4:
            del lines[-1] # remove last element

        self.__consoleOutput.setProperty("text", '\n'.join(lines))
        if changed is True:
            self.__chart.addDatapoint(average, maximum, minimum)
        #QMetaObject.invokeMethod(self.__chart, "addDatapoint", Qt.DirectConnection, Q_ARG(QVariant, average))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
