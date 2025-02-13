import tkinter as tk
from tkinter import messagebox, Toplevel
from db.connection import get_connection
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image
from PIL import Image, ImageTk, ImageWin
import win32print
import win32ui


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Turnos - Municipalidad De Nuevo Chimbote")
        self.root.state("zoomed")
        self.root.configure(bg="#FFFFFF")

        # Cambiar el ícono de la ventana
        icon_path = r"C:\Users\Max\Desktop\Sistema_muni_g2-main\assets\logo.ico"
        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error al cargar el ícono: {e}")

        # Marco principal
        main_frame = tk.Frame(root, bg="#FFFFFF")
        main_frame.place(relx=0, rely=0, relwidth=1.02, relheight=1)

        # Marco izquierdo para el logo, título y botones
        left_frame = tk.Frame(main_frame, bg="#FFFFFF")
        left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Título
        tk.Label(left_frame, text="GESTIÓN DE TURNOS", font=("Sora", 18, "bold"), bg="#FFFFFF").pack(pady=10)


        # Logo
        try:
            logo_path = r"C:\Users\Max\Desktop\Sistema_muni_g2-main\assets\logo.png"
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((120, 150), Image.Resampling.LANCZOS)
            self.logo_main = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(left_frame, image=self.logo_main, bg="#FFFFFF")
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error al cargar la imagen del logo: {e}")

        # Título
        tk.Label(left_frame, text="Seleccionar motivo:", font=("Sora", 17, "bold"), bg="#FFFFFF").pack(pady=10)


        # Botones de opciones
        buttons_frame = tk.Frame(left_frame, bg="#FFFFFF")
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  

        self.motivo_info = {
            "CONSULTAS": ("C", r"C:\Users\Max\Desktop\Sistema_muni_g2-main\assets\iconsultas.png"),
            "DEUDAS": ("S", r"C:\Users\Max\Desktop\Sistema_muni_g2-main\assets\ideudas.png"),
            "DOCUMENTOS": ("D", r"C:\Users\Max\Desktop\Sistema_muni_g2-main\assets\idocumentos.png"),
            "MULTAS": ("M", r"C:\Users\Max\Desktop\Sistema_muni_g2-main\assets\imultas.png"),
            "PAGOS": ("P", r"C:\Users\Max\Desktop\Sistema_muni_g2-main\assets\ipagos.png"),
            "OTROS": ("O", r"C:\Users\Max\Desktop\Sistema_muni_g2-main\assets\iotros.png")
        }

        # Declaramos una variable para almacenar el motivo seleccionado
        self.motivo_var = tk.StringVar()  # Esta será usada para almacenar el motivo seleccionado

        # Crear botones con imágenes más grandes y espacio entre la imagen y el texto
        for idx, (text, (prefijo, image_path)) in enumerate(self.motivo_info.items()):
            try:
                # Cargar la imagen
                image = Image.open(image_path)
                image = image.resize((110, 110), Image.Resampling.LANCZOS)  # Redimensionar la imagen a 80x80 píxeles
                photo = ImageTk.PhotoImage(image)
                # Crear el botón con la imagen arriba del texto y más espacio
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    image=photo,
                    compound=tk.TOP,  # Colocar la imagen arriba del texto
                    bg="#0056B3",
                    fg="white",
                    font=("Sora SemiBold", 16, "bold"),  # Fuente más grande
                    width=200,  # Ajustar el ancho del botón
                    height=150,  # Ajustar la altura del botón para acomodar la imagen y el texto
                    relief="flat",
                    command=lambda t=text: self.abrir_ventana_dni(t),
                    padx=10,  # Espacio horizontal interno
                    pady=10,  # Espacio vertical interno
                )
                btn.image = photo  # Guardar una referencia para evitar que la imagen sea eliminada por el recolector de basura
                btn.grid(row=idx // 3, column=idx % 3, padx=20, pady=20, sticky="nsew")  # Organizar en una cuadrícula de 3 columnas
                # Efecto hover
                btn.bind("<Enter>", lambda event, button=btn: button.config(bg="#5996d9"))  # Cambio de color cuando el cursor entra
                btn.bind("<Leave>", lambda event, button=btn: button.config(bg="#0056B3"))  # Vuelve a color original al salir
            except Exception as e:
                print(f"Error al cargar la imagen para {text}: {e}")

        # Ajustar el peso de las filas y columnas para que los botones se expandan correctamente
        for i in range(2):  # 2 filas
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(3):  # 3 columnas
            buttons_frame.grid_columnconfigure(j, weight=1)

        # Marco derecho para la imagen adicional (Walter_S)
        right_frame = tk.Frame(main_frame, bg="#FFFFFF")
        right_frame.pack(side="right", fill="both", expand= True, padx=0, pady=0)

        # Función para ajustar la imagen adicional de Walter_S
        self.ajustar_imagen_walter(right_frame)

    def ajustar_imagen_walter(self, right_frame):
        try:
            image_path =  r"C:\Users\Max\Desktop\Sistema_muni_g2-main\assets\plaza.png"
            additional_image = Image.open(image_path)

            # Obtener la altura y ancho total de la ventana
            ventana_height = self.root.winfo_screenheight()  # Altura de la pantalla
            #ventana_width = self.root.winfo_screenwidth()  # Ancho total de la ventana

            # Nueva altura para la imagen (altura de la ventana)
            aspect_ratio = additional_image.width / additional_image.height
            new_width = int(ventana_height * aspect_ratio)  # Mantener la proporción de la imagen

            # Redimensionar la imagen con la nueva altura
            additional_image = additional_image.resize((new_width, ventana_height), Image.Resampling.LANCZOS)

            # Obtener la altura y el ancho escalado de la imagen
            #image_width = additional_image.width

            # Cargar la imagen escalada
            self.additional_image = ImageTk.PhotoImage(additional_image)
            image_label = tk.Label(right_frame, image=self.additional_image, bg="#FFFFFF")
            image_label.pack(fill="both", expand=True, padx=0, pady=0)
            
        except Exception as e:
            print(f"Error al cargar la imagen adicional: {e}")
    
 


    def abrir_ventana_dni(self, motivo):
        """Abre una nueva ventana para ingresar el DNI."""
        self.top = Toplevel(self.root)
        self.top.title("Ingresar DNI")
        self.top.geometry("600x500")
        self.top.configure(bg="#FFFFFF")

        # Establecer el ícono de la ventana emergente
        icon_path = r"C:\Users\Max\Desktop\Sistema_muni_g2-main\assets\logo.ico"
        try:
            self.top.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error al cargar el ícono en la ventana emergente: {e}")

        # Mostrar el motivo
        tk.Label(self.top, text=f"Motivo: {motivo}", font=("Sora SemiBold", 16), bg="#FFFFFF").pack(pady=10)

        # Cargar y mostrar el logo entre los textos
        try:
            logo_path = r"C:\Users\Max\Desktop\Sistema_muni_g2-main\assets\logo.png"
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((120, 150), Image.Resampling.LANCZOS)
            self.logo_popup = ImageTk.PhotoImage(logo_image)

            logo_label = tk.Label(self.top, image=self.logo_popup, bg="#FFFFFF")
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error al cargar el logo: {e}")

        tk.Label(self.top, text="Ingrese DNI o RUC:", font=("Sora Light", 14), bg="#FFFFFF").pack(pady=5)
        self.dni_ruc_entry = tk.Entry(self.top, font=("Sora Light", 14))
        self.dni_ruc_entry.pack(pady=10)
        self.dni_ruc_entry.insert(0, "Ingrese DNI o RUC")
        self.dni_ruc_entry.bind("<FocusIn>", self.borrar_texto_dni)
        self.dni_ruc_entry.bind("<FocusOut>", self.reemplazar_texto_dni)

        # Botón para generar turno, pasando el motivo
        # Aquí está el cambio principal: obtenemos solo el prefijo de la tupla
        prefijo = self.motivo_info[motivo][0]  # Tomamos solo el primer elemento (el prefijo)
        tk.Button(
            self.top,
            text="Generar Turno",
            bg="#0056B3",
            fg="white",
            font=("Arial", 14),
            command=lambda: self.generar_turno(motivo, prefijo),
        ).pack(pady=20)


    def borrar_texto_dni(self, event):
        if self.dni_ruc_entry.get() == "Ingrese DNI o RUC":
            self.dni_ruc_entry.delete(0, tk.END)

    def reemplazar_texto_dni(self, event):
        if self.dni_ruc_entry.get() == "":
            self.dni_ruc_entry.insert(0, "Ingrese DNI o RUC")

    def generar_turno(self, motivo, prefijo):
        dni_ruc = self.dni_ruc_entry.get()
        #motivo = self.motivo_var.get()

        # Verificar que el DNI sea válido
        if len(dni_ruc) != 8 and len(dni_ruc) != 11:  # Consideramos también RUC de 11 dígitos
            messagebox.showerror("Error", "DNI o RUC inválido")
            return
        
        # Verificar si el motivo seleccionado es válido
        if motivo not in self.motivo_info:
            messagebox.showerror("Error", "Motivo no válido")
            return

        # Obtener prefijo y prioridad directamente desde el diccionario
        #prefijo, prioridad = motivo_info[motivo]
        motivo = motivo.capitalize() #Para que la bd reciba los motivos con minusculas

        hora_actual = datetime.now().strftime("%H:%M:%S")  # Hora actual en formato HH:MM:SS

        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()

            
                # Determinar si es un DNI o un RUC según la longitud del dni_ruc
                if len(dni_ruc) == 8:
                    # Si el valor tiene 8 dígitos, buscar en registros_dni
                    cursor.execute("""
                        SELECT dni, nombres FROM registros_dni WHERE dni = ?
                    """, (dni_ruc,))
                    result_dni = cursor.fetchone()

                    if result_dni:
                        nombre = result_dni[1]
                        detalle = f"{nombre}"
                    else:
                        # Si no se encuentra en registros_dni, mandar a registrar
                        self.registrar_usuario(dni_ruc)
                        return  # Detener el flujo si no se encuentra

                elif len(dni_ruc) == 11:
                    # Si el valor tiene 11 dígitos, buscar en registros_ruc
                    cursor.execute("""
                        SELECT ruc, empresa FROM registros_ruc WHERE ruc = ?
                    """, (dni_ruc,))
                    result_ruc = cursor.fetchone()

                    if result_ruc:
                        empresa = result_ruc[1]
                        detalle = f"Empresa: {empresa}"
                    else:
                        # Si no se encuentra en registros_ruc, mandar a registrar
                        self.registrar_usuario(dni_ruc)
                        return  # Detener el flujo si no se encuentra

                else:
                    # Si el DNI/RUC no tiene ni 8 ni 11 dígitos, mostrar un error
                    messagebox.showerror("Error", "DNI/RUC inválido.")
                    
                # Obtener el siguiente número de turno
                numero_turno = self.obtener_siguiente_numero(cursor, prefijo)
                


                # Insertar los datos del turno en la base de datos (con OUTPUT para obtener el numero_turno)
                # Crear una tabla temporal para capturar el valor del OUTPUT
                cursor.execute("""
                     INSERT INTO turnos (dni_ruc, numero_turno, estado, fecha_hora, motivo) 
                     VALUES (?, ?, 'espera', CURRENT_TIMESTAMP, ?);
                 """, (dni_ruc, numero_turno, motivo))
                

                # Ahora, consulta el número de turno que fue generado
                cursor.execute("""
                    SELECT TOP 1 numero_turno FROM turnos 
                    WHERE dni_ruc = ? 
                    AND CONVERT(VARCHAR(MAX), motivo) = ?
                    ORDER BY id DESC;
                """, (dni_ruc, motivo))


                turno = cursor.fetchone()
                if turno:
                    turno = turno[0]
                    connection.commit()  # Confirmar la transacción
                    print(f"Turno generado: {turno}")
                else:
                    print("No se pudo obtener el número de turno")


                print(f"Turno generado exitosamente: {turno}")

                # Mostrar mensaje con los detalles del turno
                mensaje = (
                    f"----------------------------------------------\n"
                    f"Municipalidad de Nuevo Chimbote\n"
                    f"----------------------------------------------\n"
                    f"Hora: {hora_actual}\n"
                    f"Bienvenido\n"
                    f"{detalle}\n"  # Muestra el nombre o la empresa
                    f"{turno}\n"
                    f"Motivo: {motivo}\n"
                    f"DNI/RUC: {dni_ruc}\n"
                    f"----------------------------------------------\n"
                    f"Por favor espere su turno.\n"
                    f"Gracias por su paciencia.\n"
                )    
                messagebox.showinfo("Turno Generado", mensaje)
                # Aquí puedes llamar a la función de impresión
                self.imprimir_turno(turno, motivo, detalle, dni_ruc, hora_actual)

                # Limpiar el campo de DNI
                self.dni_ruc_entry.delete(0, tk.END)
                self.dni_ruc_entry.insert(0, "Ingrese su DNI o RUC")

            except Exception as e:
                connection.rollback()
                print(f"Error al generar turno: {e}")  # Imprimir el error en consola para depuración
                messagebox.showerror("Error", f"Error al generar turno: {e}")
            finally:
                cursor.close()
                connection.close()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")

    ###################################


    def abrir_ventana_motivo_especifico(self, motivo):
        """Abre una nueva ventana para seleccionar el motivo específico."""
        self.top_motivo = Toplevel(self.root)
        self.top_motivo.title("Seleccionar Motivo Específico")
        self.top_motivo.geometry("600x500")
        self.top_motivo.configure(bg="#FFFFFF")

        # Título
        tk.Label(self.top_motivo, text=f"Motivo General: {motivo}", font=("Sora SemiBold", 16), bg="#FFFFFF").pack(pady=10)

        # Opciones de motivo específico
        opciones = [
            "Opción 1", "Opción 2", "Opción 3", 
            "Opción 4", "Opción 5", "Opción 6"
        ]
        
        # Crear botones para cada opción
        for idx, opcion in enumerate(opciones):
            btn = tk.Button(
                self.top_motivo,
                text=opcion,
                bg="#0056B3",
                fg="white",
                font=("Sora SemiBold", 14, "bold"),
                width=27,
                height=2,
                relief="flat",
                command=lambda o=opcion: self.abrir_ventana_dni(motivo, o),
            )
            btn.pack(pady=10)






    #################33333333333333333333333



    def registrar_usuario(self, dni):
        """Esta función será llamada cuando el DNI o RUC no se encuentre en la base de datos y el usuario deba registrarse."""
        self.top_registro = Toplevel(self.root)
        self.top_registro.title("Registrar Usuario")
        self.top_registro.geometry("600x500")
        self.top_registro.configure(bg="#FFFFFF")

        self.top_registro.iconbitmap(r"C:\Users\Max\Desktop\Sistema_muni_g2-main\assets\logo.ico")
        # Título
        tk.Label(self.top_registro, text="Registro de Usuario", font=("Sora SemiBold", 16), bg="#FFFFFF").pack(pady=10)

        # Opción para elegir DNI o RUC
        self.tipo_id_var = tk.StringVar(value="dni")

        tk.Radiobutton(self.top_registro, text="DNI", variable=self.tipo_id_var, value="dni", font=("Sora Light", 14), bg="#FFFFFF").pack(pady=10)
        tk.Radiobutton(self.top_registro, text="RUC", variable=self.tipo_id_var, value="ruc", font=("Sora Light", 14), bg="#FFFFFF").pack(pady=10)

        # Botón para proceder al formulario dependiendo de la elección
        tk.Button(
            self.top_registro,
            text="Siguiente",
            bg="#0056B3",
            fg="white",
            font=("Arial", 14),
            command=self.mostrar_formulario_registro
        ).pack(pady=20)
        

    def mostrar_formulario_registro(self):
        """Muestra el formulario de acuerdo al tipo de documento (DNI o RUC)."""
        tipo_id = self.tipo_id_var.get()

        # Limpiar la ventana de registro
        for widget in self.top_registro.winfo_children():
            widget.destroy()

        # Título
        tk.Label(self.top_registro, text="Registro de Usuario", font=("Sora SemiBold", 16), bg="#FFFFFF").pack(pady=10)

        if tipo_id == "dni":
            # Campos para ingresar dni, apellidos y nombres
            tk.Label(self.top_registro, text="Ingrese su DNI:", font=("Sora Light", 14), bg="#FFFFFF").pack(pady=5)
            self.dni_entry = tk.Entry(self.top_registro, font=("Sora Light", 14))
            self.dni_entry.pack(pady=10)

            tk.Label(self.top_registro, text="Ingrese sus apellidos:", font=("Sora Light", 14), bg="#FFFFFF").pack(pady=5)
            self.apellido_entry = tk.Entry(self.top_registro, font=("Sora Light", 14))
            self.apellido_entry.pack(pady=10)

            tk.Label(self.top_registro, text="Ingrese sus nombres:", font=("Sora Light", 14), bg="#FFFFFF").pack(pady=5)
            self.nombre_entry = tk.Entry(self.top_registro, font=("Sora Light", 14))
            self.nombre_entry.pack(pady=10)

        elif tipo_id == "ruc":
            # Campo para ingresar el ruc y nombre de la empresa
            tk.Label(self.top_registro, text="Ingrese su RUC:", font=("Sora Light", 14), bg="#FFFFFF").pack(pady=5)
            self.ruc_entry = tk.Entry(self.top_registro, font=("Sora Light", 14))
            self.ruc_entry.pack(pady=10)

            tk.Label(self.top_registro, text="Ingrese el nombre de su empresa:", font=("Sora Light", 14), bg="#FFFFFF").pack(pady=5)
            self.empresa_entry = tk.Entry(self.top_registro, font=("Sora Light", 14))
            self.empresa_entry.pack(pady=10)

        # Botón para registrar
        tk.Button(
            self.top_registro,
            text="Registrar",
            bg="#0056B3",
            fg="white",
            font=("Arial", 14),
            #command=lambda: self.guardar_registro_usuario(self.dni_ruc_entry.get())
            command=self.guardar_registro_usuario
        ).pack(pady=20)


    def guardar_registro_usuario(self):
        """Guardar el nuevo registro en la base de datos."""
        tipo_id = self.tipo_id_var.get()
        
        if tipo_id == "dni":
            dni = self.dni_entry.get().strip()  # Eliminar espacios en blanco
            apellido = self.apellido_entry.get().strip()
            nombre = self.nombre_entry.get().strip()
            nombres_completos = f"{apellido} {nombre}"  # Concatenar apellido y nombre para el DNI

            # Validar que el DNI tenga 8 dígitos
            if len(dni) != 8 or not dni.isdigit():
                messagebox.showwarning("Advertencia", "¡Ups! Al parecer ingresó un número de RUC en el apartado de DNI. Por favor, registre su número de DNI (8 dígitos) nuevamente.")
                self.top_registro.destroy()  # Cerrar la ventana de registro
                if hasattr(self, 'top'):
                    self.top.destroy()  # Cerrar la ventana de ingreso de DNI/RUC
                return

            # Validar que el campo de apellidos y nombres no esté vacío
            if not apellido or not nombre:
                messagebox.showerror("Error", "Por favor ingrese los apellidos y nombres.")
                return

            tabla = "registros_dni"
            columna_id = "dni"
            columna_nombres = "nombres"

        elif tipo_id == "ruc":
            ruc = self.ruc_entry.get().strip()
            empresa = self.empresa_entry.get().strip()

            # Validar que el RUC tenga 11 dígitos
            if len(ruc) != 11 or not ruc.isdigit():
                messagebox.showwarning("Advertencia", "¡Ups! Al parecer ingresó un número de DNI en el apartado de RUC. Por favor, registre su número de RUC (11 dígitos) nuevamente.")
                self.top_registro.destroy()  # Cerrar la ventana de registro
                if hasattr(self, 'top'):
                    self.top.destroy()  # Cerrar la ventana de ingreso de DNI/RUC
                return

            # Validar que el campo de empresa no esté vacío
            if not empresa:
                messagebox.showerror("Error", "Por favor ingrese el nombre de la empresa.")
                return

            tabla = "registros_ruc"
            columna_id = "ruc"
            columna_nombres = "empresa"

        # Realizar la inserción en la base de datos
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()

                # Verificar si ya existe el DNI o RUC en la base de datos
                if tipo_id == "dni":
                    cursor.execute(f"SELECT {columna_id} FROM {tabla} WHERE {columna_id} = ?", (dni,))
                elif tipo_id == "ruc":
                    cursor.execute(f"SELECT {columna_id} FROM {tabla} WHERE {columna_id} = ?", (ruc,))

                result = cursor.fetchone()

                if result:
                    # Si ya existe el DNI o RUC, mostrar un mensaje de error
                    messagebox.showerror("Error", f"El {columna_id.upper()} ya está registrado.")
                    return

                if tipo_id == "dni":
                    # Insertar en la tabla de registros_dni
                    cursor.execute(f"""
                        INSERT INTO registros_dni (dni, nombres)
                        VALUES (?, ?)
                    """, (dni, nombres_completos))

                elif tipo_id == "ruc":
                    # Insertar en la tabla de registros_ruc
                    cursor.execute(f"""
                        INSERT INTO registros_ruc (ruc, empresa)
                        VALUES (?, ?)
                    """, (ruc, empresa))

                connection.commit()

                messagebox.showinfo("Registro Exitoso", "¡Su registro fue exitoso!")
                self.top_registro.destroy()  # Cerrar la ventana de registro
                if hasattr(self, 'top'):
                    self.top.destroy()  # Cerrar la ventana de ingreso de DNI/RUC

            except Exception as e:
                connection.rollback()
                print(f"Error al registrar usuario: {e}")
                messagebox.showerror("Error", f"Error al registrar usuario: {e}")
            finally:
                cursor.close()
                connection.close()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")

    

################################################################################################################################################


    

    def imprimir_turno(self, turno, motivo, detalle, dni_ruc, hora_actual):
        """Función para generar un ticket de turno en PDF con imagen de fondo."""

        # Ruta para guardar el PDF
        pdf_path = r"C:\Users\Max\Desktop\ticket_turno.pdf"

        # Crear PDF
        c = canvas.Canvas(pdf_path, pagesize=A4)
        ancho_hoja, alto_hoja = A4  # Dimensiones de la página

        # Cargar la imagen de fondo
        logo_path = r"C:\Users\Max\Desktop\Sistema_muni_g2-main\assets\logobn.png"
        try:
            img = Image.open(logo_path)
            img_width, img_height = img.size

            # Redimensionar imagen para que ocupe toda la página
            ratio = ancho_hoja / img_width
            new_height = img_height * ratio
            c.drawImage(logo_path, 0, alto_hoja - new_height, width=ancho_hoja, height=new_height)
        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")

        # Configuración de fuentes
        x_centro = ancho_hoja / 2

        # Posiciones iniciales
        y_inicio = 720  # Ajuste vertical para comenzar    ################# 650
        espacio_entre_lineas = 40  # Espaciado entre líneas

        # Texto "N° de Turno:" en la parte superior
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(x_centro, y_inicio, "N° de Turno:")
        y_inicio -= 150                                      ################ 50

        # Número de Turno grande y llamativo
        c.setFont("Helvetica-Bold", 120)
        c.drawCentredString(x_centro, y_inicio, turno)
        y_inicio -= espacio_entre_lineas + 30

        # DNI
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(x_centro, y_inicio, f"DNI: {dni_ruc}")
        y_inicio -= espacio_entre_lineas

        # Motivo
        c.drawCentredString(x_centro, y_inicio, f"Motivo: {motivo}")
        y_inicio -= espacio_entre_lineas

        # Línea separadora
        c.setLineWidth(2)
        c.line(100, y_inicio, ancho_hoja - 100, y_inicio)
        y_inicio -= espacio_entre_lineas

        # Fecha
        from datetime import datetime
        fecha_actual = datetime.today().strftime('%d-%m-%Y')
        c.drawCentredString(x_centro, y_inicio, f"Fecha: {fecha_actual}")
        y_inicio -= espacio_entre_lineas

        # Hora
        c.drawCentredString(x_centro, y_inicio, f"Hora: {hora_actual}")
        y_inicio -= espacio_entre_lineas

        # Segunda línea separadora
        c.line(100, y_inicio, ancho_hoja - 100, y_inicio)
        y_inicio -= espacio_entre_lineas

        # Detalle (Nombre del usuario)
        c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(x_centro, y_inicio, detalle)
        y_inicio -= espacio_entre_lineas

        # Mensaje final
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(x_centro, y_inicio, "Por favor espere su turno")
        y_inicio -= espacio_entre_lineas
        c.drawCentredString(x_centro, y_inicio, "¡¡Gracias por su paciencia!!")

        # Guardar el PDF
        c.save()

        print(f"Ticket guardado en: {pdf_path}")

        self.top.after(100, self.top.destroy)  # Espera 100ms antes de destruir la ventana
        self.top = None  # Eliminar la referencia a la ventana


#######################################################################################################################################################




    def obtener_siguiente_numero(self, cursor, prefijo):
        # Obtener la fecha actual
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        # Consultar el último turno del día actual con el prefijo dado
        cursor.execute("""
            SELECT TOP 1 numero_turno 
            FROM turnos 
            WHERE numero_turno LIKE ? 
            AND CONVERT(DATE, fecha_hora) = ?
            ORDER BY id DESC
        """, (f"{prefijo}%", fecha_actual))

        ultimo_turno = cursor.fetchone()

        if ultimo_turno:
            # Extraer el número del último turno y sumar 1
            ultimo_numero = int(ultimo_turno[0].split('-')[1])
            siguiente_numero = ultimo_numero + 1
        else:
            # Si no hay turnos para el día actual, empezar desde 1
            siguiente_numero = 1

        # Formatear el número de turno con el prefijo y ceros a la izquierda
        return f"{prefijo}-{str(siguiente_numero).zfill(4)}"


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()