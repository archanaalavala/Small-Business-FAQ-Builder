import streamlit as st

from document_store import store_documents
from rag_engine import generate_answer

st.set_page_config(
    page_title="Sweet Bites FAQ",
    page_icon="🧁",
    layout="centered"
)

st.title("🧁 Brew Bakes Bakery")

st.subheader("🌸 Your little business FAQ assistant")

st.write(
    "Hello! 💕 Ask me anything about our products, "
    "delivery, payments, opening hours and more."
)

st.divider()

with st.sidebar:

    st.header("🌷 Business Panel")

    st.write(
        "Manage your business knowledge base here."
    )

    st.divider()

    if st.button("📚 Load Business Information"):

        with st.spinner(
            "Loading business information... ✨"
        ):

            try:

                store_documents()

                st.success(
                    "Business information loaded! 💕"
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

    st.divider()

    st.info(
        """
        🤖 AI System

        🧠 Ollama  
        📖 RAG  
        🗂️ ChromaDB  
        💻 Streamlit
        """
    )

st.info(
    """
    🌸 Welcome to Brew Bakes Bakery!

    I'm here to help you with questions about:

    🧁 Products  
    🚚 Delivery  
    💰 Payments  
    🕐 Opening Hours  
    🔄 Returns & Refunds  
    🎂 Custom Orders
    """
)

if "messages" not in st.session_state:

    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

question = st.chat_input(
    "💬 Ask me something..."
)

if question:
    with st.chat_message("user"):

        st.write(question)
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )
    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking... 🌸"
        ):

            try:

                answer, sources = generate_answer(
                    question
                )

                st.write(answer)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )
                with st.expander(
                    "📖 View retrieved business information"
                ):

                    for index, source in enumerate(
                        sources
                    ):

                        st.write(
                            f"**🌷 Information {index + 1}**"
                        )

                        st.write(source)

                        if index < len(sources) - 1:

                            st.divider()

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )
st.divider()

st.subheader("🌼 Try asking")

st.write(
    "Click one of these questions to get started:"
)


example_questions = [
    "What products do you sell?",
    "Do you provide delivery?",
    "How much is delivery?",
    "What are your opening hours?",
    "Do you accept UPI?",
    "Can I return a custom cake?"
]

for question_text in example_questions:

    if st.button(
        f"💭 {question_text}",
        key=f"example_{question_text}"
    ):
        with st.chat_message("user"):

            st.write(question_text)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question_text
            }
        )

       
        with st.chat_message("assistant"):

            with st.spinner(
                "Finding your answer... ✨"
            ):

                try:

                    answer, sources = generate_answer(
                        question_text
                    )

                    st.write(answer)

                   
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                    with st.expander(
                        "📖 View retrieved information"
                    ):

                        for index, source in enumerate(
                            sources
                        ):

                            st.write(
                                f"**🌷 Information {index + 1}**"
                            )

                            st.write(source)

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )

st.divider()

st.caption(
    "🌸 Made with Ollama • RAG • ChromaDB • Streamlit 💕"
)



