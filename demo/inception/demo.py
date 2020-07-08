import tensorflow as tf
import gradio as gr
import numpy as np
import requests

mobile_net = tf.keras.applications.MobileNetV2()

response = requests.get("https://gist.githubusercontent.com/yrevar/942d3a0ac09ec9e5eb3a/raw/238f720ff059c1f82f368259d1ca4ffa5dd8f9f5/imagenet1000_clsidx_to_labels.txt")
idx_to_labels = {index : name.split('\'')[1].split(',')[0] for index, name in enumerate(response.text.split("\n"))}

def classify_image(inp):
  inp = np.expand_dims(inp, 0)  # Insert the batch dimension.
  prediction = mobile_net.predict(inp).flatten()
  return {idx_to_labels[i]: float(prediction[i]) for i in range(1000)}  # Take the first word in each label.

image = gr.inputs.Image(shape=(224, 224))
label = gr.outputs.Label(num_top_classes=3)

iface = gr.Interface(classify_image, image, label, capture_session=True);