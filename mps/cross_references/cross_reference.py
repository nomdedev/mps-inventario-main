from mps.utils.file_utils import write_file

class CrossReference:
    def generate_report(self, dependencies):
        if not dependencies:
            raise ValueError("No se proporcionaron dependencias para generar el reporte.")
        # Lógica para generar referencias cruzadas
        print(f"Generando reporte de referencias cruzadas para: {dependencies}")

    def save_report(self, dependencies, output_path):
        if not dependencies:
            raise ValueError("No se proporcionaron dependencias para guardar el reporte.")
        report_content = f"Reporte de referencias cruzadas:\n{dependencies}"
        write_file(output_path, report_content)
        print(f"Reporte guardado en {output_path}")

    def load_report(self, input_path):
        from mps.utils.file_utils import read_file
        content = read_file(input_path)
        print(f"Reporte cargado desde {input_path}:\n{content}")
        return content
