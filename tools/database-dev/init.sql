-- Create Enum Type for the Questions Table Type column
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'question_type') THEN
        CREATE TYPE question_type AS ENUM ('TEXT', 'CHECKBOX', 'RADIO', 'ORDER');
    END IF;
END $$;

-- Create Questions Table
CREATE TABLE Questions (
    id SERIAL PRIMARY KEY,
    text VARCHAR NOT NULL,
    type question_type NOT NULL,
    difficulty INT DEFAULT 1,
    category VARCHAR
);

-- Create Answers Table (for TEXT, ORDER types)
CREATE TABLE Answers (
    id SERIAL PRIMARY KEY,
    question_id INT REFERENCES Questions(id) ON DELETE CASCADE,
    answer_text VARCHAR,
    order_position INT
);

-- Create AnswersMultipleOptions Table (for CHECKBOX, RADIO types)
CREATE TABLE AnswersMultipleOptions (
    id SERIAL PRIMARY KEY,
    question_id INT REFERENCES Questions(id) ON DELETE CASCADE,
    option_text VARCHAR NOT NULL,
    is_correct BOOLEAN NOT NULL
);

-- Create UserData Table
CREATE TABLE UserData (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    surname VARCHAR NOT NULL
);

-- Create Credentials Table
CREATE TABLE Credentials (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES UserData(id) ON DELETE CASCADE,
    login VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);

-- Create History Table
CREATE TABLE History (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES UserData(id) ON DELETE CASCADE,
    question_id INT REFERENCES Questions(id) ON DELETE CASCADE,
    users_answer VARCHAR,
    correctly_answered BOOLEAN,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TEST DATA DELETE
INSERT INTO questions (id, text, type, difficulty, category) VALUES
(1, 'What is the capital of France?', 'TEXT', 1, 'Geography'),
(2, 'Select the prime numbers.', 'CHECKBOX', 2, 'Mathematics'),
(3, 'What is 2 + 2?', 'RADIO', 1, 'Mathematics'),
(4, 'Arrange these planets by size.', 'ORDER', 3, 'Astronomy');

INSERT INTO answers (id, question_id, answer_text, order_position) VALUES
(1, 1, 'Paris', NULL),
(2, 4, 'Jupiter', 1),
(3, 4, 'Saturn', 2),
(4, 4, 'Neptune', 3);

INSERT INTO answersmultipleoptions (id, question_id, option_text, is_correct) VALUES
(1, 2, '2', FALSE),
(2, 2, '3', TRUE),
(3, 2, '5', TRUE),
(4, 2, '6', FALSE),
(5, 3, '3', FALSE),
(6, 3, '4', TRUE),
(7, 3, '5', FALSE);

INSERT INTO userdata (id, name, surname) VALUES
(1, 'Alice', 'Johnson'),
(2, 'Bob', 'Smith');

INSERT INTO credentials (id, user_id, login, password) VALUES
(1, 1, 'alice123', 'passalice'),
(2, 2, 'bob_the_best', 'passbob');
