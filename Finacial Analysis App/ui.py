import streamlit as st



st.title("Finacial AI Chat")

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")   


