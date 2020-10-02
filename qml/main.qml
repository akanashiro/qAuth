import QtQuick 2.2
import QtQuick.Layouts 1.1
import QtQuick.Controls 2.4
import org.kde.kirigami 2.0 as Kirigami

Kirigami.ApplicationWindow
{
    width: 700
    height: 365

    title: "qAuth - 2 Steps Authentication"

    pageStack.initialPage: Qt.resolvedUrl("StartPage.qml")
}
