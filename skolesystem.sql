CREATE DATABASE IF NOT EXISTS skolesystem;
USE skolesystem;

CREATE TABLE bruker (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brukernavn VARCHAR(50) UNIQUE NOT NULL,
    epost VARCHAR(100) UNIQUE NOT NULL,
    passord_hash VARCHAR(255) NOT NULL,
    rolle ENUM('elev', 'laerer', 'admin') DEFAULT 'elev',
    opprettet TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE klasse (
    id INT AUTO_INCREMENT PRIMARY KEY,
    navn VARCHAR(20) NOT NULL UNIQUE,
    trinn TINYINT NOT NULL
);

CREATE TABLE elev (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fornavn VARCHAR(50) NOT NULL,
    etternavn VARCHAR(50) NOT NULL,
    bruker_id INT UNIQUE,
    klasse_id INT NOT NULL,
    FOREIGN KEY (bruker_id) REFERENCES bruker(id),
    FOREIGN KEY (klasse_id) REFERENCES klasse(id)
);

CREATE TABLE deadline (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tittel VARCHAR(100) NOT NULL,
    beskrivelse TEXT,
    frist DATETIME NOT NULL,
    bruker_id INT NOT NULL,
    fullfort BOOLEAN DEFAULT 0,
    FOREIGN KEY (bruker_id) REFERENCES bruker(id)
);

CREATE TABLE quote (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tekst TEXT NOT NULL,
    bruker_id INT NOT NULL,
    opprettet TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bruker_id) REFERENCES bruker(id)
);

CREATE TABLE holdeplass (
    id INT AUTO_INCREMENT PRIMARY KEY,
    navn VARCHAR(100) NOT NULL
);

CREATE TABLE favoritt_holdeplass (
    bruker_id INT NOT NULL,
    holdeplass_id INT NOT NULL,
    PRIMARY KEY (bruker_id, holdeplass_id),
    FOREIGN KEY (bruker_id) REFERENCES bruker(id),
    FOREIGN KEY (holdeplass_id) REFERENCES holdeplass(id)
);

