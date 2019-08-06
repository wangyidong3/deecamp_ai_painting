from flask import Flask,request,redirect,url_for
import os
import werkzeug
import base64
from PIL import Image

base_url='/infer-66f28b95-d8ec-4e11-a2fe-14a544cc6b16'

app = Flask(__name__)
@app.route(base_url+'/', methods=['POST'])
def upload_image():
    # 接收图片
    upload_file = request.files['file']
    # 获取图片名
    file_name = upload_file.filename
    # 文件保存目录（桌面）
    if upload_file:
        # 地址拼接
        file_paths = os.path.join(app.root_path, file_name)
        # 保存接收的图片到桌面
        upload_file.save('./demo.jpg')
        resize()
        # 随便打开一张其他图片作为结果返回，
        with open(r'4.png', 'rb') as f:
            res = base64.b64encode(f.read())
            return res

def resize():
    img = Image.open("demo.jpg")
    img = img.convert("RGB")
    resized = img.resize((256,256))
    resized.save("resized.jpg")
    os.system('python /data/code/233/pix2pix-origin/process-local.py --model_dir /data/code/233/pix2pix-origin/export_0806 --input_file resized.jpg --output_file 4.png')

if __name__ == '__main__':

    app.run(host='0.0.0.0',port='8080')