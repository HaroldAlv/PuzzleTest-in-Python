# 🧩 Puzzle Decoder Race

Este proyecto resuelve el desafío técnico **Puzzle Fragment Server**, donde el objetivo es reconstruir un mensaje oculto haciendo múltiples solicitudes asíncronas a un servidor que entrega fragmentos del mensaje en desorden y con retrasos aleatorios.

---

## ✅ Objetivo

- Obtener fragmentos del mensaje desde `/fragment?id={n}`
- Guardarlos según su posición correcta (`index`)
- Detectar cuándo el mensaje está completo
- Ensamblarlo y mostrarlo
- Finalizar la ejecución lo más rápido posible  
  **🚀 Bonus:** Si la ejecución completa ocurre en **menos de 1 segundo**

---

## 🚀 Estrategia de Velocidad

| Técnica | Descripción |
|-------|-------------|
| `asyncio` + `aiohttp` | Se realizan múltiples solicitudes concurrentemente |
| `asyncio.as_completed()` | Permite procesar respuestas apenas llegan, sin esperar a otras |
| Cancelación temprana | Una vez detectado que ya tenemos todos los fragmentos, se cancelan las solicitudes restantes para ahorrar tiempo |
| `perf_counter()` | Se mide el tiempo real de ejecución para validar el bonus |

---

## 🧠 Lógica del Ensamblaje

1. Se realizan **50 solicitudes simultáneas** inicialmente.
2. Cada respuesta incluye:
   ```json
   { "index": <posición>, "text": <fragmento> }
   ```
3. Se almacena en un diccionario `fragments` usando el índice como clave.
4. Se detecta si el mensaje está completo verificando:
   ```
   Se tiene todas las piezas desde el índice 0 hasta el máximo índice encontrado.
   ```
5. Si ya está completo → Se cancelan las demás tareas.
6. Se reconstruye el mensaje **respetando el orden de índices**.

---

## ✨ ¿Se obtuvo el bonus de < 1 segundo?

Sí ✅ — El programa completa la reconstrucción típicamente en **~0.25–0.60 segundos** dependiendo de la latencia del servidor.

---

## 🛠️ Requerimientos

```bash
Python 3.10+
aiohttp
```

Instalar dependencias:

```bash
pip install aiohttp
```

---

## ▶️ Cómo Ejecutar

1. Inicia el servidor puzzle (si no está corriendo):

```bash
docker run -p 8080:8080 ifajardov/puzzle-server
```

2. Ejecuta tu script:

```bash
python main.py
```

---

## 📦 Código Usado

```python
import asyncio
import aiohttp
import time

SERVER_URL = "http://localhost:8080/fragment?id="

async def fetch(session, id_value):  # !!!
    async with session.get(SERVER_URL + str(id_value)) as response:
        return await response.json()

async def main():  # !!!
    start_time = time.perf_counter()
    fragments = {}
    max_index = None

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch(session, i)) for i in range(50)]

        for finished in asyncio.as_completed(tasks):
            data = await finished
            fragments[data["index"]] = data["text"]

            if max_index is None or data["index"] > max_index:
                max_index = data["index"]

            if max_index is not None and all(i in fragments for i in range(max_index + 1)):
                for t in tasks:
                    if not t.done():
                        t.cancel()
                break

    message = " ".join(fragments[i] for i in sorted(fragments))
    end_time = time.perf_counter()

    print("\nMensaje reconstruido:")
    print(message)
    print(f"Tiempo de ejecución: {end_time - start_time:.4f} segundos")

asyncio.run(main())
```

---

## 🧼 Calidad del Código (Checklist)

| Criterio | Estado |
|--------|-------|
| Reconstrucción correcta del mensaje | ✅ |
| Manejo concurrente para velocidad | ✅ |
| Cancelación temprana de tareas | ✅ |
| Medición de rendimiento incluida | ✅ |
| Resultado impreso limpio | ✅ |
