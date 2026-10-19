import flet as ft
from automata import AutomataSimulador
import formatos
# Importamos las operaciones de la Práctica 1
from lenguajes import prefijos, sufijos, subcadenas, cerradura_kleene, cerradura_positiva

def main(page: ft.Page):
    page.title = "Simulador de Autómatas y Lenguajes - TC"
    page.scroll = "adaptive"
    page.padding = 20

    # --- PESTAÑA 1: SIMULADOR DE AUTÓMATAS ---
    ruta_archivo = ft.Text("Ningún archivo cargado", italic=True)
    cadena_validar = ft.TextField(label="Ingresa cadena a validar")
    resultado_simulacion = ft.Text(size=16, weight="bold")
    traza_salida = ft.Text(selectable=True)
    
    # Variable global para el simulador instanciado
    simulador_actual = [None] 

    def cargar_archivo(e: ft.FilePickerResultEvent):
        if e.files:
            ruta = e.files[0].path
            ruta_archivo.value = f"Cargado: {e.files[0].name}"
            
            try:
                if ruta.endswith('.json'):
                    definicion = formatos.importar_json(ruta)
                elif ruta.endswith('.xml'):
                    definicion = formatos.importar_xml(ruta)
                elif ruta.endswith('.jff'):
                    definicion = formatos.importar_jff(ruta)
                else:
                    raise ValueError("Formato no soportado")
                
                simulador_actual[0] = AutomataSimulador(definicion)
                traza_salida.value = f"Autómata cargado con {len(definicion['estados'])} estados."
            except Exception as ex:
                traza_salida.value = f"Error al cargar: {ex}"
            page.update()

    file_picker = ft.FilePicker(on_result=cargar_archivo)
    page.overlay.append(file_picker)

    def btn_validar(e):
        if not simulador_actual[0]:
            resultado_simulacion.value = "Error: Carga un autómata primero."
            resultado_simulacion.color = "red"
            page.update()
            return
            
        es_aceptada, traza = simulador_actual[0].validar_cadena(cadena_validar.value)
        if es_aceptada:
            resultado_simulacion.value = "¡Cadena ACEPTADA!"
            resultado_simulacion.color = "green"
        else:
            resultado_simulacion.value = "Cadena RECHAZADA."
            resultado_simulacion.color = "red"
            
        traza_str = "Traza de estados (ε-clausura):\n"
        for i, paso in enumerate(traza):
            traza_str += f"Paso {i}: {paso}\n"
        traza_salida.value = traza_str
        page.update()

    tab_simulador = ft.Tab(
        text="Simulador de Autómatas",
        content=ft.Column([
            ft.Text("Importar Autómata (.jff, .json, .xml)", size=20, weight="bold"),
            ft.ElevatedButton("Seleccionar Archivo", on_click=lambda _: file_picker.pick_files()),
            ruta_archivo,
            ft.Divider(),
            cadena_validar,
            ft.ElevatedButton("Validar Cadena", on_click=btn_validar),
            resultado_simulacion,
            traza_salida
        ], spacing=15)
    )

    # --- PESTAÑA 2: OPERACIONES (PRÁCTICA 1) ---
    entrada_op = ft.TextField(label="Cadena o alfabeto (separado por comas)")
    n_max = ft.TextField(label="N (solo Kleene/Positiva)", value="3", width=150)
    salida_op = ft.Text(selectable=True)

    def ejecutar_op(operacion):
        val = entrada_op.value
        try:
            if operacion == "prefijos":
                res = prefijos(val)
            elif operacion == "sufijos":
                res = sufijos(val)
            elif operacion == "kleene":
                alf = [x.strip() for x in val.split(",") if x.strip()]
                res = cerradura_kleene(alf, int(n_max.value))
            salida_op.value = f"Resultado ({len(res)}):\n" + ", ".join(res)
        except Exception as ex:
            salida_op.value = f"Error: {ex}"
        page.update()

    tab_operaciones = ft.Tab(
        text="Operaciones de Lenguajes",
        content=ft.Column([
            ft.Text("Herramientas de la Práctica 1", size=20, weight="bold"),
            entrada_op, n_max,
            ft.Row([
                ft.ElevatedButton("Prefijos", on_click=lambda _: ejecutar_op("prefijos")),
                ft.ElevatedButton("Sufijos", on_click=lambda _: ejecutar_op("sufijos")),
                ft.ElevatedButton("C. Kleene", on_click=lambda _: ejecutar_op("kleene")),
            ]),
            salida_op
        ])
    )

    # --- AGREGAR TABS A LA PÁGINA ---
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[tab_simulador, tab_operaciones],
        expand=True
    )
    
    page.add(
        ft.Text("Práctica 2 - Acosta Rojano Gustavo Emiliano", size=24, weight="bold"),
        tabs
    )

if __name__ == "__main__":
    ft.run(main)