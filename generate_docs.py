import json
from gradio.inputs import InputComponent
from gradio.outputs import OutputComponent
from gradio.interface import Interface
import inspect
from os import listdir
from os.path import join, exists
import re

GRADIO_DIR = "../gradio/"
 
def get_demos():
    in_demos, out_demos = {}, {}
    demo_regex = "# Demo: \((.*)\) -> \((.*)\)"
    for demo in listdir(join(GRADIO_DIR, "demo")):
        if demo.endswith(".py"):
            demo_dir = join(GRADIO_DIR, "demo/screenshots", demo[:-3])
            if not exists(demo_dir):
                continue
            screenshots = listdir(demo_dir)[0]
            demoset = [demo, [screenshots]]
            with open(join(GRADIO_DIR, "demo", demo)) as demo_file:
                first_line = demo_file.readline()
                match = re.match(demo_regex, first_line)
                if not match:
                    continue
                inputs = match.group(1).split(", ")
                outputs = match.group(2).split(", ")
                for i in inputs:
                    if i not in in_demos:
                        in_demos[i] = []
                    if demoset not in in_demos[i]:
                        in_demos[i].append(demoset)
                for o in outputs:
                    if o not in out_demos:
                        out_demos[o] = []
                    if demoset not in out_demos[o]:
                        out_demos[o].append(demoset)
    return in_demos, out_demos

def get_ins_and_outs(func):
    doc_str = inspect.getdoc(func)
    func_doc, params_doc, return_doc = [], [], []
    documented_params = {"self"}
    mode = "pre"
    for line in doc_str.split("\n"):
        if line.startswith("Parameters:"):
            mode = "in"
            continue
        if line.startswith("Returns:"):
            mode = "out"
            continue
        if mode == "pre":
            func_doc.append(line)            
        elif mode == "in":
            space_index = line.index(" ")
            colon_index = line.index(":")
            name = line[:space_index]
            documented_params.add(name)
            params_doc.append((name, line[space_index+2:colon_index-1], line[colon_index+2:]))
        elif mode == "out":
            colon_index = line.index(":")
            return_doc.append((line[1:colon_index-1], line[colon_index+2:]))
    params = inspect.getfullargspec(func)
    param_set = []
    for i in range(len(params.args)):
        neg_index = -1 - i
        if params.args[neg_index] not in documented_params:
            continue
        if params.defaults and i < len(params.defaults):
            default = params.defaults[neg_index]
            if type(default) == str:
                default = '"' + default + '"'
            else:
                default = str(default)
            param_set.insert(0, (params.args[neg_index], default))
        else:
            param_set.insert(0, (params.args[neg_index],))
    return "\n".join(func_doc), param_set, params_doc, return_doc

def document(cls_set, demos):
    docset = []
    for cls in cls_set:
        inp = {}
        inp["name"] = cls.__name__
        doc = inspect.getdoc(cls)
        if doc.startswith("DEPRECATED"):
            continue
        inp["doc"] = "\n".join(doc.split("\n")[:-1])
        inp["type"] = doc.split("\n")[-1].split("type: ")[-1]
        _, inp["params"], inp["params_doc"], _ = get_ins_and_outs(cls.__init__)
        inp["shortcuts"] = list(cls.get_shortcut_implementations().items())
        cls_name = cls.__name__
        if cls_name in demos:
            inp["demos"] = demos.get(cls_name, [])
        if "interpret" in cls.__dict__:
            inp["interpret"], inp["interpret_params"], inp["interpret_params_doc"], _ = get_ins_and_outs(cls.interpret)
            _, _, _, inp["interpret_returns_doc"] = get_ins_and_outs(cls.get_interpretation_scores)

        docset.append(inp)
    return docset

def generate():
    in_demos, out_demos = get_demos()
    inputs = document(InputComponent.__subclasses__(), in_demos)
    outputs = document(OutputComponent.__subclasses__(), out_demos)
    interface_params = get_ins_and_outs(Interface.__init__)
    interface = {
        "doc": inspect.getdoc(Interface),
        "params": interface_params[1],
        "params_doc": interface_params[2],
    }
    launch_params = get_ins_and_outs(Interface.launch)
    launch = {
        "params": launch_params[1],
        "params_doc": launch_params[2],
    }

    return {
        "inputs": inputs,
        "outputs": outputs,
        "interface": interface,        
        "launch": launch,
    }

