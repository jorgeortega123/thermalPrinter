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
    p.text("Jandrea - www.jandrea.art \n")
    #p.text("www.jandrea.art\n")
    p.text("098 638 7530\n")
    
    p.set(align='center', bold=False)
    p.text("Comprobante de venta\n")
    p.text("Tumbaco, Abdón Calderón y\n Eugenio Espejo\n")
    p.text(datetime.now().strftime("%d/%m/%Y %H:%M") + "\n")
    p.text("-------------------------------\n")

    p.set(align='left', bold=False)
    p.text(f"Cliente: {clientData.get("name")}\n")
    if clientData.get("email"):
     p.text(f"CI: {clientData.get("dni")}\n")
     if clientData.get("phone"):
      p.text(f"Teléfono: {clientData.get("phone")}\n")
     p.text(f"Correo: {clientData.get("email")}\n")
     p.text(f"Dirección: {clientData.get("address")}\n")
    p.text("-------------------------------\n")
    p.set(bold=True)
    p.text("Cant  Descripción      Precio\n")
    p.set(bold=False)
    total = 0.0
    for item in productos:
     cantidad = int(item.get("cantidad", 1))
     descripcion = item.get("descripcion", "")
     precio = float(item.get("precio", 0))
     subtotal = cantidad * precio
     total += subtotal
 
     # Ajustamos descripción a 18 caracteres por línea
     desc_lines = textwrap.wrap(descripcion, width=18)
 
     # Primera línea con cantidad y precio
     cant_str = str(cantidad).ljust(5)
     price_str = f"{precio * cantidad:.2f}".rjust(7)
     p.text(f"{cant_str}{desc_lines[0].ljust(18)}{price_str}\n")

     # Líneas siguientes solo continúan descripción
     for line in desc_lines[1:]:
        p.text(f"{' '*5}{line}\n")  # Indentar descripción
    p.text("-------------------------------\n")
    p.text(f"{'SubTotal:'.ljust(25)} {total:.2f}\n")
    p.text(f"{'IVA 0%:'.ljust(25)} 0.00\n")
    descuentos_validos = [d for d in descuentos if float(d.get("amount", 0)) > 0]
    if descuentos_validos:
     p.text("Descuentos:\n")
     for d in descuentos_validos:
        titulo = d.get("title", "")
        monto = float(d.get("amount", 0))
        titulo_lines = textwrap.wrap(titulo, width=23)
        p.text(f" {titulo_lines[0].ljust(22)} -{monto:>5.2f}\n")
        for extra_line in titulo_lines[1:]:
            p.text(f"{' '*2}{extra_line}\n")

# Línea separadora
    p.text("-" * 32 + "\n")

# Total final
    total_final = total - total_descuentos
  
    p.set(align='left', bold=True)
    p.text(f"{'TOTAL:'.ljust(25)}${total_final:>5.2f}\n")
    p.set(align='left', bold=False)
    if show_cupon:
     p.text("\n-------------------------------\n")
     p.set(align='center', bold=True)
     p.text(f"Has ganado 1 STICKER en esta \ncompra. Completa 4 más y gana \npremios\n")
     p.text("-------------------------------\n")
     p.set(align='left', bold=False)
     p.text("Conoce los beneficios del club\n Jandrea:")
     #p.text(f"Codigo de cupón: {code} \ncaduca el {expire}.")
     #p.qr("https://jandrea.art/?cupon=" + code, size=8,ec='H', model=2 )
     p.qr("https://jandrea.art/club/registro?id=" + code, size=9, model=2 )    
     p.text(f"{code}")
    p.set(bold=True)
    p.text("\nGracias por su compra!\n\n")
    #p.cut()

    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
