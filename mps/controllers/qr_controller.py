import qrcode
from pyzbar.pyzbar import decode
from PIL import Image

class QRController:
    def generar_qr(self, data, output_path):
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(output_path)
            print(f"Código QR generado y guardado en {output_path}")
        except Exception as e:
            raise RuntimeError(f"Error al generar el código QR: {e}")

    def escanear_qr(self, image_path):
        try:
            img = Image.open(image_path)
            decoded_objects = decode(img)
            if decoded_objects:
                return decoded_objects[0].data.decode("utf-8")
            else:
                raise ValueError("No se detectó ningún código QR en la imagen.")
        except Exception as e:
            raise RuntimeError(f"Error al escanear el código QR: {e}")
