CREATE TABLE word (
        id SERIAL PRIMARY KEY,
        word VARCHAR(32) NOT NULL,
        word_en VARCHAR(32) NOT NULL,
        category INTEGER REFERENCES category(id),
        created timestamp DEFAULT now(),
        UNIQUE (word, word_en)
);


CREATE TYPE tenses as enum('Present', 'Preterite', 'Imperfect', 'Conditional', 'Future');

CREATE TABLE verb (
        id SERIAL PRIMARY KEY,
        word INTEGER REFERENCES word(id),
        tense tenses NOT NULL,
        yo VARCHAR(32) DEFAULT NULL,
        tu VARCHAR(32) DEFAULT NULL,
        usted VARCHAR(32) DEFAULT NULL,
        nosotros VARCHAR(32) DEFAULT NULL,
        vosotros VARCHAR(32) DEFAULT NULL,
        ustedes VARCHAR(32) DEFAULT NULL,
        created timestamp DEFAULT now(),
        UNIQUE (word,tense)
);


CREATE TABLE sentence (
        id SERIAL PRIMARY KEY,
        sentence VARCHAR(255) NOT NULL,
        sentence_en VARCHAR(255) NOT NULL,
        category INTEGER REFERENCES category(id),
        created timestamp DEFAULT now(),
        UNIQUE (sentence, sentence_en)
);


CREATE TABLE result (
		id SERIAL PRIMARY KEY,
        word INTEGER REFERENCES word(id),
        sentence INTEGER REFERENCES sentence(id),
        attempts INTEGER DEFAULT 1,
        created timestamp DEFAULT now()
);
