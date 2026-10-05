# 02 — Servidor mínimo e Inspector

## Propósito

Construir el servidor MCP más pequeño posible y probarlo con MCP Inspector. En esta etapa no se integra Django: así se separan protocolo, SDK y reglas de negocio.

## Requisitos

- Python y `uv` instalados.
- Un proyecto Python inicializado con `uv`.

## Actividad

1. El archivo `server.py` ya declara una tool `health` funcional y una tool
   `add` intencionalmente incompleta. Prepará el entorno:

   ```sh
   uv sync
   ```

2. Revisá el contrato de `add` y completá únicamente su cuerpo, sin cambiar su
   nombre, documentación ni tipos.
3. Iniciá el Inspector:

   ```sh
   uv run mcp dev server.py
   ```

4. En Inspector, verificá que ambas tools aparezcan en el catálogo y llamá a
   `add` con dos valores válidos y un caso inválido.

## Punto de control

- La tool se descubre sin escribir manualmente JSON Schema.
- Inspector muestra sus argumentos como enteros requeridos.
- `add(2, 3)` devuelve `5`.
- Un argumento inválido produce un error comprensible, no un traceback opaco.

## Entrega mínima

- `server.py` ejecutable con una tool pequeña, nombrada y documentada con claridad.
- Una captura o registro de una invocación exitosa en Inspector.
- Una frase que explique cómo las anotaciones de tipos forman parte del contrato visible para el host.

## Para pensar

- ¿Por qué Inspector es útil antes de probar con un agente?
- ¿Qué información debe tener una tool para que un modelo pueda usarla sin adivinar?


## Entrega 
Server.py ejecutable con tool completa

Inspector funcionando bien

Las anotaciones de tipos (a y b que son int) y el docstring se convierten automaticamente en el JSON Schema y la descripción que el host le muestra al modelo, así que forman parte del contrato visible: el modelo sabe qué argumentos enviar y de qué tipo sin tener que adivinar

### ¿Por qué Inspector es útil antes de probar con un agente?
el modelo es no determinista: si algo falla con un agente, no sabés si el problema es el servidor, el prompt o el modelo. Inspector prueba solo la capa determinista, donde la misma entrada da siempre la misma salida

### ¿Qué información debe tener una tool para que un modelo pueda usarla sin adivinar?
Un nombre preciso, un docstring que diga qué hace y qué efecto tiene, y argumentos tipados con su significado. El modelo no ve tu código, solo ese contrato