DROP TABLE Sobre;
DROP TABLE Escrito_por;
-- DROP TABLE Livros_alugados;
DROP TABLE Historico;
DROP table Livro;
DROP TABLE Editora;
DROP TABLE Cliente;
DROP TABLE Autor;
DROP TABLE Genero;

CREATE TABLE Editora 
( 
 id SERIAL PRIMARY KEY,
 nome VARCHAR(30) NOT NULL,
 endereco VARCHAR(75),
 contato VARCHAR(20) NOT NULL
); 

CREATE TABLE Livro 
( 
 titulo VARCHAR(50) NOT NULL,
 lancamento DATE NOT NULL,
 id SERIAL PRIMARY KEY,  -- Utilize SERIAL para autoincremento em PostgreSQL
 editora INT REFERENCES Editora(id),
 num_copias INT NOT NULL DEFAULT 0,  -- Removi as aspas simples e ajustei o valor padrão
 UNIQUE (id)
);

CREATE TABLE Cliente 
( 
 cpf CHAR(11) PRIMARY KEY,  -- Alterei de CHAR para VARCHAR e defini o tamanho n
 nome VARCHAR(50) NOT NULL,
 data_nascimento DATE,
 data_registro DATE NOT NULL
);

CREATE TABLE Autor 
( 
 id SERIAL PRIMARY KEY,
 nome VARCHAR(50) NOT NULL,
 biografia VARCHAR(300),
 data_nascimento DATE NOT NULL
); 

CREATE TABLE Genero 
( 
 nome VARCHAR(30) PRIMARY KEY NOT NULL,
 descricao VARCHAR(100) NOT NULL
); 

CREATE TABLE Historico 
( 
 data_aluguel DATE NOT NULL,
 data_devolucao DATE,
 valor_pago FLOAT,
 cliente CHAR(11) REFERENCES Cliente(cpf),
 livro INT REFERENCES Livro(id),
 id SERIAL PRIMARY KEY
); 

-- CREATE TABLE Livros_alugados 
-- ( 
--  cliente CHAR(11) NOT NULL REFERENCES Cliente (cpf),
--  id_historico INT PRIMARY KEY REFERENCES Historico(id) 
-- ); 

CREATE TABLE Escrito_por 
( 
 autor INT REFERENCES Autor(id),
 livro INT REFERENCES Livro(id),
 PRIMARY KEY (autor, livro)
); 

CREATE TABLE Sobre 
( 
 genero VARCHAR(30) REFERENCES Genero(nome),
 livro INT REFERENCES Livro(id),
 PRIMARY KEY (genero, livro)
); 