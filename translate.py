import streamlit as st
import os
import google.generativeai as genai

# Set up the GenAI client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def translate_document(file, source_language="en", target_language="ja"):
    try:
        text = file.read().decode("utf-8")

        text1 = "How are you?"

        # Create the generation configuration
        generation_config = {
            "temperature": 1.0,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        # Create the generative model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
        )

        # Generate the translation
        prompt = f"Translate the following text from {source_language} to {target_language}:\n{text1}.Dont provide anything else just translate"
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"An error occurred: {e}"

def main():
    st.title("Document Translator")

    uploaded_file = st.file_uploader("Choose a file to translate")

    if uploaded_file is not None:
        file_text = uploaded_file.read().decode("utf-8")
        st.write("Uploaded file content:")
        st.write(file_text)

        translated_text = translate_document(uploaded_file)
        st.write("Translated text:")
        st.write(translated_text)

if __name__ == "__main__":
    main()