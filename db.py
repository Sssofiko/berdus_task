import mysql.connector

# Подключение к базе данных MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ametist1!",  # Мой пароль :)))
    database="test"
)

cursor = conn.cursor()

cursor.execute("DELETE FROM records;")
cursor.execute("DELETE FROM markers;")
cursor.execute("DELETE FROM errors;")
cursor.execute("DELETE FROM distribs;")
cursor.execute("DELETE FROM severity;")
conn.commit()

insert_data_query = [
    "INSERT INTO records (id, date, distr_id, error_id, status) VALUES (1, '2024-01-01', 10, 100, 3)",
    "INSERT INTO records (id, date, distr_id, error_id, status) VALUES (2, '2024-02-01', 11, 101, 2)",
    "INSERT INTO records (id, date, distr_id, error_id, status) VALUES (3, '2024-03-01', 10, 102, 1)",
    "INSERT INTO records (id, date, distr_id, error_id, status) VALUES (4, '2024-04-01', 12, 104, 2)",
    "INSERT INTO records (id, date, distr_id, error_id, status) VALUES (5, '2024-05-01', 10, 104, 1)",
    "INSERT INTO records (id, date, distr_id, error_id, status) VALUES (6, '2024-06-01', 11, 102, 1)",
    "INSERT INTO markers (id, analyzed_sev) VALUES (1, 3)",
    "INSERT INTO markers (id, analyzed_sev) VALUES (2, 0)",
    "INSERT INTO markers (id, analyzed_sev) VALUES (3, 2)",
    "INSERT INTO markers (id, analyzed_sev) VALUES (4, 0)",
    "INSERT INTO markers (id, analyzed_sev) VALUES (5, 3)",
    "INSERT INTO markers (id, analyzed_sev) VALUES (6, 3)",
    "INSERT INTO errors (id, ename, severity) VALUES (100, 'ERRORNAME1', 1)",
    "INSERT INTO errors (id, ename, severity) VALUES (101, 'ERRORNAME2', 2)",
    "INSERT INTO errors (id, ename, severity) VALUES (102, 'ERRORNAME3', 3)",
    "INSERT INTO errors (id, ename, severity) VALUES (104, 'ERRORNAME4', 3)",
    "INSERT INTO distribs (id, name, version) VALUES (10, 'Windows 7', 'SP1')",
    "INSERT INTO distribs (id, name, version) VALUES (11, 'Windows 8', 'RTM')",
    "INSERT INTO distribs (id, name, version) VALUES (12, 'Linux', '6.1')",
    "INSERT INTO severity (id, sname) VALUES (0, 'Не указана')",
    "INSERT INTO severity (id, sname) VALUES (1, 'Низкая')",
    "INSERT INTO severity (id, sname) VALUES (2, 'Средняя')",
    "INSERT INTO severity (id, sname) VALUES (3, 'Критичная')"
]

for query in insert_data_query:
    cursor.execute(query)

conn.commit()

# Запрос
test_query = """
SELECT 
    r.id AS `ID Записи`,
    r.date AS `Дата`,
    CASE
        WHEN m.analyzed_sev IS NOT NULL THEN
            CASE m.analyzed_sev
                WHEN 3 THEN 'Критичная'
                ELSE NULL
            END
        ELSE
            CASE e.severity
                WHEN 3 THEN 'Критичная'
                ELSE NULL
            END
    END AS `Критичность`,
    r.status AS `Статус ошибки`,
    CONCAT(d.name, ' ', d.version) AS `Дистрибутив`
FROM 
    records r
LEFT JOIN 
    markers m ON r.id = m.id
JOIN 
    errors e ON r.error_id = e.id
JOIN 
    distribs d ON r.distr_id = d.id
WHERE 
    r.date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) 
    AND (
        (m.analyzed_sev = 3) OR 
        (m.analyzed_sev IS NULL AND e.severity = 3)
    )
    AND d.name LIKE 'Windows%'  
ORDER BY 
    r.date DESC;
"""

cursor.execute(test_query)
result = cursor.fetchall()

cursor.close()
conn.close()

for row in result:
    print(row)
