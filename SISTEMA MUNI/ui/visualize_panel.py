import tkinter as tk
from db.connection import get_connection  # Asegúrate de que esta importación sea correcta

class VisualizePanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Pantalla de Visualización de Turnos")
        self.root.geometry("800x400")
        self.root.configure(bg="#000000")

        # Etiqueta para mostrar el turno actual
        self.turno_actual_label = tk.Label(root, text="Turno Actual: --", font=("Arial", 30), bg="#000000", fg="#FFFFFF")
        self.turno_actual_label.pack(pady=20)

        # Etiqueta para mostrar los siguientes turnos
        self.siguientes_label = tk.Label(root, text="Siguientes Turnos:", font=("Arial", 24), bg="#000000", fg="#FFFFFF")
        self.siguientes_label.pack(pady=10)

        self.siguientes_list = tk.Label(root, text="", font=("Arial", 20), bg="#000000", fg="#FFD700")
        self.siguientes_list.pack(pady=10)

        # Actualizar turnos en tiempo real
        self.cargar_turnos()
        self.root.after(5000, self.cargar_turnos)

    def cargar_turnos(self):
        """Carga los turnos actuales y los siguientes."""
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT numero_turno, ventanilla FROM turnos WHERE estado = 'atendiendo' ORDER BY fecha_hora ASC LIMIT 1")
                turno_actual = cursor.fetchone()

                cursor.execute("SELECT numero_turno FROM turnos WHERE estado = 'espera' ORDER BY prioridad DESC, fecha_hora ASC LIMIT 3")
                siguientes = cursor.fetchall()

                # Actualizar la pantalla
                if turno_actual:
                    self.turno_actual_label.config(text=f"Turno Actual: {turno_actual[0]} Ventanilla {turno_actual[1]}")
                else:
                    self.turno_actual_label.config(text="Turno Actual: --")

                # Mostrar los siguientes turnos
                self.siguientes_list.config(text="\n".join([f"{t[0]}" for t in siguientes]))
            except Exception as e:
                print(f"Error al cargar turnos: {e}")
            finally:
                cursor.close()
                connection.close()

# Código para ejecutar el panel de visualización
if __name__ == "__main__":
    root = tk.Tk()
    app = VisualizePanel(root)
    root.mainloop()
