-- Database Section
-- ________________ 

create database museo;
use museo;

-- Tables Section
-- _____________ 

create table ACCESSO (
     idBiglietto varchar(10) not null,
     nomeSezione varchar(50) not null,
     constraint ID_ACCESSO_ID primary key (idBiglietto, nomeSezione));

create table ANAGRAFICA (
     nome varchar(50) not null,
     cognome varchar(50) not null,
     dataDiNascita date not null,
     CodiceFiscale char(16) not null,
     constraint ID_ANAGRAFICA_ID primary key (CodiceFiscale));

create table AUTORE (
     nomeDArte varchar(100) not null,
     nomeCompleto varchar(100),
     nazionalita varchar(30),
     dataNascita date,
     dataMorte date,
     nomeMovimento varchar(50),
     constraint ID_AUTORE_ID primary key (nomeDArte));

create table BIGLIETTO_ACQUISTATO (
     idBiglietto varchar(10) not null,
     data_acquisto date not null,
     dataPerIngresso date not null,
     ingressoAvvenuto boolean not null,
     perVisita varchar(20) not null,
     categoriaBiglietto varchar(20) not null,
     CodiceFiscale char(16) not null,
     Pre_CodiceFiscale char(16),
     Pre_dataVisita date,
     constraint ID_BIGLIETTO_ACQUISTATO_ID primary key (idBiglietto));

create table CONOSCENZA (
     ID_LIN int not null,
     CodiceFiscale char(16) not null,
     constraint ID_CONOSCENZA_ID primary key (CodiceFiscale, ID_LIN));

create table EFFETUAZIONE (
     CodiceFiscale char(16) not null,
     idOpera varchar(10) not null,
     dataInizio date not null,
     constraint ID_EFFETUAZIONE_ID primary key (CodiceFiscale, idOpera, dataInizio));

create table GUIDA (
     CodiceFiscale char(16) not null,
     biografia text not null,
     nomeMovimento varchar(50) not null,
     constraint FKR_10_ID primary key (CodiceFiscale));

create table LINGUA (
     ID_LIN int not null auto_increment,
     nomeNativo varchar(50) not null,
     nomeInItaliano varchar(50) not null,
     constraint ID_ID primary key (ID_LIN));

create table MOVIMENTO_ARTISTICO (
     nomeMovimento varchar(50) not null,
     secolo varchar(10) not null,
     constraint ID_MOVIMENTO_ARTISTICO_ID primary key (nomeMovimento));

create table OPERA (
     idOpera varchar(10) not null,
     dataCompletamento varchar(20) not null,
     nomeOpera varchar(100) not null,
     nomeDArte varchar(100) not null,
     nomeCategoria varchar(50) not null,
     nomeSezione varchar(50) not null,
     numeroSala varchar(10) not null,
     constraint ID_OPERA_ID primary key (idOpera));

create table RESTAURATORE (
     CodiceFiscale char(16) not null,
     formazione varchar(100) not null,
     telefono varchar(20) not null,
     constraint FKR_8_ID primary key (CodiceFiscale));

create table RESTAURO (
     idOpera varchar(10) not null,
     dataInizio date not null,
     dataFine date not null,
     dettagliRestauro text not null,
     constraint ID_RESTAURO_ID primary key (idOpera, dataInizio));

create table SALA (
     nomeSezione varchar(50) not null,
     numeroSala varchar(10) not null,
     superficie int not null,
     capienza int not null,
     constraint ID_SALA_ID primary key (nomeSezione, numeroSala));

create table SEZIONE (
     nomeSezione varchar(50) not null,
     tempoVisita int not null,
     prezzoSezione int not null,
     constraint ID_SEZIONE_ID primary key (nomeSezione));

create table SPECIALIZZAZIONE (
     CodiceFiscale char(16) not null,
     nomeCategoria varchar(50) not null,
     constraint ID_SPECIALIZZAZIONE_ID primary key (CodiceFiscale, nomeCategoria));

create table TIPO_BIGLIETTO (
     fattorePrezzo int not null,
     categoriaBiglietto varchar(20) not null,
     constraint ID_TIPO_BIGLIETTO_ID primary key (categoriaBiglietto));

create table TIPO_OPERA (
     nomeCategoria varchar(50) not null,
     descrizione text not null,
     constraint ID_TIPO_OPERA_ID primary key (nomeCategoria));

create table VISITA_GUIDATA (
     CodiceFiscale char(16) not null,
     numeroPosti int not null,
     dataVisita date not null,
     prezzoVisita int not null,
     oraInizio int not null,
     oraFine int not null,
     ID_LIN int not null,
     constraint ID_VISITA_GUIDATA_ID primary key (CodiceFiscale, dataVisita));

create table VISITATORE (
     CodiceFiscale char(16) not null,
     e_mail varchar(100) not null,
     constraint FKR_9_ID primary key (CodiceFiscale));

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
     foreign key (CodiceFiscale)
     references VISITATORE (CodiceFiscale);

alter table BIGLIETTO_ACQUISTATO add constraint FKprenotazione_FK
     foreign key (Pre_CodiceFiscale, Pre_dataVisita)
     references VISITA_GUIDATA (CodiceFiscale, dataVisita);

alter table BIGLIETTO_ACQUISTATO add constraint FKprenotazione_CHK
     check((Pre_CodiceFiscale is not null and Pre_dataVisita is not null)
           or (Pre_CodiceFiscale is null and Pre_dataVisita is null)); 

alter table CONOSCENZA add constraint FKR_6
     foreign key (CodiceFiscale)
     references GUIDA (CodiceFiscale);

alter table CONOSCENZA add constraint FKR_7_FK
     foreign key (ID_LIN)
     references LINGUA (ID_LIN);

alter table EFFETUAZIONE add constraint FKR_3_FK
     foreign key (idOpera, dataInizio)
     references RESTAURO (idOpera, dataInizio);

alter table EFFETUAZIONE add constraint FKR_2
     foreign key (CodiceFiscale)
     references RESTAURATORE (CodiceFiscale);

-- Not implemented
-- alter table GUIDA add constraint FKR_10_CHK
--     check(exists(select * from CONOSCENZA
--                  where CONOSCENZA.CodiceFiscale = CodiceFiscale)); 

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
-- alter table RESTAURATORE add constraint FKR_8_CHK
--     check(exists(select * from SPECIALIZZAZIONE
--                  where SPECIALIZZAZIONE.CodiceFiscale = CodiceFiscale)); 

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
     foreign key (CodiceFiscale)
     references RESTAURATORE (CodiceFiscale);

alter table VISITA_GUIDATA add constraint FKconduzione
     foreign key (CodiceFiscale)
     references GUIDA (CodiceFiscale);

alter table VISITA_GUIDATA add constraint FKcomunicazione_FK
     foreign key (ID_LIN)
     references LINGUA (ID_LIN);

-- Not implemented
-- alter table VISITATORE add constraint FKR_9_CHK
--     check(exists(select * from BIGLIETTO_ACQUISTATO
--                  where BIGLIETTO_ACQUISTATO.CodiceFiscale = CodiceFiscale)); 

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
     on BIGLIETTO_ACQUISTATO (CodiceFiscale);

create index FKprenotazione_IND
     on BIGLIETTO_ACQUISTATO (Pre_CodiceFiscale, Pre_dataVisita);

create unique index ID_CONOSCENZA_IND
     on CONOSCENZA (CodiceFiscale, ID_LIN);

create index FKR_7_IND
     on CONOSCENZA (ID_LIN);

create unique index ID_EFFETUAZIONE_IND
     on EFFETUAZIONE (CodiceFiscale, idOpera, dataInizio);

create index FKR_3_IND
     on EFFETUAZIONE (idOpera, dataInizio);

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

create unique index FKR_8_IND
     on RESTAURATORE (CodiceFiscale);

create unique index ID_RESTAURO_IND
     on RESTAURO (idOpera, dataInizio);

create unique index ID_SALA_IND
     on SALA (nomeSezione, numeroSala);

create unique index ID_SEZIONE_IND
     on SEZIONE (nomeSezione);

create unique index ID_SPECIALIZZAZIONE_IND
     on SPECIALIZZAZIONE (CodiceFiscale, nomeCategoria);

create index FKR_5_IND
     on SPECIALIZZAZIONE (nomeCategoria);

create unique index ID_TIPO_BIGLIETTO_IND
     on TIPO_BIGLIETTO (categoriaBiglietto);

create unique index ID_TIPO_OPERA_IND
     on TIPO_OPERA (nomeCategoria);

create unique index ID_VISITA_GUIDATA_IND
     on VISITA_GUIDATA (CodiceFiscale, dataVisita);

create index FKcomunicazione_IND
     on VISITA_GUIDATA (ID_LIN);

create unique index FKR_9_IND
     on VISITATORE (CodiceFiscale);

