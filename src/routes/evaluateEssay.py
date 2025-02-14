
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import re

# Carregar variáveis de ambiente
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class State(TypedDict):
    """Representa o estado do processo de avaliação da redação."""
    essay: str
    relevance_score: float
    grammar_score: float
    structure_score: float
    depth_score: float
    final_score: float

llm = ChatOpenAI(model="gpt-4o-mini")

# Funções
def extract_score(content: str) -> float:
    """Extrair a pontuação númerica da resposta do LLM."""
    match = re.search(r'Pontuação: \s*(\d+(\.\d+)?)', content)
    if match:
        return float(match.group(1))
    raise ValueError(f"Não foi possível extrair a pontuação do texto: {content}")

def check_relavance(state: State) -> State:
    """Verificar a relevância do texto."""
    prompt = ChatPromptTemplate.from_template(
        "Analise a relevância da seguinte redação em relação ao tema dado, prezando pela excelência da Lingua Portuguesa. "
        "Forneça uma pontuação de relevância entre 0 e 1. "
        "Sua resposta deve começar com 'Pontuação: ' seguida da pontuação de númerica, "
        "depois forneça sua explicação.\n\nRedação: {essay}"
        )
    result = llm.invoke(prompt.format(essay=state["essay"]))
    try:
        state["relevance_score"] = extract_score(result.content)
    except ValueError as e:
        print(f"Erro ao extrair pontuação de relevância: {e}")
        state["relevance_score"] = 0.0
    return state

def check_grammar(state: State) -> State:
    """Verificar a gramática do texto."""
    prompt = ChatPromptTemplate.from_template(
        "Analise a gramática da Língua portuguesa na seguinte redação. "
        "Forneça uma pontuação de gramática entre 0 e 1. "
        "Sua resposta deve começar com 'Pontuação: ' seguida da pontuação de númerica, "
        "depois forneça sua explicação.\n\nRedação: {essay}"
        )
    result = llm.invoke(prompt.format(essay=state["essay"]))
    try:
        state["grammar_score"] = extract_score(result.content)
    except ValueError as e:
        print(f"Erro ao extrair pontuação de gramática: {e}")
        state["grammar_score"] = 0.0
    return state

def analyze_structure(state: State) -> State:
    """Analisar a estrutura do texto."""
    prompt = ChatPromptTemplate.from_template(
        "Analise a estrutura da redação em relação ao tema dado. "
        "Forneça uma pontuação de estrutura entre 0 e 1. "
        "Sua resposta deve começar com 'Pontuação: ' seguida da pontuação de númerica, "
        "depois forneça sua explicação.\n\nRedação: {essay}"
        )
    result = llm.invoke(prompt.format(essay=state["essay"]))
    try:
        state["structure_score"] = extract_score(result.content)
    except ValueError as e:
        print(f"Erro ao extrair pontuação de estrutura: {e}")
        state["structure_score"] = 0.0
    return state

def evaluate_depth(state: State) -> State:
    """Avaliar a profundidade da redação."""
    prompt = ChatPromptTemplate.from_template(
        "Analise a profundidade da redação em relação ao tema dado. "
        "Forneça uma pontuação de profundidade entre 0 e 1. "
        "Sua resposta deve começar com 'Pontuação: ' seguida da pontuação de númerica, "
        "depois forneça sua explicação.\n\nRedação: {essay}"
        )
    result = llm.invoke(prompt.format(essay=state["essay"]))
    try:
        state["depth_score"] = extract_score(result.content)
    except ValueError as e:
        print(f"Erro ao extrair pontuação de profundidade: {e}")
        state["depth_score"] = 0.0
    return state

def calculate_final_score(state: State) -> State:
    """Calcular a pontuação final da redação."""
    state["final_score"] = (
        state["relevance_score"] * 0.3 +
        state["grammar_score"] * 0.2 +
        state["structure_score"] * 0.2 +
        state["depth_score"] * 0.3
    )
    return state

workflow = StateGraph(State)

workflow.add_node("check_relavance", check_relavance)
workflow.add_node("check_grammar", check_grammar)
workflow.add_node("analyze_structure", analyze_structure)
workflow.add_node("evaluate_depth", evaluate_depth)
workflow.add_node("calculate_final_score", calculate_final_score)

workflow.add_conditional_edges(
    "check_relavance",
    lambda x: "check_grammar" if x["relevance_score"] > 0.5 
    else "calculate_final_score"
    )

workflow.add_conditional_edges(
    "check_grammar",
    lambda x: "analyze_structure" if x["grammar_score"] > 0.6 
    else "calculate_final_score"
    )

workflow.add_conditional_edges(
    "analyze_structure",
    lambda x: "evaluate_depth" if x["structure_score"] > 0.7 
    else "calculate_final_score"
    )

workflow.add_conditional_edges(
    "evaluate_depth",
    lambda x: "calculate_final_score"
    )

workflow.set_entry_point("check_relavance")
workflow.add_edge("calculate_final_score", END)

app = workflow.compile()

# função de avaliação
def grade_essay(essay: str) -> State:
    """Avaliar uma redação."""
    initial_state = State(
        essay=essay,
        relevance_score=0.0,
        grammar_score=0.0,
        structure_score=0.0,
        depth_score=0.0,
        final_score=0.0
    )
    result = app.invoke(initial_state)
    return result