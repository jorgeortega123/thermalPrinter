from flask import Flask, request, jsonify
from flask_cors import CORS
from escpos.printer import Usb
from PIL import Image
from datetime import datetime
import textwrap
app = Flask(__name__)

CORS(app)
# Inicializa impresora
p = Usb(0x28E9, 0x0289) 
image = Image.open("logo horizontal black.png")  # Cambia por la ruta de tu imagen
imageEx = Image.open("ejemplo stickers.png")  # Cambia por la ruta de tu imagen
max_width = 384
if image.width > max_width:
    ratio = max_width / image.width
    new_height = int(image.height * ratio)
    image = image.resize((max_width, new_height))

@app.route('/print', methods=['POST'])
def print_ticket():
    #return jsonify({'status': 'ok'}), 200
    print("data")
    data = request.get_json()
    

    #if not data or 'nombre' not in data or 'productos' not in data:
     #   return jsonify({'error': 'Faltan datos'}), 400

    show_cupon = data.get('showCupon', True) 
    productos = data['productos']
    cupon = data['cupon']
    code = cupon['code']
    amount = cupon['amount']
    expire = cupon['expire']
    descuentos = data.get("descuentos", [])
    clientData = data.get("clientData", {})
    nombre = clientData.get('nombre')
    total_descuentos = sum(float(d.get("amount", 0)) for d in descuentos)
    # Comenzar impresión




    

    p.set(align='center', bold=True)
    p.image(image)
    
    #p.cut()

    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
