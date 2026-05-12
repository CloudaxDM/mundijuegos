---
name: reflex-docs
description: >
  Reflex framework for full-stack Python web apps. Use when writing code that imports reflex,
  working with rx.State, rx.Component, event handlers, vars, uploads, database models,
  authentication, styling, or deploying Reflex apps. Includes critical 0.9.x gotchas and
  full official doc index with markdown URLs for on-demand fetching.
---

# Reflex Development Skill

## Cuándo usar esta skill (y cuándo NO)

✅ Generar código que use la API de Reflex (componentes, state, events, uploads...)
✅ Implementar algo que dependa de versión ≥0.9.x
✅ Resolver errores relacionados con Reflex
❌ Preguntas conceptuales / arquitectónicas que no requieren API exacta
❌ Debugging de lógica Python pura sin Reflex
❌ Preguntas de "¿es posible X?" — responde desde los gotchas de abajo primero

> **Regla de fetch:** Solo hacer fetch de URLs del índice si los gotchas de abajo no cubren el caso.
> Para docs completas en un archivo: https://reflex.dev/docs/llms-full.txt

---

## ⚠️ Gotchas críticos Reflex 0.9.x — leer SIEMPRE antes de generar código

### 1. Setters auto-generados ELIMINADOS en ≥0.9.x
`set_<var>` ya NO existe automáticamente. Definir siempre manualmente:
```python
# ❌ NO funciona en 0.9.x
on_change=MyState.set_name

# ✅ Correcto
class MyState(rx.State):
    name: str = ""
    def set_name(self, value: str):
        self.name = value
```

### 2. Autenticación sin flash de contenido no autenticado
```python
@rx.page(on_load=AuthState.check_auth)
def protected_page():
    return rx.cond(AuthState.is_authenticated, page_content(), rx.spinner())

class AuthState(rx.State):
    is_authenticated: bool = False
    def check_auth(self):
        if not self.is_authenticated:
            return rx.redirect("/login")
```

### 3. Background tasks para operaciones largas (ffmpeg, IO pesado...)
```python
@rx.background
async def long_task(self):
    async with self:
        self.is_loading = True
    # trabajo pesado aquí — NO bloquea frontend
    async with self:
        self.is_loading = False
        self.result = "done"
```

### 4. rx.SharedState para broadcast a TODAS las sesiones conectadas
```python
class QueueState(rx.SharedState):  # No rx.State
    queue: list[str] = []
    def add_to_queue(self, item: str):
        self.queue.append(item)
```

### 5. Chunked upload + progress para archivos grandes
```python
async def handle_upload(self, files: list[rx.UploadFile]):
    for file in files:
        data = await file.read()
        yield MyState.set_progress(50)
    yield MyState.set_progress(100)
```

### 6. Rutas y URLs de archivos subidos
```python
upload_dir = rx.get_upload_dir()          # REFLEX_UPLOADED_FILES_DIR o ./uploaded_files
url = rx.get_upload_url("path/file.mp4")  # Sirve desde backend /_upload/<path>
```

### 7. State vars en componentes — siempre reactivo
```python
# ❌ No reactivo (valor fijo en render)
def my_component(value: str):
    return rx.text(value)

# ✅ Reactivo
def my_component():
    return rx.text(MyState.value)
```

### 8. foreach — requiere función nombrada, no lambda compleja
```python
def item_card(item: str) -> rx.Component:
    return rx.text(item)

rx.foreach(MyState.items, item_card)  # ✅
```

### 9. Computed vars — usar cache=True para evitar recálculos
```python
@rx.var(cache=True)
def item_count(self) -> int:
    return len(self.items)
```

### 10. rxconfig.py — api_url accesible desde el navegador del cliente
```python
config = rx.Config(
    app_name="myapp",
    api_url="https://tu-dominio.com:8000",  # ❌ No localhost si hay usuarios externos
)
```

---

## Índice oficial de documentación (llms.txt)

> Fuente: https://reflex.dev/docs/llms.txt
> Docs completas en un archivo: https://reflex.dev/docs/llms-full.txt
> Todas las URLs tienen versión markdown: añade `.md` al final.

### Advanced Onboarding
- [Project Structure (Advanced)](https://reflex.dev/docs/advanced-onboarding/code-structure.md)
- [Configuration](https://reflex.dev/docs/advanced-onboarding/configuration.md)
- [How Reflex Works](https://reflex.dev/docs/advanced-onboarding/how-reflex-works.md)

### MCP oficial de Reflex
- [MCP Overview](https://reflex.dev/docs/ai/integrations/mcp-overview.md)
- [MCP Installation](https://reflex.dev/docs/ai/integrations/mcp-installation.md)
- [Skills](https://reflex.dev/docs/ai/integrations/skills.md)

### API Reference
- [Browser Javascript](https://reflex.dev/docs/api-reference/browser-javascript.md)
- [Browser Storage](https://reflex.dev/docs/api-reference/browser-storage.md)
- [CLI](https://reflex.dev/docs/api-reference/cli.md)
- [Event Triggers](https://reflex.dev/docs/api-reference/event-triggers.md)
- [Special Events](https://reflex.dev/docs/api-reference/special-events.md)
- [Utility Functions](https://reflex.dev/docs/api-reference/utils.md)
- [Var System](https://reflex.dev/docs/api-reference/var-system.md)
- [App](https://reflex.dev/docs/api-reference/app.md)
- [State](https://reflex.dev/docs/api-reference/state.md)
- [Config](https://reflex.dev/docs/api-reference/config.md)
- [Event](https://reflex.dev/docs/api-reference/event.md)
- [Var](https://reflex.dev/docs/api-reference/var.md)
- [Environment Variables](https://reflex.dev/docs/api-reference/environment-variables.md)

### API Routes
- [API Routes Overview](https://reflex.dev/docs/api-routes/overview.md)

### Assets
- [Assets](https://reflex.dev/docs/assets/overview.md)
- [Upload & Download Files](https://reflex.dev/docs/assets/upload-and-download-files.md)

### Authentication
- [Authentication Overview](https://reflex.dev/docs/authentication/authentication-overview.md)

### Client Storage
- [Client Storage Overview](https://reflex.dev/docs/client-storage/overview.md)

### Components
- [Conditional Rendering](https://reflex.dev/docs/components/conditional-rendering.md)
- [Props](https://reflex.dev/docs/components/props.md)
- [Rendering Iterables](https://reflex.dev/docs/components/rendering-iterables.md)

### Database
- [Database Overview](https://reflex.dev/docs/database/overview.md)
- [Queries](https://reflex.dev/docs/database/queries.md)
- [Relationships](https://reflex.dev/docs/database/relationships.md)
- [Tables](https://reflex.dev/docs/database/tables.md)

### Events
- [Background Tasks](https://reflex.dev/docs/events/background-events.md)
- [Chaining Events](https://reflex.dev/docs/events/chaining-events.md)
- [Decentralized Event Handlers](https://reflex.dev/docs/events/decentralized-event-handlers.md)
- [Event Actions](https://reflex.dev/docs/events/event-actions.md)
- [Event Arguments](https://reflex.dev/docs/events/event-arguments.md)
- [Events Overview](https://reflex.dev/docs/events/events-overview.md)
- [Page Load Events](https://reflex.dev/docs/events/page-load-events.md)
- [Setters](https://reflex.dev/docs/events/setters.md)
- [Special Events](https://reflex.dev/docs/events/special-events.md)
- [Yielding Updates](https://reflex.dev/docs/events/yield-events.md)

### Getting Started
- [Basics](https://reflex.dev/docs/getting-started/basics.md)
- [Installation](https://reflex.dev/docs/getting-started/installation.md)
- [Introduction](https://reflex.dev/docs/getting-started/introduction.md)
- [Project Structure](https://reflex.dev/docs/getting-started/project-structure.md)

### Hosting / Deploy
- [Self Hosting](https://reflex.dev/docs/hosting/self-hosting.md)
- [Deploy Quick Start](https://reflex.dev/docs/hosting/deploy-quick-start.md)
- [Deploy with Github Actions](https://reflex.dev/docs/hosting/deploy-with-github-actions.md)
- [Secrets / Env Vars](https://reflex.dev/docs/hosting/secrets-environment-vars.md)
- [Config File](https://reflex.dev/docs/hosting/config-file.md)
- [Custom Domains](https://reflex.dev/docs/hosting/custom-domains.md)

### Component Library
- [File Upload](https://reflex.dev/docs/library/forms/upload.md)
- [Input](https://reflex.dev/docs/library/forms/input.md)
- [Form](https://reflex.dev/docs/library/forms/form.md)
- [Button](https://reflex.dev/docs/library/forms/button.md)
- [Select](https://reflex.dev/docs/library/forms/select.md)
- [Checkbox](https://reflex.dev/docs/library/forms/checkbox.md)
- [Switch](https://reflex.dev/docs/library/forms/switch.md)
- [Text Area](https://reflex.dev/docs/library/forms/text-area.md)
- [Cond](https://reflex.dev/docs/library/dynamic-rendering/cond.md)
- [Foreach](https://reflex.dev/docs/library/dynamic-rendering/foreach.md)
- [Match](https://reflex.dev/docs/library/dynamic-rendering/match.md)
- [Auto Scroll](https://reflex.dev/docs/library/dynamic-rendering/auto-scroll.md)
- [Dialog](https://reflex.dev/docs/library/overlay/dialog.md)
- [Drawer](https://reflex.dev/docs/library/overlay/drawer.md)
- [Toast](https://reflex.dev/docs/library/overlay/toast.md)
- [Popover](https://reflex.dev/docs/library/overlay/popover.md)
- [Tooltip](https://reflex.dev/docs/library/overlay/tooltip.md)
- [Table](https://reflex.dev/docs/library/tables-and-data-grids/table.md)
- [Data Table](https://reflex.dev/docs/library/tables-and-data-grids/data-table.md)
- [Spinner](https://reflex.dev/docs/library/data-display/spinner.md)
- [Progress](https://reflex.dev/docs/library/data-display/progress.md)
- [Badge](https://reflex.dev/docs/library/data-display/badge.md)
- [Code Block](https://reflex.dev/docs/library/data-display/code-block.md)
- [Icon](https://reflex.dev/docs/library/data-display/icon.md)
- [Image](https://reflex.dev/docs/library/media/image.md)
- [Video](https://reflex.dev/docs/library/media/video.md)
- [Audio](https://reflex.dev/docs/library/media/audio.md)
- [Markdown](https://reflex.dev/docs/library/typography/markdown.md)
- [Heading](https://reflex.dev/docs/library/typography/heading.md)
- [Text](https://reflex.dev/docs/library/typography/text.md)
- [Link](https://reflex.dev/docs/library/typography/link.md)
- [Stack](https://reflex.dev/docs/library/layout/stack.md)
- [Flex](https://reflex.dev/docs/library/layout/flex.md)
- [Box](https://reflex.dev/docs/library/layout/box.md)
- [Grid](https://reflex.dev/docs/library/layout/grid.md)
- [Container](https://reflex.dev/docs/library/layout/container.md)
- [Card](https://reflex.dev/docs/library/layout/card.md)
- [Separator](https://reflex.dev/docs/library/layout/separator.md)
- [Scroll Area](https://reflex.dev/docs/library/data-display/scroll-area.md)
- [Accordion](https://reflex.dev/docs/library/disclosure/accordion.md)
- [Tabs](https://reflex.dev/docs/library/disclosure/tabs.md)
- [Theme](https://reflex.dev/docs/library/other/theme.md)
- [Skeleton](https://reflex.dev/docs/library/other/skeleton.md)
- [HTML Embed](https://reflex.dev/docs/library/other/html-embed.md)
- [Script](https://reflex.dev/docs/library/other/script.md)

### Pages
- [Pages Overview](https://reflex.dev/docs/pages/overview.md)
- [Dynamic Routes](https://reflex.dev/docs/pages/dynamic-routing.md)

### Recipes
- [Login Form](https://reflex.dev/docs/recipes/auth/login-form.md)
- [Sign up Form](https://reflex.dev/docs/recipes/auth/signup-form.md)
- [Navbar](https://reflex.dev/docs/recipes/layout/navbar.md)
- [Sidebar](https://reflex.dev/docs/recipes/layout/sidebar.md)
- [Footer](https://reflex.dev/docs/recipes/layout/footer.md)
- [Dark Mode Toggle](https://reflex.dev/docs/recipes/others/dark-mode-toggle.md)
- [Stats](https://reflex.dev/docs/recipes/content/stats.md)
- [Forms](https://reflex.dev/docs/recipes/content/forms.md)

### State
- [State Overview](https://reflex.dev/docs/state/overview.md)
- [Component State](https://reflex.dev/docs/state-structure/component-state.md)
- [State Mixins](https://reflex.dev/docs/state-structure/mixins.md)
- [State Structure Overview](https://reflex.dev/docs/state-structure/overview.md)
- [Shared State](https://reflex.dev/docs/state-structure/shared-state.md)

### Styling
- [Styling Overview](https://reflex.dev/docs/styling/overview.md)
- [Common Props](https://reflex.dev/docs/styling/common-props.md)
- [Theming](https://reflex.dev/docs/styling/theming.md)
- [Responsive](https://reflex.dev/docs/styling/responsive.md)
- [Tailwind](https://reflex.dev/docs/styling/tailwind.md)
- [Custom Stylesheets](https://reflex.dev/docs/styling/custom-stylesheets.md)

### Utility Methods
- [State Utility Methods (router)](https://reflex.dev/docs/utility-methods/router-attributes.md)
- [Lifespan Tasks](https://reflex.dev/docs/utility-methods/lifespan-tasks.md)
- [Exception Handlers](https://reflex.dev/docs/utility-methods/exception-handlers.md)
- [Other Methods](https://reflex.dev/docs/utility-methods/other-methods.md)

### Vars
- [Base Vars](https://reflex.dev/docs/vars/base-vars.md)
- [Computed Vars](https://reflex.dev/docs/vars/computed-vars.md)
- [Custom Vars](https://reflex.dev/docs/vars/custom-vars.md)
- [Var Operations](https://reflex.dev/docs/vars/var-operations.md)

### Wrapping React
- [Wrapping React Overview](https://reflex.dev/docs/wrapping-react/overview.md)
- [Step By Step](https://reflex.dev/docs/wrapping-react/step-by-step.md)
- [Custom Code & Hooks](https://reflex.dev/docs/wrapping-react/custom-code-and-hooks.md)
- [Props](https://reflex.dev/docs/wrapping-react/props.md)
- [Styles and Imports](https://reflex.dev/docs/wrapping-react/imports-and-styles.md)
- [Serializers](https://reflex.dev/docs/wrapping-react/serializers.md)

---

## Estructura de proyecto recomendada

```
myapp/
├── myapp/
│   ├── myapp.py          # Entrada principal, rx.app()
│   ├── pages/
│   ├── state/
│   │   └── shared.py     # rx.SharedState si hay broadcast
│   ├── models/           # SQLModel tables
│   └── components/
├── assets/
├── rxconfig.py
└── requirements.txt
```
