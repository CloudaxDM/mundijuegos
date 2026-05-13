# Mundijuegos

Web de juegos infantiles hecha con [Reflex](https://reflex.dev/) para Zoa.

## Juegos incluidos

- 🌸 **La Floripondia**: juego tipo ahorcado con una flor.
- 🎨 **Colores**: identifica colores por nombre o tocando el círculo correcto.
- 🐾 **Memoria**: encuentra parejas de animalitos.
- 🧩 **Puzzle**: puzzle deslizante con animalitos.

## Requisitos

- Python 3.10 o superior.
- Entorno virtual local `.venv`.
- Reflex `0.9.2.post1` con extra de base de datos (`reflex[db]`).

> En este entorno no hay `uv` disponible en PATH, por eso los comandos usan directamente el Python de `.venv`.

## Instalar dependencias

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Validar la app

```powershell
.venv\Scripts\python.exe -m reflex compile --dry
```

## Base de datos

Las puntuaciones se guardan en SQLite mediante Reflex/SQLModel.

Primera inicialización o cambios de esquema:

```powershell
.venv\Scripts\python.exe -m reflex db init
.venv\Scripts\python.exe -m reflex db makemigrations --message "game scores"
.venv\Scripts\python.exe -m reflex db migrate
```

El archivo local `mundijuegos.db` está ignorado por Git. Las migraciones viven en `alembic/` y sí deben versionarse.

## Ejecutar la app

```powershell
.venv\Scripts\python.exe -m reflex run --env prod --single-port
```

## Estructura principal

```text
mundijuegos/
├── components/   # Layout, tarjetas y estadísticas reutilizables
├── pages/        # Pantallas de home y juegos
├── state/        # Estado y lógica de cada juego
├── config.py     # Nombre, colores y configuración visual
├── scores.py     # Persistencia SQLite de puntuaciones
└── mundijuegos.py # Entrada Reflex y rutas
```

## Buenas prácticas aplicadas

- Componentes interactivos como botones HTML reales, no `div` clicables.
- Foco visible para navegación con teclado.
- Scroll vertical permitido en móvil/tablet.
- Tamaños responsive con `clamp()` en cartas y piezas.
- Respeto de `prefers-reduced-motion` para reducir animaciones si el sistema lo pide.
- Estado derivado con `@rx.var(cache=True)` cuando conviene evitar lógica en la UI.

## Notas de persistencia

Si existe un `scores.json` antiguo, `scores.py` lo usa como fuente de importación inicial cuando crea filas nuevas en la base de datos. Después, la fuente de verdad es SQLite (`mundijuegos.db`).
