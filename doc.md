# Relaciones entre modelos

# **Hacer las vistas de activos e inactivos en Docente,Alumnos, Coordinadores**
**En alumnos hay get para regulares también**

## Modelos a Probar y Cerrar
- [x] Personas
    - [x] Coordinador
    - [x] Docente
    - [x] Alumno
- [x]Especialidades (solo staff or Coordinador)
- [x]Materias (solo staff or Coordinador)
- [x]Comisiones
- [x]Examenes







## Uno a uno (OneToOneField)

- Un Examen tiene una Comisión (relación one to one)
- Un Alumno tiene un Examen (relación one to one)

## Uno a muchos (ForeignKey)

- Un Coordinador puede tener muchos Alumnos (relación de uno a muchos)
- Un Docente puede tener muchos Alumnos (relación de uno a muchos)
- Un Coordinador puede tener muchos Docentes (relación de uno a muchos)
- Un Docente puede tener muchos Exámenes (relación de uno a muchos)
- Un Coordinador puede tener muchos Exámenes (relación de uno a muchos)

## Muchos a muchos (ManyToManyField)

- Un Alumno puede tener muchos Coordinadores (relación de muchos a muchos)
- Un Alumno puede tener muchos Docentes (relación de muchos a muchos)
- Un Coordinador puede tener muchos Alumnos (relación de muchos a muchos)
- Un Docente puede tener muchos Alumnos (relación de muchos a muchos)
- Un Examen puede tener muchos Alumnos (relación de muchos a muchos)
