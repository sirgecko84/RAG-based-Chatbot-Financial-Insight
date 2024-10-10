from dataclasses import dataclass
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain_aws import ChatBedrock
from rag_app.get_chroma_db import get_chroma_db
import cohere
from dotenv import load_dotenv
import os
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

BEDROCK_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"


@dataclass
class QueryResponse:
    query_text: str
    response_text: str
    sources: List[str]


def query_rag(query_text: str) -> QueryResponse:
    db = get_chroma_db()
    load_dotenv()
    co = cohere.Client(os.getenv("COHERE_API_KEY"))

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=25)
    data = [doc.page_content for doc, _score in results]
    # rerank the result
    rerank_data = co.rerank(query=query_text, documents=data, top_n=3, model='rerank-english-v3.0')
    final_results = []
    for result in rerank_data.results:
        final_results.append(data[result.index])
    # add context to prompt
    context_text = "\n\n---\n\n".join(final_results)
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = ChatBedrock(model_id=BEDROCK_MODEL_ID)
    response = model.invoke(prompt)
    response_text = response.content

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    print(f"Response: {response_text}\nSources: {sources}")

    return QueryResponse(
        query_text=query_text, response_text=response_text, sources=sources
    )


if __name__ == "__main__":
    query_rag("Tell me about the Culture of Sun* Inc?")