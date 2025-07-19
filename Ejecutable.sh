#!/bin/bash

echo "🔍 Verificando dependencias..."

# Verificar si Docker está instalado
if command -v docker &> /dev/null; then
    echo "✅ Docker está instalado."
else
    echo "❌ Docker no está instalado o no está en el PATH."
    exit 1
fi

# Verificar si docker-compose está instalado
if command -v docker-compose &> /dev/null; then
    echo "✅ docker-compose está instalado."
else
    echo "❌ docker-compose no está instalado o no está en el PATH."
    exit 1
fi

# Verificar si ngrok está instalado
if command -v ngrok &> /dev/null; then
    echo "✅ Ngrok está instalado."
else
    echo "❌ Ngrok no está instalado o no está en el PATH."
    echo "ℹ️  Descárgalo desde https://ngrok.com/download y agrégalo al PATH."
    exit 1
fi

# Verificar archivo docker-compose.yml
if [ -f "docker-compose.yml" ]; then
    echo "✅ docker-compose.yml encontrado."
else
    echo "❌ No se encontró el archivo docker-compose.yml en el directorio actual."
    exit 1
fi

# Verificar archivo Dockerfile
if [ -f "Dockerfile" ]; then
    echo "✅ Dockerfile encontrado."
else
    echo "❌ No se encontró el archivo Dockerfile."
    exit 1
fi

# Detener contenedores previos
echo "🧹 Deteniendo contenedores anteriores (si existen)..."
docker-compose down
if [ $? -eq 0 ]; then
    echo "✅ Contenedores anteriores detenidos correctamente."
else
    echo "⚠️ No se pudo detener los contenedores anteriores (puede que no estuvieran activos)."
fi

sleep 5

# Preguntar al usuario si desea lanzar Ngrok
read -p "❓ ¿Deseas iniciar Ngrok en una nueva ventana de cmd? (y/n): " launch_ngrok

if [[ "$launch_ngrok" == "y" || "$launch_ngrok" == "Y" ]]; then
    echo "🚀 Lanzando Ngrok en nueva ventana de cmd..."
    powershell.exe -Command "Start-Process cmd -ArgumentList '/k ngrok http 3002'"
    sleep 5

    # Obtener la URL pública desde el API local con reintentos
NGROK_API="http://127.0.0.1:4040/api/tunnels"
ATTEMPTS=10
NGROK_URL=""

echo "⏳ Esperando a que Ngrok genere la URL pública..."

for ((i=1; i<=ATTEMPTS; i++)); do
    NGROK_URL=$(curl -s "$NGROK_API" | grep -oE 'https://[a-zA-Z0-9.-]+\.ngrok-free\.app' | head -n 1)
    
    if [[ -n "$NGROK_URL" ]]; then
        echo "✅ Ngrok se inició correctamente: $NGROK_URL"
        break
    else
        echo "🔁 Intento $i/$ATTEMPTS: aún no hay URL pública, reintentando en 2s..."
        sleep 2
    fi
done

if [[ -z "$NGROK_URL" ]]; then
    echo "❌ No se pudo obtener una URL pública de Ngrok después de $ATTEMPTS intentos."
    echo "   Verifica que Ngrok esté funcionando correctamente en otra ventana."
fi

else
    echo "⏩ Omitiendo lanzamiento de Ngrok por decisión del usuario."
fi

sleep 5

# Finalmente, levantar los contenedores en primer plano
echo "🐳 Ejecutando docker-compose en primer plano..."
docker-compose up --build
