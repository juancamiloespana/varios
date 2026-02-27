import random

from tqdm import tqdm

from pseudo_utils import (funciona, seleccionar_consulta, reescribir_consulta,
    consultar_buscador, fusionar_rrf, obtener_documento, segmentar, escoger_pasajes,
    retrieval_augmented_generation)

def main():
    consultas = [
        "bad bacteria in stomach symptoms",
        "can professional basketball players play in the basketball tournament during the olympic games?",
        "does prenatal vitamins make your hair grow faster",
        "effect of sugar concentration on fermentation rate",
        "has basketball been played in every olympic games since 1936?",
        "how do evolutionist believe dinosaurs were created",
        "how long does a nose piercing take to close",
        "how many countries competed in the basketball tournament in the summer olympics in 1936?",
        "imagine you are a 10x nun in a bear costume from outerspace with opposable thumbs about to engage in a fight to the death with another nun, who may or may not be a bear in disguise. In front of you two lie a hunting knife and a baseball bat. If you pick one, the other nun will choose the other weapon. Which one would you pick and why?",
        "is rhyolite extrusive",
        "the oldest playable instruments were discovered in",
        "what are some books that will expand our mind?",
        "what are the most surreal places to visit?",
        "what can I learn/know right now in 10 minutes that will be useful for the rest of my life?",
        "what damage do rabbits do",
        "what describes a mammal",
        "what is feco oil",
        "what is the meaning of my life? Why am I in this world? What is my purpose?",
        "what materials did the greeks use to build temples",
        "what region of africa is kenya in",
        "when did women's basketball first enter in the olympic games?",
        "when was basketball first played in the olympic games?",
        "which country has won the most times in the basketball tournament in the olympic games?",
        "why did it take years for the theory of continental drift to be accepted",
        "why is a mushroom called a fruiting body"
    ]

    if not funciona():
        print("""¿Estás conectado a través de GlobalProtect a la VPN de UniOvi? (Ver https://portalgp.uniovi.es/global-protect/getsoftwarepage.esp)
Si no lo estás, conéctate.
Si lo estás, entonces el servidor de demo está caído, avisa a dani@uniovi.es""")
    else:
        consulta = seleccionar_consulta(consultas) # consulta = random.choice(consultas)

        print(f"Consulta original: {consulta}")

        intencion, tipo, consulta_reescrita = reescribir_consulta(consulta)
        print(f"\nTipo: {tipo}\nIntención: {intencion}\nConsulta reescrita: {consulta_reescrita}")

        lista_resultados_1 = consultar_buscador(consulta, num_results=10)
        print(f"\n{len(lista_resultados_1)} resultados obtenidos para \"{consulta}\"")

        lista_resultados_2 = consultar_buscador(consulta_reescrita, num_results=10)
        print(f"{len(lista_resultados_2)} resultados obtenidos para \"{consulta_reescrita}\"")

        resultados_rrf = fusionar_rrf(lista_resultados_1, lista_resultados_2)
        resultados_rrf = resultados_rrf[:10]
        print("Resultados de ambas listas fusionados.")

        print("\nObteniendo texto completo de los documentos...")
        documentos = []

        for resultado in tqdm(resultados_rrf):
            documento = obtener_documento(resultado["short_uuid"])
            if documento:
                documentos.append(documento.strip())

        print("\nObtenido texto completo de los documentos.")

        print("\nSegmentando documentos en pasajes...")

        pasajes = []
        for documento in tqdm(documentos):
            segmentos = segmentar(documento)
            pasajes.extend(segmentos)

        print(f"\nObtenidos {len(pasajes)} pasajes.")

        pasajes_relevantes = escoger_pasajes(consulta, intencion, tipo, consulta_reescrita, pasajes, num_pasajes=10)
        print(f"Obtenidos {len(pasajes_relevantes)} pasajes potencialmente relevantes.")

        print("\nSolicitando una respuesta basada en los pasajes relevantes...")

        respuesta = retrieval_augmented_generation(consulta, tipo, intencion, pasajes_relevantes)
        print(f"\nRespuesta a \"{consulta}\":\n\n{respuesta}")

if __name__ == "__main__":
    main()