# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "anywidget==0.9.18",
#     "marimo",
#     "mohtml==0.1.10",
#     "polars==1.30.0",
# ]
# ///

import marimo

__generated_with = "0.13.11"
app = marimo.App(width="columns")


@app.cell(column=0, hide_code=True)
def _(mo):
    mo.md(r"""## Widget setup""")
    return


@app.cell
def _():
    import marimo as mo
    import polars as pl
    from mohtml import div, span, tailwind_css
    from mopad import GamepadWidget

    tailwind_css()
    return GamepadWidget, div, mo, pl, span


@app.cell
def _(GamepadWidget, mo):
    widget = mo.ui.anywidget(GamepadWidget())
    widget
    return (widget,)


@app.cell
def _(mo):
    get_i, set_i = mo.state(0)
    return get_i, set_i


@app.cell
def _(
    data_in,
    get_annot,
    get_ex_index,
    get_i,
    set_annot,
    set_ex_index,
    set_i,
    widget,
):
    def observer(change):
        if (get_i() + 150) < change["new"]:
            set_i(change["new"])
            if widget.current_button_press == 0:
                annotate("accept")
            elif widget.current_button_press == 1:
                annotate("reject")
            elif widget.current_button_press == 5:
                annotate("skip")
            elif widget.current_button_press == 4:
                annotate("prev")


    def annotate(outcome):
        if outcome == "prev":
            set_ex_index(get_ex_index() - 1)
            example = data_in[get_ex_index()]["text"]
            annot = get_annot()
            del annot[example]
            set_annot(annot)
            return
        example = data_in[get_ex_index()]["text"]
        annot = get_annot()
        annot[example] = outcome
        set_annot(annot)
        set_ex_index(get_ex_index() + 1)


    widget.observe(observer, ["current_timestamp"])
    return


@app.cell
def _(pl):
    data_in = pl.read_ndjson(
        "https://raw.githubusercontent.com/koaning/arxiv-frontpage/refs/heads/main/data/annot/new-dataset.jsonl"
    ).to_dicts()
    return (data_in,)


@app.cell
def _(mo):
    get_annot, set_annot = mo.state({})
    get_ex_index, set_ex_index = mo.state(0)
    return get_annot, get_ex_index, set_annot, set_ex_index


@app.cell(column=1, hide_code=True)
def _(mo):
    mo.md(r"""## The interface""")
    return


@app.cell(hide_code=True)
def _(data_in, div, get_ex_index, span):
    new_text = data_in[get_ex_index()]["text"]

    div(
        div("Does this text indicate a new dataset?", klass="font-bold text-md text-gray-300 mb-1"),
        div(new_text, klass="font-mono text-xl pb-4"),
        div(
            span("prev [L]", klass="border border-gray-500 bg-gray-800 rounded px-2 py-1"),
            span("CORRECT (B)", klass="border border-gray-500 bg-gray-800 rounded px-2 py-1"),
            span("FALSE (A)", klass="border border-gray-500 bg-gray-800 rounded px-2 py-1"),
            span("skip [R]", klass="border border-gray-500 bg-gray-800 rounded px-2 py-1"),
            klass="flex flex-row items-center justify-between",
        ),
    )
    return


@app.cell
def _(get_annot, pl):
    pl.DataFrame([{"text": k, "label": v} for k, v in get_annot().items()]).reverse()
    return


@app.cell(column=2, hide_code=True)
def _(mo):
    mo.md(r"""## The data""")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
