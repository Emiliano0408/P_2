class AutomataSimulador:
    def __init__(self, definicion):
        self.alfabeto = definicion.get("alfabeto", [])
        self.estados = definicion.get("estados", [])
        self.inicial = definicion.get("inicial")
        self.aceptacion = definicion.get("aceptacion", [])
        self.transiciones = definicion.get("transiciones", [])

    def epsilon_clausura(self, estados_actuales):
        """Calcula la cerradura lambda/epsilon de un conjunto de estados."""
        clausura = set(estados_actuales)
        pila = list(estados_actuales)
        while pila:
            estado = pila.pop()
            for trans in self.transiciones:
                if trans["desde"] == estado and trans["lee"] == "":
                    destinos = trans["hacia"] if isinstance(trans["hacia"], list) else [trans["hacia"]]
                    for dest in destinos:
                        if dest not in clausura:
                            clausura.add(dest)
                            pila.append(dest)
        return clausura

    def validar_cadena(self, cadena):
        """
        Decisión de diseño: Simular el no determinismo siguiendo todos los caminos 
        posibles (búsqueda en anchura) apoyado en la epsilon-clausura, en lugar de 
        convertir a AFD. Coste computacional: O(n * m) donde n es la longitud de 
        la cadena y m el número máximo de transiciones activas simultáneas.
        """
        estados_actuales = self.epsilon_clausura([self.inicial])
        traza = [list(estados_actuales)]
        
        for simbolo in cadena:
            siguientes = set()
            for estado in estados_actuales:
                for trans in self.transiciones:
                    if trans["desde"] == estado and trans["lee"] == simbolo:
                        destinos = trans["hacia"] if isinstance(trans["hacia"], list) else [trans["hacia"]]
                        siguientes.update(destinos)
            
            estados_actuales = self.epsilon_clausura(siguientes)
            traza.append(list(estados_actuales))
            
            if not estados_actuales:
                break # Caímos en estado de trampa/rechazo
                
        es_aceptada = any(est in self.aceptacion for est in estados_actuales)
        return es_aceptada, traza