# main.py
from app import create_app, socketio

app = create_app()

if __name__ == "__main__":
    # Rodar com debug=True para recarregar automaticamente
    # O host 0.0.0.0 permite acessar de outros dispositivos na mesma rede
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)
