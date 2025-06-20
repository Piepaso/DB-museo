# DB‑Museo · Ambiente di sviluppo

Questa guida spiega come **ricreare da zero** l’ambiente virtuale, installare le dipendenze (PySide 6, SQLAlchemy, ecc.) ed avviare l’applicazione GUI.

> **Testato il 16 giugno 2025** su macOS 14 (Apple Silicon), Ubuntu 24.04 e Windows 11 con Python 3.11.6.

---

## 1 · Prerequisiti

| Strumento  | Versione consigliata | Note                                                                               |
| ---------- | -------------------- | ---------------------------------------------------------------------------------- |
| **Python** | 3.11 x64/ARM64       | 3.9+ funziona, ma 3.11 è più veloce; evitare 3.13 (PySide non ancora compatibile). |
| **pip**    | ≥ 24                 | `python -m pip install -U pip`                                                     |
| **Git**    | qualsiasi            | per clonare il repository                                                          |
| **MySQL**  | 8.x                  | necessario solo se vuoi testare la parte DB                                        |

Facoltativo ma utile:

* **pyenv** (Linux/macOS) o **conda/mamba** se hai bisogno di isolare più interpreti.

---

## 2 · Clona il progetto

```bash
$ git clone https://github.com/tuo‑username/DB‑museo.git
$ cd DB‑museo
```

---

## 3 · Crea e attiva il virtual‑env

### macOS / Linux (bash/zsh)

```bash
$ python3.11 -m venv .venv
$ source .venv/bin/activate
(.venv) $
```

### Windows PowerShell

```powershell
PS> py -3.11 -m venv .venv
PS> .\.venv\Scripts\Activate.ps1
(.venv) PS>
```

> **Tip** : aggiungi `DB‑museo/.venv` al tuo `.gitignore`.

---

## 4 · Aggiorna gli strumenti base

```bash
(.venv) $ python -m pip install -U pip wheel setuptools
```

---

## 5 · Installa le dipendenze

Il progetto usa una **constraints file** per fissare le versioni note‑funzionanti; installa con:

```bash
(.venv) $ pip install -r requirements.txt
```

Se preferisci un comando rapido senza file:

```bash
(.venv) $ pip install "pyside6<6.8" sqlalchemy mysql‑connector‑python python‑dotenv
```

### Perché `pyside6<6.8`?

La 6.9.1 contiene un bug di packaging che lancia `SyntaxError` alla fase di `compileall`. Le release 6.7.x (LTS) o 6.8.x funzionano perfettamente.

---

## 6 · Configura le variabili d’ambiente

Copia `.env.example` → `.env` e compila la stringa di connessione MySQL:

```env
MYSQL_URL=mysql+mysqlconnector://user:password@localhost:3306/db_museo
```

---

## 7 · Avvia l’applicazione

```bash
(.venv) $ python application/main_app.py
```

Dovresti vedere la finestra **“Museo DB”** con i pulsanti **Utente** e **Museo**.

---

## 8 · Problemi comuni

### « Could not find the Qt platform plugin “cocoa” »

Su macOS Gatekeeper può bloccare i plugin Qt. Risolvi con:

```bash
$ plugin_dir=$(python - <<'PY'
import pathlib, PySide6, sys; print(pathlib.Path(PySide6.__file__).parent/'Qt/plugins')
PY)
$ sudo xattr -dr com.apple.quarantine "$plugin_dir"
```

Oppure esporta la variabile:

```bash
export QT_QPA_PLATFORM_PLUGIN_PATH=$(python - <<'PY'
import pathlib, PySide6, sys; print(pathlib.Path(PySide6.__file__).parent/'Qt/plugins/platforms')
PY)
```

### ImportError « QAction »

Assicurati che l’import sia:

```python
from PySide6.QtGui import QAction  # non in QtWidgets
```

---

## 9 · Aggiornare le dipendenze

```bash
(.venv) $ pip list --outdated
(.venv) $ pip install -U nome‑pacchetto
```

> Aggiorna PySide solo quando il team Qt pubblica note di compatibilità con la tua versione di Python.

---

## 10 · Disattivare e rimuovere l’ambiente

```bash
(.venv) $ deactivate   # esci dal venv
$ rm -rf .venv         # cancella la cartella
```

---

Buon lavoro! Se qualcosa non funziona apri una *Issue* o contattaci su Teams.

