import os
from flask import Flask, render_template, request, redirect, url_for
from CPostgreSQL import f_agregar_cliente, f_listar_clientes

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registro", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        ap_paterno = request.form.get("apellido_paterno")
        ap_materno = request.form.get("apellido_materno")
        correo = request.form.get("correo")
        telefono = request.form.get("telefono")
        
        f_agregar_cliente(nombre, ap_paterno, ap_materno, correo, telefono)
        return redirect(url_for("mostrar_clientes"))
    return render_template("registro.html")

@app.route("/mostrar_clientes")
def mostrar_clientes():
    clientes = f_listar_clientes()
    return render_template("mostrar_clientes.html", clientes=clientes)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)