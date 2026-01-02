import chromadb
import uuid

class VectorDB:
    def __init__(self, db_path="./chroma_db"):
        """
        Initializes the ChromaDB client and collection.
        """
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="agent_cache")

    def save_query_response(self, query, response):
        """
        Saves a query and its corresponding response to the vector database.
        """
        self.collection.add(
            documents=[query],
            metadatas=[{"response": response}],
            ids=[str(uuid.uuid4())]
        )

    def get_cached_response(self, query, distance_threshold=0.5):
        """
        Retrieves a cached response if a similar query exists.
        Returns the response string if found, otherwise None.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=1
        )

        # Check if we have results and if the distance is within the threshold
        # Lower distance means higher similarity
        if results['documents'] and results['distances'] and len(results['distances'][0]) > 0:
            distance = results['distances'][0][0]
            if distance < distance_threshold:
                return results['metadatas'][0][0]['response']
        
        return None

if __name__ == "__main__":
    db = VectorDB()
    db.save_query_response("What is the weather in London?", "The weather in London is 15°C.")
    print(f"Cached: {db.get_cached_response('What is the weather in London?')}")
    print(f"Similar: {db.get_cached_response('weather London')}")
