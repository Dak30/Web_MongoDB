from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Cadena de conexión a MongoDB Atlas
cadena_conexion = "mongodb+srv://root:pa55word@cluster0.tiyh3x2.mongodb.net/"

# Conexión a MongoDB Atlas
cliente = pymongo.MongoClient(cadena_conexion)
mi_base_datos = cliente["biblioteca"]

# Colecciones de la base de datos
usuarios = mi_base_datos["usuarios"]
libros = mi_base_datos["libros"]
prestamos = mi_base_datos["prestamos"]
sedes_biblioteca = mi_base_datos["sedes_biblioteca"]

@app.route('/')
def index():
    """Página principal que muestra listas de usuarios y libros."""
    lista_usuarios = list(usuarios.find())
    lista_libros = list(libros.find())
    return render_template('index.html', usuarios=lista_usuarios, libros=lista_libros)

@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    """Ruta para crear un nuevo usuario."""
    nombre = request.form['nombre']
    edad = request.form['edad']
    usuario = {"nombre": nombre, "edad": edad}
    usuarios.insert_one(usuario)
    return redirect(url_for('index'))

@app.route('/leer_usuarios')
def leer_usuarios():
    """Ruta para leer y mostrar todos los usuarios."""
    lista_usuarios = list(usuarios.find())
    return render_template('leer_usuarios.html', usuarios=lista_usuarios)

@app.route('/actualizar_usuario', methods=['POST'])
def actualizar_usuario():
    """Ruta para actualizar la información de un usuario."""
    try:
        filtro = {"nombre": request.form['nombre']}
        nuevos_datos = {"$set": {}}
        nuevo_nombre = request.form.get('nuevo_nombre')
        nueva_edad = request.form.get('edad')

        if nuevo_nombre or nueva_edad:
            if nuevo_nombre:
                nuevos_datos["$set"]["nombre"] = nuevo_nombre
            if nueva_edad:
                nuevos_datos["$set"]["edad"] = nueva_edad

            usuarios.update_one(filtro, nuevos_datos)
            flash("Usuario actualizado exitosamente", "success")
        else:
            flash("Debe proporcionar al menos un campo para actualizar (Nuevo nombre o Edad)", "error")
        return redirect(url_for('leer_usuarios'))
    except Exception as e:
        flash("Error al actualizar usuario: " + str(e), "error")
        return redirect(url_for('leer_usuarios'))

@app.route('/eliminar_usuario', methods=['POST'])
def eliminar_usuario():
    """Ruta para eliminar un usuario."""
    filtro = {"nombre": request.form['nombre']}
    usuarios.delete_one(filtro)
    return redirect(url_for('leer_usuarios'))

@app.route('/crear_libro', methods=['POST'])
def crear_libro():
    """Ruta para crear un nuevo libro."""
    titulo = request.form['titulo']
    autor = request.form['autor']
    libro = {"titulo": titulo, "autor": autor}
    libros.insert_one(libro)
    return redirect(url_for('index'))

@app.route('/leer_libros')
def leer_libros():
    """Ruta para leer y mostrar todos los libros."""
    lista_libros = list(libros.find())
    return render_template('leer_libros.html', libros=lista_libros)

@app.route('/actualizar_libro', methods=['POST'])
def actualizar_libro():
    """Ruta para actualizar la información de un libro."""
    try:
        filtro = {"titulo": request.form['titulo']}
        nuevos_datos = {"$set": {}}
        nuevo_titulo = request.form.get('nuevo_titulo')
        nuevo_autor = request.form.get('nuevo_autor')

        if nuevo_autor or nuevo_titulo:
            if nuevo_autor:
                nuevos_datos["$set"]["autor"] = nuevo_autor
            if nuevo_titulo:
                nuevos_datos["$set"]["titulo"] = nuevo_titulo

            libros.update_one(filtro, nuevos_datos)
            flash("Libro actualizado exitosamente", "success")
        else:
            flash("Debe proporcionar al menos un campo para actualizar (Nuevo Título o Autor)", "error")
        return redirect(url_for('leer_libros'))
    except Exception as e:
        flash("Error al actualizar libro: " + str(e), "error")
        return redirect(url_for('leer_libros'))

@app.route('/eliminar_libro', methods=['POST'])
def eliminar_libro():
    """Ruta para eliminar un libro."""
    filtro = {"titulo": request.form['titulo']}
    libros.delete_one(filtro)
    return redirect(url_for('leer_libros'))

@app.route('/crear_prestamo', methods=['POST'])
def crear_prestamo():
    """Ruta para crear un nuevo préstamo."""
    usuario = request.form['usuario']
    libro = request.form['libro']
    fecha_prestamo = request.form['fecha_prestamo']
    fecha_devolucion = request.form['fecha_devolucion']
    prestamo = {
        "usuario": usuario,
        "libro": libro,
        "fecha_prestamo": fecha_prestamo,
        "fecha_devolucion": fecha_devolucion
    }
    prestamos.insert_one(prestamo)
    return redirect(url_for('index'))

@app.route('/leer_prestamos')
def leer_prestamos():
    """Ruta para leer y mostrar todos los préstamos."""
    lista_prestamos = list(prestamos.find())
    return render_template('leer_prestamos.html', prestamos=lista_prestamos)

@app.route('/eliminar_prestamo', methods=['POST'])
def eliminar_prestamo():
    """Ruta para eliminar un préstamo."""
    usuario = request.form['usuario']
    libro = request.form['libro']
    filtro = {"usuario": usuario, "libro": libro}
    prestamos.delete_one(filtro)
    return redirect(url_for('leer_prestamos'))

@app.route('/crear_sede', methods=['POST'])
def crear_sede():
    """Ruta para crear una nueva sede de biblioteca."""
    nombre = request.form['nombre']
    ubicacion = request.form['ubicacion']
    titulo_libro = request.form['titulo_libro']
    libro = libros.find_one({"titulo": titulo_libro})

    if libro:
        sede = {
            "nombre": nombre,
            "ubicacion": ubicacion,
            "titulo_libro": libro['titulo']
        }
        sedes_biblioteca.insert_one(sede)
        return redirect(url_for('index'))
    else:
        flash("El libro especificado no existe", "error")
        return redirect(url_for('index'))

@app.route('/leer_sedes')
def leer_sedes():
    """Ruta para leer y mostrar todas las sedes de la biblioteca."""
    lista_sedes = list(sedes_biblioteca.find())
    return render_template('leer_sedes.html', sedes=lista_sedes)

@app.route('/actualizar_sede', methods=['POST'])
def actualizar_sede():
    """Ruta para actualizar la información de una sede de biblioteca."""
    try:
        filtro = {"nombre": request.form['nombre']}
        nuevos_datos = {"$set": {}}
        nueva_ubicacion = request.form.get('nueva_ubicacion')
        nuevo_libro = request.form.get('nuevo_libro')

        if nueva_ubicacion or nuevo_libro:
            if nueva_ubicacion:
                nuevos_datos["$set"]["ubicacion"] = nueva_ubicacion
            if nuevo_libro:
                libro = libros.find_one({"titulo": nuevo_libro})
                if libro:
                    nuevos_datos["$set"]["titulo_libro"] = libro['titulo']
                else:
                    flash("El libro especificado no existe", "error")
                    return redirect(url_for('leer_sedes'))

            sedes_biblioteca.update_one(filtro, nuevos_datos)
            flash("Sede actualizada exitosamente", "success")
        else:
            flash("Debe proporcionar al menos un campo para actualizar (Nueva Ubicación o Libro Existente)", "error")
        return redirect(url_for('leer_sedes'))
    except Exception as e:
        flash("Error al actualizar sede: " + str(e), "error")
        return redirect(url_for('leer_sedes'))

@app.route('/eliminar_sede', methods=['POST'])
def eliminar_sede():
    """Ruta para eliminar una sede de biblioteca."""
    filtro = {"nombre": request.form['nombre']}
    sedes_biblioteca.delete_one(filtro)
    return redirect(url_for('leer_sedes'))

if __name__ == '__main__':
    app.run(debug=True)
