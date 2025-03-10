import torch
# from transformers import BertTokenizer, BertModel
from sentence_transformers import SentenceTransformer, SimilarityFunction
from evaluate import load

rouge = load("rouge")

def st_score(reference, candidate, model):

    ref_embedding = model.encode(reference)
    cand_embedding = model.encode(candidate)
    sim = model.similarity(ref_embedding, cand_embedding).item()
    
    return sim


class Evaluator:

    def __init__(self, model_string=None, sim_func='cosine', **kwargs):

        if model_string is None:
            self.model_string = 'sentence-transformers/all-roberta-large-v1'
        else:
            self.model_string = model_string
        # self.model = BertModel.from_pretrained(model_string, torch_dtype=torch.bfloat16)

        if sim_func == 'cosine':
            self.model = SentenceTransformer(self.model_string, similarity_fn_name=SimilarityFunction.COSINE, **kwargs)
        elif sim_func == 'dotprod':
            self.model = SentenceTransformer(self.model_string, similarity_fn_name=SimilarityFunction.DOT_PRODUCT, **kwargs)
        elif sim_func == 'euclidean':
            self.model = SentenceTransformer(self.model_string, similarity_fn_name=SimilarityFunction.EUCLIDEAN, **kwargs)

    def compare(self, ref, gt):

        self.st_score = st_score(ref, gt, self.model)

    def rouge(self, ref, gt):

        self.rouge_score = rouge.compute(predictions=[ref], references=[gt])
        self.rougeL = self.rouge_score['rougeL']