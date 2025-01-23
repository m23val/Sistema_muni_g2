import tkinter as tk
from tkinter import messagebox, Toplevel
from db.connection import get_connection
from datetime import datetime
from PIL import Image, ImageTk


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Turnos - Municipalidad De Nuevo Chimbote")
        self.root.state("zoomed")
        self.root.configure(bg="#FFFFFF")

        # Cambiar el ícono de la ventana
        icon_path = r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\logo.ico"
        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error al cargar el ícono: {e}")

        # Franja superior
        top_bar = tk.Frame(root, bg="#33669B")
        top_bar.pack(side="top", anchor="w")

        # Marco principal
        main_frame = tk.Frame(root, bg="#FFFFFF")
        main_frame.place(relx=0, rely=0.05, relwidth=1, relheight=0.9)

        # Marco izquierdo para el logo, título y botones
        left_frame = tk.Frame(main_frame, bg="#FFFFFF")
        left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Título
        tk.Label(left_frame, text="GESTIÓN DE ###", font=("Arial", 18), bg="#FFFFFF").pack(pady=10)

        # Logo
        try:
            logo_path = r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\logo.png"
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((120, 150), Image.Resampling.LANCZOS)
            self.logo_main = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(left_frame, image=self.logo_main, bg="#FFFFFF")
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error al cargar la imagen del logo: {e}")

        # Título
        tk.Label(left_frame, text="Seleccionar motivo:", font=("Arial", 18), bg="#FFFFFF").pack(pady=10)

        # Botones de opciones
        buttons_frame = tk.Frame(left_frame, bg="#FFFFFF")
        buttons_frame.pack(pady=20)

        self.motivo_info = {
            "CONSULTAS": ("C", "Muy baja"),
            "DEUDAS": ("S", "Media"),
            "DOCUMENTOS": ("D", "Baja"),
            "MULTAS": ("M", "Muy Alta"),
            "PAGOS": ("P", "Alta"),
            "OTROS": ("O", "Baja")  
        }

        # Declaramos una variable para almacenar el motivo seleccionado
        self.motivo_var = tk.StringVar()  # Esta será usada para almacenar el motivo seleccionado
        

        
        #for idx, (text, _) in enumerate(motivo):
        for idx, (text, (prefijo, prioridad)) in enumerate(self.motivo_info.items()):
            btn = tk.Button(
                buttons_frame,
                text=text,
                bg="#008000",
                fg="white",
                font=("Arial", 16),
                width=28,
                height=3,
                command=lambda t=text: self.abrir_ventana_dni(t),
            )
            btn.grid(row=idx // 2, column=idx % 2, padx=20, pady=20)

        # Marco derecho para la imagen adicional (Walter_S)
        right_frame = tk.Frame(main_frame, bg="#FFFFFF")
        right_frame.pack(side="right", fill="y", expand=False, padx=0, pady=0)

        # Función para ajustar la imagen adicional de Walter_S
        self.ajustar_imagen_walter(right_frame)

    def ajustar_imagen_walter(self, right_frame):
        try:
            image_path = r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\Walter_S.png"
            additional_image = Image.open(image_path)

            # Obtener la altura y ancho total de la ventana
            ventana_height = self.root.winfo_screenheight()  # Altura de la pantalla
            ventana_width = self.root.winfo_screenwidth()  # Ancho total de la ventana

            # Nueva altura para la imagen (altura de la ventana)
            aspect_ratio = additional_image.width / additional_image.height
            new_width = int(ventana_height * aspect_ratio)  # Mantener la proporción de la imagen

            # Redimensionar la imagen con la nueva altura
            additional_image = additional_image.resize((new_width, ventana_height), Image.Resampling.LANCZOS)

            # Obtener la altura y el ancho escalado de la imagen
            image_width = additional_image.width

            # Cargar la imagen escalada
            self.additional_image = ImageTk.PhotoImage(additional_image)
            image_label = tk.Label(right_frame, image=self.additional_image, bg="#FFFFFF")
            image_label.pack(fill="both", expand=True, padx=0, pady=0)

        except Exception as e:
            print(f"Error al cargar la imagen adicional: {e}")

        # Establecer el ancho de la franja superior e inferior
        ventana_width = self.root.winfo_screenwidth()  # Ancho total de la ventana
        top_bar_width = ventana_width - image_width
        top_bar = tk.Frame(self.root, bg="#33669B", height=25, width=top_bar_width)
        top_bar.pack(side="top", anchor="w")

        bottom_bar = tk.Frame(self.root, bg="#33669B", height=25, width=top_bar_width)
        bottom_bar.pack(side="bottom", anchor="w")

    def abrir_ventana_dni(self, motivo):
        """Abre una nueva ventana para ingresar el DNI."""
        self.top = Toplevel(self.root)
        self.top.title("Ingresar DNI")
        self.top.geometry("500x400")
        self.top.configure(bg="#FFFFFF")

         # Establecer el ícono de la ventana emergente
        icon_path = r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\logo.ico"
        try:
            self.top.iconbitmap(icon_path)  # Establece el ícono para la ventana emergente
        except Exception as e:
            print(f"Error al cargar el ícono en la ventana emergente: {e}")

        

        # Mostrar el motivo
        tk.Label(self.top, text=f"Motivo: {motivo}", font=("Arial", 16), bg="#FFFFFF").pack(pady=10)

        # Cargar y mostrar el logo entre los textos
        try:
            logo_path = r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\logo.png"
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((120, 150), Image.Resampling.LANCZOS)
            self.logo_popup = ImageTk.PhotoImage(logo_image)

            logo_label = tk.Label(self.top, image=self.logo_popup, bg="#FFFFFF")
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error al cargar el logo: {e}")

        tk.Label(self.top, text="Ingrese su DNI:", font=("Arial", 14), bg="#FFFFFF").pack(pady=5)
        self.dni_entry = tk.Entry(self.top, font=("Arial", 14))
        self.dni_entry.pack(pady=10)
        self.dni_entry.insert(0, "Ingrese su DNI")
        self.dni_entry.bind("<FocusIn>", self.borrar_texto_dni)
        self.dni_entry.bind("<FocusOut>", self.reemplazar_texto_dni)

        # Botón para generar turno, pasando el motivo
        prefijo, prioridad = self.motivo_info[motivo]
        tk.Button(
            self.top,
            text="Generar Turno",
            bg="#008000",
            fg="white",
            font=("Arial", 14),
            command=lambda: self.generar_turno(motivo, prefijo, prioridad),
        ).pack(pady=20)


    def borrar_texto_dni(self, event):
        if self.dni_entry.get() == "Ingrese su DNI":
            self.dni_entry.delete(0, tk.END)

    def reemplazar_texto_dni(self, event):
        if self.dni_entry.get() == "":
            self.dni_entry.insert(0, "Ingrese su DNI")

    def generar_turno(self, motivo, prefijo, prioridad):
        dni = self.dni_entry.get()
        #motivo = self.motivo_var.get()

        # Verificar que el DNI sea válido
        if len(dni) != 8 or not dni.isdigit():
            messagebox.showerror("Error", "DNI inválido")
            return
        
        # Verificar si el motivo seleccionado es válido
        if motivo not in self.motivo_info:
            messagebox.showerror("Error", "Motivo no válido")
            return

        # Obtener prefijo y prioridad directamente desde el diccionario
        #prefijo, prioridad = motivo_info[motivo]
        motivo = motivo.capitalize() #Para que la bd reciba los motivos con minusculas

        hora_actual = datetime.now().strftime("%H:%M:%S")  # Hora actual en formato HH:MM:SS

        # Mensaje para conectar a la base de datos
        print("Conectando a la base de datos...")
        connection = get_connection()
        if connection:
            try:
                print(f"Conexión establecida, ejecutando consulta para obtener el siguiente número de turno con prefijo: {prefijo}")
                cursor = connection.cursor()
                numero_turno = self.obtener_siguiente_numero(cursor, prefijo)
                print(f"Número de turno generado: {numero_turno}")

                # Insertamos los datos del turno en la base de datos
                cursor.execute("""
                    INSERT INTO turnos (dni, numero_turno, estado, fecha_hora, prioridad, motivo) 
                    VALUES (%s, %s, 'espera', CURRENT_TIMESTAMP, %s, %s) 
                    RETURNING numero_turno
                """, (dni, numero_turno, prioridad, motivo))

                turno = cursor.fetchone()[0]
                connection.commit()

                print(f"Turno generado exitosamente: {turno}")

                # Mostrar mensaje con los detalles del turno
                mensaje = (
                    f"----------------------------------------------\n"
                    f"Municipalidad de Nuevo Chimbote\n"
                    f"----------------------------------------------\n"
                    f"Turno: {turno}\n"
                    f"Motivo: {motivo}\n"
                    f"DNI: {dni}\n"
                    f"Hora: {hora_actual}\n"
                    f"----------------------------------------------\n"
                    f"Por favor espere su turno.\n"
                    f"Gracias por su paciencia.\n"
                )
                messagebox.showinfo("Turno Generado", mensaje)

                # Limpiar el campo de DNI
                self.dni_entry.delete(0, tk.END)
                self.dni_entry.insert(0, "Ingrese su DNI")

            except Exception as e:
                connection.rollback()
                print(f"Error al generar turno: {e}")  # Imprimir el error en consola para depuración
                messagebox.showerror("Error", f"Error al generar turno: {e}")
            finally:
                cursor.close()
                connection.close()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")


    def obtener_siguiente_numero(self, cursor, prefijo):
        prefijo_busqueda = f"{prefijo}%"
        cursor.execute("SELECT numero_turno FROM turnos WHERE numero_turno LIKE %s ORDER BY id DESC LIMIT 1", (prefijo_busqueda,))       

        ultimo_turno = cursor.fetchone()
        if ultimo_turno:
            ultimo_numero = int(ultimo_turno[0].split('-')[1])
            siguiente_numero = ultimo_numero + 1
        else:
            siguiente_numero = 1  # Si no hay turnos previos, empezamos con el número 1

        return f"{prefijo}-{str(siguiente_numero).zfill(4)}"


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
