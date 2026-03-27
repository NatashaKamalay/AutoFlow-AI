from langchain_google_genai import ChatGoogleGenerativeAI


def answer_question(vectorstore, question: str) -> str:
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash",
        temperature=0
    )

    prompt = f"""
You are a knowledge agent for enterprise workflow analysis.

Answer the user's question only from the context below.
If the answer is not available in the context, say:
"Answer not found in the uploaded content."

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)
    return response.content