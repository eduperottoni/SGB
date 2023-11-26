DROP TABLE Escrito_por;
DROP TABLE Historico;
DROP table Livro;
DROP TABLE Editora;
DROP TABLE Cliente;
DROP TABLE Autor;
DROP TABLE Genero;

CREATE TABLE Genero 
( 
 nome VARCHAR(30) PRIMARY KEY NOT NULL,
 descricao VARCHAR(100) NOT NULL,
 ativo BOOLEAN DEFAULT true,

 CONSTRAINT generos_unicos UNIQUE (descricao)
); 

CREATE TABLE Editora 
( 
 id SERIAL PRIMARY KEY,
 nome VARCHAR(30) NOT NULL,
 endereco VARCHAR(75),
 contato VARCHAR(20) NOT NULL,
 ativo BOOLEAN DEFAULT true,

 CONSTRAINT editoras_unicas UNIQUE (nome, endereco, contato)
); 

CREATE TABLE Livro 
( 
 titulo VARCHAR(50) NOT NULL,
 lancamento DATE NOT NULL,
 id SERIAL PRIMARY KEY,
 editora INT REFERENCES Editora(id),
 genero VARCHAR(30) REFERENCES Genero(nome),
 num_copias INT NOT NULL DEFAULT 0,
 ativo BOOLEAN DEFAULT true,
 
 CONSTRAINT livros_unicos UNIQUE (titulo, lancamento, editora)
);

CREATE TABLE Cliente 
( 
 cpf CHAR(11) PRIMARY KEY,
 nome VARCHAR(50) NOT NULL,
 data_nascimento DATE,
 data_registro DATE NOT NULL,
 ativo BOOLEAN DEFAULT true
);

CREATE TABLE Autor 
( 
 id SERIAL PRIMARY KEY,
 nome VARCHAR(50) NOT NULL,
 biografia VARCHAR(300),
 data_nascimento DATE NOT NULL,
 ativo BOOLEAN DEFAULT true,

 CONSTRAINT autores_unicos UNIQUE (nome, biografia, data_nascimento)
); 

CREATE TABLE Historico
(
    id SERIAL PRIMARY KEY,
    data_aluguel DATE NOT NULL,
    data_devolucao DATE DEFAULT NULL,
    valor_pago FLOAT,
    cliente CHAR(11) REFERENCES Cliente(cpf),
    livro INT REFERENCES Livro(id)
);

CREATE TABLE Escrito_por 
( 
 autor INT REFERENCES Autor(id),
 livro INT REFERENCES Livro(id),
 PRIMARY KEY (autor, livro)
); 
