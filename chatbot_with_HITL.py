from langgraph.graph import StateGraph, START
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langgraph.types import interrupt, Command
from dotenv import load_dotenv
import requests
load_dotenv()
llm = ChatOpenAI()
@tool
def get_stock_price(symbol:str)->dict:
    """Fetch latest stock price for a given symbol(eg. 'AAPL','TSLA')
    using Alpha Vantage API key in the URL."""
    url = (
        "https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    )
    r=requests.get(url)
    return r.json()
@tool
def purchase_stock(symbol: str, quantity: int) -> dict:
    """
       Simulate purchasing a given quantity of a stock symbol.

       HUMAN-IN-THE-LOOP:
       Before confirming the purchase, this tool will interrupt
       and wait for a human decision ("yes" / anything else).
       """
    decision=interrupt(f"Approve buying {quantity}Shares of {symbol}?(yes/no)")
    if isinstance(decision,str) and decision.lower()=="yes":
        return{
            "status": "success",
            "message": f"Purchased {quantity} shares of {symbol}",
            "symbol":symbol,
            "quantity": quantity,
        }
    else:
        return {
            "status": "cancelled",
            "message": f"Purchase of {quantity} shares of {symbol} was declined by human.",
            "symbol": symbol,
            "quantity": quantity,
        }
tools=[get_stock_price,purchase_stock]
llm_with_tools=llm.bind_tools(tools)
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatState):
    """LLM node that may answer or request a tool call."""
    messages = state["messages"] #Take all the messages from the conversation history
    response = llm_with_tools.invoke(messages)#Send the conversation history to the LLM and let it decide whether it should answer directly or use a tools
    return {"messages": [response]}#Add the LLM's response back into the graph state.

#chat_node sends the conversation state to the LLM. The LLM decides whether to answer directly or generate a tool call. ToolNode executes the requested tools and returns their outputs to the graph. Together, they enable an AI agent to reason, use external tools, and produce a final response
tool_node=ToolNode(tools)
# checkpointer
memory = MemorySaver()# MemorySaver is a class
# memory is Object Its job is to remember the graph state between interactions.

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")

graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

chatbot = graph.compile(checkpointer=memory)
