import reflex as rx

config = rx.Config(
    app_name="mundijuegos",
    db_url="sqlite:///mundijuegos.db",
    show_built_with_reflex=False,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                appearance="light",
                accent_color="pink",
                gray_color="mauve",
                radius="large",
                scaling="100%",
            )
        ),
    ],
)
