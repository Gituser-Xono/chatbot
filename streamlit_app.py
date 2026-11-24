
import streamlit as st
from google import genai

# Show title and description
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot powered by Google Gemini AI. "
    "Enter your Gemini API key to start chatting."
)

# Get Gemini API key
gemini_api_key = st.text_input(
    "Gemini API Key",
    type="password"
)

if not gemini_api_key:
    st.info(
        "Please add your Gemini API key to continue.",
        icon="🗝️"
    )

else:
    # Create Gemini client
    client = genai.Client(api_key=gemini_api_key)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What is up?"):

        # Save user message
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Gemini response
        with st.chat_message("assistant"):
            try:
                response = client.models.generate_content_stream(
                    model="gemini-3.8-flash",
                    contents=[
                        {
                            "role": "user" if m["role"] == "user" else "model",
                            "parts": [{"text": m["content"]}]
                        }
                        for m in st.session_state.messages
                    ]
                )

                def response_generator():
                    for chunk in response:
                        if chunk.text:
                            yield chunk.text

                answer = st.write_stream(response_generator())

                # Save assistant response
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"Error generating response: {e}")
