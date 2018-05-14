import QtQuick 2.0
import QtQuick.Extras 1.4
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.3

ApplicationWindow {
    width: 240
    height: 240
    objectName: "DemonstratorWindow"
    title: "Demonstrator"
    id: demonstratorwindow
    color: '#343A40'

    GridLayout {
        id: grid
        columns: 1

        CircularGauge {
            x: 20
            Layout.preferredWidth: 180
            Layout.preferredHeight: 180
            objectName: "Gauge"
            id: gauge
        }

        TextEdit {
            Layout.preferredWidth: 235
            Layout.preferredHeight: 40
            objectName: "ConsoleOutput"
            id: consoleoutput
            readOnly: true
            color: '#00FF00'
            horizontalAlignment: TextEdit.AlignHCenter
        }
    }

    /*
    signal timerSignal();
    Timer {
        interval: 1000;
        running: true;
        repeat: true;
        onTriggered: timerSignal()
    }*/
}
