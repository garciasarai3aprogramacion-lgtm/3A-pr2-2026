import math
import os
from dataclasses import dataclass

from nicegui import ui


@dataclass
class CalculatorState:
    display: str = "0"
    stored_value: float | None = None
    pending_operator: str | None = None
    waiting_for_operand: bool = True
    expression: str = ""
    just_calculated: bool = False


state = CalculatorState()
history: list[tuple[str, str]] = []
display_label = None
expression_label = None
history_column = None


def format_number(value: float) -> str:
    if not math.isfinite(value):
        return "Error"
    if value == 0:
        return "0"
    if value.is_integer():
        return str(int(value))
    return f"{value:.10f}".rstrip("0").rstrip(".")


def current_number() -> float:
    return float(state.display)


def update_display() -> None:
    display_label.text = state.display
    expression_label.text = state.expression


def refresh_history() -> None:
    history_column.clear()
    if not history:
        with history_column:
            ui.label("Your completed calculations will appear here.").classes(
                "history-empty"
            )
        return

    with history_column:
        for expression, result in reversed(history[-5:]):
            with ui.row().classes("history-row w-full items-center justify-between"):
                ui.label(expression).classes("history-expression")
                ui.label(result).classes("history-result")


def reset() -> None:
    state.display = "0"
    state.stored_value = None
    state.pending_operator = None
    state.waiting_for_operand = True
    state.expression = ""
    state.just_calculated = False
    update_display()


def show_error(message: str) -> None:
    state.display = "Error"
    state.expression = message
    state.stored_value = None
    state.pending_operator = None
    state.waiting_for_operand = True
    state.just_calculated = True
    update_display()
    ui.notify(message, type="negative")


def input_digit(digit: str) -> None:
    was_just_calculated = state.just_calculated
    if state.display == "Error" or state.waiting_for_operand or was_just_calculated:
        state.display = digit
        state.waiting_for_operand = False
        state.just_calculated = False
        if was_just_calculated:
            state.expression = ""
    elif state.display == "0":
        state.display = digit
    elif len(state.display) < 16:
        state.display += digit
    update_display()


def input_decimal() -> None:
    if state.display == "Error" or state.waiting_for_operand or state.just_calculated:
        state.display = "0."
        state.waiting_for_operand = False
        state.just_calculated = False
        state.expression = ""
    elif "." not in state.display and len(state.display) < 16:
        state.display += "."
    update_display()


def backspace() -> None:
    if state.display == "Error" or state.waiting_for_operand or state.just_calculated:
        return
    state.display = state.display[:-1] or "0"
    update_display()


def toggle_sign() -> None:
    if state.display == "Error":
        return
    if state.display != "0":
        state.display = state.display[1:] if state.display.startswith("-") else "-" + state.display
    update_display()


def percentage() -> None:
    if state.display == "Error":
        return
    state.display = format_number(current_number() / 100)
    state.waiting_for_operand = True
    update_display()


def calculate(left: float, right: float, operator: str) -> float:
    if operator == "+":
        return left + right
    if operator == "−":
        return left - right
    if operator == "×":
        return left * right
    if operator == "÷":
        if right == 0:
            raise ZeroDivisionError
        return left / right
    raise ValueError(f"Unsupported operator: {operator}")


def choose_operator(operator: str) -> None:
    if state.display == "Error":
        reset()

    try:
        if state.stored_value is None:
            state.stored_value = current_number()
        elif state.pending_operator and not state.waiting_for_operand:
            state.stored_value = calculate(
                state.stored_value, current_number(), state.pending_operator
            )
            state.display = format_number(state.stored_value)

        state.pending_operator = operator
        state.waiting_for_operand = True
        state.just_calculated = False
        state.expression = f"{format_number(state.stored_value)} {operator}"
        update_display()
    except ZeroDivisionError:
        show_error("Cannot divide by zero")


def equals() -> None:
    if state.stored_value is None or state.pending_operator is None:
        return

    try:
        left = state.stored_value
        right = current_number()
        operator = state.pending_operator
        result = calculate(left, right, operator)
        expression = f"{format_number(left)} {operator} {format_number(right)}"
        result_text = format_number(result)
        history.append((expression, result_text))
        state.display = result_text
        state.stored_value = None
        state.pending_operator = None
        state.waiting_for_operand = True
        state.just_calculated = True
        state.expression = ""
        update_display()
        refresh_history()
    except ZeroDivisionError:
        show_error("Cannot divide by zero")


def handle_key(event) -> None:
    key = event.key
    if key.isdigit():
        input_digit(key)
    elif key == ".":
        input_decimal()
    elif key in {"+", "-"}:
        choose_operator("+" if key == "+" else "−")
    elif key in {"*", "x", "X"}:
        choose_operator("×")
    elif key == "/":
        choose_operator("÷")
    elif key == "%":
        percentage()
    elif key in {"Enter", "="}:
        equals()
    elif key in {"Escape", "Delete"}:
        reset()
    elif key == "Backspace":
        backspace()


ui.add_css(
    """
    :root {
        --ink: #18232f;
        --muted: #70808e;
        --paper: #f5f7f4;
        --card: #ffffff;
        --teal: #0e8077;
        --teal-dark: #075c58;
        --coral: #e66d4e;
        --line: #e2e9e7;
    }
    body {
        background: var(--paper);
        color: var(--ink);
        font-family: Inter, ui-sans-serif, system-ui, sans-serif;
    }
    .app-shell {
        max-width: 1120px;
        margin: 0 auto;
        padding: 42px 24px 56px;
    }
    .eyebrow {
        color: var(--teal);
        font-size: 12px;
        font-weight: 800;
        letter-spacing: .16em;
        text-transform: uppercase;
    }
    .page-title {
        font-size: clamp(34px, 5vw, 58px);
        font-weight: 850;
        letter-spacing: -.06em;
        line-height: .98;
        margin: 10px 0 12px;
    }
    .page-subtitle {
        color: var(--muted);
        font-size: 16px;
        line-height: 1.6;
        max-width: 520px;
    }
    .calculator-card, .history-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 28px;
        box-shadow: 0 20px 60px rgba(34, 64, 62, .08);
    }
    .calculator-card {
        padding: 22px;
    }
    .display {
        background: #15272e;
        border-radius: 20px;
        min-height: 150px;
        padding: 22px 24px;
    }
    .display-expression {
        color: #91aaa9;
        font-size: 14px;
        min-height: 22px;
        text-align: right;
    }
    .display-value {
        color: #f5fbf8;
        font-size: clamp(36px, 6vw, 64px);
        font-weight: 720;
        letter-spacing: -.06em;
        overflow-wrap: anywhere;
        text-align: right;
    }
    .calc-button {
        border-radius: 16px;
        font-size: 21px;
        font-weight: 700;
        height: 62px;
        transition: transform .15s ease, filter .15s ease;
    }
    .calc-button:hover {
        filter: brightness(1.04);
        transform: translateY(-2px);
    }
    .calc-button:active {
        transform: translateY(1px) scale(.98);
    }
    .number-button {
        background: #f0f4f1;
        color: var(--ink);
    }
    .utility-button {
        background: #e3edeb;
        color: var(--teal-dark);
    }
    .operator-button {
        background: var(--teal);
        color: white;
    }
    .equals-button {
        background: var(--coral);
        color: white;
    }
    .history-card {
        padding: 24px;
    }
    .history-title {
        color: var(--ink);
        font-size: 16px;
        font-weight: 800;
    }
    .history-caption, .history-empty {
        color: var(--muted);
        font-size: 13px;
        line-height: 1.5;
    }
    .history-row {
        border-bottom: 1px solid var(--line);
        padding: 14px 0;
    }
    .history-expression {
        color: var(--muted);
        font-size: 14px;
    }
    .history-result {
        color: var(--teal-dark);
        font-size: 16px;
        font-weight: 800;
    }
    @media (max-width: 700px) {
        .app-shell { padding: 28px 14px 40px; }
        .calculator-card { padding: 14px; }
        .calc-button { height: 56px; }
    }
    """
)


with ui.column().classes("app-shell w-full"):
    ui.label("PROGRAMMING ASSIGNMENT").classes("eyebrow")
    ui.label("A calculator that stays out of your way.").classes("page-title")
    ui.label(
        "A small, dependable NiceGUI project for practicing state, events, and arithmetic logic."
    ).classes("page-subtitle mb-8")

    with ui.row().classes("w-full items-start gap-6"):
        with ui.card().classes("calculator-card flex-1"):
            with ui.column().classes("w-full gap-4"):
                with ui.column().classes("display w-full justify-end items-end"):
                    expression_label = ui.label("").classes("display-expression w-full")
                    display_label = ui.label("0").classes("display-value w-full")

                buttons = [
                    ("AC", "utility-button", reset),
                    ("⌫", "utility-button", backspace),
                    ("±", "utility-button", toggle_sign),
                    ("÷", "operator-button", lambda: choose_operator("÷")),
                    ("7", "number-button", lambda: input_digit("7")),
                    ("8", "number-button", lambda: input_digit("8")),
                    ("9", "number-button", lambda: input_digit("9")),
                    ("×", "operator-button", lambda: choose_operator("×")),
                    ("4", "number-button", lambda: input_digit("4")),
                    ("5", "number-button", lambda: input_digit("5")),
                    ("6", "number-button", lambda: input_digit("6")),
                    ("−", "operator-button", lambda: choose_operator("−")),
                    ("1", "number-button", lambda: input_digit("1")),
                    ("2", "number-button", lambda: input_digit("2")),
                    ("3", "number-button", lambda: input_digit("3")),
                    ("+", "operator-button", lambda: choose_operator("+")),
                    ("%", "utility-button", percentage),
                    ("0", "number-button", lambda: input_digit("0")),
                    (".", "number-button", input_decimal),
                    ("=", "equals-button", equals),
                ]
                with ui.grid(columns=4).classes("w-full gap-3"):
                    for label, color_class, action in buttons:
                        ui.button(label, on_click=action).classes(
                            f"calc-button {color_class}"
                        )

        with ui.card().classes("history-card w-full md:w-80"):
            ui.label("Calculation history").classes("history-title")
            ui.label("The five most recent results stay visible while you work.").classes(
                "history-caption mt-1 mb-3"
            )
            history_column = ui.column().classes("w-full")
            refresh_history()

ui.keyboard(on_key=handle_key)

ui.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", "8080")),
    title="NiceGUI Calculator",
    reload=False,
    show=False,
)