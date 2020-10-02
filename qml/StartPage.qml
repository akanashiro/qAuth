import QtQuick 2.0
import QtQuick.Layouts 1.1
import QtQuick.Controls 2.4
import org.kde.kirigami 2.0 as Kirigami


Column {
        spacing: 15

        ColumnLayout {
            x: 20
            width: parent.width
            Label {
                width: parent.width
                text: "Service Name:"
            }
            TextField {
                width: parent.width
                /* Layout.fillWidth: true */
                placeholderText: "Würzburg..."
            }
            Label {
                width: parent.width
                text: "OTP:"
            }
            TextField {
                width: parent.width
                /*Layout.fillWidth: true*/
                echoMode: TextInput.Password
            }
    }
}
