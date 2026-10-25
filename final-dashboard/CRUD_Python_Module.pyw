from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username=None, passwd=None):
        # Initializing the MongoClient
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        if username is None and passwd is None:
            self.client = MongoClient(HOST, PORT)
        elif username is None or passwd is None:
            raise ValueError("Both username and passwd must be provided")
        else:
            uri = "mongo" + "db://%s:%s@%s:%d/" % (username, passwd, HOST, PORT)
            self.client = MongoClient(uri)
        self.database = self.client[DB]
        
    
    # === Method to implement the C in CRUD. 
    def create(self, data):
        if data is not None: 
            try: 
                result = self.database.animals.insert_one(data)  # data should be dictionary 
                return result.acknowledged
            except Exception as e:
                print(f"An error occurred during create: {e}")
                return False
        else: 
            raise Exception("Nothing to save, because data parameter is empty") 
            
            
    # === Method to implement the R in CRUD.
    def read(self, query=None):
        try:
            search_query = query if query is not None else {}
            cursor = list(self.database.animals.find(search_query))
            return cursor
        except Exception as e:
            print(f"An error occurred during query: {e}")
            return []

        
    # === Method to implement the U in CRUD.
    def update(self, query, data):
        if query is None or data is None:
            raise Exception("Query and data parameters cannot be empty")
        try:
            # Find all matching documents
            records = list(self.database.animals.find(query))
        
            if len(records) == 0: 
                return 0
    
            num_updated = 0
        
            # Update all matching
            for record in records:
                result = self.database.animals.update_one(
                    {"_id": record["_id"]},
                    {"$set": data}
                )
                num_updated += result.modified_count
        
            return num_updated
        except Exception as e:
            print(f"An error occurred during update: {e}")
            return 0
        
        
    # === Method to implement the D in CRUD.
    def delete(self, query):
        if query is None:
            raise Exception("Query parameter cannot be empty")
        try:
            result = self.database.animals.delete_one(query)
            return result.deleted_count > 0
        except Exception as e:
            print(f"An error occurred during delete: {e}")
            return False