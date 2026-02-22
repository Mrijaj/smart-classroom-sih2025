import qrcode
import base64
from io import BytesIO
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.utils import timezone

# The Signer allows us to "timestamp" the data inside the QR
signer = TimestampSigner()


def generate_classroom_qr(timetable_entry_id):
    """
    Generates a base64 encoded QR code containing a signed timetable_entry_id.
    Valid for the duration of the class.
    """
    # 1. Sign the timetable ID with the current timestamp
    signed_value = signer.sign(str(timetable_entry_id))

    # 2. Create the QR Code object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # The URL students will be redirected to when they scan
    # Example: http://yoursite.com/attendance/scan/TOKEN_HERE
    qr_data = signed_value
    qr.add_data(qr_data)
    qr.make(fit=True)

    # 3. Save the image to a buffer to send to the template
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return qr_base64


def verify_qr_token(token, max_age=60):
    """
    Verifies the token scanned by the student.
    max_age: time in seconds the QR remains valid after generation (default 60s).
    """
    try:
        # Unsgn the value and check if it has expired
        timetable_entry_id = signer.unsign(token, max_age=max_age)
        return timetable_entry_id
    except (SignatureExpired, BadSignature):
        return None