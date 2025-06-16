--1--
SELECT o.nomeOpera, o.nomeDArte
FROM OPERA o
WHERE o.nomeSezione = '[nomeSezione]'
ORDER BY o.nomeDArte;

--2--
SELECT s.nomeSezione, sa.numeroSala, sa.capienza, COUNT(a.idBiglietto) AS n_accessi
FROM SALA sa
JOIN SEZIONE s ON s.nomeSezione = sa.nomeSezione
LEFT JOIN ACCESSO a ON a.nomeSezione = sa.nomeSezione
LEFT JOIN BIGLIETTO_ACQUISTATO b ON b.idBiglietto = a.idBiglietto
WHERE b.dataPerIngresso = '[YYYY-MM-DD]'
GROUP BY s.nomeSezione, sa.numeroSala, sa.capienza
HAVING COUNT(a.idBiglietto) < sa.capienza;

--3--
SELECT DISTINCT o.nomeSezione
FROM OPERA o
WHERE o.nomeDArte = '[nomeDArte]';

--4--
SELECT o.nomeSezione
FROM OPERA o
WHERE o.nomeOpera = '[nomeOpera]';

--5--
SELECT vg.dataVisita, vg.oraInizio, vg.oraFine, vg.numeroPosti,
       COUNT(b.idBiglietto) AS prenotati,
       vg.numeroPosti - COUNT(b.idBiglietto) AS posti_rimanenti
FROM VISITA_GUIDATA vg
LEFT JOIN BIGLIETTO_ACQUISTATO b 
     ON b.Pre_CodiceFiscale = vg.CodiceFiscale AND b.Pre_dataVisita = vg.dataVisita
GROUP BY vg.CodiceFiscale, vg.dataVisita, vg.oraInizio, vg.oraFine, vg.numeroPosti
ORDER BY vg.dataVisita;

--6--
SELECT DISTINCT a.nomeDArte, a.nomeCompleto
FROM VISITA_GUIDATA vg
JOIN GUIDA g ON g.numeroBadge = vg.numeroBadge
JOIN AUTORE a ON a.nomeMovimento = g.nomeMovimento
WHERE vg.numeroBadge = '[CodiceFiscale_guida]'
  AND vg.dataVisita = '[YYYY-MM-DD]';

--7--
-- Inserimento nella tabella ANAGRAFICA
INSERT INTO ANAGRAFICA (nome, cognome, dataDiNascita, CodiceFiscale)
VALUES ('[Nome]', '[Cognome]', '[YYYY-MM-DD]', '[CodiceFiscale]');

-- Inserimento nella tabella VISITATORE
INSERT INTO VISITATORE (CodiceFiscale, e_mail)
VALUES ('[CodiceFiscale]', '[email]');

--8--
UPDATE VISITATORE
SET e_mail = '[nuova_email]'
WHERE CodiceFiscale = '[CodiceFiscale]';

--9--
-- Trova il codice fiscale dalla email
SELECT CodiceFiscale
FROM VISITATORE
WHERE e_mail = '[email]';

-- Inserimento biglietto (assumendo id generato come 'B001')
INSERT INTO BIGLIETTO_ACQUISTATO (
    idBiglietto, data_acquisto, dataPerIngresso, ingressoAvvenuto,
    perVisita, categoriaBiglietto, email
) VALUES (
    '[idBiglietto]', CURDATE(), '[dataVisita]', 'N',
    'N', '[categoriaBiglietto]', '[email]'
);

-- Per ogni sezione selezionata, inserimento in ACCESSO
-- Esempio per 2 sezioni:
INSERT INTO ACCESSO (idBiglietto, nomeSezione)
VALUES 
    ('[idBiglietto]', '[Sezione1]'),
    ('[idBiglietto]', '[Sezione2]');

--10--
UPDATE BIGLIETTO_ACQUISTATO
SET ingressoAvvenuto = 'S'
WHERE CodiceFiscale = '[CodiceFiscale]'
  AND dataPerIngresso = '[YYYY-MM-DD]';


--11--
-- Inserimento restauro
INSERT INTO RESTAURO (idOpera, dataInizio, dataFine, dettagliRestauro)
VALUES ('[idOpera]', '[dataInizio]', '[dataFine]', '[descrizione]');

-- Recupera nome, cognome, e email dei visitatori con biglietto prenotato per la sezione dell'opera nel periodo
SELECT A.nome, A.cognome, V.e_mail
FROM OPERA O
JOIN ACCESSO AC ON O.nomeSezione = AC.nomeSezione
JOIN BIGLIETTO_ACQUISTATO B ON B.idBiglietto = AC.idBiglietto
JOIN VISITATORE V ON V.CodiceFiscale = B.CodiceFiscale
JOIN ANAGRAFICA A ON A.CodiceFiscale = V.CodiceFiscale
WHERE O.idOpera = '[idOpera]'
  AND B.dataPerIngresso BETWEEN '[dataInizio]' AND '[dataFine]';

--12--
INSERT INTO VISITA_GUIDATA (
    CodiceFiscale, numeroPosti, dataVisita,
    prezzoVisita, oraInizio, oraFine, ID_LIN
) VALUES (
    '[CodiceFiscaleGuida]', [numeroPosti], '[dataVisita]',
    [prezzo], [oraInizio], [oraFine], [idLingua]
);

--13--
-- Recupera i dati dei visitatori prenotati alla visita
SELECT A.nome, A.cognome, V.e_mail
FROM BIGLIETTO_ACQUISTATO B
JOIN VISITATORE V ON V.CodiceFiscale = B.CodiceFiscale
JOIN ANAGRAFICA A ON A.CodiceFiscale = V.CodiceFiscale
WHERE B.Pre_CodiceFiscale = '[CodiceFiscaleGuida]'
  AND B.Pre_dataVisita = '[dataVisita]';

-- Rimuove la visita guidata
DELETE FROM VISITA_GUIDATA
WHERE CodiceFiscale = '[CodiceFiscaleGuida]'
  AND dataVisita = '[dataVisita]';

--14--
SELECT A.nome, A.cognome, R.CodiceFiscale
FROM EFFETUAZIONE E
JOIN RESTAURATORE R ON R.CodiceFiscale = E.CodiceFiscale
JOIN ANAGRAFICA A ON A.CodiceFiscale = R.CodiceFiscale
WHERE E.idOpera = '[idOpera]' AND E.dataInizio = '[dataInizio]';

--15--
SELECT S.nomeSezione, COUNT(DISTINCT B.idBiglietto) AS numTimbrati
FROM ACCESSO A
JOIN BIGLIETTO_ACQUISTATO B ON A.idBiglietto = B.idBiglietto
JOIN SEZIONE S ON A.nomeSezione = S.nomeSezione
WHERE B.ingressoAvvenuto = 'S'
  AND B.dataPerIngresso BETWEEN '[dataInizio]' AND '[dataFine]'
GROUP BY S.nomeSezione
ORDER BY numTimbrati DESC;

--16--
SELECT 
  VG.CodiceFiscale,
  VG.dataVisita,
  VG.numeroPosti,
  COUNT(B.idBiglietto) AS bigliettiTimbrati,
  ROUND((COUNT(B.idBiglietto) / VG.numeroPosti) * 100, 2) AS percentualeTimbrati
FROM VISITA_GUIDATA VG
LEFT JOIN BIGLIETTO_ACQUISTATO B
  ON B.Pre_CodiceFiscale = VG.CodiceFiscale
  AND B.Pre_dataVisita = VG.dataVisita
  AND B.ingressoAvvenuto = 'S'
WHERE VG.dataVisita < CURDATE()
GROUP BY VG.CodiceFiscale, VG.dataVisita, VG.numeroPosti
ORDER BY percentualeTimbrati DESC;
