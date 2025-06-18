from langchain.document_loaders import TextLoader

def load_txt_documents(file_paths):
    all_docs = []
    for path in file_paths:
        loader = TextLoader(path)
        docs = loader.load()
        all_docs.extend(docs)
    return all_docs
