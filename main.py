import openai
import os
from pydub import AudioSegment

openai.api_key = "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"

prompt_generatePodcastResume = """/
    Eres un gran comprensor de texto y contenido./
    El usuario te va a dar un texto extraído de un podcast/
    Tu misión es resumir contenido eliminando partes repetitivas y dejando sólo las partes importantes/
    Vas a seguir los siguientes pasos:/
    Leer todo el contenido/
    Entenderlo con comunicar su comprensión/
    Localizar los puntos que más valor aportan para el usuario/
    Generar un resumen eliminando los contenidos que no aportan valor y destacando los que sí/  
    """

def getOpenAiCompletion(max_tokens, temperature,  model, messages):
    print("Esperando la respuesta de GPT...")
    completion = openai.ChatCompletion.create(
        model = model,
        max_tokens = max_tokens,
        temperature = temperature,
        messages = messages
    )
    completion = completion["choices"][0]["message"]["content"]

    return completion

podcast = AudioSegment.from_mp3("podcast.mp3")

total = 70 * 60 * 1000
ten_minutes = 10 * 60 * 1000
parts = int(total/ten_minutes)+1

resume = ""  
transcript = ""

print("Iniciando la transcripción del podcast")

for part in range(1, parts):
    first_part = int(part-1)

    print()
    print(" - Parte: ", part)
    file_name = str(part)+".mp3"

    shorted = podcast[ten_minutes*first_part:ten_minutes*int(part)]
    shorted = shorted.export(os.path.abspath(file_name), format="mp3")

    audio_file = open(os.path.abspath(file_name), "rb")
    print("  - Esperando la respuesta de Whisper...")
    t = openai.Audio.transcribe("whisper-1", audio_file)
    transcript = t["text"]

    print(" - Caracteres transcritos", len(t["text"]))

    print(" - Generando resumen del podcast")
    messages = [
        {"role": "system", "content": prompt_generatePodcastResume},
        {"role": "user", "content": transcript},
    ]
    resume = resume + getOpenAiCompletion(500, 0.3,  "gpt-4", messages)
    print(" - Caracteres totales generados: ", len(resume))

print("Finalizando la transcripción del podcast")

print("Iniciando la generación de texto")


messages=[
    {"role": "system", "content": """/
    
    Actúa como un experto redactor/
    Tu misión es unificar muchos resúmenes de la misma transcripción de un podcast, para posteriormente trabajar con ese resumen/
    El podcast se llama 'El Test de Turing'
    Trata sobre la actualidad de la inteligencia artificial/
    El resumen debe contener las secciones de las que se habla en el podcast:/
        - Curiosidades
        - Noticias
        - Productos
        - Tema del Día
        - Preguntas de la audiencia
    """},

    {"role": "user", "content": resume},
]

print(" - Generando resumen unificado:")
resume = getOpenAiCompletion(2000, 0.3,  "gpt-4", messages)
print("\n", resume)

messages=[
    {"role": "system", "content": """/
    
    Actúa como el Comunity Manager de un podcast/
    El podcast se llama 'El Test de Turing'
    Trata sobre la actualidad de la inteligencia artificial/
    Genera a partir de este contenido, un post de LinkedIn, con tono amigable y cercano./
    Este contenido debe contener un resumen de los puntos más importantes del podcast/
    El resumen debe contener las secciones de las que se habla en el podcast:/
        - Curiosidades
        - Noticias
        - Productos
        - Tema del Día
        - Preguntas de la audiencia
    Puedes usar Emojis./
    Utiliza español de españa./
    Habla en primera persona./
    La persona que Postea esto no es la persona que ha escrito esto./
    El que Postea es un informador./
    No utilices hastags./
    Sólo puedes poner un emoji por párrafo./
    Habla directamente al lector del Post./
    """},

    {"role": "user", "content": resume},
]

print(" - Generando contenido para rrss")
rrss_post = getOpenAiCompletion(2000, 0.3,  "gpt-4", messages)
print("\n", rrss_post)

messages=[
    {"role": "system", "content": """/
    
    Actúa como un experto redactor/
    Tu misión es generar un resumen de 500 caracteres sobre el resumen del podcast que te provee el usuario/
    El podcast se llama 'El Test de Turing'
    Trata sobre la actualidad de la inteligencia artificial/
    El resumen debe contener las secciones de las que se habla en el podcast:/
        - Curiosidades
        - Noticias
        - Productos
        - Tema del Día
        - Preguntas de la audiencia

    Utiliza un tono amigable y cercano./
    Puedes usar Emojis./
    Utiliza español de españa./
    Habla en primera persona./
    Sólo puedes poner un emoji por párrafo./
    Habla directamente al lector del Post./
    """},

    {"role": "user", "content": resume},
]

print(" - Generando descripción para el podcast")
podcast_description = getOpenAiCompletion(2000, 0.3,  "gpt-4", messages)

print("\n", podcast_description)

print("Finalizando la generación de texto")