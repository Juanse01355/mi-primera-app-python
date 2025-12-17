from flask import Flask, request, redirect, url_for
from datetime import datetime
import uuid

app = Flask(__name__)

historial = []

MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

ICONOS = {
    "Agua": "water_drop",
    "Luz": "bolt",
    "Internet": "wifi"
}

CLAVE_ADMIN = "admin123"


def formatear_pesos(valor):
    return f"{valor:,.0f}".replace(",", ".")


@app.route("/", methods=["GET", "POST"])
def calcular():
    resultado = ""
    encabezado_resultado = ""
    mensaje_guardado = ""
    anio_actual = datetime.now().year

    if request.method == "POST" and "total" in request.form:
        total = float(request.form["total"].replace(".", ""))
        tipo = request.form["tipo_recibo"]
        mes = request.form["mes"]

        valor = total / 6
        tio = valor * 3
        tia = valor * 2
        juan = valor

        encabezado_resultado = f"""
        <div class="encabezado">
            <span class="material-icons icono">{ICONOS[tipo]}</span>
            <h3>La cuota de {tipo.lower()} de este mes es la siguiente:</h3>
        </div>
        """

        resultado = f"""
        <p><b>Tío Román:</b> ${formatear_pesos(tio)}</p>
        <p><b>Tía Rocío:</b> ${formatear_pesos(tia)}</p>
        <p><b>Juan:</b> ${formatear_pesos(juan)}</p>
        """

        historial.append({
            "id": str(uuid.uuid4()),
            "mes": mes,
            "anio": anio_actual,
            "tipo": tipo,
            "total": total
        })

        mensaje_guardado = "<p style='color:green'><b>Recibo guardado</b></p>"

    resumen = {}
    for h in historial:
        if h["anio"] == anio_actual:
            resumen.setdefault(h["mes"], [])
            resumen[h["mes"]].append(h)

    historial_html = '<div class="historial-col">'
    for mes, registros in resumen.items():
        datos = {"Agua": 0, "Luz": 0, "Internet": 0}

        for r in registros:
            datos[r["tipo"]] += r["total"]

        total_mes = sum(datos.values())
        completos = all(v > 0 for v in datos.values())

        historial_html += f"""
        <div class="historial-card">
            <h4>{mes} {anio_actual}</h4>
            <p>💧 Agua: ${formatear_pesos(datos["Agua"])}</p>
            <p>💡 Luz: ${formatear_pesos(datos["Luz"])}</p>
            <p>🌐 Internet: ${formatear_pesos(datos["Internet"])}</p>
        """

        if completos:
            historial_html += f"""
            <p class="total-mes">
                🧾 Total del mes: ${formatear_pesos(total_mes)}
            </p>
            """

        for r in registros:
            historial_html += f"""
            <form method="post" action="/borrar" class="admin-form">
                <input type="hidden" name="id" value="{r['id']}">
                <input type="password" name="clave" class="admin-input" placeholder="Clave admin" required>
                <button class="borrar-btn">🗑️ Borrar {r['tipo']}</button>
            </form>
            """

        historial_html += "</div>"

    historial_html += "</div>"

    opciones_meses = "".join([f"<option value='{m}'>{m}</option>" for m in MESES])

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Calculadora Recibos</title>

<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

<script>
function copiarResultado() {{
    const texto = document.getElementById("resultado").innerText;
    if (!texto.trim()) {{
        alert("No hay resultado para copiar");
        return;
    }}
    navigator.clipboard.writeText(texto)
        .then(() => alert("Resultado copiado"));
}}

function limpiar() {{
    document.querySelector("input[name='total']").value = "";
    document.querySelector("select[name='tipo_recibo']").value = "Agua";
    document.querySelector("select[name='mes']").value = "";
    document.getElementById("resultado").innerHTML = "";
}}
</script>

<style>
body {{
    font-family: Arial;
    background: #f4f4f4;
    padding: 20px;
    display: flex;
    justify-content: center;
}}

.main {{
    max-width: 420px;
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 30px;
}}

.card {{
    background: white;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 0 12px rgba(0,0,0,0.12);
    text-align: center;
}}

h2 {{ font-size: 26px; }}

input, select, button {{
    width: 100%;
    padding: 14px;
    margin-top: 12px;
    font-size: 16px;
    box-sizing: border-box;
}}

button {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: #28a745;
    color: white;
    border: none;
    cursor: pointer;
    font-size: 17px;
}}

.btn-blue {{ background: #007bff; }}
.btn-gris {{ background: #6c757d; }}

.material-icons {{
    font-size: 22px;
}}

.encabezado {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-top: 20px;
}}

.icono {{
    font-size: 30px;
    color: #007bff;
}}

#resultado p {{
    font-size: 18px;
    margin: 6px 0;
}}

.historial-col {{
    display: flex;
    flex-direction: column;
    gap: 14px;
}}

.historial-card {{
    background: #fafafa;
    padding: 14px;
    border-radius: 10px;
}}

.total-mes {{
    font-weight: bold;
    margin-top: 10px;
}}

.borrar-btn {{
    background: #dc3545;
    margin-top: 6px;
    padding: 8px;
    font-size: 14px;
}}

.admin-input {{
    margin-top: 6px;
    padding: 8px;
    font-size: 14px;
}}

@media (max-width:480px) {{
    input, select, button {{
        font-size: 18px;
        padding: 16px;
    }}

    #resultado p {{
        font-size: 20px;
    }}
}}
</style>
</head>

<body>

<div class="main">

<div class="card">
<h2>Calculadora Recibos</h2>

<form method="post">
    <input type="text" name="total" placeholder="Valor del recibo (ej: 75.500)" required>

    <select name="tipo_recibo">
        <option value="Agua">💧 Agua</option>
        <option value="Luz">💡 Luz</option>
        <option value="Internet">🌐 Internet</option>
    </select>

    <select name="mes" required>
        <option value="">Seleccione mes</option>
        {opciones_meses}
    </select>

    <button type="submit">
        <span class="material-icons">calculate</span>
        Calcular
    </button>
</form>

{encabezado_resultado}
<div id="resultado">{resultado}</div>

<button class="btn-blue" onclick="copiarResultado()">
    <span class="material-icons">content_copy</span>
    Copiar resultado
</button>

<button class="btn-gris" onclick="limpiar()">
    <span class="material-icons">delete</span>
    Limpiar
</button>

{mensaje_guardado}
</div>

<div class="card">
<h3>Historial {anio_actual}</h3>
{historial_html}
</div>

</div>

</body>
</html>
"""


@app.route("/borrar", methods=["POST"])
def borrar():
    clave = request.form["clave"]
    id_registro = request.form["id"]

    if clave == CLAVE_ADMIN:
        global historial
        historial = [h for h in historial if h["id"] != id_registro]

    return redirect(url_for("calcular"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

