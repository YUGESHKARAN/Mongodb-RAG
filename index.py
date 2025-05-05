import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from mongodb_database import MongoDBDatabase
import google.generativeai as genai
import os


load_dotenv()

# Set API keys
# os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ['MONGODB_URI'] = os.getenv('MONGODB_URI')
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def gemini_runnable(input_text):
    """Function to call Gemini model with improved error handling"""
  

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
   
    try:
        # Ensure input is a string
        if isinstance(input_text, tuple):
            # If it's a tuple, convert to a string
            input_text = str(input_text)
        
        # Ensure input is a string
        if not isinstance(input_text, str):
            input_text = str(input_text)
        
        # Generate content
        response = model.generate_content(input_text)
        
        # Return text response
        return response.text if response and hasattr(response, 'text') else "No response from model"
    except Exception as e:
        print(f"Error in Gemini model: {e}")
        return f"Error occurred while generating content: {str(e)}"

# Wrap the function in a RunnableLambda for LangChain
gemini_model = RunnableLambda(gemini_runnable)


app = Flask(__name__)

CORS(app)

db = MongoDBDatabase("mongodb+srv://yugeshkaran01:GEMBkFW5Ny5wi4ox@blog.adtwl.mongodb.net/Blog?retryWrites=true&w=majority&appName=blog", "Blog")

chat_history = []

def mogodb_query_generator(db):
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

Question: When last post was posted and name the author?
MongoDB Query: collection.find({{}}, {{'posts.timestamp': 1, 'authorname': 1, '_id': 0}}).sort({{'posts.timestamp': -1}}).limit(1)

Question: Posts on GenAI category?
MongoDB Query: collection.find({{ 'posts.category': 'GenAI' }})

Question: name the author who published post in both Data Science and GenAI categories?
MongoDB Query: collection.find({{"posts.category": {{"$in": ["Data Science", "GenAI"]}}}})


Note:
- With the help of schema generate a executable MongoDB Query without any error and mustt not add length() or count() method anywhere in the query, i.e `collection.find({{'authorname': "Pradeep"}}, {{'posts': 1, '_id': 0}}).count()` or `collection.find({{'authorname': "Pradeep"}}, {{'posts': 1, '_id': 0}}).length()` and must not warp query with string and should not use findOne() method insted use, collection.find({{}}, {{'authorname': 1, 'password': 0, 'email': 0, 'profile': 0, 'otp': 0, 'otpExpiresAt': 0, 'followers': 0, '__v': 0}}).
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
    


    return (
        RunnablePassthrough.assign(
            schema=lambda _: db.get_collection_schema('authors')
        )
        | prompt
        | gemini_model
        | StrOutputParser()
    )


def response_generator(user_query: str, db: MongoDBDatabase, chat_history: list):
    # Generate the MongoDB query using the query generator
    mongo_chain = mogodb_query_generator(db)

    template = """
    You are a copilot for a blog website. You are interacting with a chief who is asking you questions about the blog's database to generate content, statistics measure or required infromation from the database based on user query.
    Based on the collection schema below, cheif question, MongoDB query, and MongoDB response, write a natural language response with pre-size. 
    note:
    1. Generate the content as per the conversation history and MongoDB response.
    2. Make sure to format the response as paragraph.
    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}
    MongoDB Query: <QUERY>{query}</QUERY>
    User Question: {question}
    MongoDB Response: {response}

    If the MongoDB response is not empty, confirm the existence of the post and author and show the post content.
    If the MongoDB response is empty, inform the user that the post wasn't found or suggest alternative searches.
    """


    # Initialize the LLM (Large Language Model)
    

    # Create the prompt with the template
    prompt = ChatPromptTemplate.from_template(template)

    # Define the chain
    chain = (
        RunnablePassthrough.assign(query=mongo_chain)  # Ensure query is passed correctly
        .assign(
            schema=lambda _: db.get_collection_schema('authors'),
            response=lambda var: db.run('authors',var['query'])  # Ensure query is passed as a dictionary
        )
        | prompt
        | gemini_model
        | StrOutputParser()
    )

    # Execute the chain and return the result
    return chain.invoke({"question": user_query, "chat_history": chat_history})


@app.route("/")
def welcome_blog_backend():
    return "Welcome to Blog Browser"

@app.route("/query-rag",methods=['POST'])
def query_MongoDB_RAG():
    
    data = request.json
    user_query = data.get("query","")
    if user_query:
        chat_history.append(HumanMessage(content=user_query))

        response = response_generator(user_query, db, chat_history)

        if response:
            chat_history.append(AIMessage(content=response))

        return jsonify({"response":response})

if __name__ == "__main__":
    app.run(port=3500, host="0.0.0.0", debug=False)


