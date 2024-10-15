import io
import segno

def generate_qr_code(data):
    
    qr = segno.make_qr(data)
    buff = io.BytesIO()
    qr.save(buff, data[1]+'.png', scale=3)