# Minimal ASGI app kept import-light. FastAPI import occurs only when running as a module.
def create_app():
    try:
        from fastapi import FastAPI
    except Exception as e:
        # FastAPI not installed; provide a stub
        class Stub:
            def __init__(self): self.routes = []
        return Stub()
    app = FastAPI(title="Service")
    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}
    return app

if __name__ == "__main__":
    import os
    import sys
    if "--serve" in sys.argv:
        # run only if fastapi/uvicorn installed
        try:
            import uvicorn
            uvicorn.run(create_app(), host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
        except Exception as e:
            print("Install fastapi/uvicorn to serve: pip install -r requirements.txt")
    else:
        print("App module ready. Use: python -m src.app --serve")
