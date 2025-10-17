from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, template_folder="templates")

def conection():
    con = sqlite3.connect('costos.db')
    cur = con.cursor()
    return cur, con

@app.route("/")
def index():
    cur, con = conection()
    cur.execute("select * from cuentas")
    datos= cur.fetchall()
    return render_template("index.html",datos = datos)

@app.route("/enviar", methods=['POST'])
def enviar():
    accion = request.form['accion']
    print(accion)
    cur, con = conection()

    if accion == "enviar":
        tipo = request.form['tipo']
        modo = request.form['modo']
        conceptos = request.form['conceptos']
        dia = request.form['dia']
        mes = request.form['mes']
        costo = request.form['costo']
        cur.execute('INSERT INTO cuentas (tipo, modo, conceptos, dia, mes, costo) VALUES (?, ?, ?, ?, ?, ?)',
                    (tipo, modo, conceptos, dia, mes, costo))
        con.commit()


    elif accion == 'modificar':
        id = request.form['id']
        tipo = request.form['tipo']
        modo = request.form['modo']
        concepto = request.form['conceptos']
        dia = request.form['dia']
        mes = request.form['mes']
        costo = request.form['costo']

        conn = sqlite3.connect('base.db')
        c = conn.cursor()
        c.execute("""
            UPDATE gestion SET tipo=?, modo=?, concepto=?, dia=?, mes=?, costo=? WHERE id=?
        """, (tipo, modo, concepto, dia, mes, costo, id))
        conn.commit()
        conn.close()
        return redirect(url_for('inicio'))


    elif accion == "borrar":
            cur, con = conection()
            id = request.form['id']
            print(id)
            cur.execute("DELETE FROM cuentas WHERE id=?", (id,))
            con.commit()
            return redirect(url_for('index'))

    elif accion == "borrar_todo":
        cur.execute("DELETE FROM cuentas")
        con.commit()

    return redirect(url_for('index'))


app.run(host="localhost", port=4000, debug=True)