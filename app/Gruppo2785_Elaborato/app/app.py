"""
Flask application collegata al DB *museo*.

Sono stati corretti tutti i nomi di tabelle/colonne che in precedenza
comparivano al plurale: ora rispettano i nomi esatti definiti nello
schema `museo_normalizzato.sql` (SEZIONE, OPERA, BIGLIETTO_ACQUISTATO,
VISITA_GUIDATA, VISITATORE, GUIDA, RESTAURATORE, RESTAURO).

Le query sono inoltre adeguate alle PK/FK effettive.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email
import mysql.connector
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# ——————————————————— DB CONFIG ———————————————————
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',          # ← usa l'account applicativo in produzione
    'password': 'frittatina',
    'database': 'museo',
    'auth_plugin': 'mysql_native_password',
    'raise_on_warnings': True,
    'charset': 'utf8mb4'
}

def get_db_connection():
    """Restituisce una connessione MySQL."""
    return mysql.connector.connect(**DB_CONFIG)

# ——————————————————— FORM DEFINITIONS ——————————————————
# (nessuna modifica necessaria)
class OperePerSezioneForm(FlaskForm):
    sezione = StringField('Nome Sezione', validators=[DataRequired()])

class SezioniDisponibiliForm(FlaskForm):
    data = DateField('Data', validators=[DataRequired()])

class SezioniPerAutoreForm(FlaskForm):
    autore = StringField('Nome d’arte Autore', validators=[DataRequired()])

class SezioneOperaForm(FlaskForm):
    opera = StringField('Titolo Opera', validators=[DataRequired()])

class VisiteGuidateForm(FlaskForm):
    pass  # nessun input

class AutoriPerGuidaForm(FlaskForm):
    numero_badge = IntegerField('Numero Badge Guida', validators=[DataRequired()])
    data = DateField('Data', validators=[DataRequired()])

class RegistraVisitatore(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cognome = StringField('Cognome', validators=[DataRequired()])
    codice_fiscale = StringField('Codice Fiscale', validators=[DataRequired()])
    data_nascita = DateField('Data di Nascita', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])


class ModificaEmailForm(FlaskForm):
    codice_fiscale = StringField('Codice Fiscale', validators=[DataRequired()])
    nuova_email = StringField('Nuova Email', validators=[DataRequired()])

class AcquistaBigliettoForm(FlaskForm):
    sezioni = TextAreaField('Lista Sezioni (separate da virgola)', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    data = DateField('Data', validators=[DataRequired()])
    tipo = SelectField('Tipo Biglietto', choices=[('intero', 'Intero'), ('ridotto', 'Ridotto'), ('gratuito', 'Gratuito')])

class TimbraBigliettoForm(FlaskForm):
    codice_fiscale = StringField('Codice Fiscale', validators=[DataRequired()])
    data = DateField('Data', validators=[DataRequired()])

class ProgrammaRestauroForm(FlaskForm):
    descrizione = TextAreaField('Descrizione...', validators=[DataRequired()])
    opera = StringField('Titolo Opera', validators=[DataRequired()])
    data_inizio = DateField('Data Inizio', validators=[DataRequired()])
    data_fine = DateField('Data Fine', validators=[DataRequired()])

class ProgrammaVisitaGuidataForm(FlaskForm):
    data = DateField('Data', validators=[DataRequired()])
    ora_inizio = StringField('Ora inizio (HH:MM)', validators=[DataRequired()])
    ora_fine = StringField('Ora fine (HH:MM)', validators=[DataRequired()])
    numero_posti = IntegerField('Numero Posti', validators=[DataRequired()])
    numero_badge = IntegerField('Numero Badge Guida', validators=[DataRequired()])

class AnnullaVisitaGuidataForm(FlaskForm):
    numero_badge = IntegerField('Numero Badge Guida', validators=[DataRequired()])
    data_visita = DateField('Data Visita', validators=[DataRequired()])

class RestauratoriRestauroForm(FlaskForm):
    opera = StringField('Titolo Opera', validators=[DataRequired()])
    data_inizio = DateField('Data Inizio Restauro', validators=[DataRequired()])

class BigliettiTimbrati(FlaskForm):
    data_inizio = DateField('Data Inizio', validators=[DataRequired()])
    data_fine = DateField('Data Fine', validators=[DataRequired()])

class VisiteGuidateConcluseForm(FlaskForm):
    pass

# ——————————————————— ROUTES ———————————————————
@app.route('/')
def index():
    return render_template('index.html')

# ——— SCELTA BIGLIETTO ——————————————————————————
@app.route('/opere-per-sezione', methods=['GET', 'POST'])
def opere_per_sezione():
    form = OperePerSezioneForm()
    results = []
    if form.validate_on_submit():
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute(
            """
            SELECT o.nomeOpera, o.nomeDArte
            FROM   OPERA o
            WHERE  o.nomeSezione = %s
            ORDER  BY o.nomeDArte
            """,
            (form.sezione.data,)
        )
        results = cur.fetchall(); cur.close(); conn.close()
    return render_template('query_form.html', form=form, results=results, title="Opere per Sezione")

@app.route('/sezioni-disponibili', methods=['GET', 'POST'])
def sezioni_disponibili():
    form = SezioniDisponibiliForm(); results = []
    if form.validate_on_submit():
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute(
            """
            SELECT s.nomeSezione,
            SUM(sa.capienza) AS capienzaTotale,
            COUNT(DISTINCT a.idBiglietto) AS n_accessi
            FROM SEZIONE s
            JOIN SALA sa ON sa.nomeSezione = s.nomeSezione
            LEFT JOIN ACCESSO a ON a.nomeSezione = s.nomeSezione
            LEFT JOIN BIGLIETTO_ACQUISTATO b ON b.idBiglietto = a.idBiglietto AND b.dataPerIngresso = %s
            GROUP BY s.nomeSezione
            HAVING COUNT(DISTINCT a.idBiglietto) < SUM(sa.capienza);

            """,
            (form.data.data,)
        )
        results = cur.fetchall(); cur.close(); conn.close()
    return render_template('query_form.html', form=form, results=results, title="Sezioni Disponibili")

@app.route('/sezioni-per-autore', methods=['GET', 'POST'])
def sezioni_per_autore():
    form = SezioniPerAutoreForm(); results = []
    if form.validate_on_submit():
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute(
            """
            SELECT DISTINCT nomeSezione
            FROM   OPERA
            WHERE  nomeDArte = %s
            """,
            (form.autore.data,)
        )
        results = cur.fetchall(); cur.close(); conn.close()
    return render_template('query_form.html', form=form, results=results, title="Sezioni per Autore")

@app.route('/sezione-opera', methods=['GET', 'POST'])
def sezione_opera():
    form = SezioneOperaForm(); results = []
    if form.validate_on_submit():
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute(
            """
            SELECT nomeSezione
            FROM   OPERA
            WHERE  nomeOpera = %s
            """,
            (form.opera.data,)
        )
        results = cur.fetchall(); cur.close(); conn.close()
    return render_template('query_form.html', form=form, results=results, title="Sezione dell'Opera")

@app.route('/visite-guidate', methods=['GET', 'POST'])
def visite_guidate():
    # No form fields → mostra tutte le visite
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute(
        """
        SELECT vg.NumeroBadge,
               vg.dataVisita,
               vg.oraInizio,
               vg.oraFine,
               vg.numeroPosti,
               (vg.numeroPosti - COALESCE(COUNT(b.idBiglietto),0)) AS posti_rimanenti
        FROM   VISITA_GUIDATA vg
        LEFT   JOIN BIGLIETTO_ACQUISTATO b
               ON  b.NumeroBadge  = vg.NumeroBadge
               AND b.dataVisita   = vg.dataVisita
        GROUP  BY vg.NumeroBadge, vg.dataVisita, vg.oraInizio, vg.oraFine, vg.numeroPosti
        ORDER  BY vg.dataVisita, vg.oraInizio
        """
    )
    results = cur.fetchall(); cur.close(); conn.close()
    return render_template('query_form.html', form=VisiteGuidateForm(), results=results, title="Visite Guidate Disponibili")

@app.route('/autori-per-guida', methods=['GET', 'POST'])
def autori_per_guida():
    form = AutoriPerGuidaForm(); results = []
    if form.validate_on_submit():
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute(
            """
            SELECT DISTINCT a.nomeDArte, a.nomeCompleto
            FROM VISITA_GUIDATA vg
            JOIN GUIDA g ON g.numeroBadge = g.numeroBadge
            JOIN AUTORE a ON a.nomeMovimento = g.nomeMovimento
            WHERE g.numeroBadge = %s
            AND vg.dataVisita = %s;
            """,
            (form.numero_badge.data, form.data.data)
        )
        results = cur.fetchall(); cur.close(); conn.close()
    return render_template('query_form.html', form=form, results=results, title="Autori della Guida")

# ——— ACQUISTO BIGLIETTO ——————————————————————————
@app.route('/registra-visitatore', methods=['GET', 'POST'])
def registra_visitatore():
    form = RegistraVisitatore()
    if form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # First insert into anagrafica table
            anagrafica_query = """
            INSERT INTO anagrafica (CodiceFiscale, Nome, Cognome, DataDiNascita) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(anagrafica_query, (form.codice_fiscale.data, form.nome.data, 
                                            form.cognome.data, form.data_nascita.data))
            
            # Then insert into visitatore table
            visitatore_query = """
            INSERT INTO visitatore (CodiceFiscale, Email) 
            VALUES (%s, %s)
            """
            cursor.execute(visitatore_query, (form.codice_fiscale.data, form.email.data))
            
            conn.commit()
            flash('Visitatore registrato con successo!', 'success')
        except mysql.connector.Error as e:
            conn.rollback()
            flash(f'Errore: {e}', 'error')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('registra_visitatore'))
    return render_template('query_form.html', form=form, results=[], title="Registra Visitatore")


@app.route('/modifica-email', methods=['GET', 'POST'])
def modifica_email():
    form = ModificaEmailForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        UPDATE visitatore 
        SET Email = %s 
        WHERE CodiceFiscale = %s
        """
        cursor.execute(query, (form.nuova_email.data, form.codice_fiscale.data))
        conn.commit()
        flash(f'Email modificata per {cursor.rowcount} visitatore(i)', 'success')
        cursor.close()
        conn.close()
        return redirect(url_for('modifica_email'))
    return render_template('query_form.html', form=form, results=[], title="Modifica Email")


@app.route('/acquista-biglietto', methods=['GET', 'POST'])
def acquista_biglietto():
    form = AcquistaBigliettoForm()
    if form.validate_on_submit():
        sezioni = [s.strip() for s in form.sezioni.data.split(',') if s.strip()]
        conn = get_db_connection(); cur = conn.cursor()
        id_biglietto = f"B{uuid.uuid4().hex[:6].upper()}"  # esempio: B4F9A3
        try:
            cur.execute(
                    """
                    INSERT INTO BIGLIETTO_ACQUISTATO (
                        idBiglietto, data_acquisto, dataPerIngresso, ingressoAvvenuto,
                        perVisita, categoriaBiglietto, email
                    ) VALUES (
                        %s, CURDATE(), %s, 'N','normale', %s, %s
                    );
                    """,
                    (id_biglietto, form.data.data, form.tipo.data, form.email.data)
                )
            for sezione in sezioni:
                cur.execute(
                    """
                    INSERT INTO ACCESSO (idBiglietto, nomeSezione)
                    VALUES (%s, %s);
                    """,
                    (id_biglietto, sezione)
                )
            conn.commit(); flash('Biglietto/i acquistato/i!', 'success')
        except mysql.connector.Error as e:
            conn.rollback(); flash(f'Errore: {e}', 'error')
        finally:
            cur.close(); conn.close()
        return redirect(url_for('acquista_biglietto'))
    return render_template('query_form.html', form=form, results=[], title="Acquista Biglietto")

@app.route('/timbra-biglietto', methods=['GET', 'POST'])
def timbra_biglietto():
    form = TimbraBigliettoForm()
    if form.validate_on_submit():
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute(
            """
            UPDATE BIGLIETTO_ACQUISTATO b
            JOIN   VISITATORE v ON v.email = b.email
            SET    b.ingressoAvvenuto = 'Y'
            WHERE  v.CodiceFiscale = %s
            AND    b.dataPerIngresso = %s
            """,
            (form.codice_fiscale.data, form.data.data)
        )
        conn.commit(); flash(f'Timbrati {cur.rowcount} biglietti', 'success')
        cur.close(); conn.close()
        return redirect(url_for('timbra_biglietto'))
    return render_template('query_form.html', form=form, results=[], title="Timbra Biglietto")

# ——— AMMINISTRAZIONE ———————————————————————————
@app.route('/programma-restauro', methods=['GET', 'POST'])
def programma_restauro():
    form = ProgrammaRestauroForm(); results = []
    if form.validate_on_submit():
        conn = get_db_connection(); cur = conn.cursor()
        try:
            # Inserisci restauro
            cur.execute(
                """INSERT INTO RESTAURO (idOpera, dataInizio, dataFine, dettagliRestauro)
                       SELECT idOpera, %s, %s, %s
                       FROM   OPERA WHERE nomeOpera = %s""",
                (form.data_inizio.data, form.data_fine.data, form.descrizione.data, form.opera.data)
            )
            # Visitatori coinvolti
            cur.execute(
                """SELECT DISTINCT v.email
                   FROM   VISITATORE v
                   JOIN   BIGLIETTO_ACQUISTATO b ON b.email = v.email
                   JOIN   OPERA o              ON o.nomeSezione = b.perVisita
                   WHERE  o.nomeOpera = %s
                   AND    b.dataPerIngresso BETWEEN %s AND %s""",
                (form.opera.data, form.data_inizio.data, form.data_fine.data)
            )
            results = cur.fetchall(); conn.commit(); flash('Restauro programmato!', 'success')
        except mysql.connector.Error as e:
            conn.rollback(); flash(f'Errore: {e}', 'error')
        finally:
            cur.close(); conn.close()
    return render_template('query_form.html', form=form, results=results, title="Programma Restauro")

@app.route('/programma-visita-guidata', methods=['GET', 'POST'])
def programma_visita_guidata():
    form = ProgrammaVisitaGuidataForm()
    if form.validate_on_submit():
        conn = get_db_connection(); cur = conn.cursor()
        try:
            cur.execute(
                """INSERT INTO VISITA_GUIDATA (NumeroBadge, numeroPosti, dataVisita,
                                                 prezzoVisita, oraInizio, oraFine, postiResidui, ID_LIN)
                       VALUES (%s, %s, %s, 10, %s, %s, %s, 1)""",
                (
                    form.numero_badge.data,
                    form.numero_posti.data,
                    form.data.data,
                    int(form.ora_inizio.data.replace(':','')),
                    int(form.ora_fine.data.replace(':','')),
                    form.numero_posti.data
                )
            )
            conn.commit(); flash('Visita guidata programmata!', 'success')
        except mysql.connector.Error as e:
            conn.rollback(); flash(f'Errore: {e}', 'error')
        finally:
            cur.close(); conn.close()
        return redirect(url_for('programma_visita_guidata'))
    return render_template('query_form.html', form=form, results=[], title="Programma Visita Guidata")

@app.route('/annulla-visita-guidata', methods=['GET', 'POST'])
def annulla_visita_guidata():
    form = AnnullaVisitaGuidataForm(); results = []
    if form.validate_on_submit():
        conn = get_db_connection(); cur = conn.cursor()
        # Visitatori da avvisare
        cur.execute(
            """SELECT DISTINCT v.email
               FROM   VISITATORE v
               JOIN   BIGLIETTO_ACQUISTATO b ON b.email = v.email
               WHERE  b.NumeroBadge = %s AND b.dataVisita = %s""",
            (form.numero_badge.data, form.data_visita.data)
        )
        results = cur.fetchall()
        #Cancella i biglietti associati
        cur.execute(
            """DELETE FROM BIGLIETTO_ACQUISTATO
               WHERE NumeroBadge = %s AND dataVisita = %s""",
            (form.numero_badge.data, form.data_visita.data)
        )
        # Cancella la visita
        cur.execute(
            """DELETE FROM VISITA_GUIDATA
               WHERE NumeroBadge = %s AND dataVisita = %s""",
            (form.numero_badge.data, form.data_visita.data)
        )
        conn.commit(); cur.close(); conn.close(); flash('Visita annullata!', 'success')
    return render_template('query_form.html', form=form, results=results, title="Annulla Visita Guidata")

@app.route('/restauratori-restauro', methods=['GET', 'POST'])
def restauratori_restauro():
    form = RestauratoriRestauroForm(); results = []
    if form.validate_on_submit():
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute(
            """SELECT r.matricola, a.nome, a.cognome
               FROM   RESTAURATORE r
               JOIN   ANAGRAFICA a ON a.CodiceFiscale = r.CodiceFiscale
               JOIN   EFFETUAZIONE e ON e.matricola = r.matricola
               JOIN   OPERA o        ON o.idOpera  = e.idOpera
               WHERE  o.nomeOpera = %s AND e.dataInizio = %s""",
            (form.opera.data, form.data_inizio.data)
        )
        results = cur.fetchall(); cur.close(); conn.close()
    return render_template('query_form.html', form=form, results=results, title="Restauratori coinvolti")

@app.route('/biglietti-timbrati', methods=['GET', 'POST'])
def biglietti_timbrati():
    form = BigliettiTimbrati(); results = []
    if form.validate_on_submit():
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute(
            """SELECT perVisita AS sezione, COUNT(*)
               FROM   BIGLIETTO_ACQUISTATO
               WHERE  ingressoAvvenuto = 'Y'
               AND    dataPerIngresso BETWEEN %s AND %s
               GROUP  BY perVisita
               ORDER  BY 2 DESC""",
            (form.data_inizio.data, form.data_fine.data)
        )
        results = cur.fetchall(); cur.close(); conn.close()
    return render_template('query_form.html', form=form, results=results, title="Biglietti Timbrati")

@app.route('/visite-guidate-concluse')
def visite_guidate_concluse():
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute(
        """SELECT vg.NumeroBadge,
                   vg.dataVisita,
                   vg.oraInizio,
                   vg.oraFine,
                   vg.numeroPosti,
                   (vg.numeroPosti - vg.postiResidui) AS biglietti_timbrati,
                   ROUND((vg.numeroPosti - vg.postiResidui) * 100 / vg.numeroPosti, 2) AS percentuale
            FROM   VISITA_GUIDATA vg
            WHERE  vg.dataVisita < CURDATE()
            ORDER  BY percentuale DESC"""
    )
    results = cur.fetchall(); cur.close(); conn.close()
    return render_template('query_form.html', form=VisiteGuidateConcluseForm(), results=results, title="Visite Concluse")

# ——————————————————— MAIN ———————————————————
if __name__ == '__main__':
    app.run(debug=True)
