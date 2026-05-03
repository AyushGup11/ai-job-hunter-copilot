from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 🔥 Use local embeddings (FREE + fast)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 🧠 Skill Knowledge Base
SKILL_DOCS = [

# 🔹 Programming
"Python is used for machine learning, backend development, scripting, and data science. Related: FastAPI, Pandas, NumPy.",
"JavaScript is used for frontend and backend development. Related: React, Node.js.",
"TypeScript is a typed superset of JavaScript used for scalable frontend apps.",
"C++ is used for system programming, competitive programming, and performance-critical applications.",
"Java is used in enterprise applications and backend systems. Related: Spring Boot.",
"Go (Golang) is used for scalable backend systems and microservices.",

# 🔹 Backend & APIs
"FastAPI is used for building high-performance APIs using Python. Related: REST APIs, async programming.",
"Django is a Python web framework used for backend development and full-stack apps.",
"Flask is a lightweight Python framework for APIs and microservices.",
"Node.js is used for backend JavaScript development. Related: Express.js.",
"REST APIs are used for communication between frontend and backend systems.",
"GraphQL is an API query language for flexible data fetching.",

# 🔹 Databases
"MySQL is a relational database used in web applications.",
"PostgreSQL is an advanced relational database with strong performance.",
"MongoDB is a NoSQL database used for flexible data storage.",
"Redis is an in-memory database used for caching and fast retrieval.",
"Vector databases (FAISS, Chroma) are used for similarity search in AI systems.",

# 🔹 DevOps & Deployment
"Docker is used for containerization and application deployment.",
"Kubernetes is used for container orchestration and scaling.",
"CI/CD pipelines automate testing and deployment.",
"GitHub Actions is used for CI/CD automation.",
"Nginx is used as a web server and reverse proxy.",

# 🔹 Cloud
"AWS is a cloud platform used for deployment, storage, and scalable infrastructure.",
"Azure is a cloud platform with strong enterprise AI integration.",
"Google Cloud Platform (GCP) provides cloud computing and ML services.",
"AWS Lambda enables serverless computing.",
"S3 is used for object storage in AWS.",

# 🔹 Machine Learning
"Machine Learning involves training models using data. Related: scikit-learn, regression, classification.",
"Supervised learning uses labeled data for training models.",
"Unsupervised learning finds patterns in unlabeled data.",
"Model evaluation uses metrics like accuracy, precision, recall.",
"Feature engineering improves model performance.",

# 🔹 Deep Learning
"Deep Learning uses neural networks for complex tasks. Related: CNN, RNN, transformers.",
"PyTorch is a deep learning framework for research and production.",
"TensorFlow is used for large-scale ML systems.",
"CNNs are used for image processing tasks.",
"RNNs are used for sequential data like time series.",

# 🔹 NLP & LLMs
"Natural Language Processing (NLP) focuses on text understanding and generation.",
"Transformers are deep learning models used in LLMs.",
"BERT is used for text understanding tasks.",
"GPT models are used for text generation.",
"LLMs (Large Language Models) power chatbots and AI assistants.",

# 🔹 GenAI / RAG
"RAG (Retrieval Augmented Generation) combines LLMs with external knowledge retrieval.",
"LangChain is used for building LLM pipelines and chaining prompts.",
"LlamaIndex is used for indexing and querying documents with LLMs.",
"Prompt engineering improves LLM responses.",
"Embeddings convert text into vector representations for similarity search.",

# 🔹 Data Science
"Pandas is used for data manipulation and analysis.",
"NumPy is used for numerical computations.",
"Matplotlib is used for data visualization.",
"Seaborn provides advanced statistical visualizations.",
"EDA (Exploratory Data Analysis) helps understand datasets.",

# 🔹 MLOps
"MLOps focuses on deploying and maintaining ML models in production.",
"Model versioning tracks changes in ML models.",
"Monitoring ensures model performance in production.",
"ML pipelines automate training and deployment.",
"Docker and Kubernetes are used in ML deployment.",

# 🔹 System Design
"Microservices architecture breaks applications into small services.",
"Monolith architecture is a single unified application.",
"Load balancing distributes traffic across servers.",
"Caching improves performance using Redis or memory stores.",
"Scalability ensures system handles increasing load.",

# 🔹 Security
"Authentication verifies user identity.",
"Authorization controls access to resources.",
"JWT is used for secure authentication.",
"OAuth enables third-party authentication.",
"HTTPS ensures secure communication.",

# 🔹 Frontend
"React is used for building modern frontend applications.",
"Next.js is a React framework with server-side rendering.",
"HTML is used for structuring web pages.",
"CSS is used for styling web applications.",
"Tailwind CSS is a utility-first CSS framework.",

# 🔹 Testing
"Unit testing verifies individual components.",
"Integration testing ensures components work together.",
"PyTest is used for testing Python applications.",
"Jest is used for testing JavaScript applications.",
"Selenium is used for browser automation testing.",

# 🔹 Data Engineering
"ETL pipelines extract, transform, and load data.",
"Apache Spark processes large-scale data.",
"Kafka is used for real-time data streaming.",
"Airflow is used for workflow orchestration.",
"Data warehouses store structured data for analytics.",

# 🔹 Misc
"Git is used for version control.",
"Linux is used for server environments.",
"Bash scripting automates tasks in Unix systems.",
"Agile methodology focuses on iterative development.",
"Scrum is a framework for agile project management.",

]

# 🔧 Build FAISS index
def create_vector_store():
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    docs = splitter.create_documents(SKILL_DOCS)
    return FAISS.from_documents(docs, embedding_model)

# 🔍 Retrieve context
def retrieve_context(vector_db, query, k=4):
    docs = vector_db.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in docs])
