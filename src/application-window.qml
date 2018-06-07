import QtQuick 2.0
import QtQuick.Extras 1.4
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.3

ApplicationWindow {
    width: 1920
    height: 1080
    objectName: "DemonstratorWindow"
    title: "Demonstrator"
    id: demonstratorwindow
    color: '#343A40'

    GridLayout {
        id: grid
        anchors.fill: parent
        columns: 1
        rows: 3

        CircularGauge {
            Layout.fillWidth: true
            Layout.fillHeight: true
            objectName: "Gauge"
            id: gauge
        }

        TextEdit {
            Layout.fillWidth: true
            Layout.fillHeight: true
            objectName: "ConsoleOutput"
            id: consoleoutput
            readOnly: true
            color: '#00FF00'
            font.pointSize: 30
            text: '1.1.1 ---- 8 Byte(s) ----> 1/1/1'
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
