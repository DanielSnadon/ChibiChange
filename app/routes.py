from app import app

@app.route('/')
def home():
    return "Chibis rule the World"