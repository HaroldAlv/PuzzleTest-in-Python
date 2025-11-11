# Puzzle Decoder Race

Este proyecto resuelve la prueba técnica **Puzzle Fragment Server**, donde el objetivo es reconstruir un mensaje oculto haciendo múltiples solicitudes asíncronas a un servidor que entrega fragmentos del mensaje en desorden y con retrasos aleatorios.

---

## Objetivo

- Obtener fragmentos del mensaje desde `/fragment?id={n}`
- Guardarlos según su posición correcta (`index`)
- Detectar cuándo el mensaje está completo
- Ensamblarlo y mostrarlo
- Finalizar la ejecución lo más rápido posible  
  ** Bonus:** Si la ejecución completa ocurre en **menos de 1 segundo**

---

## Explicación estrategia para velocidad:
 -------------------------- ------------------------------------------------------------------------------------------------------------------
| Función                  | Descripción                                                                                                      |
|--------------------------|------------------------------------------------------------------------------------------------------------------|
| `asyncio` + `aiohttp`    | Se realizan múltiples solicitudes concurrentemente                                                               |
| `asyncio.as_completed()` | Permite procesar respuestas apenas llegan, sin esperar a otras                                                   |
| Cancelación temprana     | Una vez detectado que ya tenemos todos los fragmentos, se cancelan las solicitudes restantes para ahorrar tiempo |
| `perf_counter()`         | Se mide el tiempo real de ejecución para validar el bonus                                                        |

---

## Lógica del Ensamblaje

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
5. Si ya está completo entonces se cancelan las demás tareas.
6. Se reconstruye el mensaje **utilizando el orden de los indices**.

---

##  ¿Se obtuvo el bonus de < 1 segundo?

Sí — El programa completa la reconstrucción típicamente en **~0.25–0.60 segundos** dependiendo de la latencia del servidor.

<p align="center">
  <img src="images/resultado.png" width="500">
</p>

---
#Ejecución

## Requerimientos

```bash
Python 3.10+
aiohttp
```

Instalar dependencias:

```bash
pip install aiohttp
```

---

## Cómo Ejecutar

1. Inicia el servidor puzzle (si no está corriendo):

```bash
docker run -p 8080:8080 ifajardov/puzzle-server
```

2. Ejecutar el script:

```bash
python main.py
```

---
---

## Checklist de Calidad del Código

| Criterio                            | Estado |
|-------------------------------------|--------|
| Reconstrucción correcta del mensaje |aprobado|
| Manejo concurrente para velocidad   |aprobado|
| Cancelación temprana de tareas      |aprobado|
| Medición de rendimiento incluida    |aprobado|
| Resultado impreso limpio            |aprobado|
