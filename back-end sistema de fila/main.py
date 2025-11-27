from app import create_app, socketio

app = create_app()

if __name__ == "__main__":
    # em Windows use threading mode (já configurado)
    socketio.run(app, debug=True, host="0.0.0.0", port=int(__import__("os").environ.get("PORT", 5000)))
