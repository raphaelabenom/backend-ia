from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from models.evaluateEssay import State
from dotenv import load_dotenv
import os
import re

# Carregar variáveis de ambiente
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini")

# Funções
def extract_score(content: str) -> float:
    """Extrair a pontuação númerica da resposta do LLM."""
    match = re.search(r'Pontuação: \s*(\d+(.\d+)?)', content)
    if match:
        return float(match.group(1))
    raise ValueError(f"Não foi possível extrair a pontuação do texto: {content}")

def generate_corrections(state: State) -> State:
    """Gerar feedback de correção com base nas pontuações obtidas."""
    prompt = ChatPromptTemplate.from_template(
        "Com base nas pontuações fornecidas, forneça feedback detalhado sobre a redação. "
        "Inclua sugestões de melhoria para cada aspecto avaliado (relevância, gramática, estrutura e profundidade). "
        "Use as pontuações como guia para justificar suas observações.\n\n"
        "Relevância: {relevance_score} * 10 \n"
        "Gramática: {grammar_score} * 10 \n"
        "Estrutura: {structure_score} * 10 \n"
        "Profundidade: {depth_score} * 10 \n"
        "Redação: {essay}"
    )
    result = llm.invoke(prompt.format(
        relevance_score=state["relevance_score"],
        grammar_score=state["grammar_score"],
        structure_score=state["structure_score"],
        depth_score=state["depth_score"],
        essay=state["essay"]
    ))
    state["corrections"] = result.content
    return state

def check_relevance(state: State) -> State:
    """Verificar a relevância do texto."""
    prompt = ChatPromptTemplate.from_template(
        "Analise a relevância da seguinte redação em relação ao tema dado, prezando pela excelência da Língua Portuguesa. "
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
        "Analise a gramática da Língua Portuguesa na seguinte redação. "
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
workflow.add_node("check_relevance", check_relevance)
workflow.add_node("check_grammar", check_grammar)
workflow.add_node("analyze_structure", analyze_structure)
workflow.add_node("evaluate_depth", evaluate_depth)
workflow.add_node("calculate_final_score", calculate_final_score)
workflow.add_node("generate_corrections", generate_corrections)

workflow.add_conditional_edges(
    "check_relevance",
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
workflow.add_edge("calculate_final_score", "generate_corrections")
workflow.add_edge("generate_corrections", END)

workflow.set_entry_point("check_relevance")
app = workflow.compile()

# Função de avaliação
def grade_essay(essay: str) -> State:
    """Avaliar uma redação."""
    initial_state = State(
        essay=essay,
        relevance_score=0.0,
        grammar_score=0.0,
        structure_score=0.0,
        depth_score=0.0,
        final_score=0.0,
        corrections=""
    )
    result = app.invoke(initial_state)
    return result