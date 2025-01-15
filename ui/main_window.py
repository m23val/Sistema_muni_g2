import tkinter as tk
from tkinter import messagebox
from db.connection import get_connection
from datetime import datetime
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Turnos - Municipalidad De Nuevo Chimbote")
        self.root.geometry("500x500")
        self.root.configure(bg="#FFFFFF")

        # Cambiar el ícono de la ventana
        icon_path = r"C:\Users\Max\Desktop\SISTEMA MUNI\assets\logo.ico"  # Ruta del archivo .ico
        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error al cargar el ícono: {e}")


        # Cargar y mostrar la imagen
        try:
            image_path = r"C:\Users\Max\Desktop\SISTEMA MUNI\assets\logo.png"  # Asegúrate de usar la extensión correcta
            image = Image.open(image_path)
            image = image.resize((150, 150), Image.Resampling.LANCZOS)  # Corregido LANCZOS
            self.logo = ImageTk.PhotoImage(image)
            logo_label = tk.Label(self.root, image=self.logo, bg="#FFFFFF")
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

        # Etiqueta de bienvenida
        tk.Label(root, text="Bienvenido", font=("Arial", 20), bg="#FFD700").pack(pady=10)

        # Campo para ingresar DNI
        self.dni_entry = tk.Entry(root, font=("Arial", 14))
        self.dni_entry.pack(pady=20)
        self.dni_entry.insert(0, "Ingrese su DNI")

        # Botón para generar turno
        tk.Button(root, text="Generar Turno", bg="#008000", fg="white", font=("Arial", 14),
                  command=self.generar_turno).pack(pady=10)

    def obtener_siguiente_numero(self, cursor):
        cursor.execute("SELECT numero_turno FROM turnos ORDER BY id DESC LIMIT 1")
        ultimo_turno = cursor.fetchone()
        if ultimo_turno:
            ultimo_numero = int(ultimo_turno[0].split('-')[1])
            siguiente_numero = ultimo_numero + 1
        else:
            siguiente_numero = 1
        return f"T-{siguiente_numero:04d}"

    def generar_turno(self):
        dni = self.dni_entry.get()
        if len(dni) != 8 or not dni.isdigit():
            messagebox.showerror("Error", "DNI inválido")
            return

        area = "Trámites Generales"  # Esto podría ser dinámico según el sistema
        hora_actual = datetime.now().strftime("%H:%M:%S")  # Hora en formato HH:MM:SS

        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                numero_turno = self.obtener_siguiente_numero(cursor)
                cursor.execute("""
                    INSERT INTO turnos (dni, numero_turno, estado, fecha_hora) 
                    VALUES (%s, %s, 'espera', CURRENT_TIMESTAMP) 
                    RETURNING numero_turno
                """, (dni, numero_turno))
                turno = cursor.fetchone()[0]
                connection.commit()

                # Mostrar el mensaje con los detalles del turno
                mensaje = (
                    f"----------------------------------------------\n"
                    f"Municipalidad de Nuevo Chimbote\n"
                    f"----------------------------------------------\n"
                    f"Turno: {turno}\n"
                    f"DNI: {dni}\n"
                    f"Área: {area}\n"
                    f"Hora: {hora_actual}\n"
                    f"----------------------------------------------\n"
                    f"Por favor espere su turno.\n"
                    f"Gracias por su paciencia.\n"
                )
                messagebox.showinfo("Turno Generado", mensaje)

                self.dni_entry.delete(0, tk.END)
                self.dni_entry.insert(0, "Ingrese su DNI")
            except Exception as e:
                connection.rollback()
                messagebox.showerror("Error", f"Error al generar turno: {e}")
            finally:
                cursor.close()
                connection.close()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")

# Inicia la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
