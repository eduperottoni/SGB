-- create_tables.sql
CREATE TABLE IF NOT EXISTS aluno (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    idade INTEGER,
    curso VARCHAR(100)
);