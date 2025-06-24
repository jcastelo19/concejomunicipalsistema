import ttkbootstrap as ttk
from ui.dashboard import DashboardFrame
from ui.registro import RegistroFrame   
from ui.consulta import ConsultaFrame

def main():
    app = ttk.Window(themename="solar")
    app.title("Sistema de Solicitudes Ciudadanas")
    app.geometry("1080x720")

    notebook = ttk.Notebook(app)
    notebook.pack(fill="both", expand=True)

    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)

    notebook.add(tab1, text="Dashboard")
    notebook.add(tab2, text="Registrar Solicitud")
    notebook.add(tab3, text="Consultar Solicitudes")

    DashboardFrame(tab1)
    RegistroFrame(tab2)
    ConsultaFrame(tab3)

    app.mainloop()

if __name__ == "__main__":
    main()