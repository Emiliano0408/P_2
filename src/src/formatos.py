import json
import xml.etree.ElementTree as ET

def importar_json(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def importar_xml(ruta):
    tree = ET.parse(ruta)
    root = tree.getroot()
    
    alfabeto = [s.text for s in root.find('alfabeto').findall('simbolo')]
    estados = []
    inicial = None
    aceptacion = []
    
    for est in root.find('estados').findall('estado'):
        nombre = est.get('nombre')
        estados.append(nombre)
        if est.get('inicial') == 'true':
            inicial = nombre
        if est.get('aceptacion') == 'true':
            aceptacion.append(nombre)
            
    transiciones = []
    for trans in root.find('transiciones').findall('transicion'):
        transiciones.append({
            "desde": trans.get('desde'),
            "lee": trans.get('lee') or "",
            "hacia": [trans.get('hacia')]
        })
        
    return {
        "alfabeto": alfabeto,
        "estados": estados,
        "inicial": inicial,
        "aceptacion": aceptacion,
        "transiciones": transiciones
    }

def importar_jff(ruta):
    tree = ET.parse(ruta)
    root = tree.getroot()
    automaton = root.find('automaton')
    
    estados = {}
    inicial = None
    aceptacion = []
    alfabeto = set()
    
    for state in automaton.findall('state'):
        s_id = state.get('id')
        s_name = state.get('name')
        estados[s_id] = s_name
        if state.find('initial') is not None:
            inicial = s_name
        if state.find('final') is not None:
            aceptacion.append(s_name)
            
    transiciones = []
    for trans in automaton.findall('transition'):
        origen = estados[trans.find('from').text]
        destino = estados[trans.find('to').text]
        read_elem = trans.find('read')
        # Manejo de lambda/epsilon que JFLAP guarda como etiqueta vacía
        lee = read_elem.text if read_elem is not None and read_elem.text is not None else ""
        if lee:
            alfabeto.add(lee)
        transiciones.append({"desde": origen, "lee": lee, "hacia": [destino]})
        
    return {
        "alfabeto": list(alfabeto),
        "estados": list(estados.values()),
        "inicial": inicial,
        "aceptacion": aceptacion,
        "transiciones": transiciones
    }