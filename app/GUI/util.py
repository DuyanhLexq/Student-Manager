from PyQt5.QtGui import QPixmap, QPainter, QIcon
from PyQt5.QtCore import Qt

def convert_icon_to_white(icon_path:str) -> QPixmap:
    # Tạo một QPixmap mới với cùng kích thước, nền trong suốt
    pixmap = QPixmap(icon_path)
    
    white_pixmap = QPixmap(pixmap.size())
    white_pixmap.fill(Qt.transparent)

    # Dùng QPainter để vẽ icon cũ lên white_pixmap và chuyển màu
    painter = QPainter(white_pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_Source)
    painter.drawPixmap(0, 0, pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(white_pixmap.rect(), Qt.white)
    painter.end()
    return white_pixmap