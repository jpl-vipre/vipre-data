import uvicorn
from multiprocessing import cpu_count, freeze_support
import os


def start_server(host="127.0.0.1", port=5000, num_workers=4, loop="asyncio", reload=False):
    uvicorn.run(
        "vipre_data.app.main:app",
        host=host,
        port=port,
        workers=num_workers,
        loop=loop,
        reload=reload,
    )


if __name__ == "__main__":
    freeze_support()  # Needed for pyinstaller for multiprocessing on Windows
    # num_workers = int(cpu_count() * 0.5)
    num_workers = 1
    start_server(num_workers=num_workers)
