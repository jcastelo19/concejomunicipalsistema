import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH
from ttkbootstrap.dialogs import Messagebox
from tkinter import StringVar, Text, END
import sqlite3
import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "solicitudes.db")

class RegistroFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=True, padx=20, pady=20)
        self.build_ui()

    def build_ui(self):
    # Variables
        self.nombre_var = StringVar()
        self.apellido_var = StringVar()
        self.cedula_var = StringVar()
        self.contacto_var = StringVar()
        self.tipo_var = StringVar(value="Sugerencia")  # Valor predeterminado más claro

        # Frame principal con dos columnas
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=BOTH, expand=True)
    
        # Columna izquierda
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill=BOTH, expand=True, padx=(0, 10))
    
        # Columna derecha
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side="right", fill=BOTH, expand=True, padx=(10, 0))
    
        # Widgets columna izquierda
        ttk.Label(left_frame, text="Nombre", font=("Helvetica", 10, "bold")).pack(pady=(5, 2), anchor="w")
        nombre_entry = ttk.Entry(left_frame, textvariable=self.nombre_var, width=30)
        nombre_entry.pack(fill="x", pady=(0, 10))
        nombre_entry.focus()  # Poner el foco en el primer campo

        ttk.Label(left_frame, text="Apellido", font=("Helvetica", 10, "bold")).pack(pady=(5, 2), anchor="w")
        ttk.Entry(left_frame, textvariable=self.apellido_var, width=30).pack(fill="x", pady=(0, 10))

        ttk.Label(left_frame, text="Cédula", font=("Helvetica", 10, "bold")).pack(pady=(5, 2), anchor="w")
        cedula_entry = ttk.Entry(left_frame, textvariable=self.cedula_var, width=30)
        cedula_entry.pack(fill="x", pady=(0, 10))
    
        # Tooltip para cédula
        self.cedula_tooltip = ttk.Label(left_frame, text="Formato: entre 6 y 8 dígitos", 
                                      bootstyle="secondary", font=("Helvetica", 8))
        self.cedula_tooltip.pack(anchor="w", pady=(0, 5))
    
        # Widgets columna derecha
        ttk.Label(right_frame, text="Teléfono / Correo", font=("Helvetica", 10, "bold")).pack(pady=(5, 2), anchor="w")
        ttk.Entry(right_frame, textvariable=self.contacto_var, width=30).pack(fill="x", pady=(0, 10))
    
        # Tooltip para contacto
        ttk.Label(right_frame, text="Correo o número de teléfono de 11 dígitos", 
                 bootstyle="secondary", font=("Helvetica", 8)).pack(anchor="w", pady=(0, 5))

        ttk.Label(right_frame, text="Tipo de solicitud", font=("Helvetica", 10, "bold")).pack(pady=(5, 2), anchor="w")
        tipo_combo = ttk.Combobox(right_frame, textvariable=self.tipo_var,
                     values=["Sugerencia", "Consulta", "Queja", "Reclamo"],
                     width=28)
        tipo_combo.pack(fill="x", pady=(0, 10))
        tipo_combo.current(0)  # Seleccionar el primer elemento por defecto
    
        # Frame para descripción (abajo de ambas columnas)
        desc_frame = ttk.Frame(self)
        desc_frame.pack(fill="x", expand=True, pady=(10, 0))
    
        ttk.Label(desc_frame, text="Descripción", font=("Helvetica", 10, "bold")).pack(pady=(5, 2), anchor="w")
        self.descripcion_text = Text(desc_frame, height=5, width=50)
        self.descripcion_text.pack(fill="both", expand=True)
    
        # Contador de caracteres para descripción
        self.char_count = ttk.Label(desc_frame, text="0 caracteres", bootstyle="secondary")
        self.char_count.pack(anchor="e", pady=(2, 10))
    
        # Vincular evento de cambio de texto para actualizar contador
        self.descripcion_text.bind("<KeyRelease>", self.actualizar_contador)
    
        # Frame para botones
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", pady=(10, 0))
    
        # Botones con iconos
        ttk.Button(button_frame, text="Validar Datos", bootstyle="info",
                   command=self.validar_datos).pack(side="left", padx=(0, 10))
    
        ttk.Button(button_frame, text="Registrar Solicitud", bootstyle="success",
                   command=self.registrar_solicitud).pack(side="left")
    
        ttk.Button(button_frame, text="Limpiar Formulario", bootstyle="secondary",
                   command=self.limpiar_formulario).pack(side="right")

    # Añadir estos nuevos métodos
    def actualizar_contador(self, event=None):
        texto = self.descripcion_text.get("1.0", END)
        contador = len(texto.strip())
        self.char_count.config(text=f"{contador} caracteres")
    
    # Cambiar color si es menor que el mínimo requerido
        if contador < 10:
            self.char_count.config(bootstyle="danger")
        else:
            self.char_count.config(bootstyle="success")

    def limpiar_formulario(self):
        self.nombre_var.set("")
        self.apellido_var.set("")
        self.cedula_var.set("")
        self.contacto_var.set("")
        self.tipo_var.set("Sugerencia")
        self.descripcion_text.delete("1.0", END)
        self.actualizar_contador()

    def validar_datos(self):
        nombre = self.nombre_var.get().strip()
        apellido = self.apellido_var.get().strip()
        cedula = self.cedula_var.get().strip()
        contacto = self.contacto_var.get().strip()

        errores = []
        # Validaciones

        if not nombre or not apellido or not cedula:
            Messagebox.show_error("Nombre, Apellido y Cédula son obligatorios.", "Campos requeridos")
            return False

        if not re.match(r"^\d{6,8}$", cedula):
            Messagebox.show_error("la cedula debe tener entre 6 y 8 digitos.", "Cédula inválida")
            return False

        if contacto and not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", contacto) and not re.match(r"^\d{11}$", contacto):
            Messagebox.show_error("El contacto debe ser un correo electrónico o un número de teléfono válido.", "Contacto inválido")
            return False
        
        if len(self.descripcion_text.get("1.0", END).strip()) < 10:
            Messagebox.show_error("La descripción debe tener al menos 10 caracteres.", "Descripción inválida")
            return False
        
        if errores:
            Messagebox.show_error("\n".join(errores), "Errores de validación")
            return False

        return True


    def registrar_solicitud(self):
        nombre = self.nombre_var.get()
        apellido = self.apellido_var.get()
        cedula = self.cedula_var.get()
        contacto = self.contacto_var.get()
        tipo = self.tipo_var.get()
        descripcion = self.descripcion_text.get("1.0", END).strip()

        if not self.validar_datos():
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO solicitudes (nombre, apellido, cedula, contacto, tipo, descripcion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nombre, apellido, cedula, contacto, tipo, descripcion))
            conn.commit()
            conn.close()

            Messagebox.show_info("La solicitud fue registrada correctamente.", "Exito")

            # Limpiar campos
            self.limpiar_formulario()

        except Exception as e:
            Messagebox.show_error("Error al registrar la solicitud", f"Ocurrió un error: {e}")