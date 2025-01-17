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
        icon_path = r"C:\Users\Max\Desktop\Sistema_muni_g2-main\assets\logo.ico"
        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error al cargar el ícono: {e}")


        # Cargar y mostrar la imagen
        try:
            #image_path = r"C:\Users\Max\Desktop\SISTEMA MUNI\assets\logo.png"  # Asegúrate de usar la extensión correcta
            image_path = r"C:\Users\Max\Desktop\Sistema_muni_g2-main\assets\logo.png"  # Asegúrate de usar la extensión correcta
            image = Image.open(image_path)
            image = image.resize((150, 150), Image.Resampling.LANCZOS)  # Corregido LANCZOS
            self.logo = ImageTk.PhotoImage(image)
            logo_label = tk.Label(self.root, image=self.logo, bg="#FFFFFF")
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

        # Etiqueta de bienvenida
        tk.Label(root, text="Bienvenido", font=("Arial", 20), bg="#FFD700").pack(pady=10)

        #Opciones de área
        self.motivo_var=tk.StringVar()
        self.motivo_var.set("Seleccionar")
        motivo_options = ["Consultas", "Deudas", "Documentos", "Multas", "Pagos"]

        motivo_label = tk.Label(root, text="Seleccionar Motivo", font=("Arial",14), bg="#FFFFFF")
        motivo_label.pack(pady=5)

        motivo_menu = tk.OptionMenu(root, self.motivo_var, *motivo_options)
        motivo_menu.config(font=("Arial",14))
        motivo_menu.pack(pady=10)

        #Campo para ingresar DNI (después de escoger el área)
        self.dni_label = tk.Label(root, text = "Ingrese su DNI", font=("Arial", 14), bg="#FFFFFF")
        self.dni_entry = tk.Entry(root, font=("Arial", 14))
        self.dni_button = tk.Button(root, text="Generar Turno", bg="#008000", fg="white", font=("Arial", 14), command=self.generar_turno)
        self.dni_button.pack_forget()

        #Iniciar el botón y DNI pero deshabilitados
        self.dni_label.pack_forget()
        self.dni_entry.pack_forget()
        self.dni_button.pack_forget()

        #Solo cuando se seleccione el área, se muestra el campo DNI
        self.motivo_var.trace_add("write", self.mostrar_dni)
         # Establecer texto por defecto en el campo de DNI
        self.dni_entry.insert(0, "Ingrese su DNI")
        self.dni_entry.bind("<FocusIn>", self.borrar_texto_dni)
        self.dni_entry.bind("<FocusOut>", self.reemplazar_texto_dni)
#############################################################################################
    def borrar_texto_dni(self, event):
        """Borra el texto por defecto cuando el campo tiene foco."""
        if self.dni_entry.get() == "Ingrese su DNI":
            self.dni_entry.delete(0, tk.END)
#########################################################################################
    def reemplazar_texto_dni(self, event):
        """Vuelve a poner el texto por defecto si el campo está vacío."""
        if self.dni_entry.get() == "":
            self.dni_entry.insert(0, "Ingrese su DNI")
        
###############################################################################################
    def obtener_siguiente_numero(self, cursor, prefijo):
        prefijo_busqueda = f"{prefijo}%"
        cursor.execute("SELECT numero_turno FROM turnos WHERE numero_turno LIKE %s ORDER BY id DESC LIMIT 1", (prefijo_busqueda,))       

        ultimo_turno = cursor.fetchone()
        if ultimo_turno:
            ultimo_numero = int(ultimo_turno[0].split('-')[1])
            siguiente_numero = ultimo_numero + 1
        else:
            siguiente_numero = 1
        return f"{prefijo}-{siguiente_numero:04d}"
    
###############################################################################################
    def mostrar_dni(self, *args):
        motivo = self.motivo_var.get()
        if motivo != "Seleccionar":
            self.dni_label.pack(pady=10)
            self.dni_entry.pack(pady=20)
            self.dni_button.pack(pady=10)

            # Limpia el campo de DNI y muestra el texto por defecto
            self.dni_entry.delete(0, tk.END)
            self.dni_entry.insert(0, "Ingrese su DNI")  # Siempre restablece el texto por defecto
        else:
            # Se oculta el campo de DNI si no se selecciona área
            self.dni_label.pack_forget()
            self.dni_entry.pack_forget()
            self.dni_button.pack_forget()



###############################################################################################
    def generar_turno(self):
        dni = self.dni_entry.get()
        motivo = self.motivo_var.get()

        if len(dni) != 8 or not dni.isdigit():
            messagebox.showerror("Error", "DNI inválido")
            return
        # Determinar el prefijo según el área seleccionada
        if motivo == "Consultas":
            prioridad = "Muy baja"
            prefijo = "C"
        elif motivo == "Deudas":
            prioridad = "Media"
            prefijo = "S"
        elif motivo == "Documentos":
            prioridad = "Baja"
            prefijo = "D"
        elif motivo == "Multas":
            prioridad = "Muy Alta"
            prefijo = "M"
        elif motivo == "Pagos":
            prioridad = "Alta"
            prefijo = "P"
        else:
            messagebox.showerror("Error", "Motivo no válida")
            return
        
       
        #area = "Trámites Generales"  # Esto podría ser dinámico según el sistema
        hora_actual = datetime.now().strftime("%H:%M:%S")  # Hora en formato HH:MM:SS

###############################################################################################
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                numero_turno = self.obtener_siguiente_numero(cursor, prefijo)
                cursor.execute("""
                    INSERT INTO turnos (dni, numero_turno, estado, fecha_hora, prioridad, motivo) 
                    VALUES (%s, %s, 'espera', CURRENT_TIMESTAMP, %s, %s) 
                    RETURNING numero_turno
                """, (dni, numero_turno, prioridad, motivo))

                turno = cursor.fetchone()[0]
                connection.commit()

                # Mostrar el mensaje con los detalles del turno
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
