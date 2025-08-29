from pymongo import MongoClient

class MongoDBDatabase:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection_schema(self, collection_name):
        # Example method to get a sample document to infer schema
        sample_document = self.db[collection_name].find_one()
        return sample_document if sample_document else "No schema available"

    def run(self, collection_name, query ):
        # Example method to execute a MongoDB query
        collection = self.db[collection_name]
        # results = list(collection.find({'authorname': 'Yugesh Karan', 'posts.title': 'Dimensionality Reduction'}, {'posts.$': 1, '_id': 0}))
        # results =list(collection.find({'authorname': "haricharan_1133"}))
        # results =list(collection.find({'authorname': 'Yugesh Karan'}))
        # results =list(collection.find({'authorname': 'Yugesh Karan'}))
        # results =list(collection.distinct("authorname"))
        # results =list(collection.find({ 'posts.title': 'Dimensionality Reduction' }))
        
        results =list(eval(query))
        return results
    

    # def run(self, collection_name, query):
    #     collection = self.db[collection_name]

    #     if query == "unset_announcement_all":
    #         result = collection.update_many(
    #             {},  # This means update all documents
    #             {"$unset": {"announcementSchema": ""}}
    #         )
    #         results = {
    #             "matched_count": result.matched_count,
    #             "modified_count": result.modified_count,
    #             "acknowledged": result.acknowledged
    #         }
    #         return results

    #     elif query == "distinct_authorname":
    #         return collection.distinct("authorname")

    #     else:
    #         return "Invalid query"



# Usage Example
# db = MongoDBDatabase("mongodb://localhost:27017", "your_database_name")