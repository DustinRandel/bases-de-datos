---
title: "SQL: procedimientos almacenados"
subtitulo: "UT7. Dosier de apuntes"
modulo: "0484. Bases de datos"
curso: "2026-2027"
profesor: "Dustin Randel de Lara García"
centro: "Sant Josep Obrer"
ut: "UT7"
---

# Cómo usar este dosier {.nobreak}

Este dosier recoge cómo dejar **lógica en el servidor** MySQL: un procedimiento que recibe parámetros, consulta o cambia datos y devuelve un resultado. Parte de las tablas y el SQL de la UT5 y la UT6.

Encontrarás cuatro tipos de caja:

!!! definicion "Definición"
    Un término que tienes que saber explicar con tus palabras.

!!! ejemplo "Ejemplo"
    Un caso concreto. Léelo despacio.

!!! ojo "Ojo"
    Un error típico.

!!! comprueba "Comprueba"
    Preguntas al final de cada bloque.

Al final tienes un **glosario**, un **mapa resumen** y una **autoevaluación**.

## Qué vas a aprender

Al terminar esta UT deberías ser capaz de:

- Explicar qué es un procedimiento almacenado y para qué se usa.
- Escribir uno con `DELIMITER`, `BEGIN`…`END`, `DECLARE` y `SELECT INTO`.
- Usar `IF` en una consulta (`IF(expr, sí, no)`) y dentro de un procedimiento (`IF…THEN…ELSE`).
- Llamarlo con `CALL` y leer el parámetro de salida. Usar `COALESCE` cuando la suma puede ser NULL.

## Índice

| Bloque | Tema |
|---|---|
| [1](#bloque-1-que-es-un-procedimiento) | [Qué es un procedimiento](#bloque-1-que-es-un-procedimiento) |
| [2](#bloque-2-if-en-consultas-y-en-procedimientos) | [IF en consultas y en procedimientos](#bloque-2-if-en-consultas-y-en-procedimientos) |
| [3](#bloque-3-declare-select-into-y-coalesce) | [DECLARE, SELECT INTO y COALESCE](#bloque-3-declare-select-into-y-coalesce) |
| Repaso | [Glosario, mapa resumen y autoevaluación](#material-de-repaso) |

# Bloque 1. Qué es un procedimiento

## 1.1 Un programa guardado en el servidor

!!! definicion "Definición"
    Un **procedimiento almacenado** es un programa que vive en el SGBD. Recibe parámetros, ejecuta SQL y, si toca, devuelve valores. Lo llamas con `CALL`.

Sirve para no repetir la misma lógica en cada aplicación: el stock se comprueba igual desde la web y desde el TPV.

Los parámetros pueden ser `IN` (entra), `OUT` (sale) o `INOUT`. En clase usamos `IN` y `OUT`.

## 1.2 DELIMITER y el bloque BEGIN…END

MySQL usa `;` para terminar una sentencia. Dentro del procedimiento hay varios `;`. Hay que cambiar el delimitador mientras lo creas.

```sql
DELIMITER $$
CREATE PROCEDURE hola(IN quien VARCHAR(50))
BEGIN
  SELECT CONCAT('Hola, ', quien) AS saludo;
END $$
DELIMITER ;

CALL hola('Ana');
```

`DELIMITER $$` dice: «hasta que veas `$$`, no cortes». Al terminar, vuelves a `;`.

!!! ojo "Ojo"
    Si olvidas restaurar `DELIMITER ;`, las siguientes sentencias «no terminan» y parece que MySQL se ha colgado.

!!! comprueba "Comprueba"
    1. ¿Dónde se guarda el procedimiento, en tu Java o en MySQL?
    2. ¿Para qué sirve cambiar el DELIMITER?
    3. ¿Cómo se ejecuta un procedimiento ya creado?

# Bloque 2. IF en consultas y en procedimientos

## 2.1 IF como expresión

En un `SELECT`, `IF(condición, valor_si, valor_no)` es una expresión. No lleva `THEN`.

```sql
SELECT nombre,
       IF(ultima_compra >= DATE_SUB(NOW(), INTERVAL 6 MONTH),
          'Activo', 'Inactivo') AS estado
FROM cliente;
```

`DATE_SUB(NOW(), INTERVAL 6 MONTH)` es hoy menos seis meses.

## 2.2 IF…THEN…ELSE dentro del procedimiento

Ahí sí hay bloque, con `THEN`, `ELSE` y `END IF`.

```sql
DELIMITER $$
CREATE PROCEDURE hay_stock(
    IN producto_id INT,
    IN cuantos INT,
    OUT mensaje VARCHAR(255)
)
BEGIN
  DECLARE stock_actual INT;
  SELECT stock INTO stock_actual
  FROM producto
  WHERE id = producto_id;

  IF stock_actual < cuantos THEN
    SET mensaje = 'Stock insuficiente';
  ELSE
    SET mensaje = 'Stock disponible';
  END IF;
END $$
DELIMITER ;

SET @msg = '';
CALL hay_stock(1, 5, @msg);
SELECT @msg;
```

`@msg` es una variable de sesión. El `OUT` escribe en ella.

!!! comprueba "Comprueba"
    1. ¿`IF(expr, a, b)` vale dentro de un SELECT?
    2. ¿Hace falta `END IF` en la expresión IF del SELECT?
    3. ¿Qué es `@msg`?

# Bloque 3. DECLARE, SELECT INTO y COALESCE

## 3.1 Variables locales

`DECLARE` crea una variable **dentro** del procedimiento. Va al principio del `BEGIN`, antes de cualquier sentencia.

```sql
DECLARE suma_total DECIMAL(10, 2);
SELECT SUM(total) INTO suma_total
FROM compra
WHERE id_cliente = cliente_id;
```

`SELECT … INTO` guarda el resultado en la variable. Si no hay filas, la variable queda NULL.

## 3.2 COALESCE: el primer no NULL

!!! definicion "Definición"
    `COALESCE(a, b, …)` devuelve el primer valor que no es NULL. Si SUM no encuentra filas, SUM es NULL; `COALESCE(suma, 0)` lo convierte en 0.

```sql
DELIMITER $$
CREATE PROCEDURE total_compras(
    IN cliente_id INT,
    OUT total DECIMAL(10, 2)
)
BEGIN
  DECLARE suma DECIMAL(10, 2);
  SELECT SUM(total) INTO suma
  FROM compra
  WHERE id_cliente = cliente_id;
  SET total = COALESCE(suma, 0);
END $$
DELIMITER ;
```

Sin `COALESCE`, un cliente sin compras dejaría `total` a NULL y el programa que llama podría romper una cuenta.

!!! ojo "Ojo"
    `DROP PROCEDURE nombre;` borra el procedimiento. Si hay FK y quieres tirar tablas de prueba, a veces hace falta `SET FOREIGN_KEY_CHECKS = 0` (solo en ejercicios, nunca en producción a la ligera).

!!! comprueba "Comprueba"
    1. ¿Dónde se escribe DECLARE, al principio o al final del BEGIN?
    2. ¿Qué pasa si SELECT INTO no encuentra filas?
    3. ¿Qué devuelve COALESCE(NULL, 0)?

# Material de repaso

## Glosario

| Término | Qué es |
|---|---|
| Procedimiento almacenado | Programa en el SGBD. Se llama con CALL. |
| DELIMITER | Cambia el fin de sentencia para poder usar `;` dentro. |
| IN / OUT | Parámetro que entra / que sale. |
| DECLARE | Variable local del procedimiento. |
| SELECT INTO | Copia el resultado de un SELECT en una variable. |
| COALESCE | Primer valor no NULL. |
| IF(expr, a, b) | Expresión en un SELECT. |
| IF…THEN…ELSE | Condición dentro del procedimiento. |

## Mapa resumen

1. El procedimiento vive en MySQL. DELIMITER para crearlo; CALL para usarlo.
2. IF en SELECT es una expresión; en el procedimiento es un bloque con END IF.
3. DECLARE al principio. SELECT INTO puede dejar NULL: COALESCE lo arregla.

## Autoevaluación

Sin soluciones aquí.

1. ¿Por qué no basta un `;` al crear un procedimiento con varias sentencias?
2. Escribe un IF de SELECT que ponga «caro» si precio >= 10 y «barato» si no.
3. En hay_stock, ¿qué pasa si producto_id no existe?
4. ¿COALESCE(NULL, NULL, 3)?
5. ¿Puedes DECLARE después de un SELECT dentro del mismo BEGIN?
