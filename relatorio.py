import psycopg2
import pandas as pd

# --- Conexão com PostgreSQL ---
conn = psycopg2.connect(
    host="localhost",
    database="escola",
    user="Leo",       # <-- usuário correto no seu PostgreSQL
    password=""       # <-- se não tiver senha, deixe vazio
)

# --- Query 1: Horas por professor ---
query_professores = """
SELECT 
    p.id AS professor_id,
    p.name AS professor_name,
    SUM(
        EXTRACT(EPOCH FROM (cs.end_time - cs.start_time)) / 3600
    ) AS total_hours
FROM PROFESSOR p
JOIN SUBJECT s ON s.taught_by = p.id
JOIN CLASS c ON c.subject_id = s.id
JOIN CLASS_SCHEDULE cs ON cs.class_id = c.id
GROUP BY p.id, p.name
ORDER BY p.name;
"""

df_professores = pd.read_sql(query_professores, conn)
print("Horas por professor:")
print(df_professores)

# --- Query 2: Salas e horários ---
query_salas = """
SELECT 
    r.id AS room_id,
    r.name AS room_name,
    cs.day_of_week,
    cs.start_time,
    cs.end_time,
    CASE
        WHEN cs.id IS NOT NULL THEN 'Ocupada'
        ELSE 'Livre'
    END AS status
FROM ROOM r
LEFT JOIN CLASS_SCHEDULE cs ON cs.room_id = r.id
ORDER BY r.id, cs.day_of_week, cs.start_time;
"""

df_salas = pd.read_sql(query_salas, conn)
print("\nSalas e horários:")
print(df_salas)

# --- Salvar em CSV ---
df_professores.to_csv("horas_professores.csv", index=False)
df_salas.to_csv("salas_status.csv", index=False)

# --- Salvar em Excel ---
with pd.ExcelWriter("relatorio_completo.xlsx") as writer:
    df_professores.to_excel(writer, sheet_name="Horas Professores", index=False)
    df_salas.to_excel(writer, sheet_name="Salas Status", index=False)

print("\nArquivos gerados com sucesso na pasta atual!")

# --- Fechar conexão ---
conn.close()
