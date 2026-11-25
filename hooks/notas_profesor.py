"""Quita los comentarios HTML (<!-- ... -->) de las páginas antes de construir la web.

Las notas para el profesor van en comentarios HTML dentro de los .md. Sin este hook,
MkDocs los copia tal cual al HTML publicado y cualquiera los ve con "Ver código fuente".
Los comentarios dentro de bloques de código no se tocan.
"""
import re

_BLOQUE_CODIGO = re.compile(r"(^```.*?^```)", re.S | re.M)
_COMENTARIO = re.compile(r"<!--.*?-->\n?", re.S)


def on_page_markdown(markdown, **kwargs):
    partes = _BLOQUE_CODIGO.split(markdown)
    # Las posiciones impares son bloques de código: se dejan intactas
    return "".join(p if i % 2 else _COMENTARIO.sub("", p) for i, p in enumerate(partes))


_ENCABEZADO = re.compile(r"^(#{1,5}) ", re.M)


def _bajar(texto):
    return _ENCABEZADO.sub(lambda m: "#" + m.group(1) + " ", texto)


def on_page_markdown(markdown, page=None, **kwargs):  # noqa: F811
    """Quita comentarios y baja un nivel los encabezados para tener un único H1.

    El .md (y el PDF) usan # para cada bloque. En la web, con varios H1 el menú
    lateral oculta la página y la tabla de contenidos pierde los subapartados.
    Aquí se pone un solo H1 con el título de la unidad y todo lo demás cuelga de él.
    """
    partes = _BLOQUE_CODIGO.split(markdown)
    sin = [p if i % 2 else _COMENTARIO.sub("", p) for i, p in enumerate(partes)]
    sin = [p if i % 2 else _bajar(p) for i, p in enumerate(sin)]
    titulo = ""
    if page is not None and page.meta.get("ut"):
        titulo = "# %s. %s\n\n" % (page.meta["ut"], page.meta.get("title", ""))
    return titulo + "".join(sin)
