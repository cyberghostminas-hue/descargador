import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote

# Formatos de video que se van a buscar
EXTENSIONES = (".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".mpg", ".mpeg")


def obtener_videos(url_carpeta):
    # Aseguramos que la URL termine en "/" para comparar bien
    if not url_carpeta.endswith("/"):
        url_carpeta += "/"

    respuesta = requests.get(url_carpeta, timeout=30)
    respuesta.raise_for_status()

    soup = BeautifulSoup(respuesta.text, "html.parser")
    videos = []

    for enlace in soup.find_all("a", href=True):
        url_completa = urljoin(url_carpeta, enlace["href"])

        # Solo lo que esté dentro de esta carpeta, nunca fuera de ella
        if not url_completa.startswith(url_carpeta):
            continue

        # Lo que viene después de la carpeta no debe tener más "/" (sin subcarpetas)
        resto = url_completa[len(url_carpeta):]
        if not resto or "/" in resto:
            continue

        # Quitamos parámetros tipo ?C=N;O=D por si la página los trae
        resto_limpio = resto.split("?")[0]
        if resto_limpio.lower().endswith(EXTENSIONES):
            videos.append(url_completa.split("?")[0])

    # Quitamos repetidos conservando el orden
    return list(dict.fromkeys(videos))


def main():
    url = input("Pega el enlace de la carpeta: ").strip()

    try:
        videos = obtener_videos(url)
    except requests.RequestException as error:
        print(f"No se pudo abrir la carpeta: {error}")
        return

    if not videos:
        print("No encontré videos en esa carpeta.")
        return

    with open("enlaces.txt", "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(videos))

    print(f"Listo, encontré {len(videos)} videos:")
    for video in videos:
        print(" -", unquote(video.rsplit("/", 1)[-1]))
    print("\nGuardé los enlaces en enlaces.txt")


if __name__ == "__main__":
    main()