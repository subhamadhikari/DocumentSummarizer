from datetime import datetime
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from sympy import are_similar
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from difflib import SequenceMatcher

api_key = "AIzaSyAh4lGJWKH8wp8XSde624-lJtIssYv-Bj0"

class Chatbot:

    def __init__(self, model_name, temperature, vectors):
        self.model_name = model_name
        self.temperature = temperature
        self.vectors = vectors
        # self.chat_history = []
        self.chat_history = {}

    # def conversational_chat(self, query, conversation_id, session_id):
    #     """
    #     Starts a conversational chat with a model via Langchain
    #     """
        
    #     self.chat_history.extend([{"session_id":session_id, "conversation_id":conversation_id, "role": "user", "content": query, "timestamp":datetime.utcnow().isoformat()}])
    #     chain = ConversationalRetrievalChain.from_llm(
    #         llm=ChatGoogleGenerativeAI(model=self.model_name, 
    #                        temperature=self.temperature, 
    #                        google_api_key=api_key),
    #         memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True),
    #         retriever=self.vectors.as_retriever(),
    #     )

    #     result = chain({"question": query, "chat_history": self.chat_history})
    #     answer = result["answer"]

    #     self.chat_history.extend([{"session_id":session_id, "conversation_id":conversation_id, "role": "assistant", "content": result["answer"], "timestamp":datetime.utcnow().isoformat()}])
    #     for hist in self.chat_history:
    #         print(hist)
    #     return answer

    # def similar(self,response, document_context, threshold=0.2)->bool:
    #     document_texts = [doc.page_content for doc in document_context]
    #     return any(SequenceMatcher(None, response, doc_text).ratio() > threshold for doc_text in document_texts)
    
    def conversational_chat(self, query, conversation_id, session_id):
        """
        Starts a conversational chat with a model via Langchain
        """
        system_prompt = (
            "You are an assistant for question-answering tasks based solely on the given document context. "
            "Your responses should always be directly based on the retrieved context from the document. "
            "If the answer to a question is not found in the provided context, respond with: "
            "'Sorry, I am unaware of that.' "
            "Under no circumstances should you provide answers that are not directly extracted from the document context, "
            "and you must not engage in general conversation, jokes, or any other topic not covered by the document. "
            "Do not respond to greetings, small talk, or any question that deviates from the document's content. "
            "Do not offer opinions, ask questions, or suggest actions. Your sole purpose is to provide answers based on the document content. "
            "You should not respond with casual or conversational language; stick strictly to factual and document-based responses. "
            "Ensure all your responses are concise, limited to three sentences maximum, and strictly relevant to the context."
            "\n\n"
            "{context}"
                )
        # system_prompt = (
        #     "You are an assistant for question-answering tasks based on the given context only."
        #     "Beyond the context if you get any question, just tell that you do not know"
        #     "Do not answer any questions or do anything that are not covered in the provided context. Be strict about it."
        #     "For example, if the document is about computer science then answer the question based upon the provided document"
        #     "In this case, if the user asks about some question which is not available in the document. Ask to provide relevant document"
        #     """
        #         Answer the question possible from the provided context, make sure to provide the details, if the answer is not in
        #         provided context just say, "Sorry, I am unaware of that.", don't provide the wrong answer
        #     """
        #     "Do not provide answer to those questions which are beyond the provided context at any case."
        #     "Restrict yourself to the provied context only."
        #     "Do not provide answers based on general knowledge or assumptions. "
        #     "Do not answer questions that are beyond the provided context, no matter what."
        #     "Use the following pieces of retrieved context to answer "
        #     "the question. Use three sentences maximum and keep the "
        #     "answer concise."
        #     "\n\n"
        #     "{context}"
        #         )
        contextualize_q_system_prompt = (
            "Given a chat history, and the latest user question "
            "which might reference context in the chat history AND PROVIDED DOCUMENT, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        
        llm=ChatGoogleGenerativeAI(model=self.model_name, 
                           temperature=self.temperature, 
                           google_api_key=api_key)
        retriever=self.vectors.as_retriever()

        context = self.vectors.as_retriever().get_relevant_documents(query)
        print("Retrieved Context:", context)

        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )


        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
                
            ]
        )

        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        def get_session_history(session_id: str) -> BaseChatMessageHistory:
            if session_id not in self.chat_history:
                self.chat_history[session_id] = ChatMessageHistory()
            return self.chat_history[session_id]


        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        answer = conversational_rag_chain.invoke(
            {"input": query},
            config={
                "configurable": {"session_id": session_id}
            },  # constructs a key "abc123" in `store`.
        )["answer"]

        # if "Sorry" not in answer and not self.similar(answer, context):
            # answer = "Sorry, I can only assist with information found in the provided document."

        return answer
        