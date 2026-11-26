---
title: "SQL: unir tablas y resumir"
subtitulo: "UT6. Dosier de apuntes"
modulo: "0484. Bases de datos"
curso: "2026-2027"
profesor: "Dustin Randel de Lara García"
centro: "Sant Josep Obrer"
ut: "UT6"
---

# Cómo usar este dosier {.nobreak}

Este dosier recoge cómo consultar **varias tablas a la vez** (JOIN) y cómo **resumir** filas (COUNT, SUM, AVG) en MySQL. Parte de las tablas y las FK de la UT5.

Encontrarás cuatro tipos de caja:

!!! definicion "Definición"
    Un término que tienes que saber explicar con tus palabras.

!!! ejemplo "Ejemplo"
    Un caso concreto. Léelo despacio.

!!! ojo "Ojo"
    Un error típico. Suelen caer en el examen.

!!! comprueba "Comprueba"
    Preguntas al final de cada bloque. Contesta sin mirar atrás.

Al final tienes un **glosario**, un **mapa resumen** y una **autoevaluación**.

## Qué vas a aprender

Al terminar esta UT deberías ser capaz de:

- Explicar qué hace un JOIN y en qué columna se apoya (casi siempre una FK).
- Distinguir INNER, LEFT, RIGHT y SELF JOIN, y predecir qué filas salen (y cuáles quedan a NULL).
- Usar alias de tabla, COUNT, SUM, AVG, MAX y MIN.
- Ordenar, limitar, filtrar con LIKE y juntar resultados con UNION.

## Índice

| Bloque | Tema |
|---|---|
| [1](#bloque-1-inner-join) | [INNER JOIN](#bloque-1-inner-join) |
| [2](#bloque-2-left-right-y-self-join) | [LEFT, RIGHT y SELF JOIN](#bloque-2-left-right-y-self-join) |
| [3](#bloque-3-funciones-de-agregacion) | [Funciones de agregación](#bloque-3-funciones-de-agregacion) |
| [4](#bloque-4-filtrar-ordenar-y-unir-resultados) | [Filtrar, ordenar y unir resultados](#bloque-4-filtrar-ordenar-y-unir-resultados) |
| Repaso | [Glosario, mapa resumen y autoevaluación](#material-de-repaso) |

# Bloque 1. INNER JOIN

## 1.1 Varias tablas, una columna en común

En la UT5 la venta guarda `id_cliente`, que apunta a `cliente`. Para ver el **nombre** del cliente junto al importe no hace falta una sola tabla gigante: se **unen** las dos por esa columna.

!!! definicion "Definición"
    Un **JOIN** combina filas de dos (o más) tablas según una columna relacionada, casi siempre una clave ajena.
    El **INNER JOIN** (o `JOIN` a secas) devuelve **solo las filas que coinciden en las dos**.

```sql
SELECT v.id, v.importe, c.nombre, c.apellido
FROM venta v
INNER JOIN cliente c
  ON v.id_cliente = c.id;
```

`v` y `c` son **alias**: un apodo para no escribir el nombre entero. `ON` dice con qué columnas se emparejan.

!!! ejemplo "Ejemplo"
    Una venta sin cliente (`id_cliente` a NULL, un cobro en efectivo) **no sale** en el INNER JOIN: no hay fila de `cliente` con la que coincidir.
    Un cliente que aún no ha comprado **tampoco sale**.

Piensa en un diagrama de Venn: el INNER JOIN es la **intersección**.

!!! ojo "Ojo"
    Si olvidas el `ON` (o pones `FROM venta, cliente` sin WHERE), obtienes el **producto cartesiano**: cada venta con cada cliente. 10 ventas y 8 clientes: 80 filas, casi todas mentira. Lo viste en la UT3.

!!! comprueba "Comprueba"
    1. ¿Qué filas deja fuera un INNER JOIN?
    2. ¿Para qué sirve el alias `v`?
    3. ¿En qué columna se une `venta` con `cliente`?

# Bloque 2. LEFT, RIGHT y SELF JOIN

## 2.1 LEFT JOIN: quiero todas las de la izquierda

!!! definicion "Definición"
    Un **LEFT JOIN** devuelve **todas** las filas de la tabla de la izquierda y, si hay coincidencia, las de la derecha. Si no hay, las columnas de la derecha quedan a **NULL**.

```sql
SELECT v.id, v.importe, c.nombre
FROM venta v
LEFT JOIN cliente c
  ON v.id_cliente = c.id;
```

Aquí la izquierda es `venta`: salen también las ventas sin cliente. `c.nombre` será NULL en esas filas.

## 2.2 RIGHT JOIN: al revés

El **RIGHT JOIN** devuelve todas las de la **derecha**. Con las mismas tablas, un RIGHT JOIN desde `venta` hacia `cliente` saca todos los clientes, hayan comprado o no.

En la práctica se usa más el LEFT: pones a la izquierda la tabla de la que no quieres perder filas.

```sql
SELECT v.id, v.importe, c.nombre
FROM venta v
RIGHT JOIN cliente c
  ON v.id_cliente = c.id;
```

## 2.3 SELF JOIN: la tabla consigo misma

!!! definicion "Definición"
    Un **SELF JOIN** une una tabla **consigo misma**. Hace falta cuando una FK apunta a la propia tabla (el jefe es un empleado; quien recomienda es otro cliente).

Hace falta **dos alias**. Si no, MySQL no distingue el empleado del jefe.

```sql
SELECT e.nombre AS empleado,
       j.nombre AS jefe
FROM empleado e
LEFT JOIN empleado j
  ON e.id_jefe = j.id;
```

LEFT, no INNER: el director no tiene jefe y `j.nombre` queda NULL. Un INNER JOIN lo dejaría fuera.

!!! comprueba "Comprueba"
    1. En un LEFT JOIN venta-cliente, ¿sale una venta con `id_cliente` NULL?
    2. ¿Por qué el SELF JOIN lleva dos alias?
    3. ¿Qué JOIN usarías para listar clientes aunque no hayan comprado, dejando `venta` a la izquierda? (pista: no es un LEFT tal cual)

# Bloque 3. Funciones de agregación

## 3.1 Un número a partir de muchas filas

!!! definicion "Definición"
    Una **función de agregación** calcula un solo valor a partir de un conjunto de filas: `COUNT`, `SUM`, `AVG`, `MAX`, `MIN`.

```sql
SELECT COUNT(*) AS cuantas FROM venta;
SELECT SUM(importe) AS total FROM venta;
SELECT AVG(importe) AS media FROM venta;
SELECT MAX(importe), MIN(importe) FROM venta;
```

`COUNT(*)` cuenta filas. `COUNT(id_cliente)` no cuenta los NULL: las ventas sin cliente no entran.

## 3.2 GROUP BY

Sin `GROUP BY`, la agregación resume **toda** la tabla. Con `GROUP BY`, resume **cada grupo**.

```sql
SELECT id_cliente, SUM(importe) AS gastado
FROM venta
GROUP BY id_cliente;
```

Cada cliente, su total. La regla: en el SELECT, o está en el GROUP BY, o es una agregación. No pidas `nombre` sin agruparlo o unirlo antes.

!!! ojo "Ojo"
    `WHERE` filtra **antes** de agrupar. `HAVING` filtra **después**, sobre el resultado de la agregación:

    ```sql
    SELECT id_cliente, SUM(importe) AS gastado
    FROM venta
    GROUP BY id_cliente
    HAVING SUM(importe) >= 50;
    ```

!!! comprueba "Comprueba"
    1. ¿Qué diferencia hay entre `COUNT(*)` y `COUNT(id_cliente)`?
    2. ¿Cuántas filas sale `SELECT AVG(importe) FROM venta`?
    3. ¿WHERE o HAVING para «clientes que han gastado 50 o más»?

# Bloque 4. Filtrar, ordenar y unir resultados

## 4.1 AND, OR, NOT, BETWEEN, IN

```sql
SELECT * FROM empleado
WHERE fecha_alta < '2023-01-05' AND puesto = 'cocinero';

SELECT * FROM empleado
WHERE puesto IN ('cocinero', 'caja');

SELECT * FROM empleado
WHERE fecha_alta BETWEEN '2023-01-04' AND '2023-01-07';
```

`AND`: las dos. `OR`: al menos una. `NOT`: lo contrario. `IN`: cualquiera de la lista. `BETWEEN`: el rango, extremos incluidos.

## 4.2 LIKE

`%` es cualquier ristra. `_` es un solo carácter.

```sql
SELECT * FROM empleado WHERE nombre LIKE 'A%';
SELECT * FROM empleado WHERE puesto LIKE '_ocinero';
```

## 4.3 ORDER BY y LIMIT

```sql
SELECT * FROM empleado ORDER BY apellido ASC, nombre ASC;
SELECT * FROM empleado ORDER BY sueldo_hora DESC LIMIT 3;
```

`ASC` es el defecto. `LIMIT 3` son las tres primeras del orden. `LIMIT 10, 10` salta 10 y toma 10 (página 2).

## 4.4 UNION

!!! definicion "Definición"
    `UNION` junta el resultado de dos `SELECT` (mismo número de columnas). Quita duplicados. `UNION ALL` los deja.

```sql
SELECT nombre, apellido FROM empleado
UNION
SELECT nombre, apellido FROM cliente;
```

!!! comprueba "Comprueba"
    1. ¿Qué coincide `LIKE '_ocinero'` que no coincide `LIKE 'cocinero'`?
    2. ¿`UNION` y `UNION ALL` con una fila repetida en las dos tablas: cuántas filas?
    3. Escribe el SELECT de los tres empleados con sueldo más alto.

# Material de repaso

## Glosario

| Término | Qué es |
|---|---|
| JOIN | Combinar filas de dos tablas por una columna relacionada. |
| INNER JOIN | Solo coincidencias. |
| LEFT JOIN | Todas las de la izquierda; la derecha puede ser NULL. |
| RIGHT JOIN | Todas las de la derecha. |
| SELF JOIN | Una tabla consigo misma, con dos alias. |
| Agregación | COUNT, SUM, AVG, MAX, MIN: un valor a partir de muchas filas. |
| GROUP BY | Una agregación por cada grupo. |
| HAVING | Filtro después de agrupar. |
| LIKE | Patrón: `%` varios caracteres, `_` uno. |
| UNION | Junta dos SELECT; quita duplicados. |

## Mapa resumen

1. INNER es la intersección. LEFT no pierde las de la izquierda.
2. El SELF JOIN es el jefe o el recomendador: misma tabla, dos alias.
3. COUNT y SUM resumen; GROUP BY, por grupos; HAVING, después.

## Autoevaluación

Sin soluciones aquí.

1. Una venta sin cliente: ¿sale en INNER JOIN venta-cliente? ¿Y en LEFT JOIN con venta a la izquierda?
2. Escribe el JOIN que lista cada empleado y el nombre de su jefe, incluyendo al que no tiene.
3. ¿Por qué `FROM venta, cliente` sin ON suele estar mal?
4. `COUNT(*)` frente a `COUNT(id_cliente)` en `venta`.
5. Clientes con más de dos ventas: ¿WHERE o HAVING?
6. `LIKE '2023%' ` sobre una fecha. ¿Qué filas esperas?
7. Tres apellidos, página 2 de 10: escribe el LIMIT.
8. UNION de nombres de empleado y de cliente. ¿Qué pasa si Ana está en las dos tablas, con UNION y con UNION ALL?
