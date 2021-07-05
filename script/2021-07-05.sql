CREATE SEQUENCE "pointageSeq" START 1;
CREATE SEQUENCE "detailPointageSeq" START 1;

CREATE TABLE "pointage" (
    "id" INT PRIMARY KEY NOT NULL DEFAULT NEXTVAL('"pointageSeq"'),
    "iduser" INT NOT NULL,
    FOREIGN KEY ("iduser") REFERENCES "user" ("id")
);

CREATE TABLE "detailpointage" (
    "id" INT PRIMARY KEY NOT NULL DEFAULT NEXTVAL('"detailPointageSeq"'),
    "idpointage" INT NOT NULL,
    "jour" VARCHAR (20) NOT NULL,
    "est_ferier" INT NOT NULL, -- 1 si oui
    "heure_jour" INT NOT NULL CHECK ("heure_jour" >= 0),
    "heure_nuit" INT NOT NULL CHECK ("heure_nuit" >= 0),
    FOREIGN KEY ("idpointage") REFERENCES "pointage" ("id")
);

INSERT INTO Pointage VALUES (DEFAULT, '1');
    INSERT INTO DetailPointage VALUES (DEFAULT, '1', 'LUNDI', 0, 8, 0);
    INSERT INTO DetailPointage VALUES (DEFAULT, '1', 'MARDI', 0, 8, 0);
    INSERT INTO DetailPointage VALUES (DEFAULT, '1', 'MERCREDI', 0, 10, 0);
    INSERT INTO DetailPointage VALUES (DEFAULT, '1', 'JEUDI', 0, 10, 0);
    INSERT INTO DetailPointage VALUES (DEFAULT, '1', 'VENDREDI', 0, 8, 0);
    INSERT INTO DetailPointage VALUES (DEFAULT, '1', 'SAMEDI', 0, 8, 0);

INSERT INTO Pointage VALUES (DEFAULT, '2');
    INSERT INTO DetailPointage VALUES (DEFAULT, '2', 'LUNDI', 0, 10, 0);
    INSERT INTO DetailPointage VALUES (DEFAULT, '2', 'MARDI', 0, 8, 0);
    INSERT INTO DetailPointage VALUES (DEFAULT, '2', 'MERCREDI', 0, 10, 0);
    INSERT INTO DetailPointage VALUES (DEFAULT, '2', 'JEUDI', 0, 8, 1);
    INSERT INTO DetailPointage VALUES (DEFAULT, '2', 'VENDREDI', 0, 8, 0);
    INSERT INTO DetailPointage VALUES (DEFAULT, '2', 'SAMEDI', 0, 8, 0);
    INSERT INTO DetailPointage VALUES (DEFAULT, '2', 'DIMANCHE', 0, 8, 0);
