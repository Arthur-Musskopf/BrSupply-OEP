from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.memory import ConversationBufferMemory

llm = ChatOpenAI(model="gpt-4o", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

retriever = PineconeVectorStore.from_existing_index(
    index_name="brsupply-sac-agent",
    namespace="documentos-informativos",
    embedding=embeddings
).as_retriever()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

rag_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory
)
