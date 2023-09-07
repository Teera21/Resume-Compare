from langchain.document_loaders import PyPDFLoader
from translation import str_range_to_eng
import glob

def read_pfd_folder(str_path):
    ls_dir = glob.glob(f"{str_path}/*.pdf")
    data = []
    for i in ls_dir:
        loader = PyPDFLoader(i)
        pages = loader.load_and_split()
        str_trans = ''
        for i in pages:
            str_trans = str_range_to_eng(i.page_content)
            str_trans += "\*/" + pages[0].metadata['source']
            data.append(str_trans)
    return data