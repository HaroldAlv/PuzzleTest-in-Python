import asyncio
import aiohttp
import time 

SERVER_URL = "http://localhost:8080/fragment?id="

async def fetch(session, id_value):
    async with session.get(SERVER_URL + str(id_value)) as response:
        return await response.json()

async def main():
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
    end_time = time.perf_counter()  # 👈 Fin de medición

    print("\nMensaje reconstruido:\n")
    print(message)

    print(f"\nTiempo de ejecución: {end_time - start_time:.4f} segundos\n")

asyncio.run(main())
