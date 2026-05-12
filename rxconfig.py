import reflex as rx

config = rx.Config(
    app_name="mundijuegos",
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
