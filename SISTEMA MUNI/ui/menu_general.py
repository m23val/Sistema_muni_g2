import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from ui.main_window import MainWindow
from ui.admin_panel import AdminPanel  
from ui.visualize_panel import VisualizePanel  

class MenuGeneral:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Atención al Ciudadano")
        self.root.state('zoomed')  # Pantalla completa
        self.root.configure(bg="#FFFFFF")

        #ícono de la ventana
        try:
            icon_path = r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\logo.ico"  # Archivo .ico
            self.root.iconbitmap(icon_path)  # Para archivos .ico
        except Exception as e:
            print(f"Error al cargar el ícono de la ventana: {e}")


        # Logo de la Municipalidad
        try:
            image_path = r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\logo_completo.png"
            image = Image.open(image_path).resize((380, 150), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(image)
            logo_label = tk.Label(self.root, image=self.logo, bg="#FFFFFF")
            logo_label.pack(pady=15)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

        # Título
        tk.Label(
            root, 
            text="BIENVENIDO AL SISTEMA DE ATENCIÓN AL CIUDADANO", 
            font=("Sora SemiBold", 18, "bold"), 
            bg="#FFFFFF"
            ).pack(pady=20)

        # Botones con íconos
        self.create_option_button(
            "Ciudadano", 
            "#00FF00", 
            r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\ciudadano.png", 
            self.open_ciudadano
            )
        self.create_option_button(
            "Administrador", 
            "#FFFF00", 
            r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\admin.png", 
            self.open_admin
            )
        self.create_option_button(
            "Visualizar Turnos", 
            "#00BFFF", 
            r"C:\Users\marie\OneDrive\Escritorio\SISTEMA\Sistema_muni_g2\assets\visualTurno.png", 
            self.view_turns
            )

    def create_option_button(self,  text, color, icon_path, command):
        #"""Crea un botón de opción con diseño personalizado."""
        frame = tk.Frame(self.root,  bg=color, width=250, height=300, highlightthickness=3)
        frame.pack(side=tk.LEFT, expand=True, padx=30, pady=30)

        frame.pack_propagate(False)

        try:
            icon_image = Image.open(icon_path).resize((90, 90), Image.Resampling.LANCZOS)
            icon = ImageTk.PhotoImage(icon_image)
            icon_label = tk.Label(frame, image=icon, bg=color)
            icon_label.image = icon 
            icon_label.pack(pady=(70,10))
        except Exception as e:
            print(f"Error al cargar el ícono '{text}': {e}")
            icon_label = tk.Label(frame, text="●", font=("Arial", 50), bg=color)
            icon_label.pack()
        
        button = tk.Button(
            frame, 
            text=text, 
            command=command, 
            font=("Sora SemiBold", 14), 
            bg=color,
            borderwidth=5,
            width=15)
        button.pack(side="bottom", pady=10)

##########################Abre el menu del ciudadano###########################
    def open_ciudadano(self):
        self.root.destroy()
        new_root = tk.Tk()
        MainWindow(new_root)
        new_root.mainloop()

##########################Abre el menu del administrador###########################

########################## Abre el menu del administrador ###########################
    def open_admin(self):
        self.root.destroy()
        new_root = tk.Tk()
        AdminPanel(new_root)  # Crea una instancia del panel de administrador
        new_root.mainloop()

########################## Abre el menu de los turnos ###########################
    def view_turns(self):
        self.root.destroy()
        new_root = tk.Tk()
        VisualizePanel(new_root)  # Crea una instancia del panel de visualización (corrige aquí si es necesario)
        new_root.mainloop()
######################### Para mostrar la ventana #################33
def show(self):
        """Método para mostrar la ventana del menú general."""
        self.root.deiconify()  # Muestra la ventana del menú general
        self.root.mainloop()   # Ejecuta el loop de la ventana

# Código para ejecutar el menú general
if __name__ == "__main__":
    root = tk.Tk()
    app = MenuGeneral(root)
    root.mainloop()