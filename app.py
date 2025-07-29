from flask import Flask, request, send_file, abort
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/generate', methods=['GET'])
def generate_qr():
    url = request.args.get('url')
    size = request.args.get('size', default=200, type=int)

    if not url:
        return abort(400, description="Missing required parameter: url")

    # Sanitize size
    size = max(100, min(size, 1000))  # Clamp between 100 and 1000 px

    # Create QR Code
    qr = qrcode.QRCode(
        version=1,
        box_size=size // 29,  # 29 is approx module count for version 1
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Save to memory buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype='image/png',
        as_attachment=True,
        download_name='qrcode.png'
    )

if __name__ == '__main__':
    app.run(debug=True)
