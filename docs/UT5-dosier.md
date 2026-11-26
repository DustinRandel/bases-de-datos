---
title: "SQL: definir y consultar"
subtitulo: "UT5. Dosier de apuntes"
modulo: "0484. Bases de datos"
curso: "2026-2027"
profesor: "Dustin Randel de Lara García"
centro: "Sant Josep Obrer"
ut: "UT5"
---

# Cómo usar este dosier {.nobreak}

Este dosier recoge lo que trabajamos en clase sobre SQL: crear bases y tablas, meter y consultar datos, y las restricciones que impiden basura. Las palabras clave de SQL (`SELECT`, `VARCHAR`, `PRIMARY KEY`…) se escriben en inglés, tal como las verás en MySQL.

Encontrarás cuatro tipos de caja:

!!! definicion "Definición"
    Un término que tienes que saber explicar con tus palabras. Si solo sabes repetirlo de memoria, todavía no lo has aprendido.

!!! ejemplo "Ejemplo"
    Un caso concreto, con valores reales siempre que se pueda. Léelo despacio: aquí es donde la idea se entiende.

!!! ojo "Ojo"
    Un error típico o dos conceptos que se suelen confundir. Son las preguntas que salen en el examen.

!!! comprueba "Comprueba"
    De tres a cinco preguntas al final de cada bloque. Contesta sin mirar atrás. Si te atascas, vuelve a leer el bloque.

Al final tienes un **glosario**, un **mapa resumen** y una **autoevaluación**.

Los ejemplos usan MySQL, el gestor de clase. Otros gestores hablan casi igual; si algo cambia, lo dice la documentación.

## Qué vas a aprender

Al terminar esta UT deberías ser capaz de:

- Explicar qué es SQL y por qué es un lenguaje declarativo.
- Crear, usar y borrar una base de datos, y crear tablas con tipos de columna.
- Distinguir DDL (estructura) de DML (datos) y saber qué se puede deshacer con `ROLLBACK`.
- Insertar, consultar, actualizar y borrar filas, siempre con `WHERE` cuando toca.
- Poner restricciones (`NOT NULL`, `UNIQUE`, `PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `DEFAULT`) y predecir qué INSERT va a fallar.

## Índice

| Bloque | Tema |
|---|---|
| [1](#bloque-1-que-es-sql) | [Qué es SQL](#bloque-1-que-es-sql) |
| [2](#bloque-2-bases-de-datos-y-tablas) | [Bases de datos y tablas](#bloque-2-bases-de-datos-y-tablas) |
| [3](#bloque-3-meter-consultar-y-cambiar-datos) | [Meter, consultar y cambiar datos](#bloque-3-meter-consultar-y-cambiar-datos) |
| [4](#bloque-4-transacciones) | [Transacciones](#bloque-4-transacciones) |
| [5](#bloque-5-restricciones) | [Restricciones](#bloque-5-restricciones) |
| Repaso | [Glosario, mapa resumen y autoevaluación](#material-de-repaso) |

# Bloque 1. Qué es SQL

## 1.1 Un lenguaje para decir qué quieres, no cómo

!!! definicion "Definición"
    **SQL** (*Structured Query Language*) es el lenguaje de los SGBD relacionales. Es **declarativo**: describes el resultado que quieres; el gestor decide cómo obtenerlo.

No le dices a MySQL «recorre la tabla de la fila 1 a la 8000 comparando la columna 3». Le dices «los empleados del departamento Ventas, ordenados por sueldo». Eso es un lenguaje de cuarta generación (4GL): más cerca del castellano que un `for` en Java.

SQL está estandarizado y vale en MySQL, MariaDB, Oracle, PostgreSQL… Cada uno añade detalles propios. En este módulo usamos **MySQL**. Si copias un ejemplo de Internet pensado para Oracle, puede fallar.

## 1.2 Más que consultar

SQL no es solo `SELECT`. Con el mismo lenguaje:

| Qué haces | Familia | Ejemplos |
|---|---|---|
| Crear y cambiar la estructura | **DDL** (definición) | `CREATE`, `ALTER`, `DROP` |
| Meter, cambiar y leer filas | **DML** (manipulación) | `INSERT`, `UPDATE`, `DELETE`, `SELECT` |
| Decidir quién puede qué | **DCL** (control) | `GRANT`, `REVOKE` |

!!! ejemplo "Ejemplo"
    La misma cafetería, tres frases:
    `CREATE TABLE producto (...)` define la tabla.
    `INSERT INTO producto VALUES (...)` mete un café.
    `GRANT SELECT ON producto TO invitado` deja mirar, no tocar.

Los **comandos** (`SELECT`, `INSERT`…) se combinan con **cláusulas** (`WHERE`, `ORDER BY`, `GROUP BY`), **operadores** (`=`, `<`, `LIKE`, `AND`) y **funciones** (`COUNT`, `AVG`, `MAX`).

```sql
SELECT nombre, sueldo_hora
FROM empleado
WHERE departamento = 'Ventas'
ORDER BY sueldo_hora DESC;
```

Esta consulta pide nombres y sueldos de Ventas, del más alto al más bajo. No dice si MySQL usará un índice o recorrerá la tabla: eso lo decide el gestor.

!!! comprueba "Comprueba"
    1. ¿Qué significa que SQL sea declarativo?
    2. ¿`CREATE TABLE` es DDL o DML? ¿Y `DELETE`?
    3. ¿Un `SELECT` escrito para MySQL vale siempre en Oracle sin cambios?

# Bloque 2. Bases de datos y tablas

## 2.1 La base es la carpeta; las tablas, los ficheros

Una **base de datos** agrupa tablas, vistas e índices. Piensa en ella como una carpeta; las tablas son los ficheros de dentro.

```sql
CREATE DATABASE cafeteria;
USE cafeteria;
DROP DATABASE cafeteria;
```

`USE` fija la base por defecto en esa sesión. Si no la usas, tienes que escribir `cafeteria.empleado` cada vez.

!!! ojo "Ojo"
    `DROP DATABASE` borra la base **y todo lo de dentro**. No hay papelera. En clase, nunca la lances contra una base que no hayas creado tú.

Los comentarios no se ejecutan. En MySQL:

```sql
SELECT * FROM empleado;   /* una línea o varias */

/*
   bloque más largo
   que puedes dejar en un script
*/
```

## 2.2 Crear una tabla

!!! definicion "Definición"
    `CREATE TABLE` define el **nombre** de la tabla y, para cada columna, su **nombre**, su **tipo** y, si toca, una **restricción**.

```sql
CREATE TABLE empleado (
    id INT,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    sueldo_hora DECIMAL(5, 2),
    fecha_alta DATE
);
```

`DECIMAL(5, 2)` guarda cinco dígitos, dos de ellos decimales: de 0,00 a 999,99. El sueldo no va en `FLOAT`: el redondeo binario convierte 0,1 + 0,2 en basura.

## 2.3 Cambiar y borrar la estructura

Una vez creada, la tabla se retoca con `ALTER TABLE` y se tira con `DROP TABLE`.

```sql
RENAME TABLE empleado TO trabajador;

ALTER TABLE empleado ADD telefono VARCHAR(15);
ALTER TABLE empleado RENAME COLUMN telefono TO email;
ALTER TABLE empleado MODIFY COLUMN email VARCHAR(100);
ALTER TABLE empleado DROP COLUMN email;

DROP TABLE empleado;
```

`DROP TABLE` borra la tabla y **todas las filas**. No es lo mismo que `DELETE FROM empleado`, que vacía las filas y deja la estructura.

!!! comprueba "Comprueba"
    1. ¿Qué hace `USE cafeteria`?
    2. Escribe el `CREATE TABLE` de `producto (id entero, nombre hasta 25 caracteres, precio con dos decimales)`.
    3. ¿Qué se pierde con `DROP TABLE` que no se pierde con `DELETE FROM`?

# Bloque 3. Meter, consultar y cambiar datos

## 3.1 INSERT

```sql
INSERT INTO empleado
VALUES
    (1, 'Ana', 'Pérez', 15.00, '2023-01-03'),
    (2, 'Luis', 'Gómez', 12.50, '2023-01-04');

INSERT INTO empleado (id, nombre, apellido)
VALUES (5, 'Carla', 'Ruiz');
```

Si no listas columnas, tienes que dar **todas**, en el orden del `CREATE TABLE`. Si listas algunas, las que faltan quedan a `NULL` (o al `DEFAULT`, bloque 5).

## 3.2 SELECT y WHERE

```sql
SELECT * FROM empleado;
SELECT nombre, apellido FROM empleado;
SELECT * FROM empleado WHERE id = 1;
SELECT * FROM empleado WHERE id <> 1;
SELECT * FROM empleado WHERE sueldo_hora >= 15;
```

`*` es todas las columnas. En cuanto sepas cuáles necesitas, nómbralas: se lee mejor y no arrastras basura.

!!! ojo "Ojo"
    Para `NULL` no vale `=` ni `<>`. Se usa `IS NULL` e `IS NOT NULL`. Lo viste en la UT3; aquí lo vuelves a necesitar:

    ```sql
    SELECT * FROM empleado WHERE fecha_alta IS NULL;
    ```

## 3.3 UPDATE y DELETE

```sql
UPDATE empleado
SET sueldo_hora = 10.50, fecha_alta = '2023-01-07'
WHERE id = 5;

DELETE FROM empleado
WHERE id = 5;
```

!!! ojo "Ojo"
    Sin `WHERE`, `UPDATE` cambia **todas** las filas y `DELETE` las borra **todas**. El gestor no pregunta. Antes de ejecutar, lee la línea otra vez.

!!! comprueba "Comprueba"
    1. ¿Qué valor toma `fecha_alta` en el INSERT que solo pone id, nombre y apellido?
    2. Escribe el `SELECT` de los empleados con sueldo_hora menor que 13.
    3. ¿Qué pasa si ejecutas `DELETE FROM empleado;`?

# Bloque 4. Transacciones

## 4.1 Un paquete que se confirma o se deshace

!!! definicion "Definición"
    Una **transacción** es un conjunto de operaciones que se tratan como un solo trabajo: o valen todas (`COMMIT`) o no vale ninguna (`ROLLBACK`).

Por defecto MySQL tiene **autocommit**: cada sentencia se confirma sola. Eso es cómodo y peligroso: un `DELETE` mal escrito no se deshace.

```sql
SET autocommit = 0;
START TRANSACTION;

UPDATE empleado SET sueldo_hora = 20.00 WHERE id = 2;
/* miras el resultado */
COMMIT;

UPDATE empleado SET sueldo_hora = 30.00 WHERE id = 3;
/* te has equivocado */
ROLLBACK;
```

## 4.2 Lo que no se deshace

Las sentencias **DML** (`INSERT`, `UPDATE`, `DELETE`) sí entran en la transacción. Las **DDL** (`CREATE`, `ALTER`, `DROP`) en MySQL se confirman solas: un `DROP TABLE` no vuelve con `ROLLBACK`.

!!! ejemplo "Ejemplo"
    `DELETE FROM empleado WHERE id = 4;` y luego `ROLLBACK;` recupera a esa persona, si no habías hecho `COMMIT`.
    `DROP TABLE empleado;` no tiene marcha atrás.

!!! comprueba "Comprueba"
    1. ¿Qué ventaja tiene apagar el autocommit mientras pruebas?
    2. ¿`ROLLBACK` recupera una tabla que acabas de borrar con `DROP TABLE`?
    3. ¿En qué se diferencia `COMMIT` de `ROLLBACK`?

# Bloque 5. Restricciones

Las restricciones son reglas que el gestor **comprueba solo**. Si una fila las rompe, el INSERT o el UPDATE falla. Esas reglas son las mismas que viste en el modelo relacional (unicidad, NOT NULL, claves); ahora se escriben en SQL.

## 5.1 UNIQUE y NOT NULL

`UNIQUE`: esa columna (o combinación) no se repite. Admite `NULL` salvo que pongas también `NOT NULL`.
`NOT NULL`: la columna no puede quedar vacía. No exige unicidad.

```sql
CREATE TABLE producto (
    id INT,
    nombre VARCHAR(25) UNIQUE,
    precio DECIMAL(4, 2) NOT NULL
);

INSERT INTO producto VALUES (101, 'fries', 1.89);
INSERT INTO producto VALUES (104, 'fries', 1.75);
/* falla: nombre duplicado */

INSERT INTO producto VALUES (107, 'hamburger', NULL);
/* falla: precio NOT NULL */
```

Si se te olvidó al crear la tabla:

```sql
ALTER TABLE producto
ADD CONSTRAINT unique_nombre UNIQUE (nombre);

ALTER TABLE producto
MODIFY precio DECIMAL(4, 2) NOT NULL;
```

## 5.2 CHECK y DEFAULT

`CHECK` limita el rango con una condición. `DEFAULT` rellena la columna si el INSERT no la trae.

```sql
CREATE TABLE empleado (
    id INT,
    nombre VARCHAR(50),
    sueldo_hora DECIMAL(5, 2),
    CONSTRAINT chk_sueldo CHECK (sueldo_hora >= 10.00)
);

ALTER TABLE producto
ALTER precio SET DEFAULT 0.00;

INSERT INTO producto (id, nombre) VALUES (104, 'pajita');
/* precio queda 0.00 */
```

## 5.3 PRIMARY KEY y AUTO_INCREMENT

!!! definicion "Definición"
    La **clave primaria** identifica cada fila. Implica `UNIQUE` y `NOT NULL`. Una tabla tiene **una** (simple o compuesta).

```sql
CREATE TABLE venta (
    id INT PRIMARY KEY AUTO_INCREMENT,
    importe DECIMAL(5, 2)
) AUTO_INCREMENT = 1000;
```

`AUTO_INCREMENT` (propiedad de una columna `INT` que es PK, no un tipo) numera solo. El primer `INSERT` sin id pone 1000; el siguiente, 1001.

## 5.4 FOREIGN KEY

!!! definicion "Definición"
    Una **clave ajena** es una columna (o varias) cuyos valores tienen que existir como clave primaria de otra tabla, o ser `NULL`.

```sql
CREATE TABLE cliente (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50),
    apellido VARCHAR(50)
);

CREATE TABLE venta (
    id INT PRIMARY KEY AUTO_INCREMENT,
    importe DECIMAL(5, 2),
    id_cliente INT,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id)
);
```

Insertar una venta con `id_cliente = 7` falla si el cliente 7 no existe. Poner `id_cliente` a `NULL` deja la venta sin cliente (mínimo 0, como en la UT3).

La FK va en el lado **muchos**: un cliente tiene muchas ventas, así que `id_cliente` vive en `venta`.

!!! comprueba "Comprueba"
    1. ¿`UNIQUE` impide los NULL? ¿Y `PRIMARY KEY`?
    2. ¿Qué INSERT falla si `precio` es `NOT NULL` y `nombre` es `UNIQUE`?
    3. ¿Por qué la FK de las ventas no se pone en `cliente`?
    4. Escribe el `CREATE TABLE` de `venta` con PK autoincremental y FK a `cliente`.

# Material de repaso

## Glosario

| Término | Qué es |
|---|---|
| SQL | Lenguaje de los SGBD relacionales. Declarativo. |
| DDL | Define estructura: `CREATE`, `ALTER`, `DROP`. |
| DML | Manipula filas: `INSERT`, `SELECT`, `UPDATE`, `DELETE`. |
| DCL | Controla permisos: `GRANT`, `REVOKE`. |
| Transacción | Paquete que se confirma (`COMMIT`) o se deshace (`ROLLBACK`). |
| Autocommit | Cada sentencia se confirma sola. En MySQL, por defecto. |
| UNIQUE | Los valores no se repiten. NULL sí, si no hay NOT NULL. |
| NOT NULL | La columna no puede quedar vacía. |
| PRIMARY KEY | Identifica la fila. UNIQUE + NOT NULL. Una por tabla. |
| FOREIGN KEY | Tiene que existir en la PK de otra tabla, o ser NULL. |
| CHECK | Condición que cada fila debe cumplir. |
| DEFAULT | Valor si el INSERT no trae esa columna. |
| AUTO_INCREMENT | La PK entera se numera sola. |

## Mapa resumen

1. SQL describe el **qué**. El gestor se ocupa del **cómo**.
2. DDL construye el esqueleto. DML llena y consulta las filas. Un `DROP` no se deshace; un `DELETE` sí, si estás en una transacción.
3. Las restricciones son las reglas del modelo relacional escritas en SQL. Si una fila las rompe, el gestor dice que no.

## Autoevaluación

Sin mirar atrás. Las soluciones no están aquí: contrastalas con el dosier o en clase.

1. ¿Por qué se dice que SQL es declarativo? Pon un ejemplo de algo que tú no decides.
2. Clasifica cada una: `ALTER TABLE`, `INSERT`, `GRANT`, `SELECT`.
3. Escribe el `CREATE TABLE` de `producto(id PK autoincremental, nombre VARCHAR(25) único, precio NOT NULL con dos decimales)`.
4. Un compañero ejecuta `UPDATE empleado SET sueldo_hora = 8;` y se le cambian 40 filas. ¿Qué olvidó?
5. ¿`ROLLBACK` deshace un `DROP TABLE`? ¿Y un `DELETE` sin `COMMIT`?
6. `nombre UNIQUE` admite dos filas con `nombre` a NULL. ¿Por qué?
7. Dibuja (en esquema) `cliente` y `venta` con la FK en el sitio correcto.
8. ¿Qué valor toma `precio` si tiene `DEFAULT 0.00` y el INSERT no lo menciona?
9. ¿`AUTO_INCREMENT` es un tipo de dato?
10. Relaciona cada restricción con la idea de la UT3 o la UT4 que ya conocías.
