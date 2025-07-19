Créditos, mejoras y video explicativo
Este proyecto se basa en el trabajo original de Lena Shakurova, quien amablemente autorizó su traducción y adaptación (ver mensaje de Lena más arriba).
Esta versión en español incluye:
- Traducción completa del README.md

- Compatibilidad adicional con modelos vía OpenRouter

- Incorporación del script Ejecutable.sh para validar configuraciones básicas y facilitar el arranque

- Pequeñas mejoras para facilitar el despliegue y la depuración

📺 Para ver cómo funciona la API paso a paso y entender mejor el flujo de mensajes en WhatsApp, visita el video original de Lena: 

🔗 Ver en YouTube
Si compartes este proyecto, no olvides mencionar el repositorio original de Lena y su canal:
- GitHub original: https://github.com/Shakurova/Twilio-OpenAI-WhatsApp-Bot
- YouTube: [Lena Shakurova  AI, chatbots and voice agents](https://www.youtube.com/watch?v=WGklRhIYvOc&ab_channel=LenaShakurova%7CAI%2Cchatbotsandvoiceagents)


# Twilio-OpenAI-WhatsApp-Bot

Este repositorio contiene el código para construir un chatbot en Python que funciona en WhatsApp y responde a los mensajes de los usuarios utilizando la API de OpenAI. Está desarrollado con FastAPI y utiliza Twilio para la integración con WhatsApp Business. El código fuente está disponible en GitHub bajo una licencia de código abierto.

## Tecnologías utilizadas:
- Python
- Docker
- FastAPI
- Twilio
- OpenAI API
- Redis

## Primeros pasos

Para comenzar, sigue estos pasos:

1. Clona el repositorio en tu máquina local:
   ```bash
   git clone git@github.com:Shakurova/Twilio-OpenAI-WhatsApp-Bot.git
   cd Twilio-OpenAI-WhatsApp-Bot/ 
   ```

2. Configurar Twilio

   - **- Sandbox de Twilio para WhatsApp**: -  Empieza configurando el Sandbox de Twilio para WhatsApp para probar tu aplicación. Esto te permite enviar y recibir mensajes usando un número temporal de WhatsApp proporcionado por Twilio. Sigue los pasos en la Consola de Twilio dentro de la sección "Messaging" para configurar el sandbox. Puedes encontrar instrucciones detalladas en esta Guía del blog de Twilio.
 

   - **- Pasar a Producción:**- Una vez que hayas probado tu aplicación en el entorno sandbox y estés listo para ir a producción, puedes configurar un número de teléfono Twilio para uso real. Esto implica adquirir un número Twilio y configurarlo para manejar mensajes de WhatsApp. Consulta la Guía de Twilio para más detalles sobre la transición al entorno de producción.


3. Asegúrate de tener Docker y Redis instalados en tu máquina.

   - Para macOS:

   Instalar Redis usando Homebrew:
   ```bash
   brew install redis
   ```
   Start Redis:
   ```bash
   brew services start redis
   ```

   Install Docker via Homebrew:
   ```bash
   brew install --cask docker
   Open Docker Desktop and make sure it’s running.
   ```
   Verify installation:
   ```bash
   docker --version
   ```

4. - Crea un archivo .env en el directorio del proyecto y define las siguientes variables de entorno con tus credenciales de OpenAI y Twilio:

   ```plaintext
    TWILIO_WHATSAPP_NUMBER=<your Twilio phone number>
    TWILIO_ACCOUNT_SID=<your Twilio account SID>
    TWILIO_AUTH_TOKEN=<your Twilio auth token>
    OPENAI_API_KEY=<your OpenAI API key>
    REDIS_HOST=<your redis host>
    REDIS_PORT=<your redis port>
    REDIS_PASSWORD=<your redis password>
   ```

5. - Exponer tu servidor con ngrok:
   Para que Twilio pueda acceder al webhook de tu chatbot (FastAPI), necesitas una URL pública con HTTPS. Esto lo puedes lograr con ngrok:

   ```bash
   ngrok http 3002
   ```
   Después de ejecutarlo, copia la URL HTTPS que aparece en consola 
   (por ejemplo, https://abc1ngrok.io) y configúrala como Webhook en la consola de Twilio



6. - Ejecutar script de inicio:
Ejecuta ./Ejecutable.sh para lanzar la API, validar servicios activos y detectar errores básicos de configuración

   ```bash
   ./Ejecutable.sh

   ```
Si es necesario, otorga permisos de ejecución con 

   ```bash
   chmod +x Ejecutable.sh.

   ```


7. - Compila y levanta los contenedores del chatbot ejecutando:
      ```bash      
      docker-compose up --build -d
      docker-compose up --build   

      ```