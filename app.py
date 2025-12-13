from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def imc():
    resultado = ""

    if request.method == "POST":
        peso = float(request.form["peso"])
        altura = float(request.form["altura"])
        imc = peso / (altura ** 2)

        resultado = f"Tu IMC es: {imc:.2f}"

    return f"""
    <h1>Calculadora de IMC</h1>

    <form method="post">
        <label>Peso (kg):</label><br>
        <input type="number" step="0.1" name="peso" required><br><br>

        <label>Altura (m):</label><br>
        <input type="number" step="0.01" name="altura" required><br><br>

        <button type="submit">Calcular</button>
    </form>

    <h2>{resultado}</h2>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


