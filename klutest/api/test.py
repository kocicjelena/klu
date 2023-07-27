from http.client import HTTPException
import json
from collections import defaultdict

def get_all_dataset():
    with open('Share.json', 'r') as myfile:
        data = myfile.read()
        dataset = json.loads(data)
    return dataset

def make_index(dataset) -> dict:
    
    dindex = defaultdict(str)
    for dat in dataset:
        if dat["conversations"]:
            dindex[dat["id"]]=[]
            for d in dat["conversations"]:
                if d["from"] == "human":
                    dindex[dat["id"]].append(d["value"])

    return dindex

def pick(p: str, dindex:dict, dataset):
    pick = defaultdict()
    for i, j in dindex.items():
        if p in j:
                for dat in dataset:
                    if i == dat["id"]:
                        for dd in range(len(dat["conversations"])):
                            t = dat["conversations"][dd+1]["value"]
                            break
        else:
            continue
        #else:
            #raise HTTPException(status_code=404, detail=f"Please, when asking '{p}' be more precise.")
    
    return t
