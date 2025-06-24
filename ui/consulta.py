import ttkbootstrap as ttk
import sqlite3
from ttkbootstrap.constants import END, BOTH, PRIMARY, SUCCESS
from ttkbootstrap import DateEntry
from tkinter import StringVar
from datetime import datetime
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "solicitudes.db")

class ConsultaFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=True, padx=20, pady=20)
        self.build_ui()

    def build_ui(self):
        self.cedula_var = StringVar()
        self.tipo_var = StringVar()
        self.desde_var = StringVar()
        self.hasta_var = StringVar()

        filtros = ttk.Frame(self)
        filtros.pack(pady=10)

        # Campo de Cédula
        ttk.Label(filtros, text="Cédula:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(filtros, textvariable=self.cedula_var, width=20).grid(row=0, column=1)

        # Tipo de solicitud
        ttk.Label(filtros, text="Tipo:").grid(row=0, column=2, padx=5)
        ttk.Combobox(filtros, textvariable=self.tipo_var, values=["Sugerencia","Consulta", "Queja", "Reclamo"], width=18).grid(row=0, column=3)

        # Fecha desde
        ttk.Label(filtros, text="Desde:").grid(row=1, column=0, padx=5, pady=5)
        self.desde_entry = DateEntry(master=filtros,dateformat="%Y-%m-%d", width=15, startdate=datetime.now())
        self.desde_entry.grid(row=1, column=1)
        self.desde_entry.entry.configure(textvariable=self.desde_var)
        
        # Fecha hasta
        ttk.Label(filtros, text="Hasta:").grid(row=1, column=2, padx=5)
        self.hasta_entry = DateEntry(master=filtros,dateformat = "%Y-%m-%d" , width=15, startdate=datetime.now())
        self.hasta_entry.grid(row=1, column=3)
        self.hasta_entry.entry.configure(textvariable=self.hasta_var)

        ttk.Button(filtros, text="Buscar", command=self.buscar, bootstyle=PRIMARY).grid(row=2, column=0, columnspan=4, pady=10)

        # Frame para botones de búsqueda
        botones_frame = ttk.Frame(filtros)
        botones_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(botones_frame, text="Buscar", command=self.buscar, bootstyle=PRIMARY).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Limpiar filtros", command=self.limpiar_filtros, bootstyle="warning").pack(side="left", padx=5)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, apellido, cedula, contacto, tipo, estado, descripcion, fecha FROM solicitudes")
        datos_iniciales = cursor.fetchall()
        conn.close()

        # Tabla de resultados
        columns = [
            {"text": "ID", "stretch": True},
            {"text": "Nombre", "stretch": True},
            {"text": "Apellido", "stretch": True},
            {"text": "Cédula", "stretch": True},
            {"text": "Contacto", "stretch": True},
            {"text": "Tipo", "stretch": True},
            {"text": "Descripción", "stretch": True},
            {"text": "Estado", "stretch": True},
            {"text": "Fecha", "stretch": True},
        ]

        self.tabla = Tableview(
            master=self,
            coldata=columns,
            rowdata=datos_iniciales,
            paginated=False,
            searchable=False,
            bootstyle=PRIMARY
        )
        self.tabla.pack(fill=BOTH, expand=True)
        ttk.Button(self, text="Editar selección", bootstyle="warning", command=self.editar_solicitud).pack(side = "left", padx = 5, pady=10)
        ttk.Button(self, text="Eliminar selección", bootstyle="warning", command=self.eliminar_solicitud).pack(side = "left", padx = 5, pady=10)
        ttk.Button(self, text="Cambiar Estado", bootstyle="info", command=self.cambiar_estado).pack(side="left", padx=5, pady=10)
        
    def cambiar_estado(self):
        seleccion = self.tabla.get_rows(selected=True)
        if not seleccion:
            Messagebox.show_error("Debes seleccionar un registro primero.", "Error")
            return

        datos = seleccion[0].values
        if not datos:
            Messagebox.show_error("No se pudo obtener la información.", "Error")
            return

        # Crear ventana emergente
        editor = ttk.Toplevel(self)
        editor.title("Cambiar Estado")
        editor.geometry("400x200")
        editor.grab_set()

        estado_var = StringVar(value=datos[7])  # El índice 7 sería para el estado

        ttk.Label(editor, text="Estado:").pack(pady=5)
        ttk.Combobox(editor, textvariable=estado_var, 
                     values=["Pendiente", "En Revisión", "Completado", "Rechazado"],width=20).pack(pady=5)

        def guardar_estado():
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE solicitudes
                    SET estado = ?
                    WHERE id = ?
                """, (estado_var.get(), datos[0]))
                conn.commit()
                conn.close()
                Messagebox.show_info("Actualizado", "El estado fue actualizado.")
                editor.destroy()
                self.buscar()  # refrescar tabla
            except Exception as e:
                Messagebox.show_error(str(e), "Error al actualizar")

        ttk.Button(editor, text="Guardar cambios", bootstyle=SUCCESS, command=guardar_estado).pack(pady=20)



    def buscar(self):
        cedula = self.cedula_var.get().strip()
        tipo = self.tipo_var.get().strip()
        desde = self.desde_var.get().strip()
        hasta = self.hasta_var.get().strip()

        query = "SELECT id, nombre, apellido, cedula, contacto, tipo, descripcion, estado, fecha FROM solicitudes WHERE 1=1"
        params = []

        if cedula:
            query += " AND cedula = ?"
            params.append(cedula)

        if tipo:
            query += " AND tipo = ?"
            params.append(tipo)

        if desde:
            query += " AND DATE(fecha) >= ?"
            params.append(desde)

        if hasta:
            query += " AND DATE(fecha) <= ?"
            params.append(hasta)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
 
        
        for item in self.tabla.get_rows(visible=False):
            self.tabla.delete_rows()

        for row in rows:
            self.tabla.insert_row(END, values=row)
            
        self.tabla.load_table_data(clear_filters=True)


    def editar_solicitud(self):
        seleccion = self.tabla.get_rows(selected=True)

        # Verificar si hay una fila seleccionada
        if not seleccion:
            Messagebox.show_error("Debes seleccionar un registro primero.", "Error")
            return

        datos = seleccion[0].values
        print(datos[0])
        if not datos:
            Messagebox.show_error("No se pudo obtener la información.", "Error")
            return

        # Crear ventana emergente
        editor = ttk.Toplevel(self)
        editor.title("Editar Solicitud")
        editor.geometry("900x600")
        editor.grab_set()

        nombre_var = StringVar(value=datos[1])
        apellido_var = StringVar(value=datos[2])
        cedula_var = StringVar(value=datos[3])
        contacto_var = StringVar(value=datos[4])
        tipo_var = StringVar(value=datos[5])
        descripcion_var = StringVar(value=datos[6])

        ttk.Label(editor, text="Nombre").pack(pady=5)
        ttk.Entry(editor, textvariable=nombre_var).pack()

        ttk.Label(editor, text="Apellido").pack(pady=5)
        ttk.Entry(editor, textvariable=apellido_var).pack()

        ttk.Label(editor, text="Cédula").pack(pady=5)
        ttk.Entry(editor, textvariable=cedula_var).pack()

        ttk.Label(editor, text="Contacto").pack(pady=5)
        ttk.Entry(editor, textvariable=contacto_var).pack()

        ttk.Label(editor, text="Tipo").pack(pady=5)
        ttk.Combobox(editor, textvariable=tipo_var, values=["Sugerencia","Consulta", "Queja", "Reclamo"]).pack()

        ttk.Label(editor, text="Descripción").pack(pady=5)
        desc_entry = ttk.Entry(editor, textvariable=descripcion_var)
        desc_entry.pack()
        desc_entry.config(width=50)
        

        def guardar_cambios():
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE solicitudes
                    SET nombre = ?, apellido = ?, contacto = ?, cedula = ?, tipo = ?, descripcion = ?
                    WHERE id = ?
                """, (
                nombre_var.get(), apellido_var.get(), cedula_var.get(), contacto_var.get(), tipo_var.get(), descripcion_var.get(),
                datos[0]
            ))
                conn.commit()
                conn.close()
                Messagebox.show_info("Actualizado", "La solicitud fue actualizada.")
                editor.destroy()
                self.buscar()  # refrescar tabla
            except Exception as e:
                Messagebox.show_error(str(e), "Error al actualizar")

        # Botón para guardar cambios    
        ttk.Button(editor, text="Guardar cambios", bootstyle=SUCCESS, command=guardar_cambios).pack(pady=20)

    def eliminar_solicitud(self):
        seleccion = self.tabla.get_rows(selected=True)

        if not seleccion:
            Messagebox.show_error("Debes seleccionar un registro primero.", "Error")
            return

        datos = seleccion[0].values
        if not datos:
            Messagebox.show_error("No se pudo obtener la información.", "Error")
            return

        respuesta = Messagebox.yesno(
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar la solicitud de {datos[1]} {datos[2]} con cédula {datos[3]}?",
            parent=self
        )

         # Si el usuario confirma, eliminar la solicitud
        if respuesta == "yes":
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM solicitudes WHERE id = ?", (datos[0],))
                conn.commit()
                conn.close()
                Messagebox.show_info("Eliminado", "La solicitud fue eliminada.")
                self.buscar()  # refrescar tabla
            except Exception as e:
                Messagebox.show_error(str(e), "Error al eliminar")
        else:
            Messagebox.show_info("Eliminación cancelada", "No se eliminó ninguna solicitud.", parent=self)

    def limpiar_filtros(self):
        # Limpiar todos los campos de filtro
        self.cedula_var.set("")
        self.tipo_var.set("")
        self.desde_var.set("")
        self.hasta_var.set("")
        
        # Cargar todos los registros de la base de datos
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, apellido, cedula, contacto, tipo, descripcion, fecha FROM solicitudes")
        rows = cursor.fetchall()
        conn.close()
        
        # Limpiar la tabla actual
        for item in self.tabla.get_rows(visible=False):
            self.tabla.delete_rows()
            
        # Insertar todos los registros
        for row in rows:
            self.tabla.insert_row(END, values=row)
            
        self.tabla.load_table_data(clear_filters=True)
        
        # Mostrar mensaje de confirmación
        Messagebox.show_info("Filtros limpiados", "Se han limpiado todos los filtros y se muestran todos los registros.")