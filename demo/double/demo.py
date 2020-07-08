import gradio as gr

def double(num):
    return 2 * num

iface = gr.Interface(double, "number", "number")