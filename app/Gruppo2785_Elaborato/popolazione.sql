-- *********************************************
-- * DB Population Script                     *
-- *-------------------------------------------*
-- * Updated: 16 Jun 2025                     *
-- * Schema: museo                            *
-- *********************************************

USE museo;

-- =========================
-- 1. Tabelle di base
-- =========================

-- SEZIONE
INSERT INTO SEZIONE (nomeSezione, tempoVisita, prezzoSezione) VALUES
  ('Pittura',        90, 10),
  ('Scultura',       60,  8),
  ('Fotografia',     75,  7),
  ('Arte Moderna',   90,  9);

-- SALA
INSERT INTO SALA (nomeSezione, numeroSala, superficie, capienza) VALUES
  ('Pittura',      'A1', 120, 40),
  ('Pittura',      'A2', 100, 35),
  ('Scultura',     'B1', 150, 50),
  ('Fotografia',   'C1',  90, 30),
  ('Arte Moderna', 'D1', 110, 35),
  ('Arte Moderna', 'D2',  95, 30);

-- MOVIMENTO_ARTISTICO
INSERT INTO MOVIMENTO_ARTISTICO (nomeMovimento, secolo) VALUES
  ('Rinascimento',  'XV'),
  ('Barocco',       'XVII'),
  ('Impressionismo','XIX'),
  ('Cubismo',       'XX');

-- LINGUA  (ID_LIN è AUTO_INCREMENT ma forziamo per coerenza referenziale)
INSERT INTO LINGUA (ID_LIN, nomeNativo, nomeInItaliano) VALUES
  (1, 'Italiano',  'Italiano'),
  (2, 'English',   'Inglese'),
  (3, 'Français',  'Francese'),
  (4, 'Español',   'Spagnolo'),
  (5, 'Deutsch',   'Tedesco'),
  (6, '日本語',      'Giapponese');

-- TIPO_OPERA
INSERT INTO TIPO_OPERA (nomeCategoria, descrizione) VALUES
  ('Dipinto',       'Pittura su tela'),
  ('Statua',        'Scultura in marmo'),
  ('Fotografia',    'Stampa fotografica'),
  ('Installazione', 'Opera d’arte ambientale');

-- TIPO_BIGLIETTO
INSERT INTO TIPO_BIGLIETTO (fattorePrezzo, categoriaBiglietto) VALUES
  (100, 'Intero'),
  ( 50, 'Ridotto'),
  ( 75, 'Famiglia'),
  (  0, 'Gratuito');

-- =========================
-- 2. Persone (Anagrafica, Guide, Restauratori)
-- =========================

-- ANAGRAFICA
INSERT INTO ANAGRAFICA (nome, cognome, dataDiNascita, CodiceFiscale) VALUES
  ('Mario',   'Rossi',   '1980-06-10', 'RSSMRA80H10F205X'),
  ('Laura',   'Bianchi', '1975-09-23', 'BNCLRA75P63F205Y'),
  ('Giulia',  'Verdi',   '1990-01-15', 'VRDGLE90A55F205Z'),
  ('Claude',  'Monet',   '1840-11-14', 'MNTCLD40B14Z123K'),
  ('Pablo',   'Picasso', '1881-10-25', 'PCCPBL81R25Z456Q'),
  ('Anna',    'Muller',  '1985-02-10', 'MLLANN85B50Z789R'),
  ('Carlos',  'Garcia',  '1992-08-18', 'GRCCRS92M58Z321S');

-- GUIDA
INSERT INTO GUIDA (NumeroBadge, CodiceFiscale, biografia, nomeMovimento) VALUES
  (1001, 'BNCLRA75P63F205Y', 'Laureata in Storia dell’Arte, specializzata nel Barocco.',        'Barocco'),
  (1002, 'MLLANN85B50Z789R', 'Storica dell’Impressionismo, plurilingue (IT/ES).',               'Impressionismo');

-- RESTAURATORE
INSERT INTO RESTAURATORE (matricola, CodiceFiscale, formazione, telefono) VALUES
  (5001, 'RSSMRA80H10F205X', 'Accademia di Restauro di Firenze', '+39 055 1234567'),
  (5002, 'GRCCRS92M58Z321S', 'Master in Conservazione Contemporanea', '+34 91 6543210');

-- SPECIALIZZAZIONE
INSERT INTO SPECIALIZZAZIONE (matricola, nomeCategoria) VALUES
  (5001, 'Dipinto'),
  (5001, 'Statua'),
  (5002, 'Installazione');

-- =========================
-- 3. Opere e Restauri
-- =========================

-- AUTORE
INSERT INTO AUTORE (nomeDArte, nomeCompleto, nazionalita, dataNascita, dataMorte, nomeMovimento) VALUES
  ('Leonardo', 'Leonardo da Vinci', 'Italiana',   '1452-04-15', '1519-05-02', 'Rinascimento'),
  ('Bernini',  'Gian Lorenzo Bernini', 'Italiana','1598-12-07', '1680-11-28', 'Barocco'),
  ('Monet',    'Claude Monet', 'Francese',        '1840-11-14', '1926-12-05', 'Impressionismo'),
  ('Picasso',  'Pablo Picasso', 'Spagnola',       '1881-10-25', '1973-04-08', 'Cubismo');

-- OPERA
INSERT INTO OPERA (idOpera, dataCompletamento, nomeOpera, nomeDArte, nomeCategoria, nomeSezione, numeroSala) VALUES
  ('OP001', '1503', 'Mona Lisa',        'Leonardo', 'Dipinto', 'Pittura',      'A1'),
  ('OP002', '1652', 'Apollo e Dafne',   'Bernini',  'Statua',  'Scultura',     'B1'),
  ('OP003', '1916', 'Ninfee',           'Monet',    'Dipinto', 'Arte Moderna', 'D1'),
  ('OP004', '1937', 'Guernica',         'Picasso',  'Dipinto', 'Arte Moderna', 'D2');

-- RESTAURO
INSERT INTO RESTAURO (idOpera, dataInizio, dataFine, dettagliRestauro) VALUES
  ('OP001', '2023-01-10', '2023-03-15', 'Pulizia della vernice superficiale'),
  ('OP002', '2024-05-20', '2024-09-30', 'Consolidamento del marmo'),
  ('OP003', '2024-02-05', '2024-05-20', 'Rintelatura e pulitura della superficie'),
  ('OP004', '2025-03-01', NULL,         'Analisi preventiva e pulizia preliminare');

-- EFFETUAZIONE
INSERT INTO EFFETUAZIONE (matricola, idOpera, dataInizio) VALUES
  (5001, 'OP001', '2023-01-10'),
  (5001, 'OP002', '2024-05-20'),
  (5002, 'OP003', '2024-02-05'),
  (5002, 'OP004', '2025-03-01');

-- =========================
-- 4. Visite e Biglietti
-- =========================

-- VISITATORE
INSERT INTO VISITATORE (email, CodiceFiscale) VALUES
  ('giulia.verdi@example.com',  'VRDGLE90A55F205Z'),
  ('anna.muller@example.com',   'MLLANN85B50Z789R'),
  ('carlos.garcia@example.com', 'GRCCRS92M58Z321S');

-- VISITA_GUIDATA
INSERT INTO VISITA_GUIDATA (NumeroBadge, numeroPosti, dataVisita, prezzoVisita, oraInizio, oraFine, postiResidui, ID_LIN) VALUES
  (1001, 25, '2025-07-01', 15, 10, 12, 24, 2),
  (1002, 30, '2025-08-15', 12, 14, 16, 30, 1);

-- BIGLIETTO_ACQUISTATO
INSERT INTO BIGLIETTO_ACQUISTATO (idBiglietto, data_acquisto, dataPerIngresso, ingressoAvvenuto, perVisita, categoriaBiglietto, email, NumeroBadge, dataVisita) VALUES
  ('B001', '2025-06-15', '2025-06-20', 'N', 'normale',       'Intero',   'giulia.verdi@example.com',  NULL,  NULL),
  ('B002', '2025-06-15', '2025-07-01', 'N', 'visita_guidata', 'Intero',   'giulia.verdi@example.com',  1001, '2025-07-01'),
  ('B003', '2025-06-16', '2025-06-20', 'N', 'normale',       'Ridotto',  'anna.muller@example.com',   NULL,  NULL),
  ('B004', '2025-06-16', '2025-08-15', 'N', 'visita_guidata', 'Famiglia', 'carlos.garcia@example.com', 1002, '2025-08-15');

-- ACCESSO
INSERT INTO ACCESSO (idBiglietto, nomeSezione) VALUES
  ('B001', 'Pittura'),
  ('B001', 'Scultura'),
  ('B002', 'Pittura'),
  ('B003', 'Fotografia'),
  ('B003', 'Arte Moderna'),
  ('B004', 'Arte Moderna');

-- CONOSCENZA
INSERT INTO CONOSCENZA (NumeroBadge, ID_LIN) VALUES
  (1001, 1),
  (1001, 2),
  (1002, 1),
  (1002, 4);

-- =========================
-- Fine script di popolamento
