from streamlit.connections import ExperimentalBaseConnection
from qdrant_client import QdrantClient
import streamlit as st
import os


os.environ['QDRANT_HOST'] = ''
os.environ['QDRANT_API_KEY'] = ''


class QdrantConnection(ExperimentalBaseConnection[QdrantClient]):
    def _connect(self, **kwargs) -> QdrantClient:
        # Retrieve the connection parameters from st.secrets
        conn_params = st.secrets["connections"]["qdrant_connection"]

        url = conn_params.get("url")
        api_key = os.getenv('QDRANT_API_KEY')

        if not url or not api_key:
            raise ValueError("QDRANT_HOST or QDRANT_API_KEY is missing in secrets.toml")

        return QdrantClient(url=url, api_key=api_key)

    def get_collections(self) -> QdrantClient:
        return self.get_collections()

    def list_collection_aliases(self) -> QdrantClient:
        return self.list_collection_aliases()

    def update_collection_aliases(self) -> QdrantClient:
        return self.update_collection_aliases()

    def get_aliases(self) -> QdrantClient:
        return self.get_aliases()

    @st.cache_data
    def create_collection(self) -> QdrantClient:
        return self.create_collection()

    def recreate_collection(self) -> QdrantClient:
        return self.recreate_collection()

    def update_collection(self) -> QdrantClient:
        return self.update_collection()

    def delete_collection(self):
        return self.delete_collection()




