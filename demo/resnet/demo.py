import gradio as gr
import torch
from torchvision import transforms
import requests 
from PIL import Image

model = torch.hub.load('pytorch/vision:v0.6.0', 'resnet18', pretrained=True)
model.eval()

response = requests.get("https://gist.githubusercontent.com/yrevar/942d3a0ac09ec9e5eb3a/raw/238f720ff059c1f82f368259d1ca4ffa5dd8f9f5/imagenet1000_clsidx_to_labels.txt")
idx_to_labels = {index : name.split('\'')[1].split(',')[0] for index, name in enumerate(response.text.split("\n"))}

def predict(inp):
  inp = Image.fromarray(inp.astype('uint8'), 'RGB')
  inp = transforms.ToTensor()(inp).unsqueeze(0)
  with torch.no_grad():
    prediction = torch.nn.functional.softmax(model(inp)[0], dim=0) 
  return {idx_to_labels[i].split(',')[0]: float(prediction[i]) for i in range(1000)}

inputs = gr.inputs.Image()
outputs = gr.outputs.Label(num_top_classes=3)
iface = gr.Interface(fn=predict, inputs=inputs, outputs=outputs)