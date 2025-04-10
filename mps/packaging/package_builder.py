import zipfile

class PackageBuilder:
    def build_package(self, dependencies):
        if not dependencies:
            raise ValueError("No se proporcionaron dependencias para construir el paquete.")
        # Lógica para construir paquetes
        print(f"Generando paquete con dependencias: {dependencies}")

    def build_submodules(self, dependencies, submodule_name):
        if not dependencies:
            raise ValueError("No se proporcionaron dependencias para construir el submódulo.")
        print(f"Generando submódulo '{submodule_name}' con dependencias: {dependencies}")

    def build_zip_package(self, dependencies, output_path):
        if not dependencies:
            raise ValueError("No se proporcionaron dependencias para construir el paquete ZIP.")
        with zipfile.ZipFile(output_path, 'w') as zipf:
            for dep in dependencies:
                # Simulación: Crear un archivo ficticio para cada dependencia
                zipf.writestr(f"{dep}.txt", f"Contenido ficticio para {dep}")
        print(f"Paquete ZIP generado en {output_path}")
