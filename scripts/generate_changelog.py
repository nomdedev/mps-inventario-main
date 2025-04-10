import subprocess
from datetime import datetime

CHANGELOG_FILE = "CHANGELOG.md"

def obtener_commits():
    """
    Obtiene los commits recientes usando Git.
    """
    try:
        resultado = subprocess.run(
            ["git", "log", "--pretty=format:%h %s (%an) %ad", "--date=short"],
            capture_output=True,
            text=True,
            check=True
        )
        return resultado.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error al obtener commits: {e}")
        return []

def generar_changelog():
    """
    Genera un archivo CHANGELOG.md agrupado por fecha y tipo de cambio.
    """
    commits = obtener_commits()
    if not commits:
        print("No se encontraron commits recientes.")
        return

    cambios = {}
    for commit in commits:
        partes = commit.split(" ", 1)
        hash_commit = partes[0]
        mensaje = partes[1]
        fecha = mensaje.split()[-1].strip("()")
        tipo = "otros"
        if mensaje.startswith("feat:"):
            tipo = "feat"
        elif mensaje.startswith("fix:"):
            tipo = "fix"

        if fecha not in cambios:
            cambios[fecha] = {}
        if tipo not in cambios[fecha]:
            cambios[fecha][tipo] = []
        cambios[fecha][tipo].append(f"{hash_commit} {mensaje}")

    with open(CHANGELOG_FILE, "w") as f:
        f.write("# Changelog\n\n")
        for fecha, tipos in sorted(cambios.items(), reverse=True):
            f.write(f"## {fecha}\n")
            for tipo, mensajes in tipos.items():
                f.write(f"### {tipo.capitalize()}\n")
                for mensaje in mensajes:
                    f.write(f"- {mensaje}\n")
                f.write("\n")
    print(f"Changelog generado en {CHANGELOG_FILE}.")

if __name__ == "__main__":
    generar_changelog()
