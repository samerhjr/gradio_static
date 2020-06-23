import gradio as gr
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bert import QA

model = QA('bert-large-uncased-whole-word-masking-finetuned-squad')
def qa_func(context, question):
    return model.predict(context, question)["answer"]

iface = gr.Interface(qa_func, 
    [
        gr.inputs.Textbox(lines=7, label="Context"), 
        gr.inputs.Textbox(lines=1, label="Question"), 
    ], 
    gr.outputs.Textbox(lines=7, label="Answer"))