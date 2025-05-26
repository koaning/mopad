import marimo

__generated_with = "0.13.11"
app = marimo.App(width="columns")


@app.cell(column=0)
def _(mo):
    from mopad import MopadWidget

    widget = mo.ui.anywidget(MopadWidget())
    widget
    return (widget,)


@app.cell
def _(widget):
    widget.value
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(column=1)
def _():
    return


if __name__ == "__main__":
    app.run()
