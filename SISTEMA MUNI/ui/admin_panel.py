import tkinter as tk
from tkinter import ttk, messagebox
from db.connection import get_connection
from PIL import Image, ImageTk


class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Turnos - Administrador")
        self.root.state('zoomed')  # Pantalla completa
        self.root.configure(bg="#F8F8F8")

        # Ícono de la ventana
        try:
            icon_path = r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\logo.ico"
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error al cargar el ícono de la ventana: {e}")

        # Encabezado superior
        header_frame = tk.Frame(root, bg="#00E201", height=80) ##00E201
        header_frame.pack(fill=tk.X, side=tk.TOP)

        #################### LOGO DE LA MUNI ###########################
        try:
            image_path = r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\logo_completo.png"
            image = Image.open(image_path).resize((250, 80), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(image)

        except Exception as e:
            print(f"Error al cargar el logo: {e}")

        # Colocar el logo a la izquierda
        logo_label = tk.Label(header_frame, image=self.logo, bg="#00E201")
        logo_label.pack(side=tk.LEFT, padx=20, pady=12)

        ############################ LOGO DE ADMINISTRADOR ########################
        try:
            image_path_admin = r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\admin.png"
            image_admin = Image.open(image_path_admin).resize((30, 30), Image.Resampling.LANCZOS)  # Ajusta el tamaño
            self.logo_admin = ImageTk.PhotoImage(image_admin)
        except Exception as e:
            print(f"Error al cargar el logo admin: {e}")

        # Colocar el segundo logo al lado del texto "Administrador"
        admin_label = tk.Label(header_frame, text="Administrador", bg="#00E201", fg="black", font=("Arial", 14), anchor="e")
        admin_label.pack(side=tk.RIGHT, padx=20, pady=20)

        logo_admin_label = tk.Label(header_frame, image=self.logo_admin, bg="#00E201")
        logo_admin_label.pack(side=tk.RIGHT, padx=0)

        ################################################################
        # Título del panel
        logo_label = tk.Label(header_frame, image=self.logo, bg="#00E201")
        tk.Label(root, text="Atención", font=("Arial", 16, "bold"), bg="#F8F8F8", fg="#333333").pack(pady=10)

        # Ccontenedor para la tabla y la barra de desplazamiento
        tree_frame = tk.Frame(root)
        tree_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Crear la barra de desplazamiento vertical
        scrollbar = tk.Scrollbar(tree_frame, orient="vertical")

        # Tabla de turnos
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#E8E8E8", foreground="#333333")
        style.configure("Treeview", font=("Arial", 11), rowheight=30, background="white", fieldbackground="white")
        style.map("Treeview", background=[("selected", "#00E201")], foreground=[("selected", "white")])

        self.tree = ttk.Treeview(tree_frame, columns=("Turno", "DNI", "Motivo", "Estado", "Hora", "Ventanilla"), show="headings", height=10, yscrollcommand=scrollbar.set)
        self.tree.heading("Turno", text="Turno")
        self.tree.heading("DNI", text="DNI")
        self.tree.heading("Motivo", text="Motivo")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("Hora", text="Hora")    ####################### AÑADÍ HORA ###################
        self.tree.heading("Ventanilla", text="Ventanilla")

        # Empaquetar la tabla
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurar la barra de desplazamiento
        scrollbar.config(command=self.tree.yview)

        # Empaquetar la barra de desplazamiento
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Botones inferiores
        button_frame = tk.Frame(root, bg="#F8F8F8")
        button_frame.pack(pady=10, side=tk.BOTTOM)

        ######################### LOGOS DE LOS BOTONES #############################

        # Cargar el logo de "Siguiente"
        try:
            siguiente_logo_path = r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\siguiente.png"
            self.siguiente_logo = Image.open(siguiente_logo_path).resize((30, 20), Image.Resampling.LANCZOS)
            self.siguiente_logo_img = ImageTk.PhotoImage(self.siguiente_logo)
        except Exception as e:
            print(f"Error al cargar el logo de 'Siguiente': {e}")

        # Cargar el logo de "Llamar"
        try:
            llamar_logo_path = r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\llamar.png"
            self.llamar_logo = Image.open(llamar_logo_path).resize((20, 20), Image.Resampling.LANCZOS)
            self.llamar_logo_img = ImageTk.PhotoImage(self.llamar_logo)
        except Exception as e:
            print(f"Error al cargar el logo de 'Llamar': {e}")

        # Cargar el logo de "Eliminar"
        try:
            eliminar_logo_path = r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\eliminar.png"
            self.eliminar_logo = Image.open(eliminar_logo_path).resize((20, 20), Image.Resampling.LANCZOS)
            self.eliminar_logo_img = ImageTk.PhotoImage(self.eliminar_logo)
        except Exception as e:
            print(f"Error al cargar el logo de 'Eliminar': {e}")

        ######################### Botón SIGUIENTE ###################################
        siguiente_button = tk.Button(button_frame, text="Siguiente", font=("Arial", 12, "bold"), bg="#0000FF", fg="white", 
                                     compound="left", image=self.siguiente_logo_img, command=self.siguiente_turno, padx=10, pady=5)
        siguiente_button.grid(row=0, column=0, padx=15)

        ######################### Botón LLAMAR ######################################
        llamar_button = tk.Button(button_frame, text="Llamar", font=("Arial", 12, "bold"), bg="#008000", fg="white", 
                                  compound="left", image=self.llamar_logo_img, command=self.llamar_turno, padx=10, pady=5)
        llamar_button.grid(row=0, column=1, padx=15)

        ######################### Botón ANULAR ######################################
        anular_button = tk.Button(button_frame, text="Anular", font=("Arial", 12, "bold"), bg="#FF0000", fg="white", 
                                  compound="left", image=self.eliminar_logo_img, command=self.eliminar_turno, padx=10, pady=5)
        anular_button.grid(row=0, column=2, padx=15)

        ###########################################################################

        # Cargar turnos
        self.cargar_turnos()

    def cargar_turnos(self):
        """Carga los turnos desde la base de datos en la tabla."""
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT numero_turno, dni, motivo, estado, TO_CHAR(fecha_hora, 'HH12:MI AM') AS hora, ventanilla FROM turnos ORDER BY prioridad DESC, fecha_hora ASC ")
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
