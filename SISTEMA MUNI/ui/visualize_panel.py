import tkinter as tk

from db.connection import get_connection  # Asegúrate de que esta importación sea correcta
from datetime import datetime
import locale
from PIL import Image, ImageTk

# Configuración regional
locale.setlocale(locale.LC_TIME, 'es_ES')

class VisualizePanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Pantalla de Visualización de Turnos")
        self.root.state('zoomed')  # Pantalla completa
        self.root.configure(bg="#E6E6E6")

        # Ícono de la ventana
        try:
            icon_path = r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\logo.ico"
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error al cargar el ícono de la ventana: {e}")

        # Header superior
        self.header_frame = tk.Frame(root, bg="#E0E0E0")
        self.header_frame.place(relx=0, rely=0, relwidth=0.63, relheight=0.16)

        # Logo de la Municipalidad dentro del header
        try:
            logo_path = r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\logo_completo.png"
            logo_image = Image.open(logo_path).resize((300, 100), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(self.header_frame, image=self.logo, bg="#E0E0E0")
            logo_label.place(relx=0.01, rely=0.4, anchor="w")
        except Exception as e:
            print(f"Error al cargar el logo: {e}")

        # Reloj e información de hora
        self.clock_frame = tk.Frame(self.header_frame, bg="#E0E0E0")
        self.clock_frame.place(relx=0.65, rely=0.01, relwidth=0.4, relheight=0.9)

        

        self.time_label = tk.Label(
            self.clock_frame,
            font=("Arial", 35, "bold"),
            bg="#E0E0E0",
            fg="#000000",
            anchor="w",
        )
        self.time_label.place(relx=0.2, rely=0.2, relwidth=0.7, relheight=0.3)

        self.date_label = tk.Label(
            self.clock_frame,
            font=("Arial", 18, "bold"),
            bg="#E0E0E0",
            fg="#000000",
            anchor="w",
        )
        self.date_label.place(relx=0.2, rely=0.6, relwidth=1, relheight=0.3)
        self.update_time()

        # Frame con el fondo #B9C5D7 que ocupa el espacio debajo del header
        self.background_frame = tk.Frame(root)
        self.background_frame.place(relx=0, rely=0.15, relwidth=0.63, relheight=0.85)

        # 📌 Cargar imagen de fondo para todo el frame
        try:
            bg_image = Image.open(r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\plaza.png")
            bg_image = bg_image.resize(
                (int(self.root.winfo_screenwidth() * 0.63), int(self.root.winfo_screenheight() * 0.8)),
                Image.Resampling.LANCZOS
            )
            self.bg_photo = ImageTk.PhotoImage(bg_image)

            self.bg_label = tk.Label(self.background_frame, image=self.bg_photo)
            self.bg_label.place(relwidth=1, relheight=1)
            self.bg_label.lower()
        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")


        self.turno_label = tk.Label(
            self.background_frame,
            text="TURNO",
            font=("Arial", 38, "bold"),
            bg="#0056B3",
            fg="#FFFFFF",
        )
        self.turno_label.place(relx=0.08, rely=0.05, relwidth=0.45, relheight=0.25)

        self.ventanilla_label = tk.Label(
            self.background_frame,
            text="VENTANILLA",
            font=("Arial", 38, "bold"),
            bg="#3B98FF",
            fg="white",
        )
        self.ventanilla_label.place(relx=0.52, rely=0.05, relwidth=0.38, relheight=0.25)

        self.turno_actual_label = tk.Label(
            self.background_frame,
            text="--",
            font=("Arial", 80, "bold"),
            bg="#0056B3",
            fg="white",
        )
        self.turno_actual_label.place(relx=0.08, rely=0.32, relwidth=0.45, relheight=0.4)

        self.ventanilla_actual_label = tk.Label(
            self.background_frame,
            text="-",
            font=("Arial", 80, "bold"),
            bg="#3B98FF",
            fg="white",
        )
        self.ventanilla_actual_label.place(relx=0.52, rely=0.32, relwidth=0.38, relheight=0.4)


        # Próximos turnos con bordes personalizados ################################################################################### FONDO PARA LA TABLA DE SIGUIENTES TURNOS

        self.siguientes_frame = tk.Frame(root, bg="#E4E4E4")
        self.siguientes_frame.place(relx=0.67, rely=0.02, relwidth=0.3, relheight=0.98)  # Ocupa toda la parte derecha

      

        self.siguientes_label = tk.Label(
            self.siguientes_frame,
            text="Siguiente turno",
            font=("Arial", 30, "bold"),
            bg="#0056B3",
            fg="#FFFFFF",
        )
        self.siguientes_label.pack(fill="x")

        self.siguientes_turnos_frames = []
        for i in range(4):
            turno_frame = tk.Frame(self.siguientes_frame, bg="#FFFFFF", highlightbackground="#0056B3", highlightthickness=2)
            turno_frame.pack(fill="x", expand=True, pady=2)

            turno_label = tk.Label(
                turno_frame,
                text="--",
                font=("Artifakt Element Black", 35),
                bg="#FFFFFF",
                fg="#000000",
                justify="center",
            )
            turno_label.pack(pady=8)

            # Crear borde verde grueso al final del cuadro
            borde_inferior = tk.Frame(turno_frame, bg="#0056B3", height=50)
            borde_inferior.pack(fill="x", side="bottom")

            # Etiqueta para el estado (encima del borde verde grueso)
            estado_label = tk.Label(
                turno_frame,
                text="--",  # Texto inicial vacío, se actualizará dinámicamente
                font=("Artifakt Element Black", 14, "italic"),
                bg="#0056B3",
                justify="center",
                wraplength=480,
                fg="#FFFFFF"  # Color a juego con el borde
            )
            estado_label.place(relx=0.5, rely=0.85, anchor="center")  # Posicionado encima del borde      


            #self.siguientes_turnos_frames.append(turno_label)
            # Guardar referencias para actualizar más adelante
            self.siguientes_turnos_frames.append({
                "turno_label": turno_label,
                "estado_label": estado_label
            })

        # Footer con nombre
        self.footer_frame = tk.Frame(root, bg="#0056B3")
        self.footer_frame.place(relx=0.05, rely=0.78, relwidth=0.517, relheight=0.2)
        # el 0.73 es para el espaciado

        self.nombre_label = tk.Label(
            self.footer_frame,
            text="--",
            font=("Arial", 30, "bold"), #25 por si los nombres son muy largos      30 para los nombres con longitud normal 
            bg="#0056B3",  ##0056B3
            fg="white",
            anchor="center",
            justify="center",
            wraplength=500
        )
        self.nombre_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Actualizar datos
        self.cargar_turnos()
        #self.root.after(5000, self.cargar_turnos)

    def update_time(self):
        """Actualiza la hora y fecha."""
        now = datetime.now()
        hora = now.strftime("%I:%M %p")  # Hora en formato 12 horas con AM/PM
        fecha = now.strftime("%A %d de %B")
        self.time_label.config(text=hora)
        self.date_label.config(text=fecha.capitalize())
        self.root.after(1000, self.update_time)
        #cursor.execute("SELECT numero_turno, ventanilla FROM turnos WHERE estado = 'espera' LIMIT 1")
                

    def cargar_turnos(self):
        """Carga turnos desde la base de datos."""
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                # Consulta para turno actual
                cursor.execute("""
                    SELECT TOP 1 numero_turno, ventanilla, nombres_empresa 
                    FROM turnos 
                    WHERE estado = 'atendiendo' 
                    AND CONVERT(DATE, fecha_hora) = CONVERT(DATE, GETDATE())
                    ORDER BY hora_atencion DESC
                """)
                turno_actual = cursor.fetchone()

                # Consulta para próximos turnos
                cursor.execute("""
                    SELECT TOP 4 numero_turno, nombres_empresa 
                    FROM turnos 
                    WHERE estado = 'espera' 
                    AND CONVERT(DATE, fecha_hora) = CONVERT(DATE, GETDATE())     
                    ORDER BY id ASC
                """)
                siguientes = cursor.fetchall()

                # Actualizar turno actual
                if turno_actual:
                    self.turno_actual_label.config(text=turno_actual[0])  # Número de turno actual
                    self.ventanilla_actual_label.config(text=turno_actual[1])  # Ventanilla actual
                    # Actualizar el estado en el footer (correspondiente al turno actual)
                    self.nombre_label.config(text=turno_actual[2])  # Estado del turno actual
                else:
                    self.turno_actual_label.config(text="--")
                    self.ventanilla_actual_label.config(text="--")
                    self.nombre_label.config(text="--")  # Sin turno actual

                # Actualizar próximos turnos
                for idx, turno in enumerate(siguientes):
                    # turno[0] -> Número del turno, turno[1] -> Estado del turno
                    self.siguientes_turnos_frames[idx]["turno_label"].config(
                        text=turno[0]  # Número del turno
                    )
                    self.siguientes_turnos_frames[idx]["estado_label"].config(
                        text=turno[1].upper()  # Estado del turno
                    )

                # Limpia los cuadros sobrantes si hay menos de 4 turnos
                for idx in range(len(siguientes), 4):
                    self.siguientes_turnos_frames[idx]["turno_label"].config(text="--")
                    self.siguientes_turnos_frames[idx]["estado_label"].config(text="--")
                
            except Exception as e:
                print(f"Error al cargar turnos: {e}")
            finally:
                cursor.close()
                connection.close()
        self.root.after(5000, self.cargar_turnos)


# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = VisualizePanel(root)
    root.mainloop()
