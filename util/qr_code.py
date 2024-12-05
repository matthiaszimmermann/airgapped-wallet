import qrcode
from io import BytesIO

class QrCodeUtility:
    IMAGE_FILE_TYPE = "PNG"
    ENCODING_TYPE = "UTF-8"

    @staticmethod
    def content_to_png_bytes(content: str, size: int) -> bytes:
        try:
            # Create QR code instance with custom configurations
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,  # Adjusts the box size (can modify later for finer control over the final size)
                border=0,     # No border, similar to setting margin=0 in Java
            )
            qr.add_data(content)
            qr.make(fit=True)

            # Generate image
            image = qr.make_image(fill_color="black", back_color="white")
            image = image.resize((size, size))  # Resize to the specified size

            # Convert to byte array
            with BytesIO() as output:
                image.save(output, format=QrCodeUtility.IMAGE_FILE_TYPE)
                return output.getvalue()

        except Exception as e:
            raise RuntimeError("Failed to produce image byte array") from e
