-- *********************************************
-- * SQL MySQL generation                      
-- *--------------------------------------------
-- * DB-MAIN version: 11.0.2              
-- * Generator date: Sep 14 2021              
-- * Generation date: Mon Jun 16 10:55:25 2025 
-- * LUN file: C:\Users\Pietro\Desktop\DB-museo\progettazioneLogica\ER_lgico.lun 
-- * Schema: museo/1 
-- ********************************************* 


-- Database Section
-- ________________ 

create database museo;
use museo;


-- Tables Section
-- _____________ 

create table ACCESSO (
     idBiglietto VARCHAR(30) not null,
     nomeSezione VARCHAR(50) not null,
     constraint ID_ACCESSO_ID primary key (idBiglietto, nomeSezione));

create table ANAGRAFICA (
     nome VARCHAR(50) not null,
     cognome VARCHAR(50) not null,
     dataDiNascita date not null,
     CodiceFiscale VARCHAR(16) not null,
     constraint ID_ANAGRAFICA_ID primary key (CodiceFiscale));

create table AUTORE (
     nomeDArte VARCHAR(50) not null,
     nomeCompleto VARCHAR(100),
     nazionalita VARCHAR(30),
     dataNascita date,
     dataMorte DATE,
     nomeMovimento VARCHAR(50),
     constraint ID_AUTORE_ID primary key (nomeDArte));

create table BIGLIETTO_ACQUISTATO (
     idBiglietto VARCHAR(30) not null,
     data_acquisto date not null,
     dataPerIngresso DATE not null,
     ingressoAvvenuto CHAR(1) not null,
     perVisita VARCHAR(30) not null,
     categoriaBiglietto VARCHAR(30) not null,
     email VARCHAR(100) not null,
     NumeroBadge int,
     dataVisita date,
     constraint ID_BIGLIETTO_ACQUISTATO_ID primary key (idBiglietto));

create table CONOSCENZA (
     ID_LIN int not null,
     NumeroBadge int not null,
     constraint ID_CONOSCENZA_ID primary key (NumeroBadge, ID_LIN));

create table EFFETUAZIONE (
     matricola int not null,
     idOpera VARCHAR(30) not null,
     dataInizio date not null,
     constraint ID_EFFETUAZIONE_ID primary key (matricola, idOpera, dataInizio));

create table GUIDA (
     NumeroBadge int not null,
     CodiceFiscale VARCHAR(16) not null,
     biografia VARCHAR(255) not null,
     nomeMovimento VARCHAR(50) not null,
     constraint ID_GUIDA_ID primary key (NumeroBadge),
     constraint FKR_10_ID unique (CodiceFiscale));

create table LINGUA (
     ID_LIN int not null auto_increment,
     nomeNativo VARCHAR(50) not null,
     nomeInItaliano VARCHAR(50) not null,
     constraint ID_ID primary key (ID_LIN));

create table MOVIMENTO_ARTISTICO (
     nomeMovimento VARCHAR(50) not null,
     secolo VARCHAR(50) not null,
     constraint ID_MOVIMENTO_ARTISTICO_ID primary key (nomeMovimento));

create table OPERA (
     idOpera VARCHAR(30) not null,
     dataCompletamento VARCHAR(50) not null,
     nomeOpera VARCHAR(100) not null,
     nomeDArte VARCHAR(50) not null,
     nomeCategoria VARCHAR(30) not null,
     nomeSezione VARCHAR(50) not null,
     numeroSala VARCHAR(10) not null,
     constraint ID_OPERA_ID primary key (idOpera));

create table RESTAURATORE (
     matricola int not null,
     CodiceFiscale VARCHAR(16) not null,
     formazione VARCHAR(100) not null,
     telefono VARCHAR(20) not null,
     constraint ID_RESTAURATORE_ID primary key (matricola),
     constraint FKR_8_ID unique (CodiceFiscale));

create table RESTAURO (
     idOpera VARCHAR(30) not null,
     dataInizio date not null,
     dataFine date not null,
     dettagliRestauro VARCHAR(255) not null,
     constraint ID_RESTAURO_ID primary key (idOpera, dataInizio));

create table SALA (
     nomeSezione VARCHAR(50) not null,
     numeroSala VARCHAR(10) not null,
     superficie int not null,
     capienza int not null,
     constraint ID_SALA_ID primary key (nomeSezione, numeroSala));

create table SEZIONE (
     nomeSezione VARCHAR(50) not null,
     tempoVisita int not null,
     prezzoSezione int not null,
     constraint ID_SEZIONE_ID primary key (nomeSezione));

create table SPECIALIZZAZIONE (
     matricola int not null,
     nomeCategoria VARCHAR(30) not null,
     constraint ID_SPECIALIZZAZIONE_ID primary key (matricola, nomeCategoria));

create table TIPO_BIGLIETTO (
     fattorePrezzo int not null,
     categoriaBiglietto VARCHAR(30) not null,
     constraint ID_TIPO_BIGLIETTO_ID primary key (categoriaBiglietto));

create table TIPO_OPERA (
     nomeCategoria VARCHAR(30) not null,
     descrizione VARCHAR(255) not null,
     constraint ID_TIPO_OPERA_ID primary key (nomeCategoria));

create table VISITA_GUIDATA (
     NumeroBadge int not null,
     numeroPosti int not null,
     dataVisita date not null,
     prezzoVisita int not null,
     oraInizio int not null,
     oraFine int not null,
     postiResidui int not null,
     ID_LIN int not null,
     constraint ID_VISITA_GUIDATA_ID primary key (NumeroBadge, dataVisita));

create table VISITATORE (
     email VARCHAR(100) not null,
     CodiceFiscale VARCHAR(16) not null,
     constraint ID_VISITATORE_ID primary key (email),
     constraint FKR_9_ID unique (CodiceFiscale));


-- Constraints Section
-- ___________________ 

alter table ACCESSO add constraint FKR_1_FK
     foreign key (nomeSezione)
     references SEZIONE (nomeSezione);

alter table ACCESSO add constraint FKR
     foreign key (idBiglietto)
     references BIGLIETTO_ACQUISTATO (idBiglietto);

alter table AUTORE add constraint FKadesione_FK
     foreign key (nomeMovimento)
     references MOVIMENTO_ARTISTICO (nomeMovimento);

alter table BIGLIETTO_ACQUISTATO add constraint FKriferimento_FK
     foreign key (categoriaBiglietto)
     references TIPO_BIGLIETTO (categoriaBiglietto);

alter table BIGLIETTO_ACQUISTATO add constraint FKpossesso_FK
     foreign key (email)
     references VISITATORE (email);

alter table BIGLIETTO_ACQUISTATO add constraint FKprenotazione_FK
     foreign key (NumeroBadge, dataVisita)
     references VISITA_GUIDATA (NumeroBadge, dataVisita);

alter table BIGLIETTO_ACQUISTATO add constraint FKprenotazione_CHK
     check((NumeroBadge is not null and dataVisita is not null)
           or (NumeroBadge is null and dataVisita is null)); 

alter table CONOSCENZA add constraint FKR_6
     foreign key (NumeroBadge)
     references GUIDA (NumeroBadge);

alter table CONOSCENZA add constraint FKR_7_FK
     foreign key (ID_LIN)
     references LINGUA (ID_LIN);

alter table EFFETUAZIONE add constraint FKR_3_FK
     foreign key (idOpera, dataInizio)
     references RESTAURO (idOpera, dataInizio);

alter table EFFETUAZIONE add constraint FKR_2
     foreign key (matricola)
     references RESTAURATORE (matricola);

-- Not implemented
-- alter table GUIDA add constraint ID_GUIDA_CHK
--     check(exists(select * from CONOSCENZA
--                  where CONOSCENZA.NumeroBadge = NumeroBadge)); 

alter table GUIDA add constraint FKR_10_FK
     foreign key (CodiceFiscale)
     references ANAGRAFICA (CodiceFiscale);

alter table GUIDA add constraint FKcompetenza_FK
     foreign key (nomeMovimento)
     references MOVIMENTO_ARTISTICO (nomeMovimento);

alter table OPERA add constraint FKrealizzazione_FK
     foreign key (nomeDArte)
     references AUTORE (nomeDArte);

alter table OPERA add constraint FKclassificazione_FK
     foreign key (nomeCategoria)
     references TIPO_OPERA (nomeCategoria);

alter table OPERA add constraint FKpresenza_FK
     foreign key (nomeSezione, numeroSala)
     references SALA (nomeSezione, numeroSala);

-- Not implemented
-- alter table RESTAURATORE add constraint ID_RESTAURATORE_CHK
--     check(exists(select * from SPECIALIZZAZIONE
--                  where SPECIALIZZAZIONE.matricola = matricola)); 

alter table RESTAURATORE add constraint FKR_8_FK
     foreign key (CodiceFiscale)
     references ANAGRAFICA (CodiceFiscale);

-- Not implemented
-- alter table RESTAURO add constraint ID_RESTAURO_CHK
--     check(exists(select * from EFFETUAZIONE
--                  where EFFETUAZIONE.idOpera = idOpera and EFFETUAZIONE.dataInizio = dataInizio)); 

alter table RESTAURO add constraint FKripristino
     foreign key (idOpera)
     references OPERA (idOpera);

alter table SALA add constraint FKcomposizione
     foreign key (nomeSezione)
     references SEZIONE (nomeSezione);

-- Not implemented
-- alter table SEZIONE add constraint ID_SEZIONE_CHK
--     check(exists(select * from SALA
--                  where SALA.nomeSezione = nomeSezione)); 

alter table SPECIALIZZAZIONE add constraint FKR_5_FK
     foreign key (nomeCategoria)
     references TIPO_OPERA (nomeCategoria);

alter table SPECIALIZZAZIONE add constraint FKR_4
     foreign key (matricola)
     references RESTAURATORE (matricola);

alter table VISITA_GUIDATA add constraint FKconduzione
     foreign key (NumeroBadge)
     references GUIDA (NumeroBadge);

alter table VISITA_GUIDATA add constraint FKcomunicazione_FK
     foreign key (ID_LIN)
     references LINGUA (ID_LIN);

-- Not implemented
-- alter table VISITATORE add constraint ID_VISITATORE_CHK
--     check(exists(select * from BIGLIETTO_ACQUISTATO
--                  where BIGLIETTO_ACQUISTATO.email = email)); 

alter table VISITATORE add constraint FKR_9_FK
     foreign key (CodiceFiscale)
     references ANAGRAFICA (CodiceFiscale);


-- Index Section
-- _____________ 

create unique index ID_ACCESSO_IND
     on ACCESSO (idBiglietto, nomeSezione);

create index FKR_1_IND
     on ACCESSO (nomeSezione);

create unique index ID_ANAGRAFICA_IND
     on ANAGRAFICA (CodiceFiscale);

create unique index ID_AUTORE_IND
     on AUTORE (nomeDArte);

create index FKadesione_IND
     on AUTORE (nomeMovimento);

create unique index ID_BIGLIETTO_ACQUISTATO_IND
     on BIGLIETTO_ACQUISTATO (idBiglietto);

create index FKriferimento_IND
     on BIGLIETTO_ACQUISTATO (categoriaBiglietto);

create index FKpossesso_IND
     on BIGLIETTO_ACQUISTATO (email);

create index FKprenotazione_IND
     on BIGLIETTO_ACQUISTATO (NumeroBadge, dataVisita);

create unique index ID_CONOSCENZA_IND
     on CONOSCENZA (NumeroBadge, ID_LIN);

create index FKR_7_IND
     on CONOSCENZA (ID_LIN);

create unique index ID_EFFETUAZIONE_IND
     on EFFETUAZIONE (matricola, idOpera, dataInizio);

create index FKR_3_IND
     on EFFETUAZIONE (idOpera, dataInizio);

create unique index ID_GUIDA_IND
     on GUIDA (NumeroBadge);

create unique index FKR_10_IND
     on GUIDA (CodiceFiscale);

create index FKcompetenza_IND
     on GUIDA (nomeMovimento);

create unique index ID_IND
     on LINGUA (ID_LIN);

create unique index ID_MOVIMENTO_ARTISTICO_IND
     on MOVIMENTO_ARTISTICO (nomeMovimento);

create unique index ID_OPERA_IND
     on OPERA (idOpera);

create index FKrealizzazione_IND
     on OPERA (nomeDArte);

create index FKclassificazione_IND
     on OPERA (nomeCategoria);

create index FKpresenza_IND
     on OPERA (nomeSezione, numeroSala);

create unique index ID_RESTAURATORE_IND
     on RESTAURATORE (matricola);

create unique index FKR_8_IND
     on RESTAURATORE (CodiceFiscale);

create unique index ID_RESTAURO_IND
     on RESTAURO (idOpera, dataInizio);

create unique index ID_SALA_IND
     on SALA (nomeSezione, numeroSala);

create unique index ID_SEZIONE_IND
     on SEZIONE (nomeSezione);

create unique index ID_SPECIALIZZAZIONE_IND
     on SPECIALIZZAZIONE (matricola, nomeCategoria);

create index FKR_5_IND
     on SPECIALIZZAZIONE (nomeCategoria);

create unique index ID_TIPO_BIGLIETTO_IND
     on TIPO_BIGLIETTO (categoriaBiglietto);

create unique index ID_TIPO_OPERA_IND
     on TIPO_OPERA (nomeCategoria);

create unique index ID_VISITA_GUIDATA_IND
     on VISITA_GUIDATA (NumeroBadge, dataVisita);

create index FKcomunicazione_IND
     on VISITA_GUIDATA (ID_LIN);

create unique index ID_VISITATORE_IND
     on VISITATORE (email);

create unique index FKR_9_IND
     on VISITATORE (CodiceFiscale);

