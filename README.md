# Streamlit Connections Hackathon - Qdrant Connection Demo App

## Introduction
Welcome to the Streamlit Connections Hackathon! In this hackathon, I have built a custom connection for Qdrant, a vector database, using Streamlit's experimental connection feature (`st.experimental_connection`). Qdrant is a powerful tool for managing vector data, and with this custom connection, you can easily integrate it into your Streamlit apps with just a few lines of code.

## Qdrant Connection - `qdrant_connection.py`
The heart of this demo app lies in the custom Qdrant connection implemented in `qdrant_connection.py`. The Qdrant connection is a class that extends the built-in `ExperimentalBaseConnection` provided by Streamlit. It allows you to connect your Streamlit app to the Qdrant database in just a few lines of code.

The key components of the Qdrant connection are:
- `_connect()` method: This method sets up and returns the underlying QdrantClient object. It retrieves the connection parameters, such as the Qdrant API URL and API key, from Streamlit's `st.secrets` to ensure secure management of credentials.
- Convenience methods: The connection includes several methods for interacting with the Qdrant database, such as `get_collections()`, `list_collection_aliases()`, `update_collection_aliases()`, `get_aliases()`, `create_collection()`, `recreate_collection()`, `update_collection()`, and `delete_collection()`. These methods provide easy access to essential functionalities of the QdrantClient.

By using this custom Qdrant connection, you can seamlessly connect your Streamlit app to Qdrant and perform various operations on the vector data.

## Demo App - `app.py`
The demo app, hosted at [Streamlit Connections Demo](https://experimental.streamlit.app/), allows users to test out the Qdrant connection in conjunction with the Open AI API.

### Qdrant API Connection
In the "Qdrant API" tab on the sidebar, users can enter their Qdrant API key. The app validates the API key and establishes a connection to the Qdrant database using the custom Qdrant connection.

### Open AI API (Optional)
In the "Open AI API" tab on the sidebar, users can provide their Open AI API key to enable the chat feature. If the key is valid, the app will show a success message and activate the Open AI language model.

### Qdrant Collections
In the "Qdrant Collections" tab, users can create, view, and delete collections in the Qdrant database. The app uses the custom Qdrant connection to perform these operations.

### Querying Documents using Qdrant and Open AI
With the Open AI API enabled, users can query documents stored in the Qdrant database using the chat feature. The app splits the input text into chunks, adds them to the selected Qdrant collection, and then uses the Open AI language model to provide relevant responses to the queries.

## Conclusion
With this demo app and the custom Qdrant connection, users can easily test the integration of Qdrant and the Open AI language model in their Streamlit apps. The custom Qdrant connection, implemented using `st.experimental_connection`, simplifies the process of connecting to Qdrant and accessing its functionalities.

The app demonstrates the power and flexibility of Streamlit's experimental connection feature and how it can be leveraged to build efficient and robust Streamlit apps. I hope you find this app and the Qdrant connection useful for your data management and analysis needs.

Feel free to explore, experiment, and enhance the app further to suit your specific use cases. Thank you for participating in the Streamlit Connections Hackathon, and happy Streamlit-ing! :balloon:
