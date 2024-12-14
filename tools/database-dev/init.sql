-- Create Enum Type for the Questions Table Type column
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'question_type') THEN
        CREATE TYPE question_type AS ENUM ('TEXT', 'CHECKBOX', 'RADIO');
    END IF;
END $$;

-- Create Questions Table
CREATE TABLE Questions (
    id SERIAL PRIMARY KEY,
    text VARCHAR NOT NULL,
    type question_type NOT NULL,
    difficulty INT DEFAULT 1,
    category VARCHAR,
    hint VARCHAR
);

-- Create Answers Table (for TEXT, ORDER types)
CREATE TABLE Answers (
    id SERIAL PRIMARY KEY,
    question_id INT REFERENCES Questions(id) ON DELETE CASCADE,
    answer_text VARCHAR
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
    password_hash VARCHAR NOT NULL
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
INSERT INTO questions (text, type, difficulty, category, hint) VALUES
('За сколько работает алгоритм сортировки пузырьком?', 'RADIO', 1, 'Программирование', 'Каждый проход цикла делает n - i действий, всего действий n.'),
('За сколько суммарно работают следующие циклы? for (int i = 0; i < n; ++i) for (int j = 0; j < n; j += i)', 'RADIO', 3, 'Программирование', 'Количество действий - сумма гармонического ряда'),
('Какие виды тестов существуют в реальности?', 'CHECKBOX', 2, 'Программирование', 'Эти тесты тестируют покомпоненто, так и всю систему целиком'),
('Какая точка мнимизирует сумму расстояний до всех остальных?', 'RADIO', 2, 'Математика', 'Следует посмотреть, как меняется ответ при сдвиге точке'),
('При условии, что x + y = const, когда выражение x^2 + y^2 минимизируется?', 'RADIO', 2, 'Математика', 'Стоит посмотреть про метод штурма'),
('Какое поле в kubernetes, является атомарным CAS (comppare and set)?', 'TEXT', 3, 'SRE', 'Это поле сущесвтует для всех объектов, и увеличивается при любом изменении'),
('Как называется хранилище данных, оперерующих под kubeenetes', 'TEXT', 2, 'SRE', 'Почти как etc'),
('Какие выражения эквивалентны a^x?', 'CHECKBOX', 2, 'Математика', 'Нужно воспользоваться свойствами степени'),
('Что такое pod в контексте Kubernetes?', 'RADIO', 3, 'SRE', 'Базовая ячейка любого кластера, именно на ней работают все сервисы'),
('Какое из утверждений верно про транзакции в базах данных?', 'RADIO', 3, 'Программирование', 'По аналогии с банковскими транзакциями.'),
('Представим, что мы генерируем дерево последовательно, начиная с вершины 1, а затем случайно выбираем предка. Какое матожидание глубины данного дерева?', 'RADIO', 3, 'Математика', 'Следует написать перебор');
 
INSERT INTO answers (question_id, answer_text) VALUES
(6, 'generation'),
(7, 'etcd');
 
INSERT INTO answersmultipleoptions (question_id, option_text, is_correct) VALUES
(1, 'O(n log n)', FALSE),
(1, 'O(n ^ 2)', TRUE),
(1, 'O(n!)', FALSE),
(1, 'O(2 ^ n)', FALSE),
(2, 'O(n log n)', TRUE),
(2, 'O(n ^ 2)', FALSE),
(2, 'O(n!)', FALSE),
(2, 'O(2 ^ n)', FALSE),
(3, 'Интеграционные', TRUE),
(3, 'Реляционные', FALSE),
(3, 'Юнит', TRUE),
(3, 'Интегральные', FALSE),
(4, 'Медианная точка', TRUE),
(4, 'Средняя точка', FALSE),
(4, 'Минимальная точка', FALSE),
(4, 'Максимальная точка', FALSE),
(5, 'x = y = const / 2', TRUE),
(5, 'x = 0, y = const', FALSE),
(8, 'e^(ax)', FALSE),
(8, 'e^(x log a)', TRUE),
(8, 'e^(log ax)', FALSE),
(8, 'e^(a log x)', FALSE),
(9, 'Виртуальная машина, на которой развернут кластер.', FALSE),
(9, 'Группа контейнеров, которые разделяют сеть и файловую систему.', TRUE),
(9, 'Тип базы данных, управляемый Kubernetes.', FALSE),
(9, 'Ядро операционной системы контейнера.', FALSE),
(10, 'Они необратимы', FALSE),
(10, 'Они всегда завершаются успешно', FALSE),
(10, 'Они могут быть откатаны при ошибке', TRUE),
(10, 'Они выполняются моментально', FALSE),
(11, 'O(log n)', TRUE),
(11, 'O(sqrt(n))', FALSE),
(11, 'O(n)', FALSE),
(11, 'O(1)', FALSE);
