from flask import Flask,request,redirect,url_for
import os
import werkzeug
import base64
from PIL import Image
import random

import datetime
import time



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
        upload_file.save('demo.png')
        start = datetime.datetime.now()
        image_name = resize()
#         endtime = datetime.datetime.now()
#         print("infer time is :" + str(endtime-start))
        time.sleep(0.2)
        # 随便打开一张其他图片作为结果返回，
        with open(r'/data/code/233/pix2pix-origin/output_dir/'+image_name, 'rb') as f:
            res = base64.b64encode(f.read())
            return res
     


def resize():
    img = Image.open("demo.png")
    img = img.convert("RGB")
    resized = img.resize((256,256))
    image_name = str(random.random())+'.png' 
    resized.save("/data/code/233/pix2pix-origin/input_dir/"+ image_name)
    #os.system('python /data/code/233/pix2pix-origin/process-local_1.py')
    return image_name

if __name__ == '__main__':

    app.run(host='0.0.0.0',port='8080')
