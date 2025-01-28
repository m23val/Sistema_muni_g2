import tkinter as tk
from tkinter import ttk, messagebox
from db.connection import get_connection
from PIL import Image, ImageTk
import time
from threading import Thread
from datetime import datetime

class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Turnos - Administrador")
        self.root.state('zoomed')  # Pantalla completa
        self.root.configure(bg="#F8F8F8")
        self.turnos_atendidos = set()  # Para controlar el orden correcto de "Llamar" â†’ "Siguiente"

        # Ãcono de la ventana
        try:
            icon_path = "C:/Users/Max/Desktop/Sistema_muni_g2-main/assets/logo.ico"
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error al cargar el ícono de la ventana: {e}")

        # Encabezado superior
        header_frame = tk.Frame(root, bg="#00E201", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        

        try:
            image_path = "C:/Users/Max/Desktop/Sistema_muni_g2-main/assets/logo_completo.png"
            image = Image.open(image_path).resize((250, 80), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error al cargar el logo: {e}")

        logo_label = tk.Label(header_frame, image=self.logo, bg="#00E201")
        logo_label.pack(side=tk.LEFT, padx=20, pady=12)

        try:
            image_path_admin = "C:/Users/Max/Desktop/Sistema_muni_g2-main/assets/admin.png"
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

        tk.Label(root, text="Atención al ciudadano", font=("Arial", 16, "bold"), bg="#F8F8F8", fg="#333333").pack(pady=10)

        tree_frame = tk.Frame(root)
        tree_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(tree_frame, orient="vertical")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#E8E8E8", foreground="#333333")
        style.configure("Treeview", font=("Arial", 11), rowheight=30, background="white", fieldbackground="white")
        style.map("Treeview", background=[("selected", "#00E201")], foreground=[("selected", "white")])



        #TABLA DE TURNOS PENDIENTES 
        
        # Tabla de turnos pendientes
        self.tree = ttk.Treeview(tree_frame,
            columns=("Turno", "DNI/RUC", "Nombres", "Motivo", "Estado", "Hora", "Ventanilla"),
            show="headings", height=10, yscrollcommand=scrollbar.set)

        for col in ("Turno", "DNI/RUC", "Nombres", "Motivo", "Estado", "Hora", "Ventanilla"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Ajusta el ancho según sea necesario

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

        # Tabla de turnos completados
        self.completed_tree = ttk.Treeview(completed_frame,
            columns=("Turno", "DNI/RUC", "Nombres", "Hora Inicio", "Hora Término"),
            show="headings", height=5, yscrollcommand=completed_scroll.set)

        for col in ("Turno", "DNI/RUC", "Nombres", "Hora Inicio", "Hora Término"):
            self.completed_tree.heading(col,text=col)
            self.completed_tree.column(col,width=100)  # Ajusta el ancho según sea necesario

        self.completed_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        completed_scroll.config(command=self.completed_tree.yview)


    
         # Configurar las columnas del marco inferior para que ambas tablas ocupen el mismo espacio
        bottom_frame.grid_columnconfigure(0 ,weight=1)  # Para la tabla completados

        button_frame = tk.Frame(root,bg="#F8F8F8")
        button_frame.pack(pady=10 ,side=tk.BOTTOM)


        try:
            siguiente_icon = Image.open("C:/Users/Max/Desktop/Sistema_muni_g2-main/assets/siguiente.png").resize((20, 20), Image.Resampling.LANCZOS)
            llamar_icon = Image.open("C:/Users/Max/Desktop/Sistema_muni_g2-main/assets/llamar.png").resize((20, 20), Image.Resampling.LANCZOS)
            cancelar_icon = Image.open("C:/Users/Max/Desktop/Sistema_muni_g2-main/assets/cancelar.png").resize((20, 20), Image.Resampling.LANCZOS)

            self.siguiente_icon_image = ImageTk.PhotoImage(siguiente_icon)
            self.llamar_icon_image = ImageTk.PhotoImage(llamar_icon)
            self.cancelar_icon_image = ImageTk.PhotoImage(cancelar_icon)

        except Exception as e:
            print(f"Error al cargar los íconos: {e}")



        # Botón para ver turnos cancelados con solo un ícono
        try:
             cancelados_icon_path = r"C:/Users/Max/Desktop/Sistema_muni_g2-main/assets/cancelados.png"  # Asegúrate de que la ruta sea correcta
             cancelados_icon_image = Image.open(cancelados_icon_path).resize((50, 50), Image.Resampling.LANCZOS)  # Ajusta el tamaño según sea necesario
             self.cancelados_icon_photo = ImageTk.PhotoImage(cancelados_icon_image)
        except Exception as e:
             print(f"Error al cargar el ícono de cancelados: {e}")

        


        ver_cancelados_button = tk.Button(
                    root,
                    image=self.cancelados_icon_photo,
                    command=self.mostrar_cancelados,
                    bg="white",
                    borderwidth=0  # Sin borde para que se vea más limpio
                )
        ver_cancelados_button.place(relx=0.95,rely=0.67 ,anchor="e")

        button_frame = tk.Frame(root,bg="#F8F8F8")
        button_frame.pack(pady=10 ,side=tk.BOTTOM)


        siguiente_button = tk.Button(button_frame,
                                     text="Siguiente",
                                     font=("Arial", 12, "bold"),
                                     bg="#0000FF",
                                     fg="white",
                                     command=self.siguiente_turno,
                                     padx=10,
                                     pady=5,
                                     image=self.siguiente_icon_image,
                                     compound=tk.LEFT)  # Coloca el icono a la izquierda del texto
        siguiente_button.grid(row=0, column=0, padx=15)

        llamar_button = tk.Button(button_frame,
                                  text="Llamar",
                                  font=("Arial", 12, "bold"),
                                  bg="#008000",
                                  fg="white",
                                  command=self.llamar_turno,
                                  padx=10,
                                  pady=5,
                                  image=self.llamar_icon_image,
                                  compound=tk.LEFT)  # Coloca el icono a la izquierda del texto
        llamar_button.grid(row=0, column=1, padx=15)

        cancelar_button = tk.Button(button_frame,
                text="Cancelar",
                font=("Arial" ,12,"bold"),
                bg="#FF0000",
                fg="white",
                command=self.cancelar_turno,
                padx=10,
                pady=5,
                image=self.cancelar_icon_image,
                compound=tk.LEFT) 
        
        cancelar_button.grid(row=0,column=2,padx=15)

        self.cargar_turnos()





    def update_clock(self):
        now = time.strftime("%I:%M:%S %p - %d/%m/%Y")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)

    def regresar(self):
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("menu_general", r"C:\Users\Max\Desktop\Sistema_muni_g2-main\SISTEMA MUNI\ui\menu_general.py")
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
                        t.numero_turno, 
                        t.dni_ruc, 
                        t.nombres_empresa AS nombres,
                        t.motivo, 
                        t.estado, 
                        TO_CHAR(t.fecha_hora, 'HH24:MI:SS') AS hora, 
                        t.ventanilla
                    FROM turnos t
                    WHERE t.estado NOT IN ('completado', 'cancelado')
                    ORDER BY t.fecha_hora ASC
                """)
                turnos = cursor.fetchall()

                # Limpiar la tabla de turnos pendientes
                for item in self.tree.get_children():
                    self.tree.delete(item)

                for turno in turnos:
                    # Insertar el turno en la tabla
                    item_id = self.tree.insert("", tk.END, values=(
                        turno[0], 
                        turno[1], 
                        turno[2] if turno[2] is not None else "-",
                        turno[3], 
                        turno[4], 
                        turno[5], 
                        turno[6]
                    ))

                    # Aplicar color celeste pastel si el estado es 'atendiendo'
                    if turno[4] == 'atendiendo':
                        self.tree.item(item_id, tags=('atendiendo',))

                # Configurar el estilo para resaltar filas
                self.tree.tag_configure('atendiendo', background='#F4ED73')  # Color celeste pastel

                # Cargar turnos completados
                cursor.execute("""
                    SELECT 
                        numero_turno, 
                        dni_ruc, 
                        nombres_empresa AS nombres,
                        TO_CHAR(hora_atencion, 'HH24:MI:SS'), 
                        TO_CHAR(hora_termino, 'HH24:MI:SS')
                    FROM turnos
                    WHERE estado = 'completado'
                    ORDER BY hora_termino ASC
                """)
                completados = cursor.fetchall()

                # Limpiar la tabla de completados
                for item in self.completed_tree.get_children():
                    self.completed_tree.delete(item)

                for turno in completados:
                    self.completed_tree.insert("", tk.END, values=(
                        turno[0], 
                        turno[1], 
                        turno[2] if turno[2] is not None else "-",
                        turno[3], 
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
                    messagebox.showwarning("Advertencia", "Solo se pueden cancelar turnos que estén en estado 'atendiendo'.")
                    return

                cursor.execute("UPDATE turnos SET estado = 'cancelado' WHERE numero_turno = %s", (turno,))
                connection.commit()
                messagebox.showinfo("Éxito", f"Turno {turno} cancelado.")
                self.cargar_turnos()
            except Exception as e:
                connection.rollback()
                messagebox.showerror("Error", f"Error al cancelar turno: {e}")
            finally:
                cursor.close()
                connection.close()


    def mostrar_cancelados(self):
        # Crear ventana emergente
        self.ventana_cancelados = tk.Toplevel(self.root)
        self.ventana_cancelados.title("Turnos Cancelados")
        self.ventana_cancelados.geometry("600x400")
        self.ventana_cancelados.transient(self.root)  # Hace que la ventana sea dependiente de la principal
        self.ventana_cancelados.grab_set()  # Hace que la ventana sea modal

        # Crear frame para la tabla
        cancelled_frame = tk.Frame(self.ventana_cancelados)
        cancelled_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Cargar ícono para la ventana de turnos cancelados
        try:
            icon_path = "C:/Users/Max/Desktop/Sistema_muni_g2-main/assets/logo.ico"
            self.ventana_cancelados.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error al cargar el ícono de la ventana: {e}")

        
        # Título
        tk.Label(
            cancelled_frame, 
            text="Turnos Cancelados", 
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        

        # Crear tabla con scrollbar
        cancelled_tree_frame = tk.Frame(cancelled_frame)
        cancelled_tree_frame.pack(fill=tk.BOTH, expand=True)

        cancelled_scroll = tk.Scrollbar(cancelled_tree_frame)
        cancelled_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.cancelled_tree = ttk.Treeview(
            cancelled_tree_frame,
            columns=("Turno", "DNI/RUC", "Nombres", "Motivo"),
            show="headings",
            height=15
        )

        # Configurar columnas
        for col in ("Turno", "DNI/RUC", "Nombres", "Motivo"):
            self.cancelled_tree.heading(col, text=col)
            self.cancelled_tree.column(col, width=100)

        self.cancelled_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cancelled_scroll.config(command=self.cancelled_tree.yview)
        self.cancelled_tree.config(yscrollcommand=cancelled_scroll.set)

        # Botón para cerrar
        tk.Button(
            self.ventana_cancelados,
            text="Cerrar",
            font=("Arial", 10),
            command=self.ventana_cancelados.destroy,
            padx=20,
            pady=5
        ).pack(pady=10)

        # Cargar datos de turnos cancelados
        self.cargar_turnos_cancelados()



    def cargar_turnos_cancelados(self):
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT 
                        numero_turno, 
                        dni_ruc, 
                        nombres_empresa AS nombres,
                        motivo
                    FROM turnos
                    WHERE estado = 'cancelado'
                    ORDER BY fecha_hora DESC
                """)
                cancelados = cursor.fetchall()

                # Limpiar tabla actual
                for item in self.cancelled_tree.get_children():
                    self.cancelled_tree.delete(item)

                # Insertar nuevos datos
                for turno in cancelados:
                    self.cancelled_tree.insert("", tk.END, values=(
                        turno[0],
                        turno[1],
                        turno[2] if turno[2] is not None else "-",
                        turno[3]
                    ))

            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar turnos cancelados: {e}")
            finally:
                cursor.close()
                connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminPanel(root)
    root.mainloop()