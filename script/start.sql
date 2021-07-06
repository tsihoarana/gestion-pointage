\c postgres
DROP DATABASE "pointage";
CREATE DATABASE "pointage";
\c "pointage";


CREATE SEQUENCE "categorieSeq" START WITH 1;
CREATE SEQUENCE "employeSeq" START WITH 1;
CREATE SEQUENCE "matriculeSeq" START WITH 1;
CREATE SEQUENCE "configSeq" START WITH 1;

-- Categorie
CREATE TABLE "categorie" (
    "id" INT PRIMARY KEY NOT NULL DEFAULT NEXTVAL ('"categorieSeq"'),
    "nom" VARCHAR (20) UNIQUE NOT NULL,
    "heure_hebdo" INT NOT NULL, -- heure par jour otran fixe hoe 8 foana mantsy
    "salaire_hebdo" NUMERIC (15, 3),
    "liste_jour" VARCHAR(100) NOT NULL
);

-- Employe
CREATE TABLE "user" (
    "id" INT PRIMARY KEY NOT NULL DEFAULT NEXTVAL('"employeSeq"'),
    "matricule" VARCHAR (20) UNIQUE NOT NULL,
    "nom" VARCHAR (20) NOT NULL,
    "prenom" VARCHAR (20) NOT NULL,
    "date_naissance" DATE NOT NULL,
    "date_embauche" DATE NOT NULL,
    "date_fin_contrat" DATE NOT NULL,
    "type_user" INT NOT NULL DEFAULT 1, -- 1 admin, 0 normal
    "idcategorie" INT NOT NULL,
    "password" VARCHAR (100) NOT NULL,
    FOREIGN KEY ("idcategorie") REFERENCES Categorie ("id")
);

CREATE TABLE "config" (
    "id" INT NOT NULL PRIMARY KEY DEFAULT NEXTVAL('"configSeq"'),
    "cle" VARCHAR (20) UNIQUE NOT NULL,
    "description" TEXT,
    "valeur" DECIMAL (16, 3)
);

-- Categorie
INSERT INTO "categorie" VALUES (DEFAULT, 'NORMAL', 40, 100000.0, 'lundi,mardi,mercredi,jeudi,vendredi');
INSERT INTO "categorie" VALUES (DEFAULT, 'GARDIEN', 56, 110000.0, 'lundi,mardi,mercredi,jeudi,vendredi,samedi,dimanche');
INSERT INTO "categorie" VALUES (DEFAULT, 'CADRE', 40, 200000.0, 'lundi,mardi,mercredi,jeudi,vendredi');
INSERT INTO "categorie" VALUES (DEFAULT, 'CHAUFFEUR', 40, 100000.0, 'lundi,mardi,mercredi,jeudi,vendredi,samedi,dimanche');

-- Employe pwd: '123'
INSERT INTO "user" VALUES (DEFAULT, '001', 'Rabe', 'Zafy', '1998-01-01', '2021-07-04', '2021-12-30', 1, '1', '$2b$12$yl/AYNpyhpjvca6VTv47JeyS9.KgiE0FP9filxFv8vFvWH1Sa.EEu');
INSERT INTO "user" VALUES (DEFAULT, '002', 'Rakoto', 'Jean', '1999-01-01', '2021-07-06', '2021-12-30', 0, '2', '$2b$12$yl/AYNpyhpjvca6VTv47JeyS9.KgiE0FP9filxFv8vFvWH1Sa.EEu');
INSERT INTO "user" VALUES (DEFAULT, '003', 'Remove', 'Me', '1999-01-01', '2021-07-06', '2021-12-30', 1, '3', '$2b$12$yl/AYNpyhpjvca6VTv47JeyS9.KgiE0FP9filxFv8vFvWH1Sa.EEu');

-- Config
INSERT INTO "config" VALUES (DEFAULT, 'HEURE_PAR_JOUR', 'Heure par jour', 8);
INSERT INTO "config" VALUES (DEFAULT, 'HS30', 'Heure supp', 130);
INSERT INTO "config" VALUES (DEFAULT, 'HS50', 'Heure supp', 150);
INSERT INTO "config" VALUES (DEFAULT, 'HM30', 'Heure majore', 130);
INSERT INTO "config" VALUES (DEFAULT, 'HM40', 'Heure majore', 140);
INSERT INTO "config" VALUES (DEFAULT, 'HM50', 'Heure majore', 150);
