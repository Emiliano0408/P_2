from src.automata import AutomataSimulador

def test_afd_aceptacion_rechazo():
    # AFD simple que acepta cadenas que terminan en '1'
    definicion = {
        "alfabeto": ["0", "1"],
        "estados": ["q0", "q1"],
        "inicial": "q0",
        "aceptacion": ["q1"],
        "transiciones": [
            {"desde": "q0", "lee": "0", "hacia": ["q0"]},
            {"desde": "q0", "lee": "1", "hacia": ["q1"]},
            {"desde": "q1", "lee": "0", "hacia": ["q0"]},
            {"desde": "q1", "lee": "1", "hacia": ["q1"]}
        ]
    }
    sim = AutomataSimulador(definicion)
    
    # Acepta cadena válida
    es_aceptada, _ = sim.validar_cadena("001")
    assert es_aceptada == True
    
    # Rechaza cadena inválida
    es_rechazada, _ = sim.validar_cadena("010")
    assert es_rechazada == False

def test_afnd_lambda_clausura():
    # AFND-lambda que requiere transiciones vacías (lambda/epsilon)
    definicion = {
        "alfabeto": ["a"],
        "estados": ["q0", "q1", "q2"],
        "inicial": "q0",
        "aceptacion": ["q2"],
        "transiciones": [
            {"desde": "q0", "lee": "", "hacia": ["q1"]},  # Transición lambda
            {"desde": "q1", "lee": "a", "hacia": ["q2"]}
        ]
    }
    sim = AutomataSimulador(definicion)
    
    # Verifica que la epsilon-clausura inicial incluya a q1
    estados_iniciales = sim.epsilon_clausura(["q0"])
    assert "q1" in estados_iniciales
    
    # Verifica que la cadena 'a' sea aceptada gracias a la clausura
    es_aceptada, _ = sim.validar_cadena("a")
    assert es_aceptada == True