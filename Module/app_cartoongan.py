from flask import Flask,request,redirect,url_for
import os
import werkzeug
import base64
from PIL import Image
import random
import cv2
import datetime
import time



base_url='/infer-64070ab5-caa3-4782-8f6d-0f3917c5c6be'


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
        # 保存接收的图片
        image_name = str(datetime.datetime.now())+'.png' 
        input_path_file = os.path.join('/data/code/xyh/CartoonGAN-Test-Pytorch-Torch/input',image_name)
        upload_file.save(input_path_file)
        os.system('python /data/code/xyh/CartoonGAN-Test-Pytorch-Torch/test.py --input_dir /data/code/xyh/CartoonGAN-Test-Pytorch-Torch/input --style Hosoda --gpu 2 --model_path /data/code/xyh/CartoonGAN-Test-Pytorch-Torch/pretrained_model ')
#         image_name = resize()
#         endtime = datetime.datetime.now()
#         print("infer time is :" + str(endtime-start))
        # 随便打开一张其他图片作为结果返回，
        image_name = os.path.splitext(image_name)[0] + '_Hosoda.jpg'
        with open(r'/data/code/wyd/output_dir/'+image_name, 'rb') as f:
            res = base64.b64encode(f.read())
            return res
     


def resize():
#     img = Image.open("demo.png")
#     img = img.convert("RGB")
#     resized = img.resize((256,256))
    img=cv2.imread('demo.png')
    img=cv2.resize(img,(256,256),interpolation =  cv2.INTER_NEAREST)
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
#     img=255-img
#     dilated = cv2.dilate(img,kernel)  #局部最大值
#     output = dilated - img
#     output = 255 - output
    image_name = str(datetime.datetime.now())+'.png' 
    output_path = os.path.join('/data/code/233/pix2pix-origin/input_dir/',image_name)
    cv2.imwrite(output_path,img)
#     resized.save("/data/code/233/pix2pix-origin/input_dir/"+ image_name)
    #os.system('python /data/code/233/pix2pix-origin/process-local_1.py')
    return image_name

if __name__ == '__main__':

    app.run(host='0.0.0.0',port='8080')
