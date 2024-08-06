import streamlit as st
import openai
import os
import pinecone
import pandas as pd
from dotenv import load_dotenv
from PyPDF2 import PdfReader 
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.vectorstores import Pinecone
from langchain.memory import ConversationBufferMemory 
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from htmlTemplates import css, bot_template, user_template
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import firebase_admin
from firebase_admin import credentials, db
import subprocess
import webbrowser


# Initialize Firebase with your service account credentials
cred = credentials.Certificate('Firebase Json file path')

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'firebase database url'
    })

# 1. function to get text from the pdf
def get_pdf_text(pdf_docs):
    # initalize variable text for storing all text from the pdf
    text = ""
    for pdf in pdf_docs:
        # initalize with pdf object 
        pdf_reader = PdfReader(pdf)
        # reading in pages
        for page in pdf_reader.pages:
            text += page.extract_text()    
    return text 

# 2. to divide the text into the chunks
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
         separator="\n",
         chunk_size = 1000,
         chunk_overlap = 200,
    )

    chunks = text_splitter.split_text(text)
    return chunks

# 3. creating embiddings of chunks
def get_vectorstore(text_chunks):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    # print(openai.api_key)
    # embeddings = OpenAIEmbeddings(model_name="ada")
    embeddings = OpenAIEmbeddings(model_name="ada")

    docs = [Document(page_content=t) for t in text_chunks]
    doc_embeddings = []

    for doc in docs:
        query_result = embeddings.embed_query(doc.page_content)
        doc_embeddings.append(query_result)
        print(len(query_result))
    
    # to store vectors into pinecone
    pinecone.init(
    api_key="pinecone api key",
    environment="pinecone enviornment key"
    )

    index_name = "pinecone index name"

    index = Pinecone.from_documents(docs, embeddings, index_name=index_name)
    st.session_state.indexed = index
    return index


# To get similar docs
def get_similiar_docs(index, query, k=2, score=False):
  if score:
    similar_docs = index.similarity_search_with_score(query, k=k)
  else:
    similar_docs = index.similarity_search(query, k=k)

    model_name = "gpt-3.5-turbo"
    # model_name = "gpt-4"
    llm = OpenAI(model_name=model_name)

    chain = load_qa_chain(llm, chain_type="stuff")

    
    answer = chain.run(input_documents=similar_docs, question=query)
    bot_response = answer  # Replace with your bot's response
    store_chat(query, bot_response)
    retrieve_and_display_chats()
    st.success("Message sent and stored!")
    return answer

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory= memory
    )

    return conversation_chain

def handel_userinput(user_question):
    
    similardocs = get_similiar_docs(st.session_state.indexed, user_question)
            

def store_chat(user_message, bot_response):
    ref = db.reference('chats')
    new_chat_ref = ref.push()  # Generates a new unique key
    new_chat_ref.set({
        'user_message': user_message,
        'bot_response': bot_response,
    })

def retrieve_and_display_chats():
    # Create a reference to the 'chats' node
    ref = db.reference('chats')
    
    # Retrieve all chat records from the 'chats' node
    chat_records = ref.get()
    chat_records = dict(reversed(list(chat_records.items())))
    
    # Display chat records in Streamlit app
    if chat_records:
        for chat_id, chat_data in chat_records.items():
            user = f"{chat_data['user_message']}"
            bot = f"{chat_data['bot_response']}"
            print(user)
            st.write(user_template.replace(
                "{{MSG}}", user), unsafe_allow_html=True)
            
            st.write(bot_template.replace(
                "{{MSG}}", bot), unsafe_allow_html=True)
            st.write("---")

def main():
    load_dotenv()
    st.set_page_config(page_title= "Chat with Multiple PDF", page_icon="books:")

    st.write(css, unsafe_allow_html=True)

    st.header("PDF Query Assistant (DSRAR):books:")
    user_question = st.text_input("Ask questions about your documents:")

    if st.button("Get answer"):
        handel_userinput(user_question)

    col1, col2 = st.columns([1,1])

    with col1:
        if st.button("Summarize your text Here"):
            subprocess.Popen(["streamlit", "run", "summary.py"])
    with col2:
        if st.button("Let's Play Quiz"):
            url = "https://www.codeconquest.com/coding-quizzes/"
            webbrowser.open_new_tab(url)

    st.write(bot_template.replace("{{MSG}}", "Hello how I can assit you today"), unsafe_allow_html=True)

    retrieve_and_display_chats() 
    
    with st.sidebar:
                st.subheader("Your Documents")

                #To store the contents of the pdf in pdf_docs variable
                pdf_docs = st.file_uploader("Upload your pdf's here and click on process" ,accept_multiple_files=True)

                # to process the pdf if button is pressed
                if st.button("Process"):
                    
                    with st.spinner("Analyzing your pdf please wait..."):
                            # 1. get the pdf text
                            raw_text = get_pdf_text(pdf_docs)

                            # 2. get the text chunks
                            text_chunks = get_text_chunks(raw_text)

                            # 3. create vector store
                            indexes = get_vectorstore(text_chunks)
                            st.success('Analyzed your pdf now you can ask the questions!!', icon="✅")

                    
if __name__ == '__main__':
    main()