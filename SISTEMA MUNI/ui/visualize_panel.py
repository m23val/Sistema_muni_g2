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
        self.header_frame = tk.Frame(root, bg="#D9D9D9")
        self.header_frame.place(relx=0, rely=0, relwidth=0.63, relheight=0.2)

        # Logo de la Municipalidad dentro del header
        try:
            logo_path = r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\logo_completo.png"
            logo_image = Image.open(logo_path).resize((300, 100), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(self.header_frame, image=self.logo, bg="#D9D9D9")
            logo_label.place(relx=0.01, rely=0.4, anchor="w")
        except Exception as e:
            print(f"Error al cargar el logo: {e}")

        # Reloj e información de hora
        self.clock_frame = tk.Frame(self.header_frame, bg="#D9D9D9")
        self.clock_frame.place(relx=0.7, rely=0.01, relwidth=0.4, relheight=0.8)

        try:
            clock_image_path = r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\reloj.png"
            clock_image = Image.open(clock_image_path).resize((60, 60), Image.Resampling.LANCZOS)
            self.clock_icon = ImageTk.PhotoImage(clock_image)
            clock_label = tk.Label(self.clock_frame, image=self.clock_icon, bg="#D9D9D9")
            clock_label.place(relx=0.04, rely=0.5, anchor="w")
        except Exception as e:
            print(f"Error al cargar la imagen del reloj: {e}")

        self.time_label = tk.Label(
            self.clock_frame,
            font=("Arial", 30, "bold"),
            bg="#D9D9D9",
            fg="#000000",
            anchor="w",
        )
        self.time_label.place(relx=0.2, rely=0.2, relwidth=0.7, relheight=0.3)

        self.date_label = tk.Label(
            self.clock_frame,
            font=("Arial", 16, "bold"),
            bg="#D9D9D9",
            fg="#000000",
            anchor="w",
        )
        self.date_label.place(relx=0.2, rely=0.6, relwidth=1, relheight=0.3)
        self.update_time()

        # Frame con el fondo #B9C5D7 que ocupa el espacio debajo del header
        self.background_frame = tk.Frame(root, bg="#B9C5D7")
        self.background_frame.place(relx=0, rely=0.2, relwidth=0.63, relheight=0.8)  # Rellena el espacio debajo del header

        # Turno actual
        self.turno_frame = tk.Frame(root, bg="#B9C5D7")
        self.turno_frame.place(relx=0, rely=0.2, relwidth=0.63, relheight=0.6)

        self.turno_label = tk.Label(
            self.turno_frame,
            text="Turno",
            font=("Arial", 40, "bold"),
            bg="#49A11A",
            fg="#FFFFFF",
        )
        self.turno_label.place(relx=0.1, rely=0.1, relwidth=0.4, relheight=0.25)

        self.ventanilla_label = tk.Label(
            self.turno_frame,
            text="Ventanilla",
            font=("Arial", 40, "bold"),
            bg="#87CB63",
            fg="#FFFFFF",
        )
        self.ventanilla_label.place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.25)

        self.turno_actual_label = tk.Label(
            self.turno_frame,
            text="--",
            font=("Arial", 80, "bold"),
            bg="#49A11A",
            fg="#000000",
        )
        self.turno_actual_label.place(relx=0.1, rely=0.38, relwidth=0.4, relheight=0.5)

        self.ventanilla_actual_label = tk.Label(
            self.turno_frame,
            text="-",
            font=("Arial", 80, "bold"),
            bg="#87CB63",
            fg="#000000",
        )
        self.ventanilla_actual_label.place(relx=0.5, rely=0.38, relwidth=0.4, relheight=0.5)


        # Próximos turnos con bordes personalizados ################################################################################### FONDO PARA LA TABLA DE SIGUIENTES TURNOS

        #self.siguientes_background = tk.Frame(root, bg="#E4E4E4")
        #self.siguientes_background.place(relx=0.63, rely=0, relwidth=4, relheight=1)  # Ocupa toda la parte derecha

        self.siguientes_frame = tk.Frame(root, bg="#E4E4E4")
        self.siguientes_frame.place(relx=0.67, rely=0.08, relwidth=0.3, relheight=0.85)  # Ocupa toda la parte derecha

      

        self.siguientes_label = tk.Label(
            self.siguientes_frame,
            text="Siguiente turno",
            font=("Arial", 30, "bold"),
            bg="#49A11A",
            fg="#FFFFFF",
        )
        self.siguientes_label.pack(fill="x")

        self.siguientes_turnos_frames = []
        for i in range(4):
            turno_frame = tk.Frame(self.siguientes_frame, bg="#FFFFFF", highlightbackground="#49A11A", highlightthickness=2)
            turno_frame.pack(fill="x", expand=True, pady=2)

            turno_label = tk.Label(
                turno_frame,
                text="--",
                font=("Arial", 24),
                bg="#FFFFFF",
                fg="#000000",
                justify="center",
            )
            turno_label.pack(pady=10)

            # Crear borde verde grueso al final del cuadro
            borde_inferior = tk.Frame(turno_frame, bg="#49A11A", height=40)
            borde_inferior.pack(fill="x", side="bottom")

            # Etiqueta para el estado (encima del borde verde grueso)
            estado_label = tk.Label(
                turno_frame,
                text="--",  # Texto inicial vacío, se actualizará dinámicamente
                font=("Arial", 14, "italic"),
                bg="#49A11A",
                fg="#FFFFFF",  # Color a juego con el borde
            )
            estado_label.place(relx=0.5, rely=0.8, anchor="center")  # Posicionado encima del borde


            #self.siguientes_turnos_frames.append(turno_label)
            # Guardar referencias para actualizar más adelante
            self.siguientes_turnos_frames.append({
                "turno_label": turno_label,
                "estado_label": estado_label
            })

        # Footer con nombre
        self.footer_frame = tk.Frame(root, bg="#49A11A")
        self.footer_frame.place(relx=0.063, rely=0.746, relwidth=0.505, relheight=0.2)
        # el 0.73 es para el espaciado

        self.nombre_label = tk.Label(
            self.footer_frame,
            text="--",
            font=("Arial", 40, "bold"),
            bg="#49A11A",
            fg="#000000",
            anchor="center"
        )
        self.nombre_label.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.6)

        # Actualizar datos
        self.cargar_turnos()
        self.root.after(5000, self.cargar_turnos)

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
                cursor.execute("SELECT numero_turno, ventanilla, estado FROM turnos WHERE estado = 'atendiendo' LIMIT 1")
                turno_actual = cursor.fetchone()

                # Consulta para próximos turnos
                cursor.execute("SELECT numero_turno, estado FROM turnos WHERE estado = 'espera' ORDER BY id ASC LIMIT 4")
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
                        text=turno[1]  # Estado del turno
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


# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = VisualizePanel(root)
    root.mainloop()
