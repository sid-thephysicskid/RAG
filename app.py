import streamlit as st
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone as PineconeClient
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain

def initialize_components():
    model_name = 'text-embedding-ada-002'
    embed = OpenAIEmbeddings(model=model_name, openai_api_key=st.secrets["OPENAI_API_KEY"])
    pc = PineconeClient(api_key=st.secrets["PINECONE_API_KEY"])
    text_field = "text"
    index_name = 'nec23-rag'
    index = pc.Index(index_name)
    vectorstore = PineconeVectorStore(index, embed, text_field)
    llm = ChatOpenAI(openai_api_key=st.secrets["OPENAI_API_KEY"], model_name='gpt-4-turbo-preview', temperature=0.0)
    qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever(search_kwargs={'k': 3}))
    return qa_with_sources

def main():
    st.set_page_config(page_title="MH NEC 2023 QnA App", page_icon=":question:")

    qa_with_sources = initialize_components()

    header = st.container()
    question_container = st.container()
    answer_container = st.container()

    with header:
        st.title("QnA App")
        st.markdown("Ask questions about the Mike Holt's National Electrical Code (NEC) 2023 Volumes 1 and 2.")

    with question_container:
        question = st.text_input("Ask:", key="question_input")
        col1, col2 = st.columns(2)
        with col1:
            ask_button = st.button("Get Answer")
        with col2:
            clear_button = st.button("Clear")

    if clear_button:
        st.session_state["question_input"] = ""
        answer_container.empty()

    if ask_button and question.strip() != "":
        with st.spinner("Generating answer..."):
            answer = qa_with_sources.invoke(question)
        with answer_container:
            st.markdown("#### Answer:")
            st.write(answer['answer'])
            st.markdown("#### Sources:")
            st.write(answer['sources'])
    elif ask_button:
        st.warning("Please enter a valid question.")


if __name__ == '__main__':
    main()