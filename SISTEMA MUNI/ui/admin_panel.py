import tkinter as tk
from tkinter import ttk, messagebox
from db.connection import get_connection
from PIL import Image, ImageTk
import time
from threading import Thread


class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Turnos - Administrador")
        self.root.state('zoomed')  # Pantalla completa
        self.root.configure(bg="#F8F8F8")
        self.turnos_atendidos = set()  # Para controlar el orden correcto de "Llamar" â†’ "Siguiente"

        # Ãcono de la ventana
        try:
            icon_path = "C:/Users/marie/OneDrive/Escritorio/SISTEMA/Sistema_muni_g2/assets/logo.ico"
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error al cargar el ícono de la ventana: {e}")

        # Encabezado superior
        header_frame = tk.Frame(root, bg="#00E201", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        

        try:
            image_path = "C:/Users/marie/OneDrive/Escritorio/SISTEMA/Sistema_muni_g2/assets/logo_completo.png"
            image = Image.open(image_path).resize((250, 80), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error al cargar el logo: {e}")

        logo_label = tk.Label(header_frame, image=self.logo, bg="#00E201")
        logo_label.pack(side=tk.LEFT, padx=20, pady=12)

        try:
            image_path_admin = "C:/Users/marie/OneDrive/Escritorio/SISTEMA/Sistema_muni_g2/assets/admin.png"
            image_admin = Image.open(image_path_admin).resize((30, 30), Image.Resampling.LANCZOS)
            self.logo_admin = ImageTk.PhotoImage(image_admin)
        except Exception as e:
            print(f"Error al cargar el logo admin: {e}")

        
        right_container = tk.Frame(header_frame, bg="#00E201")
        right_container.pack(side=tk.RIGHT, padx=20)

        # Reloj en el contenedor derecho
        self.clock_label = tk.Label(right_container, font=("roboto", 20), bg="#00E201", fg="white")
        self.clock_label.pack(side=tk.RIGHT, padx=10)
        self.update_clock()
        
        
        
        admin_label = tk.Label(header_frame, text="Administrador", bg="#00E201", fg="black", font=("Arial", 14), anchor="e")
        admin_label.pack(side=tk.RIGHT, padx=20, pady=20)

        logo_admin_label = tk.Label(header_frame, image=self.logo_admin, bg="#00E201")
        logo_admin_label.pack(side=tk.RIGHT, padx=0)

        regresar_button = tk.Button(header_frame, text="Regresar", font=("Arial", 12, "bold"), bg="#FF8000", fg="white", command=self.regresar, padx=10, pady=5)
        regresar_button.pack(side=tk.LEFT, padx=20)

        tk.Label(root, text="Atención", font=("Arial", 16, "bold"), bg="#F8F8F8", fg="#333333").pack(pady=10)

        tree_frame = tk.Frame(root)
        tree_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(tree_frame, orient="vertical")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#E8E8E8", foreground="#333333")
        style.configure("Treeview", font=("Arial", 11), rowheight=30, background="white", fieldbackground="white")
        style.map("Treeview", background=[("selected", "#00E201")], foreground=[("selected", "white")])

        self.tree = ttk.Treeview(tree_frame, columns=("Turno", "DNI", "Nombres", "RUC", "Motivo", "Estado", "Hora", "Ventanilla"), show="headings", height=10, yscrollcommand=scrollbar.set)
        self.tree.heading("Turno", text="Turno")
        self.tree.heading("DNI", text="DNI")
        self.tree.heading("Nombres", text="Nombres")  # Nueva columna de Nombres
        self.tree.heading("RUC", text="RUC")  # Nueva columna de RUC
        self.tree.heading("Motivo", text="Motivo")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("Hora", text="Hora")
        self.tree.heading("Ventanilla", text="Ventanilla")


        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=10)



        completed_label = tk.Label(bottom_frame, text="Turnos Completados", font=("Arial", 12, "bold"), bg="#F8F8F8", fg="#333333")
        completed_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        completed_frame = tk.Frame(bottom_frame)
        completed_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        completed_scroll = tk.Scrollbar(completed_frame)
        completed_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.completed_tree = ttk.Treeview(completed_frame, 
            columns=("Turno", "DNI", "Nombres", "RUC", "Hora Inicio", "Hora Término"), 
            show="headings", height=5, yscrollcommand=completed_scroll.set)
        self.completed_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        completed_scroll.config(command=self.completed_tree.yview)

        # ModificaciÃ³n de la tabla de cancelados con scrollbar
        cancelled_label = tk.Label(bottom_frame, text="Turnos Cancelados", font=("Arial", 12, "bold"), bg="#F8F8F8", fg="#333333")
        cancelled_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")        
        cancelled_frame = tk.Frame(bottom_frame)
        cancelled_frame.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        
        cancelled_scroll = tk.Scrollbar(cancelled_frame)
        cancelled_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.cancelled_tree = ttk.Treeview(cancelled_frame, 
            columns=("Turno", "DNI", "Nombres", "RUC", "Motivo"), 
            show="headings", height=5, yscrollcommand=cancelled_scroll.set)
        self.cancelled_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cancelled_scroll.config(command=self.cancelled_tree.yview)

        # ConfiguraciÃ³n de los encabezados de las tablas
        for col in ("Turno", "DNI", "Nombres", "RUC", "Hora Inicio", "Hora Término"):
            self.completed_tree.heading(col, text=col)
            self.completed_tree.column(col, width=100)

        for col in ("Turno", "DNI", "Nombres", "RUC", "Motivo"):
            self.cancelled_tree.heading(col, text=col)
            self.cancelled_tree.column(col, width=100)






        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)

        button_frame = tk.Frame(root, bg="#F8F8F8")
        button_frame.pack(pady=10, side=tk.BOTTOM)

        siguiente_button = tk.Button(button_frame, text="Siguiente", font=("Arial", 12, "bold"), bg="#0000FF", fg="white", command=self.siguiente_turno, padx=10, pady=5)
        siguiente_button.grid(row=0, column=0, padx=15)

        llamar_button = tk.Button(button_frame, text="Llamar", font=("Arial", 12, "bold"), bg="#008000", fg="white", command=self.llamar_turno, padx=10, pady=5)
        llamar_button.grid(row=0, column=1, padx=15)

        cancelar_button = tk.Button(button_frame, text="Cancelar", font=("Arial", 12, "bold"), bg="#FF0000", fg="white", command=self.cancelar_turno, padx=10, pady=5)
        cancelar_button.grid(row=0, column=2, padx=15)

        self.cargar_turnos()

    def update_clock(self):
        now = time.strftime("%I:%M:%S %p - %d/%m/%Y")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)

    def regresar(self):
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("menu_general", r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\SISTEMA MUNI\ui\menu_general.py")
            menu_general = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(menu_general)

            self.root.destroy()  # Cierra la ventana actual
            new_root = tk.Tk()  # Crea una nueva instancia de Tkinter
            menu_general.MenuGeneral(new_root)  # Llama al menÃº principal
            new_root.mainloop()  # Ejecuta el bucle principal de la nueva ventana
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo regresar al menÃº principal: {e}")

    def cargar_turnos(self):
        connection = get_connection()

        if connection:
            try:
                cursor = connection.cursor()

                # Cargar turnos pendientes con nombre y RUC
                cursor.execute("""
                    SELECT 
                        t.numero_turno, t.dni_ruc, 
                        t.nombres_empresa AS nombres,  
                        CASE 
                            WHEN LENGTH(t.dni_ruc) = 11 THEN t.dni_ruc 
                            ELSE '-' 
                        END AS ruc,
                        t.motivo, t.estado, TO_CHAR(t.fecha_hora, 'HH24:MI:SS') AS hora, t.ventanilla
                    FROM turnos t
                    WHERE t.estado NOT IN ('completado', 'cancelado')
                    ORDER BY t.fecha_hora ASC
                """)
                turnos = cursor.fetchall()

                # Limpiar la tabla de turnos pendientes
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # Insertar los turnos pendientes en la tabla
                for turno in turnos:
                    self.tree.insert("", tk.END, values=(
                        turno[0], 
                        turno[1], 
                        turno[2] if turno[2] is not None else "-",  # Si no tiene nombre, colocar "-"
                        turno[3] if turno[3] is not None else "-",  # Si no tiene RUC, colocar "-"
                        turno[4], 
                        turno[5], 
                        turno[6], 
                        turno[7]
                    ))

                # Cargar turnos completados
                cursor.execute("""
                    SELECT numero_turno, dni_ruc, 
                        nombres_empresa AS nombres,  -- Obtener nombres desde la funciÃ³n
                        CASE 
                            WHEN LENGTH(dni_ruc) = 11 THEN dni_ruc  -- Mostrar RUC solo si tiene 11 caracteres
                            ELSE '-' 
                        END AS ruc,
                        TO_CHAR(hora_atencion, 'HH24:MI:SS'), 
                        TO_CHAR(hora_termino, 'HH24:MI:SS')
                    FROM turnos
                    WHERE estado = 'completado'
                    ORDER BY hora_termino ASC  -- Ordenar por la hora de tÃ©rmino
                """)
                completados = cursor.fetchall()

                # Limpiar la tabla de completados
                for item in self.completed_tree.get_children():
                    self.completed_tree.delete(item)

                # Insertar los turnos completados
                for turno in completados:
                    self.completed_tree.insert("", tk.END, values=(
                        turno[0], 
                        turno[1], 
                        turno[2] if turno[2] is not None else "-",  # Si no tiene nombre, colocar "-"
                        turno[3] if turno[3] is not None else "-",  # Si no tiene RUC, colocar "-"
                        turno[4], 
                        turno[5]
                    ))

                # Cargar turnos cancelados
                cursor.execute("""
                    SELECT numero_turno, dni_ruc, 
                        nombres_empresa AS nombres,  -- Obtener nombres desde la funciÃ³n
                        CASE 
                            WHEN LENGTH(dni_ruc) = 11 THEN dni_ruc  -- Mostrar RUC solo si tiene 11 caracteres
                            ELSE '-' 
                        END AS ruc,
                        motivo
                    FROM turnos
                    WHERE estado = 'cancelado'
                """)
                cancelados = cursor.fetchall()

                # Limpiar la tabla de cancelados
                for item in self.cancelled_tree.get_children():
                    self.cancelled_tree.delete(item)

                # Insertar los turnos cancelados
                for turno in cancelados:
                    self.cancelled_tree.insert("", tk.END, values=(
                        turno[0], 
                        turno[1], 
                        turno[2] if turno[2] is not None else "-",  # Si no tiene nombre, colocar "-"
                        turno[3] if turno[3] is not None else "-",  # Si no tiene RUC, colocar "-"
                        turno[4]
                    ))

            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar turnos: {e}")
            finally:
                cursor.close()
                connection.close()





    def llamar_turno(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un turno para llamar.")
            return

        turno = self.tree.item(selected_item)["values"][0]
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT ventanilla FROM encargados WHERE ventanilla NOT IN (SELECT ventanilla FROM turnos WHERE estado = 'atendiendo')")
                ventanilla = cursor.fetchone()

                if not ventanilla:
                    messagebox.showwarning("Advertencia", "No hay ventanillas disponibles.")
                    return

                cursor.execute("UPDATE turnos SET estado = 'atendiendo', ventanilla = %s, hora_atencion = NOW() WHERE numero_turno = %s", (ventanilla[0], turno))
                connection.commit()
                self.turno_actual = turno  # Registrar turno en atenciÃ³n
                messagebox.showinfo("Ã‰xito", f"Turno {turno} asignado a la ventanilla {ventanilla[0]}.")
                self.cargar_turnos()
            except Exception as e:
                connection.rollback()
                messagebox.showerror("Error", f"Error al llamar turno: {e}")
            finally:
                cursor.close()
                connection.close()


                

    def siguiente_turno(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un turno para completar.")
            return

        turno = self.tree.item(selected_item)["values"][0]
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()

                # Verificar el estado del turno
                cursor.execute("SELECT estado FROM turnos WHERE numero_turno = %s", (turno,))
                estado = cursor.fetchone()

                if not estado or estado[0] != "atendiendo":
                    messagebox.showwarning("Advertencia", "El turno debe estar en estado 'atendiendo'.")
                    return

                # Marcar turno actual como completado
                cursor.execute(
                    "UPDATE turnos SET estado = 'completado', hora_termino = NOW() WHERE numero_turno = %s",
                    (turno,)
                )

                # Buscar y llamar automáticamente al próximo turno más antiguo
                cursor.execute("""
                    SELECT numero_turno, ventanilla 
                    FROM turnos 
                    WHERE estado NOT IN ('completado', 'cancelado', 'atendiendo') 
                    ORDER BY fecha_hora ASC 
                    LIMIT 1
                """)
                next_turno = cursor.fetchone()

                if next_turno:
                    # Seleccionar ventanilla actual
                    cursor.execute("SELECT ventanilla FROM turnos WHERE numero_turno = %s", (turno,))
                    ventanilla_actual = cursor.fetchone()[0]

                    # Asignar el próximo turno a la misma ventanilla
                    cursor.execute(
                        "UPDATE turnos SET estado = 'atendiendo', ventanilla = %s, hora_atencion = NOW() WHERE numero_turno = %s", 
                        (ventanilla_actual, next_turno[0])
                    )
                    connection.commit()
                    messagebox.showinfo("Información", f"Turno {turno} completado. Siguiente turno {next_turno[0]} llamado automáticamente.")
                else:
                    connection.commit()
                    messagebox.showinfo("Información", f"Turno {turno} completado. No hay más turnos pendientes.")

                self.cargar_turnos()

            except Exception as e:
                connection.rollback()
                messagebox.showerror("Error", f"Error al procesar turno: {e}")
            finally:
                cursor.close()
                connection.close()




    def cancelar_turno(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un turno para cancelar.")
            return

        turno = self.tree.item(selected_item)["values"][0]

        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT estado FROM turnos WHERE numero_turno = %s", (turno,))
                estado = cursor.fetchone()

                if not estado or estado[0] != "atendiendo":
                    messagebox.showwarning("Advertencia", "Solo se pueden cancelar turnos que estÃ©n en estado 'atendiendo'.")
                    return

                cursor.execute("UPDATE turnos SET estado = 'cancelado' WHERE numero_turno = %s", (turno,))
                connection.commit()
                messagebox.showinfo("Ã‰xito", f"Turno {turno} cancelado.")
                self.cargar_turnos()
            except Exception as e:
                connection.rollback()
                messagebox.showerror("Error", f"Error al cancelar turno: {e}")
            finally:
                cursor.close()
                connection.close()



if __name__ == "__main__":
    root = tk.Tk()
    app = AdminPanel(root)
    root.mainloop()