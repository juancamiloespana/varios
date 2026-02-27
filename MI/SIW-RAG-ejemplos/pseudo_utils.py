import keyboard
import random
import requests
import time

BASE_URL = "http://156.35.98.199:8000"

def funciona():
    expected_json = {"message": "I'm completely operational, and all my circuits are functioning perfectly."}

    status = False

    try:
        response = requests.get(BASE_URL)

        # Check status code
        if response.status_code == 200:
            status = True

        try:
            json_data = response.json()
            if json_data == expected_json:
                status = True
        except ValueError:
            pass

    except requests.RequestException as e:
        pass

    return status

def reescribir_consulta(consulta):
    """Calls /reescribir_consulta endpoint."""
    resp = requests.post(f"{BASE_URL}/reescribir_consulta", json={"consulta": consulta})
    resp.raise_for_status()
    data = resp.json()
    return data["inferred_intent"], data["query_type"], data["rewritten_query"]

def consultar_buscador(consulta, num_results=10):
    """Calls /consultar_buscador endpoint."""
    resp = requests.post(f"{BASE_URL}/consultar_buscador", json={
        "consulta": consulta,
        "num_results": num_results
    })
    resp.raise_for_status()
    return resp.json()

def fusionar_rrf(list1, list2, k=60):
    """Calls /fusionar_rrf endpoint."""
    resp = requests.post(f"{BASE_URL}/fusionar_rrf", json={
        "list1": list1,
        "list2": list2,
        "k": k
    })
    resp.raise_for_status()
    return resp.json()

def obtener_documento(short_uuid):
    """Calls /obtener_documento/<short_uuid> endpoint."""
    resp = requests.get(f"{BASE_URL}/obtener_documento/{short_uuid}")
    resp.raise_for_status()
    return resp.json()["text"]

def segmentar(documento):
    """Calls /segmentar endpoint."""
    resp = requests.post(f"{BASE_URL}/segmentar", json={"documento": documento})
    resp.raise_for_status()
    return resp.json()

def escoger_pasajes(consulta, intencion, tipo, consulta_reescrita, pasajes, num_pasajes=40):
    """Calls /escoger_pasajes endpoint."""
    payload = {
        "consulta": consulta,
        "intencion": intencion,
        "tipo": tipo,
        "consulta_reescrita": consulta_reescrita,
        "pasajes": pasajes,
        "num_pasajes": num_pasajes
    }
    resp = requests.post(f"{BASE_URL}/escoger_pasajes", json=payload)
    resp.raise_for_status()
    return resp.json()

def retrieval_augmented_generation(consulta, tipo, intencion, pasajes):
    """Calls /rag endpoint."""
    payload = {
        "consulta": consulta,
        "tipo": tipo,
        "intencion": intencion,
        "pasajes": pasajes
    }
    resp = requests.post(f"{BASE_URL}/rag", json=payload)
    resp.raise_for_status()
    return resp.json()["response"]

def seleccionar_consulta(consultas):
    selected = None
    print("Pulsa ESPACIO para ver consultas al azar, ENTER para seleccionar.")

    last_space = False
    try:
        while True:
            space_pressed = keyboard.is_pressed("space")
            if space_pressed and not last_space:  # detect new key press
                selected = random.choice(consultas)
                print(f"\r{selected}", end="", flush=True)
            last_space = space_pressed

            if keyboard.is_pressed("enter"):
                print("")
                return selected

            time.sleep(0.05)
    except KeyboardInterrupt:
        pass