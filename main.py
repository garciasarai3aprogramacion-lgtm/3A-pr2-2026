import os

from nicegui import ui


def sumar() -> None:
    try:
        numero_1 = float(numero1.value)
        numero_2 = float(numero2.value)
        resultado.text = f"Resultado: {numero_1 + numero_2:g}"
    except (TypeError, ValueError):
        resultado.text = "Ingresa números válidos"


def limpiar() -> None:
    numero1.value = ""
    numero2.value = ""
    resultado.text = "Resultado: 0"


with ui.column().classes("w-full h-screen items-center justify-center"):
    with ui.card().style(
        "width:400px; background-color:purple;"
    ).classes("items-center"):
        ui.label("Calculadora de Suma").style(
            "color:white; font-size:24px; font-weight:bold"
        )

        numero1 = ui.input("Número 1").props("dark outlined").style("width:300px")
        numero2 = ui.input("Número 2").props("dark outlined").style("width:300px")

        with ui.row().classes("w-full justify-center no-wrap").style("gap:16px"):
            ui.button(
                "SUMAR",
                icon="calculate",
                color="green",
                on_click=sumar,
            ).style("color:white; width:140px")

            ui.button(
                "LIMPIAR",
                icon="delete",
                color="red",
                on_click=limpiar,
            ).style("color:white; width:140px")

        resultado = ui.label("Resultado: 0").style(
            "color:white; font-size:20px"
        )


ui.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", "8080")),
    title="Calculadora de Suma",
    reload=False,
    show=False,
)