import gradio as gr
import tensorflow as tf
import numpy as np
from PIL import Image
import requests

response = requests.get("https://gist.githubusercontent.com/yrevar/942d3a0ac09ec9e5eb3a/raw/238f720ff059c1f82f368259d1ca4ffa5dd8f9f5/imagenet1000_clsidx_to_labels.txt")
idx_to_labels = {index : name.split('\'')[1].split(',')[0] for index, name in enumerate(response.text.split("\n"))}

mobile_net = tf.keras.applications.MobileNetV2()
inception_net = tf.keras.applications.InceptionV3()


def classify_image_with_mobile_net(im):
	arr = im.reshape((-1, 224, 224, 3))	
	arr = tf.keras.applications.mobilenet.preprocess_input(arr)
	prediction = mobile_net.predict(arr).flatten()
	return {idx_to_labels[i].split(',')[0]: float(prediction[i]) for i in range(1000)}


def classify_image_with_inception_net(im):
	im = Image.fromarray(im.astype('uint8'), 'RGB')
	im = im.resize((299, 299))
	arr = np.array(im).reshape((-1, 299, 299, 3))
	arr = tf.keras.applications.inception_v3.preprocess_input(arr)
	prediction = inception_net.predict(arr).flatten()
	return {idx_to_labels[i].split(',')[0]: float(prediction[i]) for i in range(1000)}

imagein = gr.inputs.Image()
label = gr.outputs.Label(num_top_classes=3)

sample_images = [
                 ["https://www.sciencemag.org/sites/default/files/styles/article_main_large/public/cc_BE6RJF_16x9.jpg?itok=nP17Fm9H"],
                 ["https://www.discoverboating.com/sites/default/files/inline-images/buying-a-sailboat-checklist.jpg"],
                 ["https://external-preview.redd.it/lG5mI_9Co1obw2TiY0e-oChlXfEQY3tsRaIjpYjERqs.jpg?auto=webp&s=ea81982f44b83efbb803c8cff8953ee547624f70"]
]

iface = gr.Interface(
    [classify_image_with_mobile_net, classify_image_with_inception_net], 
    imagein, 
    label,
    title="MobileNet vs. InceptionNet",
    description="Let's compare 2 state-of-the-art machine learning models that classify images into one of 1,000 categories: MobileNet (top), a lightweight model that has an accuracy of 0.704, vs. InceptionNet (bottom), a much heavier model that has an accuracy of 0.779.",
    examples=sample_images
)