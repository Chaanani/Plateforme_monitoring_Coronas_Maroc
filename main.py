from flask import Flask, request, render_template, flash,  redirect, url_for, session
import hashlib, uuid, os
from werkzeug.utils import secure_filename
puh = Flask(__name__)
import mysql.connector as MS
UPLOAD_FOLDER = '/mnt/c/Users'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])



connection = MS.connect(user='root', password='', host='localhost', buffered=True)
cursor = connection.cursor()

utiliser_bd = "USE pyflask"
cursor.execute(utiliser_bd)
puh.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
puh.config['IMAGES_PATH'] = UPLOAD_FOLDER
puh.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)

@puh.route('/',methods=["GET","POST"])
def connecter():
    if  request.method=="POST":
        cursor=connection.cursor()
        e_mail=request.form["e_mail"]
        req_no="select * from client where Email=%s"
        cursor.execute(req_no, (e_mail,))
        data = cursor.fetchall()
        connection.commit()
        if len(data)==0:
            error="compte n'existe pas"
            return render_template('connecter.html',error=error)
        else:
            return render_template('region.html')
    else:
        return render_template('connecter.html')
@puh.route('/index', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        prenom = request.form["prenom"]
        nom = request.form["nom"]
        e_mail = request.form["e_mail"]
        mot_de_passe = request.form["mot_de_passe"]
        mot_de_passe_hash = hashlib.sha256(str(mot_de_passe).encode("utf-8")).hexdigest()
        description = request.form["description"]
        req_enregister_client = "INSERT INTO Client ( Prenom, Nom, Email, MotDePasseHash, Description)VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(req_enregister_client, ( prenom, nom, e_mail, mot_de_passe_hash, description))
        connection.commit()
        return render_template('region.html')

@puh.route('/region',methods=["GET","POST"])
def region():
    if request.method=="POST":
        return "hello word"
    else:
        return "hello youness"   
@puh.route('/informations',methods=["GET","POST"])
def informations():
    if request.method=="GET":
        cur = connection.cursor()
        requette_avoir_id_client = 'SELECT * FROM Client;'
        cur.execute(requette_avoir_id_client)
        data= cur.fetchall()
        connection.commit()
        return render_template('informations.html',data=data)
    else:
        return "bonjourtout"
@puh.route('/supprimer/<int:id>',methods=["GET","POST"])
def supprimer(id):
    cursor = connection.cursor()
    sql_Delete_query = """Delete from client where IdClient = %s"""
    cursor.execute(sql_Delete_query,(id,))
    connection.commit()
    return redirect(url_for('informations'))
@puh.route('/modifier/<int:id>',methods=["GET","POST"])
def modifier(id):
    if request.method=="POST":
        cursor = connection.cursor()
        idClient=request.form["idClient"]
        prenom = request.form["prenom"]
        nom = request.form["nom"]
        e_mail = request.form["e_mail"]
        mot_de_passe = request.form["mot_de_passe"]
        description = request.form["description"]
        rqt_update_sql="UPDATE client SET Prenom = %s ,Nom=%s ,Email=%s,MotDePasseHash=%s,Description=%s where IdClient=%s"
        cursor.execute(rqt_update_sql,(prenom,nom,e_mail,mot_de_passe,description,idClient,))
        connection.commit()
        return redirect(url_for('informations'))
    if request.method=="GET":
      cursor = connection.cursor()
      sql_Delete_query = """select * from client where IdClient = %s"""
      cursor.execute(sql_Delete_query, (id,))
      data = cursor.fetchall()
      connection.commit()
      return render_template('modifier.html',data=data)
@puh.route('/deconnexion',methods=["GET","POST"])
def se_deconnecter():
        session.pop("e_mail", None)
        flash('Vous etes maintenant deconnecte')
        return redirect(url_for('connecter'))
if __name__ == '__main__':
    puh.run(debug=True)
    