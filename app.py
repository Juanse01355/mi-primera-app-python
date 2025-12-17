from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

# =====================
# CONFIGURACIÓN ADMIN
# =====================
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

    if request.method == "POST":
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
            "mes": mes,
            "anio": anio_actual,
            "tipo": tipo,
            "total": total
        })

        mensaje_guardado = "<p style='color:green'><b>Recibo guardado</b></p>"

    resumen = {}
    for h in historial:
        if h["anio"] == anio_actual:
            resumen.setdefault(h["mes"], {"Agua": 0, "Luz": 0, "Internet": 0})
            resumen[h["mes"]][h["tipo"]] += h["total"]

    historial_html = '<div class="historial-col">'
    for mes, datos in resumen.items():
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

function confirmarBorrado() {{
    return confirm("¿Seguro que deseas borrar TODO el historial?");
}}
</script>
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

    <button type="submit">Calcular</button>
</form>

{encabezado_resultado}
<div id="resultado">{resultado}</div>

<button onclick="copiarResultado()">Copiar resultado</button>

{mensaje_guardado}

<hr>

<h4>Admin</h4>
<form method="post" action="/borrar" onsubmit="return confirmarBorrado()">
    <input type="password" name="clave" placeholder="Clave administrador" required>
    <button style="background:#dc3545;color:white">Borrar historial</button>
</form>

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
# RUTA BORRADO (ADMIN)
# =====================
@app.route("/borrar", methods=["POST"])
def borrar_historial():
    clave = request.form.get("clave")

    if clave != CLAVE_ADMIN:
        return "Acceso denegado ❌", 403

    historial.clear()
    return "<h2>Historial borrado correctamente ✅</h2><a href='/'>Volver</a>"
