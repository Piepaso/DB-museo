from __future__ import annotations

from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QTableView, QToolBar, QPushButton, QListWidget, QListWidgetItem,
    QCalendarWidget, QWizard, QWizardPage, QFormLayout, QLineEdit, QLabel,
    QMessageBox, QHeaderView, QLineEdit
)

# ────────────────────────────────────────────────────────────────────────────
# Stile globale: ereditato dall'app principale e miglioramenti estetici
# ---------------------------------------------------------------------------
try:
    from style import BASE_STYLE  # noqa: F401 – usato via setStyleSheet()
except ModuleNotFoundError:
    BASE_STYLE = ""  # Fallback: nessuno stile di base

# Stile aggiuntivo per un'estetica più moderna e spaziosa
EXTRA_STYLE = """
/* Tab bar più ariosa e leggibile */
QTabBar::tab {
    padding: 10px 25px; /* Aumenta il padding per un look più spazioso */
    font-size: 16px;    /* Aumenta la dimensione del font */
    font-weight: 500;   /* Rende il testo leggermente più audace */
    color: #4a5568;     /* Colore del testo più scuro per contrasto */
    border-top-left-radius: 8px; /* Bordi arrotondati */
    border-top-right-radius: 8px;
    margin-right: 4px; /* Spazio tra i tab */
}
QTabBar::tab:selected {
    background: #e0e7ff; /* Sfondo per il tab selezionato */
    color: #2b6cb0;      /* Colore del testo per il tab selezionato */
    font-weight: 600;    /* Testo più audace quando selezionato */
    border-bottom: 3px solid #2b6cb0; /* Sottolineatura per il tab selezionato */
}
QTabBar::tab:hover {
    background: #edf2f7; /* Sfondo al passaggio del mouse */
}

/* Tabelle con righe alternate (zebra) e header migliorato */
QTableView {
    background: #ffffff;
    alternate-background-color: #f8fafc; /* Colore più chiaro per le righe alternate */
    border: 1px solid #e2e8f0; /* Bordo sottile per la tabella */
    border-radius: 8px; /* Bordi leggermente arrotondati */
    gridline-color: #cbd5e1; /* Colore delle linee della griglia */
}
QHeaderView::section {
    background: #ebf4ff; /* Sfondo più chiaro per l'header */
    font-weight: 600;
    padding: 8px 12px; /* Padding aumentato per l'header */
    border-bottom: 2px solid #a7c7ed; /* Bordo inferiore più pronunciato */
    color: #2d3748; /* Colore del testo dell'header */
}

/* LineEdit generale con stile moderno */
QLineEdit {
    padding: 10px 12px; /* Padding generoso */
    border: 1px solid #cbd5e1;
    border-radius: 8px; /* Bordi più arrotondati */
    font-size: 15px;
    color: #2d3748;
    background-color: #ffffff;
}
QLineEdit:focus {
    border: 1px solid #6366f1; /* Bordo evidenziato al focus */
    background-color: #f0f4ff; /* Sfondo leggermente colorato al focus */
}

/* Pulsanti con effetto hover */
QPushButton {
    padding: 10px 20px;
    border-radius: 8px;
    background-color: #4299e1; /* Blu primario */
    color: white;
    font-weight: 600;
    border: none;
    cursor: pointer;
}
QPushButton:hover {
    background-color: #3182ce; /* Blu più scuro all'hover */
}
QPushButton:pressed {
    background-color: #2c5282; /* Blu ancora più scuro al click */
}

/* QLabel per header di sezione */
QLabel[class="section-header"] {
    font-size: 20px; /* Dimensione maggiore per i titoli di sezione */
    font-weight: 700; /* Più audace */
    color: #2d3748; /* Colore scuro per il testo */
    margin-bottom: 10px; /* Spazio sotto l'header */
    padding-bottom: 5px; /* Padding interno */
    border-bottom: 1px solid #e2e8f0; /* Linea sottile sotto il titolo */
}

/* QToolBar */
QToolBar {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 5px;
    spacing: 10px; /* Spazio tra gli elementi della toolbar */
}
QToolBar QToolButton {
    padding: 8px 12px;
    border-radius: 6px;
    background: transparent;
    color: #2d3748;
    font-weight: 500;
}
QToolBar QToolButton:hover {
    background: #edf2f7;
}
QToolBar QToolButton:pressed {
    background: #e2e8f0;
}

/* QListWidget nel wizard */
QListWidget {
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 5px;
    background-color: #ffffff;
}
QListWidget::item {
    padding: 8px 5px;
}
QListWidget::item:selected {
    background: #e0e7ff;
    color: #2b6cb0;
}
"""


# ═════════════════════════════ TAB 1 · BIGLIETTI ════════════════════════════
class TicketsTab(QWidget):
    """
    Gestisce la visualizzazione e l'acquisto dei biglietti.
    Include una barra di ricerca e una tabella interattiva.
    """
    def __init__(self, services):
        super().__init__()
        self.services = services
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20) # Aggiunge margini per estetica

        # — Header & search bar —
        header = QLabel("🎟️ I miei Biglietti")
        header.setProperty("class", "section-header") # Applica stile header
        root.addWidget(header)

        search_bar = QLineEdit(placeholderText="Cerca per sezione o data...")
        search_bar.textChanged.connect(self._filter_table)
        root.addWidget(search_bar)

        # — Toolbar —
        tb = QToolBar()
        tb.setMovable(False) # Rende la toolbar fissa
        act_refresh = QAction(QIcon.fromTheme("view-refresh"), "Aggiorna", self)
        act_purchase = QAction(QIcon.fromTheme("document-new"), "Acquista Biglietto...", self)
        tb.addActions((act_refresh, act_purchase))
        root.addWidget(tb)

        # — Table —
        self.table = QTableView(alternatingRowColors=True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        root.addWidget(self.table, 1)

        act_refresh.triggered.connect(self.refresh)
        act_purchase.triggered.connect(self.open_wizard)

    # TODO: implementare modello + filtro
    def refresh(self):
        """Popola la tabella con i dati da services.list_tickets()"""
        # Esempio: self.table.setModel(TicketTableModel(self.services.list_tickets()))
        QMessageBox.information(self, "Aggiorna", "Funzione di aggiornamento da implementare.")
        pass

    def _filter_table(self, text: str):
        """Filtra la tabella dei biglietti in base al testo inserito."""
        # Se usi QSortFilterProxyModel: self.proxy_model.setFilterFixedString(text)
        pass

    def open_wizard(self):
        """Apre il wizard per l'acquisto di un nuovo biglietto."""
        if PurchaseWizard(self.services, self).exec():
            QMessageBox.information(self, "Acquisto Completato", "Biglietto acquistato con successo!")
            self.refresh()


# ═══════════════════════════ TAB 2 · VISITE GUIDATE ══════════════════════════
class VisitsTab(QWidget):
    """
    Visualizza le visite guidate disponibili e permette la prenotazione.
    """
    def __init__(self, services):
        super().__init__()
        self.services = services
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)

        header = QLabel("🗓️ Visite Guidate Disponibili")
        header.setProperty("class", "section-header")
        root.addWidget(header)

        self.table = QTableView(alternatingRowColors=True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        root.addWidget(self.table, 1)

        btn_box = QHBoxLayout()
        btn_box.addStretch(1) # Spinge il bottone a destra
        self.btn_book = QPushButton("Prenota Visita", cursor=Qt.PointingHandCursor)
        self.btn_book.clicked.connect(self.book_selected)
        btn_box.addWidget(self.btn_book)
        root.addLayout(btn_box)

        self.refresh_visits() # Popola la tabella all'inizializzazione

    # TODO: modello + prenotazione
    def refresh_visits(self):
        """Popola la tabella con le visite guidate disponibili."""
        # Esempio: self.table.setModel(VisitsTableModel(self.services.list_available_visits()))
        QMessageBox.information(self, "Visite", "Funzione di caricamento visite da implementare.")
        pass

    def book_selected(self):
        """Gestisce la prenotazione della visita selezionata."""
        # Esempio: selected_row = self.table.currentIndex().row()
        # if selected_row >= 0:
        #     visit_data = self.table.model().data_at_row(selected_row)
        #     self.services.book_visit(visit_data)
        QMessageBox.information(self, "Prenota", "Funzione di prenotazione da implementare.")
        pass


# ═════════════════════════════ TAB 3 · PROFILO ═════════════════════════════
class ProfileTab(QWidget):
    """
    Permette all'utente di visualizzare e aggiornare i propri dati del profilo.
    """
    def __init__(self, services):
        super().__init__()
        self.services = services
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)

        header = QLabel("👤 I Miei Dati")
        header.setProperty("class", "section-header")
        root.addWidget(header)

        form = QFormLayout()
        form.setRowWrapPolicy(QFormLayout.WrapAllRows)
        form.setLabelAlignment(Qt.AlignLeft)
        form.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.le_cf = QLineEdit()
        self.le_mail = QLineEdit()
        self.le_mail.setInputMask("99/99/9999") # Esempio di input mask

        form.addRow("Codice Fiscale:", self.le_cf)
        form.addRow("E-mail:", self.le_mail)
        root.addLayout(form)

        btn_box = QHBoxLayout()
        btn_box.addStretch(1)
        btn_save = QPushButton("Salva Modifiche", cursor=Qt.PointingHandCursor)
        btn_save.clicked.connect(self._save)
        btn_box.addWidget(btn_save)
        root.addLayout(btn_box)

        self._load_profile_data() # Carica i dati del profilo all'inizializzazione

    def _load_profile_data(self):
        """Carica i dati del profilo utente nei campi."""
        try:
            # TODO: implementare self.services.get_profile_data()
            demo_data = {"cf": "RSSMRA80A01H501U", "email": "mario.rossi@example.com"}
            self.le_cf.setText(demo_data.get("cf", ""))
            self.le_mail.setText(demo_data.get("email", ""))
        except Exception as e:
            QMessageBox.warning(self, "Caricamento Fallito", f"Impossibile caricare i dati del profilo: {e}")

    def _save(self):
        """Salva le modifiche ai dati del profilo."""
        try:
            self.services.update_profile(self.le_cf.text(), self.le_mail.text())
            QMessageBox.information(self, "Successo", "Profilo aggiornato con successo!")
        except Exception as e:
            QMessageBox.critical(self, "Errore di Salvataggio", f"Errore durante l'aggiornamento del profilo: {e}")


# ═════════════════════ Wizard · Acquisto Biglietto ══════════════════════════
class PurchaseWizard(QWizard):
    """
    Wizard guidato per l'acquisto di un biglietto, che include la selezione
    della data, delle sezioni e un riepilogo finale.
    """
    def __init__(self, services, parent=None):
        super().__init__(parent)
        self.services = services
        self.setWindowTitle("Acquisto Biglietto")
        self.setWizardStyle(QWizard.ModernStyle) # Stile moderno per il wizard
        self.setOption(QWizard.NoCancelButtonOnStartPage, True) # Nasconde il tasto Annulla all'inizio

        # Pagina 1 – Data della visita
        p1 = QWizardPage()
        p1.setTitle("1. Seleziona la Data")
        p1.setSubTitle("Scegli il giorno in cui desideri effettuare la visita.")
        v1 = QVBoxLayout(p1)
        self.cal = QCalendarWidget(minimumDate=QDate.currentDate())
        self.cal.setStyleSheet("""
            QCalendarWidget QToolButton {
                background-color: #6366f1; /* Colore pulsanti navigazione calendario */
                color: white;
                border-radius: 4px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #4f46e5;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: #2d3748;
                selection-background-color: #bfdbfe; /* Colore selezione */
                selection-color: #2b6cb0;
            }
        """)
        v1.addWidget(self.cal)
        self.addPage(p1)

        # Pagina 2 – Sezioni disponibili
        p2 = QWizardPage()
        p2.setTitle("2. Scegli le Sezioni")
        p2.setSubTitle("Seleziona le sezioni che desideri visitare.")
        v2 = QVBoxLayout(p2)
        self.list_sez = QListWidget()
        self.list_sez.setSelectionMode(QListWidget.MultiSelection) # Permette selezioni multiple
        v2.addWidget(self.list_sez)
        self.addPage(p2)

        # Pagina 3 – Riepilogo acquisto
        p3 = QWizardPage()
        p3.setTitle("3. Riepilogo Acquisto")
        p3.setSubTitle("Controlla i dettagli del tuo acquisto prima di confermare.")
        v3 = QVBoxLayout(p3)
        self.lbl_sum = QLabel()
        self.lbl_sum.setStyleSheet("font-size: 16px; padding: 10px; border: 1px dashed #cbd5e1; border-radius: 8px;")
        v3.addWidget(self.lbl_sum)
        self.addPage(p3)

        self.currentIdChanged.connect(self._on_page_change)

    # — override —
    def accept(self):
        """
        Convalida e finalizza l'acquisto del biglietto.
        Chiamato quando il wizard è completato (tasto 'Finish').
        """
        date = self.cal.selectedDate().toPyDate() # Usa toPyDate() per un oggetto date standard
        selected_sections = [
            self.list_sez.item(i).text()
            for i in range(self.list_sez.count())
            if self.list_sez.item(i).checkState() == Qt.Checked
        ]

        if not selected_sections:
            QMessageBox.warning(self, "Attenzione", "Seleziona almeno una sezione per continuare.")
            return

        try:
            # TODO: Aggiungi parametri per email/tipo se necessario
            self.services.purchase_ticket(date, selected_sections)
            super().accept() # Chiude il wizard se l'acquisto va a buon fine
        except Exception as e:
            QMessageBox.critical(self, "Errore di Acquisto", f"Si è verificato un errore durante l'acquisto: {e}")

    # — internal logic —
    def _on_page_change(self, idx: int):
        """Gestisce le azioni da eseguire al cambio di pagina del wizard."""
        if idx == 1:  # Pagina 2 (indice 1): Sezioni disponibili
            self._fill_sections()
        elif idx == 2:  # Pagina 3 (indice 2): Riepilogo
            self._make_summary()

    def _fill_sections(self):
        """Popola la lista delle sezioni disponibili in base alla data selezionata."""
        self.list_sez.clear()
        # TODO: Implementare la logica per ottenere le sezioni disponibili per la data
        # sez_disponibili = self.services.sections_available(self.cal.selectedDate())
        demo_sections = ["Impressionismo", "Rinascimento", "Arte Moderna", "Scultura Classica", "Collezione Egizia"]
        for s in demo_sections:
            it = QListWidgetItem(s)
            it.setFlags(it.flags() | Qt.ItemIsUserCheckable)
            it.setCheckState(Qt.Checked) # Di default, tutte le sezioni sono selezionate
            self.list_sez.addItem(it)

    def _make_summary(self):
        """Genera il riepilogo dell'acquisto per la pagina finale del wizard."""
        selected_date = self.cal.selectedDate().toString("dd/MM/yyyy")
        selected_sections_text = ", ".join([
            self.list_sez.item(i).text()
            for i in range(self.list_sez.count())
            if self.list_sez.item(i).checkState() == Qt.Checked
        ])
        if not selected_sections_text:
            selected_sections_text = "Nessuna sezione selezionata."

        summary_html = (
            f"<b>Data della visita:</b> {selected_date}<br>"
            f"<b>Sezioni selezionate:</b> {selected_sections_text}<br><br>"
            f"<i>Conferma per procedere all'acquisto.</i>"
        )
        self.lbl_sum.setText(summary_html)


# ═══════════════════════════ Wrapper UtentePage ═════════════════════════════
class UtentePage(QWidget):
    """
    Widget principale che aggrega tutte le schede dell'interfaccia utente.
    Applica lo stile globale definito.
    """
    def __init__(self, services):
        super().__init__()
        # Applica lo stile combinando BASE_STYLE e EXTRA_STYLE
        if BASE_STYLE or EXTRA_STYLE:
            self.setStyleSheet(BASE_STYLE + EXTRA_STYLE)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0) # Rimuove margini per un look "edge-to-edge"

        tabs = QTabWidget(self)
        tabs.addTab(TicketsTab(services), "🎟️ Biglietti")
        tabs.addTab(VisitsTab(services), "🗓️ Visite Guidate")
        tabs.addTab(ProfileTab(services), "👤 Profilo")

        main_layout.addWidget(tabs)