from flask import Flask, request
from datetime import datetime
import uuid

app = Flask(__name__)

CLAVE_ADMIN = "RecibosJuanse2025"

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

def formatear_pesos(valor):
    return f"{valor:,.0f}".replace(",", ".")

# =====================
# RUTA PRINCIPAL
# =====================
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

        historial.append({
            "id": str(uuid.uuid4()),
            "mes": mes,
            "anio": anio_actual,
            "tipo": tipo,
            "total": total
        })

        encabezado_resultado = f"""
        <div class="encabezado">
            <span class="material-icons icono">{ICONOS[tipo]}</span>
            <h3>La cuota de {tipo.lower()} de este mes es la siguiente:</h3>
        </div>
        """

        resultado = f"""
        <p><b>Tío Román:</b> ${formatear_pesos(valor * 3)}</p>
        <p><b>Tía Rocío:</b> ${formatear_pesos(valor * 2)}</p>
        <p><b>Juan:</b> ${formatear_pesos(valor)}</p>
        """

        mensaje_guardado = "<p style='color:green'><b>Recibo guardado</b></p>"

    resumen = {}
    for h in historial:
        if h["anio"] == anio_actual:
            resumen.setdefault(h["mes"], [])
            resumen[h["mes"]].append(h)

    historial_html = ""
    for mes, registros in resumen.items():
        historial_html += f"<div class='historial-card'><h4>{mes} {anio_actual}</h4>"

        for r in registros:
            historial_html += f"""
            <p>🧾 {r["tipo"]}: ${formatear_pesos(r["total"])}</p>

            <form method="post" action="/borrar_registro" style="margin-bottom:10px">
                <input type="hidden" name="id" value="{r["id"]}">
                <input type="password" name="clave" placeholder="Clave admin" required>
                <button style="background:#dc3545;font-size:14px">
                    🗑️ Borrar este registro
                </button>
            </form>
            """

        historial_html += "</div>"

    opciones_meses = "".join([f"<option value='{m}'>{m}</option>" for m in MESES])

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Calculadora Recibos</title>
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
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

.historial-card {{
    background: #fafafa;
    padding: 14px;
    border-radius: 10px;
    margin-bottom: 15px;
}}
</style>
</head>

<body>
<div class="main">

<div class="card">
<h2>Calculadora Recibos</h2>

<form method="post">
    <input type="text" name="total" placeholder="Valor del recibo" required>
    <select name="tipo_recibo">
        <option value="Agua">Agua</option>
        <option value="Luz">Luz</option>
        <option value="Internet">Internet</option>
    </select>
    <select name="mes" required>
        <option value="">Seleccione mes</option>
        {opciones_meses}
    </select>
    <button type="submit">Calcular</button>
</form>

{encabezado_resultado}
{resultado}
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

# =====================
# BORRAR REGISTRO
# =====================
@app.route("/borrar_registro", methods=["POST"])
def borrar_registro():
    clave = request.form.get("clave")
    registro_id = request.form.get("id")

    if clave != CLAVE_ADMIN:
        return "Acceso denegado ❌", 403

    global historial
    historial = [h for h in historial if h["id"] != registro_id]

    return "<h3>Registro eliminado ✅</h3><a href='/'>Volver</a>"
