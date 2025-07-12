# API para administration de colegios y curso de estudiantes

En el proyecto se implementa una API RESTful para la administración de colegios y cursos de estudiantes.
Se van a poder de alta los modelos de

- **Alumnos**: Representa a los estudiantes que están inscritos en los colegios.
- **Docentes**: Representa a los profesores que imparten clases en los colegios.
- **Coordinador**: Representa a los a una persona que puede realizar taras de administración.
- **Especialidad**: Representa las especialidades o áreas de conocimiento que pueden tener los docentes.
- **Materias**: Representa las asignaturas que se enseñan en los colegios.
- **comisiones**: Representa las comisiones o grupos de estudiantes que cursan las materias.
- **Examenes**: Representa los exámenes que se realizan a los estudiantes.

## Características Principales
- **Autenticación y Autorización**: Implementa autenticación básica para proteger los endpoints de la API.
- **Operaciones CRUD**: Permite crear, leer, actualizar y eliminar registros de todos los modelos.
- **Serialización**: Utiliza serializadores para convertir los modelos de Django en formatos JSON y viceversa.
- **Paginación**: Implementa paginación para manejar grandes volúmenes de datos de manera eficiente.
- **Validación de Datos**: Incluye validaciones para asegurar la integridad de los datos ingresados.
- **Documentación de la API**: Utiliza herramientas como Swagger o ReDoc para generar documentación interactiva de la API.
- **Relaciones entre Modelos**: Maneja relaciones entre los modelos, como la relación entre alumnos y comisiones, o docentes y materias.
- **Manejo de Errores**: Implementa un manejo adecuado de errores para proporcionar respuestas claras en caso de fallos.

## Tecnologías Utilizadas
- **Django**: Framework web para el desarrollo de aplicaciones en Python.
- **Django REST Framework**: Extensión de Django para construir APIs RESTful.
- **SQLite**: Base de datos ligera para el almacenamiento de datos.
- **PDM**: Gestor de paquetes para manejar las dependencias del proyecto.
- **Swagger/ReDoc**: Herramientas para la documentación de la API.

