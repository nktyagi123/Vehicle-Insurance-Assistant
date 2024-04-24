from dotenv import load_dotenv
from prompt_template import PromptTemplate

load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to load Google Gemini Pro Vision API And get response
def get_gemini_response(image, input_text):
    model = genai.GenerativeModel('gemini-pro-vision')
    template = """
    You are an expert to Defect analyser where you need to see the defective items from the image
               and calculate the total cost to replace it, also provide the details of every defective items with cost 
               in below format

            Also get the details of cost for some parts from this {input_text}

               Defective Items : 

               1. Item 1 - cost in $
               2. Item 2 - cost in $
               ----
               ----

    """

    # Create an instance of PromptTemplate
    prompt = PromptTemplate(input_variables=["input_text"], template=template)

    filled_prompt = prompt.fill_template(input_text=input_text)

    print(filled_prompt)
    response = model.generate_content([image, filled_prompt])
    return response.text


# Function to setup input images
def input_image_setup(uploaded_files):
    image_parts_list = []
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.getvalue()
            image_parts_list.append({
                "mime_type": uploaded_file.type,
                "data": bytes_data
            })
    else:
        raise FileNotFoundError("No files uploaded")
    return image_parts_list


# Initialize our streamlit app
# st.set_page_config(page_title="Defect Inspector")

streamlit_version = st.__version__.split(".")[0]

# Set a wider page layout
st.set_page_config(page_title="Defect Inspector", page_icon="🧊")
st.header("Defect Inspector", divider='rainbow')
# Inputs
input_text = st.text_input("Enter the cost of items you have (optional):", value="")
uploaded_files = st.file_uploader("Choose images files...", accept_multiple_files=True)
if uploaded_files is not None:
  col1, col2, col3 = st.columns(3)  # Adjust number of columns based on preference
  for i, file in enumerate(uploaded_files):
    if file.type.startswith("image/"):
      if i % 3 == 0:  # Display on the first column, then move to the next
        col = col1
      elif i % 3 == 1:
        col = col2
      else:
        col = col3
      file_bytes = file.read()
      col.image(file_bytes, width=200)  # Adjust width as needed
    else:
      st.write("Please upload only image files.")
submit = st.button("Submit for Analysis")



# Function to load Google Gemini Pro Vision API And get response
def get_gemini_response1(consolidated_response):
    model = genai.GenerativeModel('gemini-pro')
    template = """
    Convert the following text into a single list of items with their associated costs:

    {consolidated_response}

    Provide the list of defective items with their associated costs in the format:

    1. Item 1 - cost in $
    2. Item 2 - cost in $
    
    Finally Calculate the total cost and provide in the format :
    -------------------
    Total Cost: $

    """

    # Create an instance of PromptTemplate
    prompt = PromptTemplate(input_variables=["consolidated_response"], template=template)
    filled_prompt = prompt.fill_template(consolidated_response=consolidated_response)
    print(filled_prompt)
    response = model.generate_content(filled_prompt)
    return response.text

# If submit button is clicked
if submit:
    if uploaded_files is None:
       print(11111111232332423423623456)
       st.error("Please upload an image of the defect to proceed. Image upload is mandatory!")
    else:
        st.subheader(":red[*Defective Parts*]", divider='rainbow')
        image_data = input_image_setup(uploaded_files)
        st.success("Analysing..")
        consolidated_response = ""
        for image in image_data:
            response = get_gemini_response(image, input_text)
            consolidated_response += response + "\n"  # Concatenate individual responses with a newline
        
        st.success("Generating Response", icon="✅")
        response = get_gemini_response1(consolidated_response)
        #st.markdown(":red[*Defective Parts*]")
        st.write(response)
