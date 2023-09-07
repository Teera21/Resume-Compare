import faiss
import numpy as np 
import uuid
import pickle
from translation import str_range_to_eng

def convert_to_vector(data,model):
    encoded_data = model.encode(data)
    index = faiss.IndexIDMap(faiss.IndexFlatIP(model.get_sentence_embedding_dimension()))
    index.add_with_ids(encoded_data, np.array(range(0, len(data))))
    index_filename = str(uuid.uuid4())
    list_filename = str(uuid.uuid4())
    faiss.write_index(index, "./data_cach/"+index_filename)
    with open("./data_cach/"+list_filename, "wb") as fp:   
        pickle.dump(data, fp)
    return index_filename,list_filename

def search(query,index_filename,top_k,model):
    query = str_range_to_eng(query)
    index = faiss.read_index("./data_cach/"+index_filename)
    query_vector = model.encode([query])
    k = top_k
    top_ks = index.search(query_vector, k)
    return top_ks