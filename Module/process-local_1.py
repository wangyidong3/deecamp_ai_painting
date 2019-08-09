import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np
import argparse
import json
import base64
import os
import time
#parser = argparse.ArgumentParser()
#parser.add_argument("--model_dir", required=True, help="directory containing exported model")
#parser.add_argument("--input_file", required=True, help="input PNG image file")
#parser.add_argument("--output_file", required=True, help="output PNG image file")
#a = parser.parse_args()
model_dir='/data/code/233/pix2pix-origin/export_0806'
input_dir='input_dir'
output_dir='output_dir'
def main():
    

    with tf.Session() as sess:
        saver = tf.train.import_meta_graph(model_dir + "/export.meta")
        saver.restore(sess, model_dir + "/export")
        input_vars = json.loads(tf.get_collection("inputs")[0].decode('utf-8'))
        output_vars = json.loads(tf.get_collection("outputs")[0].decode('utf-8'))
        input = tf.get_default_graph().get_tensor_by_name(input_vars["input"])
        output = tf.get_default_graph().get_tensor_by_name(output_vars["output"])
        file_handled=[]
        while True:
            files=os.listdir(input_dir)
            for file in files:
                file_path=os.path.join(input_dir,file)
                if os.path.exists(file_path) and ('.png' in file) and (file not in file_handled):
                    t0=time.time()
                    file_handled.append(file)
                    with open(file_path, "rb") as f:
                        input_data = f.read()

                    input_instance = dict(input=base64.urlsafe_b64encode(input_data).decode("ascii"), key="0")
                    input_instance = json.loads(json.dumps(input_instance))
                    input_value = np.array(input_instance["input"])
                    output_value = sess.run(output, feed_dict={input: np.expand_dims(input_value, axis=0)})[0]

                    output_instance = dict(output=output_value.decode("ascii"), key="0")

                    b64data = output_instance["output"]
                    b64data += "=" * (-len(b64data) % 4)
                    output_data = base64.urlsafe_b64decode(b64data.encode("ascii"))
                    output_path=os.path.join(output_dir,file)
                    with open(output_path, "wb") as f:
                        f.write(output_data)
                        print("%s already created"%(file))
                        print(time.time()-t0,'is needed')

main()