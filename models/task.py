from db.connection import get_connection

class Task:
    @staticmethod
    def create_table():
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id SERIAL PRIMARY KEY,
                        sequence INTEGER UNIQUE,
                        nombre TEXT NOT NULL,
                        descripcion TEXT,
                        due_date TIMESTAMP,
                        completado BOOLEAN DEFAULT FALSE
                    );
                """)
                cur.execute("""
                    DO $$
                    BEGIN
                        IF EXISTS (
                            SELECT 1 FROM pg_trigger WHERE tgname = 'trg_update_sequence'
                        ) THEN
                            DROP TRIGGER trg_update_sequence ON tasks;
                        END IF;
                    END;
                    $$;
                """)

                cur.execute("""
                    CREATE OR REPLACE FUNCTION update_sequence_column()
                    RETURNS TRIGGER AS $$
                    BEGIN
                        NEW.sequence := (SELECT COALESCE(MAX(sequence), 0) + 1 FROM tasks);
                        RETURN NEW;
                    END;
                    $$ LANGUAGE plpgsql;
                """)
                cur.execute("""
                    CREATE TRIGGER trg_update_sequence
                    BEFORE INSERT ON tasks
                    FOR EACH ROW
                    EXECUTE FUNCTION update_sequence_column();
                """)
                conn.commit()

    @staticmethod
    def create(nombre, descripcion, due_date=None):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tasks (nombre, descripcion, due_date) VALUES (%s, %s, %s) RETURNING id;",
                    (nombre, descripcion, due_date)
                )
                conn.commit()
                return cur.fetchone()[0]

    @staticmethod
    def get_all():
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, sequence, nombre, descripcion, due_date, completado FROM tasks ORDER BY sequence;")
                return cur.fetchall()

    @staticmethod
    def update(task_id, nombre, descripcion, due_date=None):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE tasks SET nombre = %s, descripcion = %s, due_date = %s WHERE id = %s;",
                    (nombre, descripcion, due_date, task_id)
                )
                conn.commit()

    @staticmethod
    def mark_completed(task_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE tasks SET completado = TRUE WHERE id = %s;", (task_id,))
                conn.commit()

    @staticmethod
    def mark_notcompleted(task_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE tasks SET completado = FALSE WHERE id = %s;", (task_id,))
                conn.commit()

    @staticmethod
    def delete(task_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
                conn.commit()
