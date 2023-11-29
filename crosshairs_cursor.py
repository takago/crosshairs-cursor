# 鷹合研(2023,11/29)
# テキトウに作った十字カーソル
# (タイマーを使っているので重いかも)

from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *
import sys

class GUI(QWidget):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        self.setGeometry(0, 0, screen_size.width(), screen_size.height())

        # アイコンを作成
        self.myicon=dict()

        self.myicon['show']=QPixmap( 32, 32 )
        painter=QPainter(self.myicon['show'])
        painter.eraseRect(0, 0, 32, 32)
        painter.setPen(QColor("#000000"))
        # painter.setFont( QFont("IPAGothic") )
        painter.drawText( QPoint(16, 16), "✚" )
        painter.end()

        self.myicon['hide']=QPixmap( 32, 32 )
        painter=QPainter(self.myicon['hide'])
        painter.eraseRect(0, 0, 32, 32)
        painter.setPen(QColor("#AAAAAA"))
        # painter.setFont( QFont("IPAGothic") )
        painter.drawText( QPoint(16, 16), "✚" )
        painter.end()

        self.setWindowIcon(QIcon(self.myicon['show']))

        if True:
            win_flags =  Qt.FramelessWindowHint       # フレームなし．
            win_flags |= Qt.WindowStaysOnTopHint      # 常に最前面になる（他が全画面表示しても大丈夫）
            win_flags |= Qt.WindowTransparentForInput # 下側のアプリを操作できる(その代わり，テキスト入力やボタンが押せなくなる)
                                                      # 文字列などを画面上にオーバレイ表示させるのに使えそう
            win_flags |= Qt.Tool                      # 「パネル」にアプリケーションアイコンを表示しない
            
            self.setWindowFlags(win_flags)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setStyleSheet("background: rgba(0,0,0,0%)")


        # 空の縦レイアウトを作る
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # シーン
        self.scene = QGraphicsScene()
        view = QGraphicsView(self.scene)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # スクロールバーを表示しない
        self.layout.addWidget(view)

        # タイマー
        self.timer = QTimer()
        self.timer.setSingleShot(False)  # 連続 or 1ショットか
        self.timer.setInterval(25)
        self.timer.timeout.connect(self.TimeUp)
        self.timer.start()

        #-----------------------------------------------------
        # システムトレイの設置

        self.tray = QSystemTrayIcon(QIcon(self.myicon['show']))
        self.tray.show()
        self.tray.setToolTip('Crosshairs Cursor')
        self.SHOW=True
        self.tray.activated.connect(self.onActivated)       # クリックされたら

    def TimeUp(self):
        x = QCursor.pos().x()-10
        y = QCursor.pos().y()-5  # カーソルサイズ
        # print(x,y)
        pen = QPen(QColor(0xFF, 0, 0, 50)) # カーソルの色，透明度
        pen.setWidth(16)
        self.scene.clear()
        self.scene.addLine(QLineF(x,  0, x, screen_size.height()), pen) # 横線
        self.scene.addLine(QLineF(0,  y, screen_size.width(),y), pen)   # 縦線

    def onActivated(self, reason):
        self.SHOW = not self.SHOW
        if self.SHOW: # チェックされたら
            ui.show() # メインウィンドウを表示する
            self.tray.setIcon(QIcon(self.myicon['show']))
            self.timer.start()
        else:
            ui.hide() # メインウィンドウを表示しない（タスクトレイのみになる）
            self.tray.setIcon(QIcon(self.myicon['hide']))
            self.timer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    print('Screen: %s' % screen.name())
    screen_size = screen.size()
    print('Size: %d x %d' % (screen_size.width(), screen_size.height()))

    ui = GUI()
    ui.show()
    sys.exit(app.exec_())
