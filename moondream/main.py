import time

from flask import Flask, request
import moondream
from PIL import Image
import io

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MOONDREAM_MODEL = "2b"

    app = Flask(__name__)

    print(f"Loading moondream model {MOONDREAM_MODEL}...")
    md = moondream.vl(api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiIwODE3NDRjMi1lM2JhLTRiOGUtYjVhNi02ZmFkZTE3MDgxNjgiLCJvcmdfaWQiOiJiZ1hsYXcyTUlwbjlVOXYwQ2FSa1RCSGVsYXBoYkxQWiIsImlhdCI6MTc0NTA3NjEyMywidmVyIjoxfQ.mlD-nOkYM3dcd9PMd9l6oHdam7Gu-n2fhRHkm1PpVsY")

    @app.route('/send-image', methods=['POST'])
    def upload_file():
        # check if the post request has the file part
        if 'file' not in request.files:
            return
        file = request.files['file']
        if file.filename == '':
            return
        if file and allowed_file(file.filename):
            print("Image received!" + file.mimetype )
            img = Image.open(io.BytesIO(file.read()))
            encoded_image = md.encode_image(img)
            start_time = time.time()

            response = md.query(encoded_image, "Is there any sensitive data in this image?")

            return f"Response: {response['answer']}\nElapsed time: {str(time.time() - start_time)}"
    app.run()
