from io import BytesIO
import qrcode

data = "https://t.me/vl_start_bot?start=analitic"

img = qrcode.make(data)

img.save('qr-code analitic.png')

data = "https://t.me/vl_start_bot?start=resp"

img = qrcode.make(data)

img.save('qr-code resp.png')



