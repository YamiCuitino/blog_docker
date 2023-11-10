from datetime import *
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
    )
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey


app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:contraseña@ip/nombre_db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/efi_blog'

db = SQLAlchemy(app=app)
migrate = Migrate(app, db)

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable = False)
    correo = db.Column(db.String(100), nullable = False)
    contraseña = db.Column(db.String(100), nullable = False)


    def __str__(self):
        return self.nombre

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    contenido = db.Column(db.String(1000), nullable=False)
    fecha_creacion = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('posts', lazy=True))
    categorias = db.relationship("Categoria", secondary="post_categoria", backref=db.backref('posts', lazy=True))

    def __str__(self):
        return self.titulo

class Comentario(db.Model):
    __tablename__ = 'comentario'
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    entrada_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    usuario = db.relationship('Usuario',backref=db.backref('comentarios', lazy=True))
    entrada = db.relationship('Post',backref=db.backref('comentarios', lazy=True))

    def __str__(self):
        return self.texto


class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return self.nombre

post_categoria = db.Table('post_categoria', 
    db.Column('entrada_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('categoria_id', db.Integer, db.ForeignKey('categoria.id'), primary_key=True)
)
    
@app.context_processor
def inject_mensaje():
    usuarios = Usuario.query.all()
    posteos = Post.query.all()
    comentarios = Comentario.query.all()
    categorias = Categoria.query.all()

    return dict(
        usuarios = usuarios,
        posteos = posteos,
        comentarios = comentarios,
        categorias = categorias
    )

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/posteos.html")
def posteos():
    categoria_id = request.args.get('categoria_id')

    if categoria_id:
        categoria_elegida = Categoria.query.get(categoria_id)
        entradas = categoria_elegida.posts if categoria_elegida else []
    else:
        categoria_elegida = None
        entradas = Post.query.all()

    return render_template('posteos.html', categoria_elegida=categoria_elegida, posteos=entradas)


@app.route('/crear_usuario', methods = ['POST'])
def add_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña_Usuario = request.form['contraseña']
        usuario = Usuario(nombre = nombre, correo = correo, contraseña = contraseña_Usuario)
        db.session.add(usuario)
        db.session.commit()

        return redirect(url_for('posteos')) 

@app.route('/crear_posteo', methods = ['GET','POST'])
def postear():
    if request.method == 'POST':
        titulo_posteo = request.form['titulo']
        contenido_posteo = request.form['contenido']
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime("%Y-%m-%d %H:%M")
        categoria_seleccionada = request.form.getlist('categorias')
        nuevo_posteo = Post(titulo = titulo_posteo, contenido = contenido_posteo, fecha_creacion = fecha_formateada, usuario_id = 1)
        for categoria_id in categoria_seleccionada:
            categoria = Categoria.query.get(categoria_id)
            if categoria:
                nuevo_posteo.categorias.append(categoria)
        db.session.add(nuevo_posteo)
        db.session.commit()
        return redirect(url_for('posteos'))


    
@app.route('/crear_comentario', methods = ['POST'])
def comentar():
    if request.method == 'POST':
        posteo_id = request.form.get('posteo_id')
        comentario = request.form.get('comentario')
        fecha_comentario = datetime.now()
        fecha_formateada = fecha_comentario.strftime("%Y-%m-%d %H:%M")
        if posteo_id and comentario:
            entrada = Post.query.get(posteo_id)
            if entrada:
                nuevo_comentario = Comentario(texto = comentario, fecha_creacion = fecha_formateada, usuario_id = 1, entrada_id=posteo_id)
                db.session.add(nuevo_comentario)
                db.session.commit()

        return redirect(url_for('posteos'))



@app.route('/template_posteos')
def otro_template():
    return render_template(
        'posteos.html',
    )


