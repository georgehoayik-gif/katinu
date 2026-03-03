import uvicorn
from fastapi import FastAPI
from MilvusPiper import main

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API rodando 🚀"}

@app.post("/nova-proposta")
def executar_integracao():
    try:
        main()
        return {"status": "Integração executada com sucesso"}
    except Exception as e:
        return {"erro": str(e)}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

    