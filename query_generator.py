from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from mongodb_database import MongoDBDatabase

from langchain_groq import ChatGroq

# from pymongo import MongoClient
import os

load_dotenv()



# Set API keys
os.environ['groq_api_key'] = os.getenv('groq_api_key')
os.environ['MONGODB_URI'] = os.getenv('MONGODB_URI')


db = MongoDBDatabase("mongodb+srv://yugeshkaran01:GEMBkFW5Ny5wi4ox@blog.adtwl.mongodb.net/Blog-Data?retryWrites=true&w=majority&appName=blog", "Blog-Data")


# db.get_collection_schema('authors')

# # MongoDB connection
# client = MongoClient(os.getenv('MONGODB_URI'))
# db = client['Blog-Data']  # Replace with your database name
# collection = db['authors']  # Replace with your collection name


chat_history = []

def mogodb_query_generator(db:MongoDBDatabase,user_query:str, chat_history:list):
    
    template = """
You are a data analyst of a blog website. You are interacting with a user who is asking you questions about the blog app's database.
Based on the collection schema below, write a MongoDB query that would answer the user's question. Take the Conversation History into account.

<SCHEMA>{schema}</SCHEMA>

Conversation History: {chat_history}

Write only the MongoDB query and nothing else. Do not wrap the query in any other text, not even backticks.

For example:
Question: Show all the data?
MongoDB Query: collection.find{{}}

Question: total numeber of authors?
MongoDB Query:collection.distinct("authorname")

Question: total number of categories?
MongoDB Query: collection.distinct("posts.category")

Question: about the post Dimensionality Reduction?
MongoDB Query: collection.find({{'posts.title': 'Dimensionality Reduction'}})

Question: List of posts posted by author Yugesh Karan?
MongoDB Query:collection.find({{'authorname': "Yugesh Karan" }})

Question: display all the categories
MongoDB Query:collection.distinct("posts.category")

Question: how many followers author ajayvarsanr have?
MongoDB Query:collection.distinct("followers", {{"authorname": "ajayvarsanr"}})

Question: how many followers author ajayvarsan2020@gmail.com have?
MongoDB Query:collection.distinct("followers", {{"email": "ajayvarsan2020@gmail.com"}})

Question: how many post author ajayvarsanr posted?
MongoDB Query:collection.find({{'authorname': "ajayvarsanr"}}, {{'posts': 1, '_id': 0}})

Note:
- With the help of schema generate a executable MongoDB Query without any error and mustt not add length() or count() method anywhere in the query, i.e `collection.find({{'authorname': "Pradeep"}}, {{'posts': 1, '_id': 0}}).count()` or `collection.find({{'authorname': "Pradeep"}}, {{'posts': 1, '_id': 0}}).length()` and must not warp query with string.
- Do not escape characters like underscores (`_`) or slashes (`/`) in names, emails, description, category or any other data. eg:'posts.description': '/Unsupervised learning/i' or  'posts.description': /.*Supervised Learning.*/i .
- collection name is collection  not db.collection.
- Do not add length() and count() attribute to the query, i.e. no `collection.distinct("authorname").length()` or `collection.distinct("followers", {{"authorname": "ajayvarsanr"}}).length()` or `collection.count({{'authorname': 'ajayvarsanr', 'posts': {{'$ne': []}}}})` or `collection.distinct("followers", {{"authorname": "ajayvarsanr"}}).length()` or `collection.distinct("posts", {{"authorname": "ajayvarsanr"}}).length()`.
- Provide the data exactly as given without adding unnecessary characters.
- correct format for generating projection is {{'authorname': 'haricharan_1133', 'posts.title': 'Computer Vision'}}, {{'posts.$': 1, '_id': 0}} so you must take this fromat as your primary reference.
- should not generate the query in the format of {{'authorname': 'haricharan_1133' }}, {{'posts.title': 'Computer Vision', 'posts.$': 1, '_id': 0 }} or collection.find({{'authorname': "ajayvarsanr"}}, {{'posts': 1, '_id': 0}}).count().
- should not generate the query in the format of collection.distinct("authorname").length() or collection.distinct("followers", {{"authorname": "ajayvarsanr"}}).length().
- correct format for generating the total  is collection.distinct("authorname") or collection.distinct("posts.category") or collection.distinct("posts") or collection.distinct("followers", {{"authorname": "ajayvarsanr"}}).
- Do not use `.count()`, i.e. no collection.find({{'authorname': "ajayvarsanr"}}, {{'posts': 1, '_id': 0}}).count() or any other query with count().
- Follow all the above instruction and look the example Question and MongoDB Query before generating the query.

Your turn:
Question:{question}
MongoDB Query:
"""

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGroq(model_name="mixtral-8x7b-32768")

    chain = (
    RunnablePassthrough.assign(
        schema=lambda _: db.get_collection_schema('authors')  # Correct method call
    )
    | prompt
    | llm
    | StrOutputParser()
    )


    return chain.invoke({"question":user_query,"chat_history":chat_history})


while True:
    user_query = input('enter your query').strip()
    if user_query:
        chat_history.append(HumanMessage(content=user_query))

        query = mogodb_query_generator(db,user_query,chat_history)

        if query:
            chat_history.append(AIMessage(content=query))
        print(query)
        print("response",db.run('authors',query))

