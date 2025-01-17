import tkinter as tk
from tkinter import ttk, messagebox
from db.connection import get_connection


class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel de Administrador")
        self.root.geometry("800x600")
        self.root.configure(bg="#FFFFFF")

        # Título
        tk.Label(root, text="Panel de Administrador", font=("Arial", 20), bg="#FFD700").pack(pady=10)

        # Tabla de turnos
        self.tree = ttk.Treeview(root, columns=("Turno", "DNI", "Motivo", "Estado", "Ventanilla"), show="headings")
        self.tree.heading("Turno", text="Turno")
        self.tree.heading("DNI", text="DNI")
        self.tree.heading("Motivo", text="Motivo")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("Ventanilla", text="Ventanilla")
        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)

        # Botones
        button_frame = tk.Frame(root, bg="#FFFFFF")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Llamar Turno", font=("Arial", 14), bg="#008000", fg="white", command=self.llamar_turno).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Siguiente Turno", font=("Arial", 14), bg="#0000FF", fg="white", command=self.siguiente_turno).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Eliminar Turno", font=("Arial", 14), bg="#FF0000", fg="white", command=self.eliminar_turno).grid(row=0, column=2, padx=10)

        # Cargar turnos en la tabla
        self.cargar_turnos()

    def cargar_turnos(self):
        """Carga los turnos desde la base de datos en la tabla."""
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT numero_turno, dni, motivo, estado, ventanilla FROM turnos ORDER BY prioridad DESC, fecha_hora ASC")
                turnos = cursor.fetchall()

                # Limpiar la tabla
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # Insertar turnos
                for turno in turnos:
                    self.tree.insert("", tk.END, values=turno)
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar turnos: {e}")
            finally:
                cursor.close()
                connection.close()

    def llamar_turno(self):
        """Asigna un turno a una ventanilla y lo marca como 'atendiendo'."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un turno para llamar.")
            return

        turno = self.tree.item(selected_item)["values"][0]
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()

                # Obtener ventanilla disponible
                cursor.execute("SELECT ventanilla FROM encargados WHERE ventanilla NOT IN (SELECT ventanilla FROM turnos WHERE estado = 'atendiendo')")
                ventanilla = cursor.fetchone()

                if not ventanilla:
                    messagebox.showwarning("Advertencia", "No hay ventanillas disponibles.")
                    return

                # Actualizar estado del turno
                cursor.execute("UPDATE turnos SET estado = 'atendiendo', ventanilla = %s WHERE numero_turno = %s", (ventanilla[0], turno))
                connection.commit()
                messagebox.showinfo("Éxito", f"Turno {turno} asignado a la ventanilla {ventanilla[0]}.")

                self.cargar_turnos()
            except Exception as e:
                connection.rollback()
                messagebox.showerror("Error", f"Error al llamar turno: {e}")
            finally:
                cursor.close()
                connection.close()

    def siguiente_turno(self):
        """Pasa al siguiente turno y libera la ventanilla."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un turno para continuar.")
            return

        turno = self.tree.item(selected_item)["values"][0]
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()

                # Marcar el turno como completado
                cursor.execute("UPDATE turnos SET estado = 'completado' WHERE numero_turno = %s", (turno,))
                connection.commit()
                messagebox.showinfo("Éxito", f"Turno {turno} completado.")

                self.cargar_turnos()
            except Exception as e:
                connection.rollback()
                messagebox.showerror("Error", f"Error al pasar al siguiente turno: {e}")
            finally:
                cursor.close()
                connection.close()

    def eliminar_turno(self):
        """Elimina un turno seleccionado."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un turno para eliminar.")
            return

        turno = self.tree.item(selected_item)["values"][0]
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM turnos WHERE numero_turno = %s", (turno,))
                connection.commit()
                messagebox.showinfo("Éxito", f"Turno {turno} eliminado.")
                self.cargar_turnos()
            except Exception as e:
                connection.rollback()
                messagebox.showerror("Error", f"Error al eliminar turno: {e}")
            finally:
                cursor.close()
                connection.close()


# Prueba del panel de administrador
if __name__ == "__main__":
    root = tk.Tk()
    app = AdminPanel(root)
    root.mainloop()
