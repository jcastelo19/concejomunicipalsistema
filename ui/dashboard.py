import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "solicitudes.db")

class DashboardFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=True, padx=20, pady=20)
        self.build_ui()
        
    def build_ui(self):
        # Título del Dashboard
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=X, pady=10)
        
        ttk.Label(
            header_frame, 
            text="Dashboard de Solicitudes Ciudadanas", 
            font=("Helvetica", 16, "bold")
        ).pack(side=LEFT, padx=10)
        
        # Fecha actual
        ttk.Label(
            header_frame,
            text=f"Fecha: {datetime.now().strftime('%d/%m/%Y')}",
            bootstyle="secondary"
        ).pack(side=RIGHT, padx=10)
        
        # Contenedor principal
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=BOTH, expand=True, pady=10)
        
        # Dividir en dos columnas
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))

        
        # Tarjetas de resumen (izquierda)
        self.create_summary_cards(left_frame)
        
        # Gráficos (derecha)
        self.create_charts(right_frame)
        
        # Acciones rápidas (izquierda)
        self.create_quick_actions(left_frame)
    
    def create_summary_cards(self, parent):
        # Frame para las tarjetas
        cards_frame = ttk.Frame(parent)
        cards_frame.pack(fill=X, pady=10)
        
        # Obtener estadísticas de la base de datos
        stats = self.get_statistics()
        
        # Tarjeta 1: Total de solicitudes
        card1 = ttk.Frame(cards_frame, bootstyle="light")
        card1.pack(fill=X, pady=5, ipady=10)
        
        ttk.Label(
            card1, 
            text="Total de Solicitudes", 
            font=("Helvetica", 12, "bold"),
            bootstyle="inverse-light"
        ).pack(fill=X, ipady=5)
        
        ttk.Label(
            card1, 
            text=str(stats['total']), 
            font=("Helvetica", 24),
            bootstyle="inverse-light"
        ).pack(pady=10)
        
        # Tarjeta 2: Solicitudes por tipo
        card2 = ttk.Frame(cards_frame, bootstyle="info")
        card2.pack(fill=X, pady=5, ipady=10)
        
        ttk.Label(
            card2, 
            text="Solicitudes por Tipo", 
            font=("Helvetica", 12, "bold"),
            bootstyle="inverse-info"
        ).pack(fill=X, ipady=5)
        
        tipos_frame = ttk.Frame(card2, bootstyle="info")
        tipos_frame.pack(pady=5)
        
        for tipo, count in stats['por_tipo'].items():
            tipo_frame = ttk.Frame(tipos_frame, bootstyle="info")
            tipo_frame.pack(fill=X, pady=2)
            
            ttk.Label(
                tipo_frame, 
                text=f"{tipo}:", 
                bootstyle="inverse-info"
            ).pack(side=LEFT, padx=10)
            
            ttk.Label(
                tipo_frame, 
                text=str(count), 
                bootstyle="inverse-info"
            ).pack(side=RIGHT, padx=10)
        
        # Tarjeta 3: Solicitudes recientes
        card3 = ttk.Frame(cards_frame, bootstyle="success")
        card3.pack(fill=X, pady=5, ipady=10)
        
        ttk.Label(
            card3, 
            text="Solicitudes Recientes (7 días)", 
            font=("Helvetica", 12, "bold"),
            bootstyle="inverse-success"
        ).pack(fill=X, ipady=5)
        
        ttk.Label(
            card3, 
            text=str(stats['recientes']), 
            font=("Helvetica", 24),
            bootstyle="inverse-success"
        ).pack(pady=10)
    
    def create_charts(self, parent):
        # Frame para los gráficos
        charts_frame = ttk.Frame(parent)
        charts_frame.pack(fill=BOTH, expand=True, pady=10)
        
        # Obtener datos para los gráficos
        stats = self.get_statistics()
        
        # Gráfico 1: Distribución por tipo de solicitud
        fig1 = plt.Figure(figsize=(5, 4), dpi=100)
        ax1 = fig1.add_subplot(111)
        
        tipos = list(stats['por_tipo'].keys())
        valores = list(stats['por_tipo'].values())
        
        ax1.pie(valores, labels=tipos, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Distribución por Tipo de Solicitud')
        
        canvas1 = FigureCanvasTkAgg(fig1, charts_frame)
        canvas1.get_tk_widget().pack(fill=BOTH, expand=True, pady=10)

    
    def create_quick_actions(self, parent):
        # Frame para acciones rápidas
        actions_frame = ttk.Frame(parent)
        actions_frame.pack(fill=X, pady=10)
        
        ttk.Label(
            actions_frame, 
            text="Acciones Rápidas", 
            font=("Helvetica", 12, "bold")
        ).pack(anchor=W, pady=5)
        
        buttons_frame = ttk.Frame(actions_frame)
        buttons_frame.pack(fill=X)
        
        # Botón para registrar nueva solicitud
        ttk.Button(
            buttons_frame,
            text="Nueva Solicitud",
            bootstyle="success",
            command=self.nueva_solicitud
        ).pack(side=LEFT, padx=10, pady=10)
        
        # Botón para consultar solicitudes
        ttk.Button(
            buttons_frame,
            text="Consultar Solicitudes",
            bootstyle="info",
            command=self.consultar_solicitudes
        ).pack(side=LEFT, padx=10, pady=10)
        
        # Botón para exportar datos
        ttk.Button(
            buttons_frame,
            text="Exportar Datos",
            bootstyle="warning",
            command=self.exportar_datos
        ).pack(side=LEFT, padx=10, pady=10)
        
        # Botón para actualizar dashboard
        ttk.Button(
            buttons_frame,
            text="Actualizar Dashboard",
            bootstyle="secondary",
            command=self.actualizar_dashboard
        ).pack(side=LEFT, padx=10, pady=10)
    
    def get_statistics(self):
        # Conectar a la base de datos
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Total de solicitudes
        cursor.execute("SELECT COUNT(*) FROM solicitudes")
        total = cursor.fetchone()[0]
        
        # Solicitudes por tipo
        cursor.execute("SELECT tipo, COUNT(*) FROM solicitudes GROUP BY tipo")
        por_tipo = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Solicitudes recientes (últimos 7 días)
        fecha_limite = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        cursor.execute("SELECT COUNT(*) FROM solicitudes WHERE fecha >= ?", (fecha_limite,))
        recientes = cursor.fetchone()[0]
        
        # Solicitudes por día (últimos 7 días)
        cursor.execute("""
            SELECT DATE(fecha) as dia, COUNT(*) 
            FROM solicitudes 
            WHERE fecha >= ? 
            GROUP BY dia
            ORDER BY dia
        """, (fecha_limite,))
        por_dia = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Completar días faltantes
        for i in range(7):
            fecha = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            if fecha not in por_dia:
                por_dia[fecha] = 0
        
        # Ordenar por fecha
        por_dia = dict(sorted(por_dia.items()))
        
        conn.close()
        
        return {
            'total': total,
            'por_tipo': por_tipo,
            'recientes': recientes,
            'por_dia': por_dia
        }
    
    def nueva_solicitud(self):
        # Cambiar a la pestaña de registro
        notebook = self.master.master  # Obtener el notebook desde el frame padre
        notebook.select(1)  # Seleccionar la pestaña de registro (índice 1)
    
    def consultar_solicitudes(self):
        # Cambiar a la pestaña de consulta
        notebook = self.master.master  # Obtener el notebook desde el frame padre
        notebook.select(2)  # Seleccionar la pestaña de consulta (índice 2)
    
    def exportar_datos(self):
        # Implementar funcionalidad de exportación (por ejemplo, a CSV)
        # Esta es una función básica que se puede expandir
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM solicitudes")
            datos = cursor.fetchall()
            conn.close()
            
            # Crear archivo CSV
            import csv
            from tkinter import filedialog
            
            # Solicitar ubicación para guardar
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Guardar datos como CSV"
            )
            
            if file_path:
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    # Escribir encabezados
                    writer.writerow(['ID', 'Nombre', 'Apellido', 'Cédula', 'Contacto', 'Tipo', 'Descripción', 'Fecha'])
                    # Escribir datos
                    writer.writerows(datos)
                
                ttk.Messagebox.show_info(
                    "Exportación exitosa", 
                    f"Los datos han sido exportados a {file_path}"
                )
        except Exception as e:
            ttk.Messagebox.show_error(
                "Error al exportar", 
                f"Ocurrió un error: {e}"
            )
    
    def actualizar_dashboard(self):
        # Destruir widgets actuales
        for widget in self.winfo_children():
            widget.destroy()
        
        # Reconstruir la interfaz
        self.build_ui()