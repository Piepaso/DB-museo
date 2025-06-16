import sys
from PySide6.QtCore    import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget,
    QVBoxLayout, QWidget, QPushButton, QLabel
)

from style        import BASE_STYLE
from utente_page  import UtentePage
# ── segnaposto per non far crashare la demo ──
class Services: pass                        # TODO: implementa layer DB
class MuseoPage(QWidget):                   # placeholder
    def __init__(self, back_home): 
        super().__init__(); QVBoxLayout(self).addWidget(
        QLabel("Museo – work-in-progress")); b=QPushButton("← Indietro"); b.clicked.connect(back_home);
        QVBoxLayout(self).addWidget(b, alignment=Qt.AlignCenter)

# ─────────────────────────────────────────────────────────────────────────────
class HomePage(QWidget):
    def __init__(self, go_utente, go_museo):
        super().__init__()
        v = QVBoxLayout(self); v.addStretch(1)
        for text, slot in (("👤 Utente", go_utente), ("🏛️ Museo", go_museo)):
            btn = QPushButton(text, cursor=Qt.PointingHandCursor, minimumWidth=220)
            btn.clicked.connect(slot); v.addWidget(btn, alignment=Qt.AlignCenter)
            v.addSpacing(24)
        v.addStretch(1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Museo DB")
        self.setStyleSheet(BASE_STYLE)

        self.stack = QStackedWidget(self); self.setCentralWidget(self.stack)
        self.home   = HomePage(self.go_utente, self.go_museo)
        self.utente = UtentePage(Services())
        self.museo  = MuseoPage(self.go_home)

        for w in (self.home, self.utente, self.museo):
            self.stack.addWidget(w)

    # router
    def go_home  (self): self.stack.setCurrentWidget(self.home)
    def go_utente(self): self.stack.setCurrentWidget(self.utente)
    def go_museo (self): self.stack.setCurrentWidget(self.museo)

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow(); win.resize(480, 360); win.show()
    sys.exit(app.exec())
