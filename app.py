import time
import streamlit as st
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from qdrant_client import http
from qdrant_openapi_client.exceptions import UnexpectedResponse
import os


def main():
    with st.sidebar:
        tab1, tab2, tab3 = st.tabs(["Qdrant API", "Open AI API", "Collections"])

        with tab1:
            st.subheader("Qdrant API 🔑")
            qdrant_api_key = st.text_input("Please enter your Qdrant API Key: ", type="password")
            if qdrant_api_key != '':
                try:
                    os.environ['QDRANT_API_KEY'] = qdrant_api_key

                    qdrant_conn = st.experimental_connection("qdrant_connection")

                    # Now you can use the QdrantClient instance through the connection object
                    qdrant_client = qdrant_conn._instance
                    st.success("Thanks mate, You're in!", icon="⚡️")
                    placeholder_qdrant_api = st.empty()
                    placeholder_qdrant_api.image(
                        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXV1d2I2aDgwMTJ4NGJkNWs5Mzg5NzVhbDNvcWNvZzV1dG4ycHMzciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/tlGD7PDy1w8fK/giphy.gif")
                    time.sleep(3)
                    placeholder_qdrant_api.empty()
                except ValueError:
                    st.warning("Please enter a valid API Key and try again!", icon="🤖")
                    placeholder_valueerror = st.empty()
                    placeholder_valueerror.image(
                        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmNpYzZrN3NmeWg3c2pwNWU1ZHc4MnhnNDYzOG92dnY0d2Q4dnV2aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ljtfkyTD3PIUZaKWRi/giphy.gif")
                    time.sleep(5)
                    placeholder_valueerror.empty()
            else:
                st.info("Please enter a valid API Key to access Qdrant", icon="🗝️")

        with tab2:
            st.subheader("Qdrant API 🗝️")
            open_ai_api = st.text_input("Please enter your Open AI Api Key: ", type="password")
            if open_ai_api:
                try:
                    os.environ['OPENAI_API_KEY'] = open_ai_api
                    placeholder_openai_key = st.empty()
                    placeholder_openai_key.image(
                        "https://media2.giphy.com/media/BpGWitbFZflfSUYuZ9/giphy.gif?cid=ecf05e471yrng589z3czqyc6994yahj5l2nyn6km3snkl5t0&ep=v1_gifs_search&rid=giphy.gif&ct=g")
                    time.sleep(5)
                    placeholder_openai_key.empty()
                except:
                    st.warning("Hmmm something went wrong 🤔 Please check you entered a valid Open AI API Key",
                               icon="🔐")
            else:
                st.info("🗝️ Please enter a valid API Key to access Open AI chat features")

        with tab3:
            st.subheader("Qdrant Collections")
            selection_qdrant = st.selectbox(
                "Choose one of these options:",
                ("Create Collection", "Get All Collections", "Delete Collection"),
                placeholder="Waiting..."
            )

            if selection_qdrant == "Create Collection":
                with st.form("Create New Collection", clear_on_submit=True):
                    collection_name = st.text_input("Name your new collection: ",
                                                    placeholder="Has to be a unique name...")
                    submitted = st.form_submit_button("Add Collection!")
                    if submitted:
                        try:
                            vectors_config = http.models.VectorParams(
                                size=1536,
                                distance=http.models.Distance.COSINE,
                            )

                            qdrant_client.create_collection(
                                collection_name=collection_name,
                                vectors_config=vectors_config,
                            )

                            st.success(f"The Collection titled '{collection_name}' has been created!", icon="🙌")

                        except UnexpectedResponse:
                            st.warning(
                                f"This collection name already exists. \nPlease choose a unique colelction name, or delete collection '{collection_name}'!",
                                icon="🚨")
                        except UnboundLocalError:
                            st.warning(
                                "Looks like you haven't entered an API key? Something is wrong...please take a few steps back and try again!",
                                icon="🔙")

            if selection_qdrant == "Get All Collections":
                collections = qdrant_client.get_collections().dict()["collections"]
                for i in collections:
                    st.write(f"- {i['name']}")

            if selection_qdrant == "Delete Collection":
                collections = qdrant_client.get_collections().dict()["collections"]
                collection_to_delete = st.selectbox(label="Please choose a collection to delete:",
                                                    options=[i['name'] for i in collections])
                delete_button = st.button("Delete!")
                if delete_button:
                    qdrant_client.delete_collection(collection_name=f"{collection_to_delete}")
                    st.success(f"Collection '{collection_to_delete}' has been deleted!", icon="💨")

    st.header("Query a Document using Qdrant and Open AI")

    if open_ai_api:
        try:
            os.environ['OPENAI_API_KEY'] = open_ai_api
            collections = qdrant_client.get_collections().dict()["collections"]
            collection_to_store = st.selectbox(
                label="Please choose a collection to store the text you wish to query:",
                options=[i['name'] for i in collections])
            embeddings = OpenAIEmbeddings()

            vector_store = Qdrant(
                client=qdrant_client,
                collection_name=collection_to_store,
                embeddings=embeddings,
            )

            def get_chunks(text):
                text_splitter = CharacterTextSplitter(
                    separator='\n',
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len
                )

                chunks = text_splitter.split_text(text)
                return chunks

            raw_text = st.text_area(label="Paste some text here")
            if raw_text != "":
                texts = get_chunks(raw_text)
                vector_store.add_texts(texts)

            # Plug Vector store into retrieval chain

            qa = RetrievalQA.from_chain_type(
                llm=OpenAI(),
                chain_type='stuff',
                retriever=vector_store.as_retriever()
            )

            with st.chat_message("assistant"):
                st.write("Hello 👋 Ask me something about this text: ")
            query = st.chat_input("Ask GPT something about this text: ")

            # query = st.text_input("Ask GPT something about this text: ")
            if query:
                with st.chat_message("user"):
                    st.write(query)
                response = qa.run(query)
                with st.chat_message("assistant"):
                    st.write(response)
        except:
            st.warning("Hmmm something went wrong 🤔 Please check you entered a valid Open AI API Key", icon="🔐")
    else:
        st.info("🗝️ Please enter a valid API Key to access Open AI chat features")
        placeholder_query_document = st.empty()
        placeholder_query_document.image(
            "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXB2YWNndGJrNTZhMmN0MXBzdmRhMGo3eDcwOTE4aGE4emtibDQ5eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/k7LvfbDPWR0Uxcqm6f/giphy.gif")
        time.sleep(5)
        placeholder_query_document.empty()


if __name__ == "__main__":
    main()
