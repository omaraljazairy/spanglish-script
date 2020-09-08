BEGIN TRANSACTION;

CREATE TABLE "Words" (
	id INTEGER NOT NULL,
	word VARCHAR(32) NOT NULL,
	word_en VARCHAR(32) NOT NULL,
	created DATETIME DEFAULT CURRENT_TIMESTAMP,
	type VARCHAR(32) DEFAULT NULL
	PRIMARY KEY (id),
	UNIQUE (word)
);

CREATE TABLE "Verbs" (
	id INTEGER NOT NULL,
	word_Id VARCHAR(32) NOT NULL,
	tenses VARCHAR(32) NOT NULL,
	yo VARCHAR(32) DEFAULT NULL,
	tu VARCHAR(32) DEFAULT NULL,
	usted VARCHAR(32) DEFAULT NULL,
	nosotros VARCHAR(32) DEFAULT NULL,
	vosotros VARCHAR(32) DEFAULT NULL,
	ustedes VARCHAR(32) DEFAULT NULL,
	created DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	UNIQUE (word_id,tenses)
);

CREATE TABLE "Sentences" (
	id INTEGER NOT NULL,
	sentence VARCHAR(255) NOT NULL,
	sentence_en VARCHAR(255) NOT NULL,
	created DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	UNIQUE (sentence)
);

DROP TABLE IF EXISTS "Results";
CREATE TABLE "Results" (
	id INTEGER NOT NULL,
	word_id INTEGER DEFAULT 0,
	sentence_id INTEGER DEFAULT 0,
	attempt INTEGER NOT NULL,
	created DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id)
);
COMMIT;