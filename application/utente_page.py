"""Pagina Utente → 3 tab (Biglietti, Visite, Profilo) + wizard di acquisto"""
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QAction
from PySide6.QtWidgets import *
from style import BASE_STYLE            # << qui importiamo lo stile GLOBAL

# ────────────────────────────── TAB 1 ── Biglietti ──────────────────────────
class TicketsTab(QWidget):
    def __init__(self, services):
        super().__init__()
        self.services = services
        lay = QVBoxLayout(self)

        toolbar = QToolBar()
        act_refresh  = QAction("Aggiorna", self)
        act_purchase = QAction("Acquista…", self)
        toolbar.addActions((act_refresh, act_purchase))
        lay.addWidget(toolbar)

        self.table = QTableView()
        lay.addWidget(self.table)

        act_refresh.triggered.connect(self.refresh)
        act_purchase.triggered.connect(self.open_wizard)

    # TODO: collega a services.list_tickets(email)
    def refresh(self): ...

    def open_wizard(self):
        if PurchaseWizard(self.services, self).exec():
            self.refresh()

# ────────────────────────────── TAB 2 ── Visite ─────────────────────────────
class VisitsTab(QWidget):
    def __init__(self, services):
        super().__init__()
        self.services = services
        lay = QVBoxLayout(self)

        self.table = QTableView()
        lay.addWidget(self.table)

        btn_book = QPushButton("Prenota visita")
        btn_book.clicked.connect(self.book_selected)
        lay.addWidget(btn_book, alignment=Qt.AlignRight)

    def book_selected(self): ...

# ────────────────────────────── TAB 3 ── Profilo ────────────────────────────
class ProfileTab(QWidget):
    def __init__(self, services):
        super().__init__()
        self.services = services
        form = QFormLayout(self)

        self.le_cf    = QLineEdit()
        self.le_mail  = QLineEdit()
        btn_save      = QPushButton("Salva")

        form.addRow("Codice fiscale", self.le_cf)
        form.addRow("E-mail",         self.le_mail)
        form.addRow(btn_save)

        btn_save.clicked.connect(self.save)

    def save(self):
        try:
            self.services.update_profile(self.le_cf.text(), self.le_mail.text())
            QMessageBox.information(self, "Ok", "Profilo aggiornato")
        except Exception as e:
            QMessageBox.critical(self, "Errore", str(e))

# ───────────────────────── Wizard di acquisto ───────────────────────────────
class PurchaseWizard(QWizard):
    def __init__(self, services, parent=None):
        super().__init__(parent)
        self.services = services
        self.setWindowTitle("Acquisto biglietto")

        # 1. data
        page1 = QWizardPage(); page1.setTitle("Scegli la data")
        self.cal = QCalendarWidget(minimumDate=QDate.currentDate())
        QVBoxLayout(page1).addWidget(self.cal)
        self.addPage(page1)

        # 2. sezioni
        page2 = QWizardPage(); page2.setTitle("Sezioni disponibili")
        self.list_sez = QListWidget()
        QVBoxLayout(page2).addWidget(self.list_sez)
        self.addPage(page2)

        # 3. riepilogo
        page3 = QWizardPage(); page3.setTitle("Riepilogo")
        self.lbl = QLabel(); QVBoxLayout(page3).addWidget(self.lbl)
        self.addPage(page3)

        self.currentIdChanged.connect(self._on_page)

    # — override —
    def accept(self):
        date = self.cal.selectedDate().toPython()
        sez  = [self.list_sez.item(i).text()
                for i in range(self.list_sez.count())
                if self.list_sez.item(i).checkState()==Qt.Checked]
        try:
            self.services.purchase_ticket(date, sez)  # + email/tipo se vuoi
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "Errore", str(e))

    # — internals —
    def _on_page(self, idx):
        if idx==1:       # SEZIONI
            self._fill_sections()
        elif idx==2:     # RIEPILOGO
            d = self.cal.selectedDate().toString("dd/MM/yyyy")
            s = ", ".join([self.list_sez.item(i).text()
                           for i in range(self.list_sez.count())
                           if self.list_sez.item(i).checkState()==Qt.Checked])
            self.lbl.setText(f"<b>Data:</b> {d}<br><b>Sezioni:</b> {s}")

    def _fill_sections(self):
        self.list_sez.clear()
        # TODO: sections = self.services.sections_available(self.cal.selectedDate())
        dummy = ["Impressionismo", "Rinascimento", "Arte Moderna"]
        for s in dummy:
            item = QListWidgetItem(s); item.setFlags(item.flags()|Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked); self.list_sez.addItem(item)

# ──────────────────────────── Wrapper UtentePage ────────────────────────────
class UtentePage(QWidget):
    def __init__(self, services):
        super().__init__()
        self.setStyleSheet(BASE_STYLE)          # <-- stile ereditato
        tabs = QTabWidget(self)
        tabs.addTab(TicketsTab(services), "Biglietti")
        tabs.addTab(VisitsTab(services),  "Visite guidate")
        tabs.addTab(ProfileTab(services), "Profilo")
        QVBoxLayout(self).addWidget(tabs)
