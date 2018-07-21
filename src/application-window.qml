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
                objectName: "Chart"
                id: chart
                width: 1200
                height: 900
                property var chartMeanData: [65,59,90,81,55]
                property var chartMinData: [40,45,76,50,30]
                property var chartMaxData: [90,70,98,86,78]
                property var chartLabels: ["5min","4min","3min","2min","1min"]
                property int maxData: 5
                onPaint: {
                    line({
                        labels : chartLabels,
                        datasets : [
                            {
                                fillColor : "rgba(220,220,220,0.5)",
                                strokeColor : "rgba(220,220,220,1)",
                                pointColor : "rgba(220,220,220,1)",
                                pointStrokeColor : "#fff",
                                data : chartMeanData
                            },
                            {
                                fillColor : "rgba(151,187,205,0.5)",
                                strokeColor : "rgba(151,187,205,1)",
                                pointColor : "rgba(151,187,205,1)",
                                pointStrokeColor : "#fff",
                                data : chartMaxData
                            },
                            {
                                fillColor : "rgba(100,110,205,0.5)",
                                strokeColor : "rgba(100,110,205,1)",
                                pointColor : "rgba(100,110,205,1)",
                                pointStrokeColor : "#fff",
                                data : chartMinData
                            }
                        ]
                    })
                }

                function addDatapoint(mean,max,min) {
                    var newlen = chartMeanData.push(mean)
                    if (newlen >= maxData) {
                        chartMeanData = new Object(chartMeanData.slice(1))
                    }
                    newlen = chartMaxData.push(max)
                    if (newlen >= maxData) {
                        chartMaxData = new Object(chartMaxData.slice(1))
                    }
                    newlen = chartMinData.push(min)
                    if (newlen >= maxData) {
                        chartMinData = new Object(chartMinData.slice(1))
                    }
                    requestPaint();
                }
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
