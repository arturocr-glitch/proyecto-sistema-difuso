# =============================================================
# PROYECTO FINAL
# SISTEMAS DIFUSOS INTELIGENTES
# MAESTRÍA EN INTELIGENCIA ARTIFICIAL
# ING. ARTURO CAMPOS RODRIGUEZ
# SISTEMA INTELIGENTE DE CÁLCULO DE PRODUCCIÓN
# T&C FRUITS
# =============================================================

# =============================================================
# IMPORTACIÓN DE LIBRERÍAS
# =============================================================

from flask import Flask, render_template, request, send_file

import numpy as np

import skfuzzy as fuzz
from skfuzzy import control as ctrl

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

import os

from datetime import datetime

# =============================================================
# CREAR APLICACIÓN WEB
# =============================================================

app = Flask(__name__)

# =============================================================
# PÁGINA PRINCIPAL
# =============================================================

@app.route('/')

def inicio():

    return render_template('index.html')

# =============================================================
# DESCARGAR PDF
# =============================================================

@app.route('/descargar_pdf')

def descargar_pdf():

    return send_file(
        "Reporte_TYC_FRUITS.pdf",
        as_attachment=True
    )

# =============================================================
# FUNCIÓN PRINCIPAL DEL SISTEMA DIFUSO
# =============================================================

@app.route('/calcular', methods=['POST'])

def calcular():

    # =========================================================
    # OBTENER DATOS DEL FORMULARIO HTML
    # =========================================================

    velocidad_usuario = float(
        request.form['velocidad']
    )

    cajas_usuario = float(
        request.form['cajas']
    )

    calidad_usuario = float(
        request.form['calidad']
    )

    # =========================================================
    # VARIABLES DIFUSAS DE ENTRADA
    # =========================================================

    velocidad = ctrl.Antecedent(
        np.arange(0, 101, 1),
        'velocidad'
    )

    cajas = ctrl.Antecedent(
        np.arange(0, 501, 1),
        'cajas'
    )

    calidad = ctrl.Antecedent(
        np.arange(0, 11, 1),
        'calidad'
    )

    # =========================================================
    # VARIABLES DIFUSAS DE SALIDA
    # =========================================================

    produccion = ctrl.Consequent(
        np.arange(0, 501, 1),
        'produccion'
    )

    etiquetado = ctrl.Consequent(
        np.arange(0, 101, 1),
        'etiquetado'
    )

    # =========================================================
    # FUNCIONES DE MEMBRESÍA
    # =========================================================

    # VELOCIDAD

    velocidad['baja'] = fuzz.trimf(
        velocidad.universe,
        [0, 0, 40]
    )

    velocidad['media'] = fuzz.trimf(
        velocidad.universe,
        [20, 50, 80]
    )

    velocidad['alta'] = fuzz.trimf(
        velocidad.universe,
        [60, 100, 100]
    )

    # CAJAS

    cajas['pocas'] = fuzz.trimf(
        cajas.universe,
        [0, 0, 200]
    )

    cajas['moderadas'] = fuzz.trimf(
        cajas.universe,
        [100, 250, 400]
    )

    cajas['muchas'] = fuzz.trimf(
        cajas.universe,
        [300, 500, 500]
    )

    # CALIDAD

    calidad['mala'] = fuzz.trimf(
        calidad.universe,
        [0, 0, 4]
    )

    calidad['regular'] = fuzz.trimf(
        calidad.universe,
        [2, 5, 8]
    )

    calidad['buena'] = fuzz.trimf(
        calidad.universe,
        [6, 10, 10]
    )

    # PRODUCCIÓN

    produccion['baja'] = fuzz.trimf(
        produccion.universe,
        [0, 0, 200]
    )

    produccion['media'] = fuzz.trimf(
        produccion.universe,
        [100, 250, 400]
    )

    produccion['alta'] = fuzz.trimf(
        produccion.universe,
        [300, 500, 500]
    )

    # ETIQUETADO

    etiquetado['deficiente'] = fuzz.trimf(
        etiquetado.universe,
        [0, 0, 40]
    )

    etiquetado['aceptable'] = fuzz.trimf(
        etiquetado.universe,
        [30, 50, 70]
    )

    etiquetado['excelente'] = fuzz.trimf(
        etiquetado.universe,
        [60, 100, 100]
    )

    # =========================================================
    # 27 REGLAS DIFUSAS
    # =========================================================

    reglas = [

        ctrl.Rule(
            velocidad['baja'] &
            cajas['pocas'] &
            calidad['mala'],
            [produccion['baja'],
             etiquetado['deficiente']]
        ),

        ctrl.Rule(
            velocidad['baja'] &
            cajas['pocas'] &
            calidad['regular'],
            [produccion['baja'],
             etiquetado['aceptable']]
        ),

        ctrl.Rule(
            velocidad['baja'] &
            cajas['pocas'] &
            calidad['buena'],
            [produccion['media'],
             etiquetado['excelente']]
        ),

        ctrl.Rule(
            velocidad['baja'] &
            cajas['moderadas'] &
            calidad['mala'],
            [produccion['baja'],
             etiquetado['deficiente']]
        ),

        ctrl.Rule(
            velocidad['baja'] &
            cajas['moderadas'] &
            calidad['regular'],
            [produccion['media'],
             etiquetado['aceptable']]
        ),

        ctrl.Rule(
            velocidad['baja'] &
            cajas['moderadas'] &
            calidad['buena'],
            [produccion['media'],
             etiquetado['excelente']]
        ),

        ctrl.Rule(
            velocidad['baja'] &
            cajas['muchas'] &
            calidad['mala'],
            [produccion['baja'],
             etiquetado['deficiente']]
        ),

        ctrl.Rule(
            velocidad['baja'] &
            cajas['muchas'] &
            calidad['regular'],
            [produccion['media'],
             etiquetado['aceptable']]
        ),

        ctrl.Rule(
            velocidad['baja'] &
            cajas['muchas'] &
            calidad['buena'],
            [produccion['alta'],
             etiquetado['excelente']]
        ),

        ctrl.Rule(
            velocidad['media'] &
            cajas['pocas'] &
            calidad['mala'],
            [produccion['baja'],
             etiquetado['deficiente']]
        ),

        ctrl.Rule(
            velocidad['media'] &
            cajas['pocas'] &
            calidad['regular'],
            [produccion['media'],
             etiquetado['aceptable']]
        ),

        ctrl.Rule(
            velocidad['media'] &
            cajas['pocas'] &
            calidad['buena'],
            [produccion['media'],
             etiquetado['excelente']]
        ),

        ctrl.Rule(
            velocidad['media'] &
            cajas['moderadas'] &
            calidad['mala'],
            [produccion['media'],
             etiquetado['deficiente']]
        ),

        ctrl.Rule(
            velocidad['media'] &
            cajas['moderadas'] &
            calidad['regular'],
            [produccion['media'],
             etiquetado['aceptable']]
        ),

        ctrl.Rule(
            velocidad['media'] &
            cajas['moderadas'] &
            calidad['buena'],
            [produccion['alta'],
             etiquetado['excelente']]
        ),

        ctrl.Rule(
            velocidad['media'] &
            cajas['muchas'] &
            calidad['mala'],
            [produccion['media'],
             etiquetado['deficiente']]
        ),

        ctrl.Rule(
            velocidad['media'] &
            cajas['muchas'] &
            calidad['regular'],
            [produccion['alta'],
             etiquetado['aceptable']]
        ),

        ctrl.Rule(
            velocidad['media'] &
            cajas['muchas'] &
            calidad['buena'],
            [produccion['alta'],
             etiquetado['excelente']]
        ),

        ctrl.Rule(
            velocidad['alta'] &
            cajas['pocas'] &
            calidad['mala'],
            [produccion['media'],
             etiquetado['deficiente']]
        ),

        ctrl.Rule(
            velocidad['alta'] &
            cajas['pocas'] &
            calidad['regular'],
            [produccion['media'],
             etiquetado['aceptable']]
        ),

        ctrl.Rule(
            velocidad['alta'] &
            cajas['pocas'] &
            calidad['buena'],
            [produccion['alta'],
             etiquetado['excelente']]
        ),

        ctrl.Rule(
            velocidad['alta'] &
            cajas['moderadas'] &
            calidad['mala'],
            [produccion['media'],
             etiquetado['deficiente']]
        ),

        ctrl.Rule(
            velocidad['alta'] &
            cajas['moderadas'] &
            calidad['regular'],
            [produccion['alta'],
             etiquetado['aceptable']]
        ),

        ctrl.Rule(
            velocidad['alta'] &
            cajas['moderadas'] &
            calidad['buena'],
            [produccion['alta'],
             etiquetado['excelente']]
        ),

        ctrl.Rule(
            velocidad['alta'] &
            cajas['muchas'] &
            calidad['mala'],
            [produccion['media'],
             etiquetado['aceptable']]
        ),

        ctrl.Rule(
            velocidad['alta'] &
            cajas['muchas'] &
            calidad['regular'],
            [produccion['alta'],
             etiquetado['excelente']]
        ),

        ctrl.Rule(
            velocidad['alta'] &
            cajas['muchas'] &
            calidad['buena'],
            [produccion['alta'],
             etiquetado['excelente']]
        )

    ]

    # =========================================================
    # CREAR SISTEMA DIFUSO
    # =========================================================

    sistema_control = ctrl.ControlSystem(
        reglas
    )

    sistema = ctrl.ControlSystemSimulation(
        sistema_control
    )

    # =========================================================
    # INGRESAR DATOS
    # =========================================================

    sistema.input['velocidad'] = velocidad_usuario
    sistema.input['cajas'] = cajas_usuario
    sistema.input['calidad'] = calidad_usuario

    # =========================================================
    # EJECUTAR SISTEMA
    # =========================================================

    sistema.compute()

    # =========================================================
    # RESULTADOS NUMÉRICOS
    # =========================================================

    resultado_produccion = round(
        sistema.output['produccion'],
        2
    )

    resultado_etiquetado = round(
        sistema.output['etiquetado'],
        2
    )

    # =========================================================
    # RESULTADOS DIFUSOS
    # =========================================================

    if resultado_produccion <= 180:

        produccion_difusa = "BAJA"

    elif resultado_produccion <= 350:

        produccion_difusa = "MEDIA"

    else:

        produccion_difusa = "ALTA"

    if resultado_etiquetado <= 40:

        etiquetado_difuso = "DEFICIENTE"

    elif resultado_etiquetado <= 70:

        etiquetado_difuso = "ACEPTABLE"

    else:

        etiquetado_difuso = "EXCELENTE"

    # =========================================================
    # CREAR CARPETA DE GRÁFICAS
    # =========================================================

    if not os.path.exists("static/graficas"):
        os.makedirs("static/graficas")

    # =========================================================
    # GENERAR GRÁFICAS
    # =========================================================

    velocidad.view()
    plt.title("Velocidad")
    plt.savefig("static/graficas/velocidad.png")
    plt.close()

    cajas.view()
    plt.title("Cantidad de Cajas")
    plt.savefig("static/graficas/cajas.png")
    plt.close()

    calidad.view()
    plt.title("Calidad del Aguacate")
    plt.savefig("static/graficas/calidad.png")
    plt.close()

    produccion.view(sim=sistema)
    plt.title("Producción")
    plt.savefig("static/graficas/produccion.png")
    plt.close()

    etiquetado.view(sim=sistema)
    plt.title("Etiquetado")
    plt.savefig("static/graficas/etiquetado.png")
    plt.close()

    # =========================================================
    # FECHA Y HORA
    # =========================================================

    fecha_actual = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    # =========================================================
    # CREAR PDF
    # =========================================================

    pdf = canvas.Canvas(
        "Reporte_TYC_FRUITS.pdf",
        pagesize=letter
    )

    # =========================================================
    # LOGO
    # =========================================================

    pdf.drawImage(
        "static/logo.png",
        220,
        700,
        width=150,
        height=70
    )

    # =========================================================
    # TÍTULOS
    # =========================================================

    pdf.setFont("Helvetica-Bold", 18)

    pdf.drawString(
        120,
        660,
        "T&C FRUITS"
    )

    pdf.setFont("Helvetica", 13)

    pdf.drawString(
        70,
        630,
        "Sistema Inteligente de Cálculo de Producción"
    )

    # =========================================================
    # DATOS ACADÉMICOS
    # =========================================================

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        70,
        600,
        "Alumno: Arturo Campos Rodriguez"
    )

    pdf.drawString(
        70,
        580,
        "Materia: Sistemas Difusos Inteligentes"
    )

    pdf.drawString(
        70,
        560,
        "Maestría: Inteligencia Artificial"
    )

    pdf.drawString(
        70,
        540,
        "Instituto Tecnológico Superior de Uruapan"
    )

    # =========================================================
    # FECHA
    # =========================================================

    pdf.drawString(
        70,
        510,
        f"Fecha y hora: {fecha_actual}"
    )

    # =========================================================
    # DATOS INGRESADOS
    # =========================================================

    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawString(
        70,
        470,
        "DATOS INGRESADOS"
    )

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        90,
        445,
        f"Velocidad: {velocidad_usuario}"
    )

    pdf.drawString(
        90,
        425,
        f"Cajas: {cajas_usuario}"
    )

    pdf.drawString(
        90,
        405,
        f"Calidad: {calidad_usuario}"
    )

    # =========================================================
    # RESULTADOS
    # =========================================================

    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawString(
        70,
        370,
        "RESULTADOS OBTENIDOS"
    )

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        90,
        345,
        f"Producción numérica: {resultado_produccion}"
    )

    pdf.drawString(
        90,
        325,
        f"Producción difusa: {produccion_difusa}"
    )

    pdf.drawString(
        90,
        305,
        f"Etiquetado numérico: {resultado_etiquetado}"
    )

    pdf.drawString(
        90,
        285,
        f"Etiquetado difuso: {etiquetado_difuso}"
    )

    # =========================================================
    # NUEVA PÁGINA
    # =========================================================

    pdf.showPage()

    pdf.setFont("Helvetica-Bold", 16)

    pdf.drawString(
        170,
        750,
        "GRÁFICAS DEL SISTEMA DIFUSO"
    )

    # =========================================================
    # INSERTAR GRÁFICAS
    # =========================================================

    pdf.drawImage(
        "static/graficas/velocidad.png",
        30,
        500,
        width=170,
        height=150
    )

    pdf.drawImage(
        "static/graficas/cajas.png",
        220,
        500,
        width=170,
        height=150
    )

    pdf.drawImage(
        "static/graficas/calidad.png",
        410,
        500,
        width=170,
        height=150
    )

    pdf.drawImage(
        "static/graficas/produccion.png",
        60,
        220,
        width=220,
        height=180
    )

    pdf.drawImage(
        "static/graficas/etiquetado.png",
        320,
        220,
        width=220,
        height=180
    )

    # =========================================================
    # GUARDAR PDF
    # =========================================================

    pdf.save()

    # =========================================================
    # MOSTRAR RESULTADOS
    # =========================================================

    return f'''

    <h1>
        RESULTADOS DEL SISTEMA DIFUSO
    </h1>

    <h2>
        Producción numérica:
        {resultado_produccion}
    </h2>

    <h2>
        Producción difusa:
        {produccion_difusa}
    </h2>

    <h2>
        Etiquetado numérico:
        {resultado_etiquetado}
    </h2>

    <h2>
        Etiquetado difuso:
        {etiquetado_difuso}
    </h2>

    <h3>
        PDF generado correctamente.
    </h3>

    <a href="/descargar_pdf">
        Descargar PDF
    </a>

    <br><br>

    <a href="/">
        Volver al sistema
    </a>

    '''

# =============================================================
# EJECUTAR SERVIDOR
# =============================================================

if __name__ == '__main__':

    app.run()
