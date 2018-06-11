import QtQuick 2.0
import QtQuick.Extras 1.4
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.3
import "./Chart"

ApplicationWindow {
    objectName: "DemonstratorWindow"
    title: "Demonstrator"
    id: demonstratorwindow
    color: '#343A40'
    width: 1920
    height: 1080

    GridLayout {
        id: grid
        anchors.fill: parent
        columns: 1
        rows: 2

        GridLayout {
            id: grid2
            anchors.fill: parent
            columns: 2
            rows: 1

            CircularGauge {
                objectName: "Gauge"
                id: gauge
                maximumValue: 100
                minimumValue: 0
                stepSize: 1
                Layout.fillWidth: true
                Layout.fillHeight: true
            }

            Chart {
                width: 1200
                height: 900
                onPaint: {
                    line({
                        labels : ["30min","25min","20min","15min","10min","5min"],
                        datasets : [
                            {
                                fillColor : "rgba(220,220,220,0.5)",
                                strokeColor : "rgba(220,220,220,1)",
                                pointColor : "rgba(220,220,220,1)",
                                pointStrokeColor : "#fff",
                                data : [65,59,90,81,56,55]
                            }
                        ]
                    })
                }
                /*Timer {
                    id:t
                    interval: 100
                    repeat: true
                    running: true
                    onTriggered: {
                        test+=1
                        requestPaint();
                    }
                }*/
            }
        }

        TextEdit {
            objectName: "ConsoleOutput"
            id: consoleoutput
            readOnly: true
            height: 90
            Layout.fillWidth: true
            color: '#FFFFFF'
            font.pointSize: 30
            text: '1.1.1 ---- 8 Byte(s) ----> 1/1/1'
            horizontalAlignment: TextEdit.AlignHCenter
        }
    }
}
