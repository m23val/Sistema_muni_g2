import tkinter as tk
from tkinter import ttk, messagebox
from db.connection import get_connection
from PIL import Image, ImageTk
import time
from threading import Thread
from datetime import datetime
import math

class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Turnos - Administrador")
        self.root.state('zoomed')  # Pantalla completa
        self.root.configure(bg="#F8F8F8")
        self.turnos_atendidos = set()  # Para controlar el orden correcto de "Llamar" â†’ "Siguiente"
        self.limpiar_tablas_diariamente()

        # Ãcono de la ventana
        try:
            icon_path = "C:/Users/marie/OneDrive/Escritorio/SISTEMA/sistema_muni_g2/assets/logo.ico"
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
        self.clock_canvas = tk.Canvas(right_container, width=100, height=100, bg="#00E201", highlightthickness=0)
        self.clock_canvas.pack(side=tk.RIGHT, padx=10)

        self.clock_label = tk.Label(right_container, font=("roboto", 14), bg="#00E201", fg="black")
        self.clock_label.pack(side=tk.RIGHT)

        self.update_clock()  # Iniciar el reloj
        
        
        
        admin_label = tk.Label(header_frame, text="Administrador", bg="#00E201", fg="black", font=("Arial", 14), anchor="e")
        admin_label.pack(side=tk.RIGHT, padx=20, pady=20)

        logo_admin_label = tk.Label(header_frame, image=self.logo_admin, bg="#00E201")
        logo_admin_label.pack(side=tk.RIGHT, padx=0)

        regresar_button = tk.Button(header_frame, text="Regresar", font=("Arial", 12, "bold"), bg="#FF8000", fg="white", command=self.regresar, padx=10, pady=5)
        regresar_button.pack(side=tk.LEFT, padx=20)

        tk.Label(root, text="Atención al ciudadano", font=("Arial", 16, "bold"), bg="#F8F8F8", fg="#333333").pack(pady=10)

        tree_frame = tk.Frame(root)
        tree_frame.pack(pady=0, padx=20, fill=tk.BOTH, expand=True)

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
        completed_label.grid(row=0, column=0, padx=10, pady=0, sticky="w")

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
            siguiente_icon = Image.open("C:/Users/marie/OneDrive/Escritorio/SISTEMA/Sistema_muni_g2/assets/siguiente.png").resize((20, 20), Image.Resampling.LANCZOS)
            llamar_icon = Image.open("C:/Users/marie/OneDrive/Escritorio/SISTEMA/Sistema_muni_g2/assets/llamar.png").resize((20, 20), Image.Resampling.LANCZOS)
            cancelar_icon = Image.open("C:/Users/marie/OneDrive/Escritorio/SISTEMA/Sistema_muni_g2/assets/cancelar.png").resize((20, 20), Image.Resampling.LANCZOS)

            self.siguiente_icon_image = ImageTk.PhotoImage(siguiente_icon)
            self.llamar_icon_image = ImageTk.PhotoImage(llamar_icon)
            self.cancelar_icon_image = ImageTk.PhotoImage(cancelar_icon)

        except Exception as e:
            print(f"Error al cargar los íconos: {e}")



        # Botón para ver turnos cancelados con solo un ícono
        try:
             cancelados_icon_path = r"C:/Users/marie/OneDrive/Escritorio/SISTEMA/Sistema_muni_g2/assets/cancelados.png"  # Asegúrate de que la ruta sea correcta
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
        now = time.localtime()

        # Calcular la posición de las manecillas del reloj
        seconds_angle = (now.tm_sec / 60) * 360 - 90
        minutes_angle = (now.tm_min / 60) * 360 + (now.tm_sec / 60) * 6 - 90
        hours_angle = ((now.tm_hour % 12) / 12) * 360 + (now.tm_min / 60) * 30 - 90

        # Limpiar el canvas del reloj
        self.clock_canvas.delete("all")

        # Dibujar círculo del reloj
        self.clock_canvas.create_oval(5, 5, 95, 95, outline="black")

        # Dibujar números en el reloj en posiciones correctas
        
        for i in range(12):
            angle_rad = math.radians((i - 2) * 30)  # Restar 3 ajusta el inicio al 12 en la parte superior
            x_numero = 50 + (35 * math.cos(angle_rad))  # Se usa coseno para el eje X
            y_numero = 50 + (35 * math.sin(angle_rad))  # Se usa seno para el eje Y
            self.clock_canvas.create_text(x_numero, y_numero, text=str(i + 1), font=("Arial", 10))




        # Dibujar manecillas del reloj
        hour_hand_length = 25
        minute_hand_length = 35
        second_hand_length = 40

        hour_x = 50 + hour_hand_length * math.cos(math.radians(hours_angle))
        hour_y = 50 + hour_hand_length * math.sin(math.radians(hours_angle))

        minute_x = 50 + minute_hand_length * math.cos(math.radians(minutes_angle))
        minute_y = 50 + minute_hand_length * math.sin(math.radians(minutes_angle))

        second_x = 50 + second_hand_length * math.cos(math.radians(seconds_angle))
        second_y = 50 + second_hand_length * math.sin(math.radians(seconds_angle))

        # Dibujar las manecillas en el canvas del reloj
        self.clock_canvas.create_line(50, 50, hour_x, hour_y, width=4)   # Manecilla de horas
        self.clock_canvas.create_line(50, 50, minute_x, minute_y, width=3)   # Manecilla de minutos
        self.clock_canvas.create_line(50, 50, second_x, second_y, fill='red', width=1)   # Manecilla de segundos

        # Actualizar la etiqueta con la hora actual en formato texto.
        current_time_text = time.strftime("%I:%M:%S %p")
        self.clock_label.config(text=current_time_text)

        # Agregar la fecha
        current_date_text = time.strftime("%d-%m-%Y")
        date_label = tk.Label(self.root, text=current_date_text, font=("Roboto", 18), bg="#00E201", fg="black")
        date_label.place(relx=0.5, rely=0.05, anchor="center")

        self.root.after(1000, self.update_clock)   # Actualizar cada segundo


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
         # Guardar el numero_turno del item seleccionado
            selected_item = self.tree.selection()
            selected_turno = None
            if selected_item:
                selected_turno = self.tree.item(selected_item)["values"][0]  # Guardamos el número del turno

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
                            FORMAT (t.fecha_hora, 'HH:mm:ss') AS hora, 
                            t.ventanilla
                        FROM turnos t
                        WHERE t.estado NOT IN ('completado', 'cancelado')
                            AND CONVERT (DATE, t.fecha_hora) = CONVERT(DATE, GETDATE())
                        ORDER BY t.fecha_hora ASC;
                    """)
                    turnos = cursor.fetchall()

                    # Limpiar la tabla de turnos pendientes
                    for item in self.tree.get_children():
                        self.tree.delete(item)

                    for turno in turnos:
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
                            FORMAT(hora_atencion, 'HH:mm:ss'), 
                            FORMAT(hora_termino, 'HH:mm:ss')
                        FROM turnos
                        WHERE estado = 'completado'
                            AND CONVERT (DATE, fecha_hora) = CONVERT(DATE, GETDATE())
                        ORDER BY hora_termino ASC;
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

            # Actualizar automáticamente cada 5 segundos
            self.root.after(5000, self.cargar_turnos)

            # Restaurar la selección después de la actualización
            if selected_turno:
                # Verificar si el turno aún está en la lista después de la actualización
                for item in self.tree.get_children():
                    if self.tree.item(item)["values"][0] == selected_turno:
                        self.tree.selection_set(item)
                        break



    def llamar_turno(self):
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()

                # 🔎 Buscar el primer turno pendiente más antiguo
                cursor.execute("""
                    SELECT TOP 1 numero_turno 
                    FROM turnos 
                    WHERE estado NOT IN ('completado', 'cancelado', 'atendiendo') 
                    ORDER BY fecha_hora ASC;
                """)
                turno = cursor.fetchone()

                if not turno:
                    messagebox.showwarning("Advertencia", "No hay turnos pendientes para llamar.")
                    return

                turno = turno[0]  # Extraer el número de turno

                #Buscar ventanilla libre
                cursor.execute("""
                    SELECT TOP 1 ventanilla 
                    FROM encargados 
                    WHERE ventanilla NOT IN (
                        SELECT ventanilla 
                        FROM turnos 
                        WHERE estado = 'atendiendo'
                    ) 
                """)
                ventanilla = cursor.fetchone()

                if not ventanilla:
                    messagebox.showwarning("Advertencia", "No hay ventanillas disponibles.")
                    return

                ventanilla = ventanilla[0]

                # Asignar el turno a la ventanilla y actualizar estado
                cursor.execute("""
                    UPDATE turnos 
                    SET estado = 'atendiendo', ventanilla = ?, hora_atencion = GETDATE() 
                    WHERE numero_turno = ?
                """, (ventanilla, turno))
                connection.commit()

                messagebox.showinfo("Éxito", f"Turno {turno} asignado a la ventanilla {ventanilla}.")

                # Recargar la lista de turnos
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
                cursor.execute("SELECT estado FROM turnos WHERE numero_turno = ?", (turno,))
                estado = cursor.fetchone()

                if not estado or estado[0] != "atendiendo":
                    messagebox.showwarning("Advertencia", "El turno debe estar en estado 'atendiendo'.")
                    return

                # Marcar turno actual como completado
                cursor.execute(
                    "UPDATE turnos SET estado = 'completado', hora_termino = GETDATE() WHERE numero_turno = ?", (turno,))

                # Buscar y llamar automáticamente al próximo turno más antiguo
                cursor.execute("""
                    SELECT TOP 1 numero_turno, ventanilla 
                    FROM turnos 
                    WHERE estado NOT IN ('completado', 'cancelado', 'atendiendo') 
                    AND CONVERT(DATE, fecha_hora) = CONVERT(DATE, GETDATE()) 
                    ORDER BY fecha_hora ASC 
                """)
                next_turno = cursor.fetchone()

                if next_turno:
                    # Seleccionar ventanilla actual
                    cursor.execute("SELECT ventanilla FROM turnos WHERE numero_turno = ?", (turno,))
                    ventanilla_actual = cursor.fetchone()[0]

                    # Asignar el próximo turno a la misma ventanilla
                    cursor.execute(
                        "UPDATE turnos SET estado = 'atendiendo', ventanilla = ?, hora_atencion = GETDATE() WHERE numero_turno = ?", 
                        (ventanilla_actual, next_turno[0])
                    )
                    connection.commit()
                    messagebox.showinfo("Información", f"Turno {turno} completado. Siguiente turno {next_turno[0]} llamado automáticamente.")
                else:
                    connection.commit()
                    messagebox.showinfo("Información", f"Turno {turno} completado. No hay más turnos pendientes.")

                #Selección del turno
                self.tree.selection_set(selected_item)

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
                # Verificar el estado del turno
                cursor.execute("SELECT estado, ventanilla FROM turnos WHERE numero_turno = ?", (turno,))
                resultado = cursor.fetchone()
                cursor.execute("SELECT estado FROM turnos WHERE numero_turno = ?", (turno,))
                estado = cursor.fetchone()

                if not estado or estado[0] != "atendiendo":
                    messagebox.showwarning("Advertencia", "Solo se pueden cancelar turnos que estén en estado 'atendiendo'.")
                    return
                ventanilla = resultado[1]  # Obtener la ventanilla del turno cancelado

                cursor.execute("UPDATE turnos SET estado = 'cancelado' WHERE numero_turno = ?", (turno,))
                connection.commit()
                messagebox.showinfo("Éxito", f"Turno {turno} cancelado.")
                self.cargar_turnos()



                # Buscar el siguiente turno más temprano
                cursor.execute("""
                    SELECT TOP 1 numero_turno 
                    FROM turnos 
                    WHERE estado NOT IN ('completado', 'cancelado', 'atendiendo') 
                    ORDER BY fecha_hora ASC
                """)
                siguiente_turno = cursor.fetchone()

                if siguiente_turno:
                    # Asignar el siguiente turno a la ventanilla que quedó disponible
                    cursor.execute("""
                        UPDATE turnos 
                        SET estado = 'atendiendo', ventanilla = ?, hora_atencion = GETDATE() 
                        WHERE numero_turno = ?
                    """, (ventanilla, siguiente_turno[0]))
                    connection.commit()
                    messagebox.showinfo("Información", f"Turno {siguiente_turno[0]} asignado automáticamente a la ventanilla {ventanilla}.")

                self.cargar_turnos()  # Actualizar la interfaz






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
        self.ventana_cancelados.geometry("1000x400")
        self.ventana_cancelados.transient(self.root)  # Hace que la ventana sea dependiente de la principal
        self.ventana_cancelados.grab_set()  # Hace que la ventana sea modal

        # Crear frame para la tabla
        cancelled_frame = tk.Frame(self.ventana_cancelados)
        cancelled_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Cargar ícono para la ventana de turnos cancelados
        try:
            icon_path = "C:/Users/marie/OneDrive/Escritorio/SISTEMA/Sistema_muni_g2/assets/logo.ico"
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

    def limpiar_tablas_diariamente(self):
        # Verificar si es un nuevo día
        current_date = datetime.now().date()
        if hasattr(self, 'last_date') and current_date != self.last_date:
            self.limpiar_tablas()
        self.last_date = current_date
         # Volver a ejecutar la función después de 1 hora (3600000 ms)
        self.root.after(60000, self.limpiar_tablas_diariamente)  

    def limpiar_tablas(self):
        connection = get_connection()
        if connection: 
            try:
                cursor = connection.cursor()
                # Liberar ventanillas ocupadas por turnos anteriores
                cursor.execute("""
                    UPDATE turnos
                    SET ventanilla = NULL
                    WHERE CONVERT(DATE, fecha_hora) < CONVERT(DATE, GETDATE())
                    OR estado IN ('completado', 'cancelado')
                """)
                connection.commit()  # Confirmar cambios en la BD

                # Limpiar la tabla de turnos pendientes en la interfaz
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # Limpiar la tabla de turnos completados en la interfaz
                for item in self.completed_tree.get_children():
                    self.completed_tree.delete(item)

            except Exception as e:
                messagebox.showerror("Error", f"Error al limpiar las tablas: {e}")

            finally:
                cursor.close()
                connection.close()

        self.root.after(60000, self.limpiar_tablas)  



    def cargar_turnos_cancelados(self):
        if not hasattr(self, 'ventana_cancelados') or not self.ventana_cancelados.winfo_exists():
            return  # No actualiza si la ventana ha sido cerrada
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
                        AND CONVERT (DATE, fecha_hora) = CONVERT(DATE, GETDATE())
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

        # Solo actualizar si la ventana sigue abierta
        if hasattr(self, 'ventana_cancelados') and self.ventana_cancelados.winfo_exists():
            self.root.after(5000, self.cargar_turnos_cancelados) 
        # Actualizar automáticamente cada 5 segundos
        #self.root.after(5000, self.cargar_turnos_cancelados)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminPanel(root)
    app.limpiar_tablas_diariamente
    app.limpiar_tablas
    root.mainloop()