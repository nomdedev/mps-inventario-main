import os

class DependencyAnalyzer:
    def analyze(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no existe.")
        # Lógica para analizar dependencias
        print(f"Analizando dependencias en {file_path}...")
        return ["modulo1", "modulo2", "modulo3"]

    def analyze_multiple(self, file_paths):
        all_dependencies = []
        for file_path in file_paths:
            try:
                dependencies = self.analyze(file_path)
                all_dependencies.extend(dependencies)
            except FileNotFoundError as e:
                print(f"Advertencia: {e}")
        return list(set(all_dependencies))  # Eliminar duplicados

    def filter_dependencies(self, dependencies, keyword):
        return [dep for dep in dependencies if keyword in dep]
