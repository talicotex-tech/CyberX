from flask import Flask, render_template_string, request
import re
import random

app = Flask(__name__)

# ==================================================
# BASE DE DATOS OFICIAL
# ==================================================

empresas_oficiales = {

    "Banco Nacional": {

        "telefono": "3001234567",
        "correo": "soporte@banconacional.com"
    },

    "Tienda Plus": {

        "telefono": "3109998888",
        "correo": "contacto@tiendaplus.com"
    },

    "PaySecure": {

        "telefono": "3201112233",
        "correo": "ayuda@paysecure.com"
    }
}

# ==================================================
# PALABRAS SOSPECHOSAS
# ==================================================

palabras_peligrosas = {

    # Riesgo bajo
    "actualiza": 8,
    "verifique": 8,
    "confirme": 8,
    "paquete": 8,
    "entrega": 8,
    "seguridad": 10,
    "alerta": 10,

    # Riesgo medio
    "actividad inusual": 15,
    "suspendido": 15,
    "bloqueada": 15,
    "movimientos sospechosos": 15,
    "transferencia": 15,
    "premio": 18,
    "ganaste": 18,

    # Riesgo alto
    "contraseña": 25,
    "datos personales": 25,
    "cuenta bancaria": 25,

    # Urgencia extrema
    "urgente": 20,
    "inmediatamente": 20,
    "10 minutos": 25,
    "evitar bloqueo": 20,
    "recupere el acceso": 20,
    "será suspendida": 25,

    # Acciones peligrosas
    "haz clic": 20
}

# ==================================================
# CONSEJOS DE SEGURIDAD
# ==================================================

consejos = [

    "No abras enlaces sospechosos.",
    "Verifica siempre el remitente.",
    "Los bancos nunca solicitan claves por SMS.",
    "No compartas datos personales.",
    "Desconfía de mensajes urgentes."
]

# ==================================================
# ANALIZAR MENSAJES
# ==================================================

def analizar_mensaje(texto):

    texto_minuscula = texto.lower()

    riesgo = 0

    alertas = []

    # ==============================================
    # VALIDAR REMITENTES OFICIALES
    # ==============================================

    for empresa, datos in empresas_oficiales.items():

        if datos["telefono"] in texto:

            riesgo -= 40

            alertas.append(
                f"✅ Número oficial verificado: {empresa}"
            )

        if datos["correo"] in texto:

            riesgo -= 40

            alertas.append(
                f"✅ Correo oficial verificado: {empresa}"
            )

    # ==============================================
    # DETECTAR PALABRAS SOSPECHOSAS
    # ==============================================

    for palabra, puntos in palabras_peligrosas.items():

        if palabra in texto_minuscula:

            riesgo += puntos

            alertas.append(
                f"⚠️ Detectado: {palabra}"
            )

    # ==============================================
    # DETECTAR ENLACES
    # ==============================================

    links = re.findall(r'https?://\S+', texto)

    if links:

        riesgo += 10

        alertas.append(
            "🚨 Contiene enlaces"
        )

    # ==============================================
    # DETECTAR DOMINIOS SOSPECHOSOS
    # ==============================================

    dominios_sospechosos = [

        ".xyz",
        ".ru",
        ".info",
        "bit.ly",
        "tinyurl"
    ]

    for link in links:

        for dominio in dominios_sospechosos:

            if dominio in link:

                riesgo += 15

                alertas.append(
                    f"🚨 Dominio sospechoso detectado: {dominio}"
                )

    # ==============================================
    # LIMITAR RANGO DEL RIESGO
    # ==============================================

    if riesgo < 0:
        riesgo = 0

    if riesgo > 100:
        riesgo = 100

    # ==============================================
    # CLASIFICACIÓN
    # ==============================================

    if riesgo >= 80:

        categoria = "🚨 MENSAJE PELIGROSO"
        color = "#ef4444"

    elif riesgo >= 40:

        categoria = "⚠️ MENSAJE SOSPECHOSO"
        color = "#f59e0b"

    else:

        categoria = "✅ MENSAJE SEGURO"
        color = "#22c55e"

    return categoria, color, riesgo, alertas

# ==================================================
# ANALIZAR FUENTES
# ==================================================

def analizar_fuente(texto):

    texto = texto.lower().strip()

    riesgo = 0

    alertas = []

    # ==============================================
    # DETECTAR DOMINIOS SOSPECHOSOS
    # ==============================================

    dominios_sospechosos = [

        ".xyz",
        ".ru",
        ".info",
        "bit.ly",
        "tinyurl"
    ]

    for dominio in dominios_sospechosos:

        if dominio in texto:

            categoria = "🚨 FUENTE SOSPECHOSA"
            color = "#ef4444"
            riesgo = 90

            alertas.append(
                f"🚨 Dominio sospechoso detectado: {dominio}"
            )

            return categoria, color, riesgo, alertas

    # ==============================================
    # VALIDAR FUENTES OFICIALES
    # ==============================================

    for empresa, datos in empresas_oficiales.items():

        if datos["telefono"] in texto:

            categoria = "✅ FUENTE OFICIAL"
            color = "#22c55e"
            riesgo = 0

            alertas.append(
                f"✅ Número oficial verificado: {empresa}"
            )

            return categoria, color, riesgo, alertas

        if datos["correo"] in texto:

            categoria = "✅ FUENTE OFICIAL"
            color = "#22c55e"
            riesgo = 0

            alertas.append(
                f"✅ Correo oficial verificado: {empresa}"
            )

            return categoria, color, riesgo, alertas

    # ==============================================
    # FUENTE DESCONOCIDA
    # ==============================================

    categoria = "⚠️ FUENTE DESCONOCIDA"
    color = "#f59e0b"
    riesgo = 45

    alertas.append(
        "⚠️ La fuente no existe en la base de datos oficial."
    )

    return categoria, color, riesgo, alertas

# ==================================================
# HTML
# ==================================================

HTML = '''

<!DOCTYPE html>
<html lang="es">

<head>

<meta charset="UTF-8">

<title>CyberX</title>

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{

    font-family:Arial;

    background:
    linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #111827
    );

    min-height:100vh;

    color:white;
}

.contenedor{

    max-width:850px;

    margin:auto;

    padding:35px 20px;
}

.header{

    text-align:center;

    margin-bottom:30px;
}

.header h1{

    font-size:65px;

    color:#38bdf8;

    text-shadow:0px 0px 20px #38bdf8;
}

.header p{

    color:#cbd5e1;

    margin-top:8px;

    font-size:18px;
}

.top{

    display:flex;

    gap:20px;

    margin-bottom:25px;
}

.card{

    flex:1;

    background:rgba(255,255,255,0.05);

    backdrop-filter:blur(12px);

    border:1px solid rgba(255,255,255,0.1);

    border-radius:20px;

    padding:18px;
}

.card h3{

    color:#38bdf8;

    margin-bottom:10px;
}

.analizador{

    background:rgba(255,255,255,0.05);

    backdrop-filter:blur(12px);

    border:1px solid rgba(255,255,255,0.1);

    border-radius:25px;

    padding:25px;
}

select{

    width:100%;

    padding:15px;

    margin-bottom:15px;

    border-radius:15px;

    background:#0f172a;

    color:white;

    border:none;

    font-size:16px;
}

textarea{

    width:100%;

    height:200px;

    border:none;

    border-radius:18px;

    padding:18px;

    background:#0f172a;

    color:white;

    font-size:16px;

    resize:none;

    outline:none;
}

button{

    width:100%;

    margin-top:15px;

    background:linear-gradient(
        90deg,
        #2563eb,
        #38bdf8
    );

    border:none;

    color:white;

    padding:16px;

    border-radius:18px;

    font-size:18px;

    cursor:pointer;

    transition:0.3s;
}

button:hover{

    transform:scale(1.02);

    box-shadow:0px 0px 15px #38bdf8;
}

.resultado{

    margin-bottom:20px;

    padding:25px;

    border-radius:22px;
}

.riesgo{

    font-size:70px;

    font-weight:bold;

    margin:15px 0px;
}

ul{

    padding-left:20px;
}

li{

    margin-bottom:10px;
}

.nuevo{

    display:block;

    text-align:center;

    margin-top:18px;

    color:white;

    text-decoration:none;

    background:#0f172a;

    padding:14px;

    border-radius:16px;
}

.footer{

    text-align:center;

    margin-top:20px;

    color:#94a3b8;
}

</style>

</head>

<body>

<div class="contenedor">

<div class="header">

<h1>🛡️ CyberX</h1>

<p>
Sistema Inteligente de Detección de Phishing
</p>

</div>

<div class="top">

<div class="card">

<h3>💡 Consejo</h3>

<p>{{ consejo }}</p>

</div>

<div class="card">

<h3>🛡️ Sistema Heurístico</h3>

<p>
Sistema avanzado de detección de phishing y amenazas digitales.
</p>

</div>

</div>

{% if categoria %}

<div class="resultado"
style="background:{{ color }};">

<h2>{{ categoria }}</h2>

<div class="riesgo">

{{ riesgo }}%

</div>

<h3>Resultados del análisis:</h3>

<ul>

{% for alerta in alertas %}

<li>{{ alerta }}</li>

{% endfor %}

</ul>

<a href="/" class="nuevo">

Analizar nuevo contenido

</a>

</div>

{% endif %}

<div class="analizador">

<h2>🔍 Centro de Análisis</h2>

<form method="POST">

<select name="tipo">

<option value="mensaje">
📩 Analizar Mensaje
</option>

<option value="fuente">
🌐 Analizar Fuente
</option>

</select>

<textarea
name="mensaje"
placeholder="Pega aquí el mensaje, enlace, correo o número sospechoso..."
>{{ mensaje }}</textarea>

<button type="submit">

Analizar Riesgo

</button>

</form>

</div>

<div class="footer">

CyberX © Universidad Popular del César - Proyecto Universitario de Ciberseguridad

</div>

</div>

</body>
</html>

'''

# ==================================================
# RUTA PRINCIPAL
# ==================================================

@app.route("/", methods=["GET", "POST"])

def inicio():

    categoria = None
    color = None
    riesgo = 0
    alertas = []
    mensaje = ""

    consejo = random.choice(consejos)

    if request.method == "POST":

        mensaje = request.form.get("mensaje", "")
        tipo = request.form.get("tipo", "")

        # ==========================================
        # ANALIZAR MENSAJE
        # ==========================================

        if tipo == "mensaje":

            categoria, color, riesgo, alertas = analizar_mensaje(mensaje)

        # ==========================================
        # ANALIZAR FUENTE
        # ==========================================

        elif tipo == "fuente":

            categoria, color, riesgo, alertas = analizar_fuente(mensaje)

    return render_template_string(

        HTML,

        categoria=categoria,
        color=color,
        riesgo=riesgo,
        alertas=alertas,
        consejo=consejo,
        mensaje=mensaje
    )

# ==================================================
# EJECUTAR APP
# ==================================================

if __name__ == '__main__':

    app.run(debug=True)
