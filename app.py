from os import write
import streamlit as st
import pandas as pd
import numpy as np
import json
from dotenv import load_dotenv
from google.cloud import vision
from google.oauth2 import service_account
import io
from PIL import Image
# import  download
load_dotenv()
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

# favicon=Image.open('img.jpg').resize((16,16))

# st.set_page_config(page_title='OCR Edu', page_icon = favicon, layout = 'wide', initial_sidebar_state = 'auto')


class Google_recognititon:
    def __init__(self, image_bytes, credentials) -> None:
        self.client= vision.ImageAnnotatorClient(credentials=credentials)
        self.image=vision.Image(content=image_bytes)         
    
    def recognition(self) -> str:
        # self.image.source.image_uri = image_url
        response = self.client.label_detection(image=self.image)
        return response.label_annotations


def parse_response(response):
	selected=[]
	lista_de_materiales=['plastic','glass','cardboard','metal','paper']
	for annotation in response:
		for word in annotation.description.split():
			print(word)
			if word.lower() in lista_de_materiales:
				selected.append((annotation.description, annotation.score))
				break
	return selected




st.title('Reconocimiento de Materiales DEMO')




st.markdown('Subir imagen abajo')

uploaded_file = st.file_uploader("Upload Files",type=['png','jpeg', 'jpg'])


if uploaded_file:
	# with open( 'image_bytes', 'wb') as file:
		# file.write(uploaded_file.read())


	# with open('image_bytes') as file2:
		# print(file2)
	with st.spinner("Reconociendo texto..."): 
		recog=Google_recognititon(uploaded_file.read(), credentials).recognition()
		parsed_response=parse_response(recog)
		# print(recog)
		st.markdown(
			"""
			# Materiales reconocidos en imagen: 
			""")
		for node in parsed_response:
			st.write('Material: {} \n'.format(node[0]))
			st.write('Puntaje: {}'.format(node[1]))

	# download.return_button(recog)	