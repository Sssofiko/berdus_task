from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()


class SARIFFile(BaseModel):
    file_path: str


@app.post("/getsarif")
def get_sarif(sarif_file: SARIFFile):
    try:
        with open(sarif_file.file_path, 'r') as file:
            sarif_data = json.load(file)
            return sarif_data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Файл не найден")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Ошибка при разборе JSON")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
