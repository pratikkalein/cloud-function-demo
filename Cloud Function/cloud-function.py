import functions_framework
import qrcode
from io import BytesIO
from PIL import Image
import flask

@functions_framework.http
def hello_http(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'link' in request_json:
        link = request_json['link']
    elif request_args and 'link' in request_args:
        link = request_args['link']
    else:
        return 'Add link'

     # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a bytes buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Return the image as a response
    return flask.send_file(buffer, mimetype='image/png')

