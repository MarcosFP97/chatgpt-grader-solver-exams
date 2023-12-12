import re
import openai 
from docx2python import docx2python
import docx
openai.api_key = "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" 


#Funcion con la que obtendremos la respuesta de GPT-4

def respuesta(prompt, model="gpt-3.5-turbo",temperature=0):
    messages = [
	{"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
    )
    return response.choices[0].message["content"]


#Lectura del documento Word

result=docx2python('exmayo2023.docx')
texto=result.text

preguntas=re.split(r"[0-9]\)\t\([0-9.]* punto[\w,. ]*\)",texto) #dividimos el texto en preguntas


#Respuesta a las preguntas (guardadas en documento docx)

file=docx.Document()

for i in range(1,len(preguntas)):
	preguntas[i]=preguntas[i].strip()
	preguntas[i]=re.sub(r"\([0-9.]* punto[\w,. ]*\)","",preguntas[i]) #eliminamos el '(x puntos)' al inicio de cada ejercicio
	preguntas[i]=re.sub(r".*punto.*","",preguntas[i]) #eliminamos todos los parrafos que traten sobre puntuacion	
	preguntas[i]=re.sub("\n+","\n\n",preguntas[i]) #eliminamos grades espacios en blanco
	preguntas[i]=re.sub(r"\n[\w.\- <,/]*[iI]mage[\w.\- >,]*\n","",preguntas[i]) #eliminamos el texto que queda en las imagenes
	#print('Pregunta '+str(i)+': \n\n'+preguntas[i])
	#print('\n\nRespuesta: \n\n'+respuesta(preguntas[i]))
	#print('\n\n-------------------------------------\n')
	file.add_paragraph('Pregunta '+str(i)+': \n\n'+preguntas[i]+'\n\n\nRespuesta '+str(i)+': \n\n'+respuesta(preguntas[i]))
	if i!=len(preguntas):
		file.add_page_break()
file.save("C:/Users/Usuario/Desktop/CiTIUS/llm-para-el-desarrollo-y-correccion-de-codigo/respuestas.docx")



