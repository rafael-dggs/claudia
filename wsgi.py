from app import create_app

# A instância 'app' que o Gunicorn/Waitress irá procurar
app = create_app()

if __name__ == "__main__":
    # Apenas para uso no Windows (fallback de produção local)
    from waitress import serve
    print("Iniciando servidor Waitress em http://0.0.0.0:8000")
    serve(app, host="0.0.0.0", port=8000)