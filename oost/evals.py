import torch
# from transformers import BertTokenizer, BertModel

def st_score(reference, candidate, model):

    ref_embedding = model.encode(reference)
    cand_embedding = model.encode(candidate)
    sim = model.similarity(ref_embedding, cand_embedding).item()
    
    return sim