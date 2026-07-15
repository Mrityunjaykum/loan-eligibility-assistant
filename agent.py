from langchain_ollama import ChatOllama
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_classic.tools.retriever import create_retriever_tool
from langchain_classic.memory import ConversationBufferMemory
from eligibility_checker import check_eligibility
from retriever import get_retriever
 
@tool
def eligibility_tool(applicant_data: dict):
    """Useful for checking if a customer is eligible for a loan."""
    return check_eligibility(applicant_data)
 
retriever = get_retriever()
policy_tool = create_retriever_tool(
    retriever,
    "loan_policy_search",
    "Searches for bank loan eligibility policy documents."
)
 
tools = [eligibility_tool, policy_tool]
llm = ChatOllama(model="llama3.1", temperature=0)
 
# The 'chat_history' variable here is what the memory will inject
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful loan assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
 
# Initialize memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)
 
agent = create_tool_calling_agent(llm, tools, prompt)
 
# Link memory to the executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory
)
 
print("System initialized with automatic conversation memory.")