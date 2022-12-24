import torch
import pandas as pd
import numpy as np
from pathlib import Path
import os

path = Path(__file__).parent.parent
model_path = os.path.join(path, 'NT-D', 'docker_image_src', 'production.pt')
print(path)

def inference():
    data = pd.read_json('output.json', typ='series')
    df = pd.DataFrame([data])
    df = df.drop(['name', 'feedback'], axis=1)
    print(df)
    list = df.values.tolist()
    nparray = np.array(list).astype(np.int32)
    nparray = nparray[0]
    print(nparray)
    tensor = torch.Tensor(nparray)
    print(tensor)
    model = torch.jit.load(model_path)
    output = model(tensor)
    print(output)
    return output