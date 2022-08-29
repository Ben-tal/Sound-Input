import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Controls 2.0


Item {

    id: root
    visible: true
    Image {

            id: image2
            anchors.fill: parent
            source: "SVG/background.svg"
            opacity: 0.5
            z: -1
            scale: Qt.KeepAspectRatio
            fillMode: Image.PreserveAspectFit
        }
    Image {
    // Thanks to this hack, qml can now only DOWN-SCALE/SHRINK the SVG, which won't cause blurriness/pixelation
        source: "SVG/needle.svg"
        id: image
        sourceSize: Qt.size(
                // first "trick" qml that the SVG is larger than we EVER NEED
                Math.max(hiddenImg.sourceSize.width, 250),
                // change 250 to a per-project "biggest icon in project" value
                Math.max(hiddenImg.sourceSize.height, 250))
        width: root.width
        height: 175  + 16.35
        horizontalAlignment: Image.AlignHCenter
        verticalAlignment: Image.AlignVCenter
        scale: Qt.KeepAspectRatio
        fillMode: Image.PreserveAspectFit
        transform: Rotation {
            id: rotation
            Behavior on angle  {
                SmoothedAnimation { velocity: 100 }
            }
            origin.x: image.width/2   // here!
            origin.y: image.height - 16.35
            angle: rotate.angle
        }
        Image {
            id: hiddenImg
            source: parent.source
            width: 0
            height: 0
        }
    }
}