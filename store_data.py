from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from helpers import get_db_client
from langchain.schema import Document

directoryPath = "/data"


def process_file(file_path: str, title: str) -> list[Document]:
    # load text
    loader = PyPDFLoader(file_path)
    data = loader.load()
    # split text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(data)
    # add metadata book_title
    for chunk in chunks:
        # print(chunk.page_content)
        chunk.metadata["title"] = title
    return chunks


def store_data(data_chunks: list[Document]):
    # add the documents to the database

    db_client = get_db_client()
    db_client.add_documents(documents=data_chunks)

    len(db_client.get()['ids'])


def process_data():
    pdf_files = Path("./data").glob("*.pdf")

    chunk_list = []

    for pdf_file in pdf_files:
        file_path = f"{pdf_file}"
        title = file_path.replace("data/", "").replace(".pdf", "")

        chunk_list.extend(process_file(file_path=file_path, title=title))

    try:
        store_data(chunk_list)
        print("File stored successfully")
    except:
        print("File could not be saved")


if __name__ == "__main__":
    process_data()
