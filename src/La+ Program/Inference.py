import torch
import torch.jit
import pandas as pd
import numpy as np
from pathlib import Path
import os

path = Path(__file__).parent.parent
model_path = os.path.join(path, 'NT-D', 'docker_image_src', 'production.pt')

def inference(name_length, name_sp, nation, city, industry, investor, ls):
    nparray = np.array([name_length, name_sp, nation, city, industry, investor, ls], dtype=np.int32).reshape(1, -1)
    
    # print("JSON read\n")
    # df = pd.DataFrame([data])
    # df = df.drop(['name', 'feedback'], axis=1)
    # print("Inference output:\n",df)
    # list = df.values.tolist()
    # nparray = np.array(list).astype(np.int32)
    # nparray = nparray[0]
    print(nparray)
    tensor = torch.Tensor(nparray)
    print(tensor)
    model = torch.jit.load(model_path)
    output = model(tensor)
    print("output: ",output)
    return output