# podcast-to-text

## ¿Cómo funciona podcast-to-text?

- Divide un archivo de audio en fragmentos que se puedan enviar a la API de Whisper
- Genera resúmenes del contenido transcrito
- Agrupa los resúmenes en uno sólo texto
- Genera en base a ese resumen descripciones para la web del Podcast y textos para los posts de RRSS

## ¿Qué debes saber del código?

- Instala los paquetes requeridos haciendo uso de:
-- pip install -r requirements.txt

- Deja en la carpeta del repositorio un archivo llamado "podcast.mp3" que contendrá el podcast (o audio a dividir)
- Añade al script tu OpenAI Api Key
- Añade al script el número de minutos que dura el podcast en la variable "podcast_minutes"
- Modifica los prompts a tu gusto
- Menciona al Test de Turing en RRSS 😁
