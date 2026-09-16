from pyscript import document
from pyodide.ffi import create_proxy

from lib.types import empty_instruction
from lib.labels import is_valid_label
from lib.encoder import encode_program
from lib.decoder import decode_q

instructions = [empty_instruction()]
touched = False
encode_result = None
decode_result = None
decode_error = ""

_proxies = []


def listen(element, event, handler):
    proxy = create_proxy(handler)
    _proxies.append(proxy)
    element.addEventListener(event, proxy)


def variable_from_form(kind, index_raw):
    if kind == "Y":
        return {"kind": "Y"}
    try:
        i = int(str(index_raw).strip())
    except (ValueError, TypeError):
        i = 0
    if not i:
        i = 1
    return {"kind": kind, "index": i}


def format_instruction(inst):
    variable = inst["variable"]
    v = variable["kind"] + (str(variable["index"]) if "index" in variable else "")
    label = f"[{inst['label']}] " if inst.get("label") else ""
    statement_type = inst["statementType"]
    if statement_type == "dummy":
        return f"{label}{v} <- {v}"
    if statement_type == "increment":
        return f"{label}{v} <- {v} + 1"
    if statement_type == "decrement":
        return f"{label}{v} <- {v} - 1"
    return f"{label}IF {v} != 0 GOTO {inst.get('targetLabel') or '?'}"


def label_error(label):
    if not label:
        return ""
    return "" if is_valid_label(label) else "invalid label, use A1..E1, A2..E2, etc.."


def show_label_error(label):
    return label_error(label) if touched else ""


def update_field(idx, field, value):
    global touched
    touched = False
    set_encode_result(None)
    inst = instructions[idx]
    if field == "label":
        inst["label"] = value or None
    elif field == "targetLabel":
        inst["targetLabel"] = value or None
    elif field == "statementType":
        inst["statementType"] = value
    elif field == "varKind":
        current_index = inst["variable"].get("index", 1)
        inst["variable"] = variable_from_form(value, current_index)
    elif field == "varIndex":
        inst["variable"] = variable_from_form(inst["variable"]["kind"], value)
    render_instructions()


def make_text_handler(idx, field):
    def handler(event):
        update_field(idx, field, event.target.value)
    return handler


def make_select_handler(idx, field):
    def handler(event):
        update_field(idx, field, event.target.value)
    return handler


def make_remove_handler(idx):
    def handler(event):
        remove_instruction(idx)
    return handler


def add_instruction(event=None):
    set_encode_result(None)
    instructions.append(empty_instruction())
    render_instructions()


def remove_instruction(idx):
    set_encode_result(None)
    instructions.pop(idx)
    render_instructions()


def build_instruction_row(idx, inst):
    row = document.createElement("div")
    row.className = "instruction-row"

    num = document.createElement("span")
    num.className = "inst-num"
    num.textContent = f"I{idx + 1}"
    row.appendChild(num)

    label_field = document.createElement("div")
    label_field.className = "field"
    label_input = document.createElement("input")
    label_input.id = f"label-{idx}"
    label_input.placeholder = "label (e.g. A1)"
    label_input.value = inst.get("label") or ""
    label_err = show_label_error(inst.get("label"))
    if label_err:
        label_input.style.borderColor = "red"
    listen(label_input, "input", make_text_handler(idx, "label"))
    label_field.appendChild(label_input)
    if label_err:
        err_span = document.createElement("span")
        err_span.className = "field-error"
        err_span.textContent = label_err
        label_field.appendChild(err_span)
    row.appendChild(label_field)

    var_select = document.createElement("select")
    for kind in ("Y", "X", "Z"):
        opt = document.createElement("option")
        opt.value = kind
        opt.textContent = kind
        var_select.appendChild(opt)
    var_select.value = inst["variable"]["kind"]
    listen(var_select, "change", make_select_handler(idx, "varKind"))
    row.appendChild(var_select)

    if inst["variable"]["kind"] != "Y":
        var_index_input = document.createElement("input")
        var_index_input.type = "number"
        var_index_input.min = "1"
        var_index_input.className = "var-index"
        var_index_input.value = str(inst["variable"].get("index", 1))
        listen(var_index_input, "input", make_text_handler(idx, "varIndex"))
        row.appendChild(var_index_input)

    stmt_select = document.createElement("select")
    for value, text in (
        ("dummy", "V ← V"),
        ("increment", "V ← V + 1"),
        ("decrement", "V ← V − 1"),
        ("Goto", "IF V != 0 GOTO"),
    ):
        opt = document.createElement("option")
        opt.value = value
        opt.textContent = text
        stmt_select.appendChild(opt)
    stmt_select.value = inst["statementType"]
    listen(stmt_select, "change", make_select_handler(idx, "statementType"))
    row.appendChild(stmt_select)

    if inst["statementType"] == "Goto":
        target_field = document.createElement("div")
        target_field.className = "field"
        target_input = document.createElement("input")
        target_input.id = f"target-{idx}"
        target_input.placeholder = "target (e.g. A1)"
        target_input.value = inst.get("targetLabel") or ""
        target_err = show_label_error(inst.get("targetLabel"))
        if target_err:
            target_input.style.borderColor = "red"
        listen(target_input, "input", make_text_handler(idx, "targetLabel"))
        target_field.appendChild(target_input)
        if target_err:
            err_span = document.createElement("span")
            err_span.className = "field-error"
            err_span.textContent = target_err
            target_field.appendChild(err_span)
        row.appendChild(target_field)

    remove_btn = document.createElement("button")
    remove_btn.type = "button"
    remove_btn.className = "remove-btn"
    remove_btn.textContent = "✕"
    listen(remove_btn, "click", make_remove_handler(idx))
    row.appendChild(remove_btn)

    return row


def render_instructions():
    container = document.getElementById("instructions-container")

    active = document.activeElement
    active_id = active.id if active else ""
    sel_start = sel_end = None
    if active_id:
        try:
            sel_start = getattr(active, "selectionStart", None)
            sel_end = getattr(active, "selectionEnd", None)
        except Exception:
            sel_start = sel_end = None

    while container.firstChild:
        container.removeChild(container.firstChild)

    for idx, inst in enumerate(instructions):
        container.appendChild(build_instruction_row(idx, inst))

    if active_id:
        el = document.getElementById(active_id)
        if el:
            el.focus()
            if sel_start is not None:
                try:
                    el.setSelectionRange(sel_start, sel_end)
                except Exception:
                    pass


def set_encode_result(result):
    global encode_result
    encode_result = result
    render_encode_output()


def render_encode_output():
    output = document.getElementById("encode-output")
    while output.firstChild:
        output.removeChild(output.firstChild)

    if encode_result is None:
        output.hidden = True
        return
    output.hidden = False

    heading = document.createElement("h2")
    heading.textContent = "steps"
    output.appendChild(heading)

    for step in encode_result["steps"]:
        row = document.createElement("div")
        row.className = "step"
        row.textContent = (
            f"I{step['instructionIndex']}   a={step['a']}   b={step['b']}   c={step['c']}   "
            f"<b,c>={step['innerFunc']}   #(I)={step['instructionCode']}"
        )
        output.appendChild(row)

    result = document.createElement("div")
    result.className = "result"
    result.textContent = f"#(P) = {encode_result['qPrimePowerString']}"
    output.appendChild(result)


def render_decode_output():
    output = document.getElementById("decode-output")
    error_el = document.getElementById("decode-error")

    if decode_error:
        error_el.textContent = decode_error
        error_el.hidden = False
    else:
        error_el.hidden = True

    while output.firstChild:
        output.removeChild(output.firstChild)

    if decode_result is None:
        output.hidden = True
        return
    output.hidden = False

    heading = document.createElement("h2")
    heading.textContent = "Gödel function"
    output.appendChild(heading)

    codes = document.createElement("div")
    codes.className = "step"
    codes.textContent = "[" + ", ".join(str(c) for c in decode_result["instructionCodes"]) + "]"
    output.appendChild(codes)

    factorization = document.createElement("div")
    factorization.className = "step"
    factor_str = " * ".join(f"{f['prime']}^{f['exp']}" for f in decode_result["factorization"]) or "1"
    factorization.textContent = f"= {factor_str}"
    output.appendChild(factorization)

    sub_heading = document.createElement("h2")
    sub_heading.style.marginTop = "16px"
    sub_heading.textContent = "decoded instructions"
    output.appendChild(sub_heading)

    for step in decode_result["steps"]:
        row = document.createElement("div")
        row.className = "step"
        row.textContent = (
            f"#(I{step['instructionIndex']}) = {step['code']}   "
            f"a={step['a']} b={step['b']} c={step['c']}   --> {format_instruction(step['instruction'])}"
        )
        output.appendChild(row)


def handle_encode(event=None):
    global touched
    has_invalid_label = any(
        (inst.get("label") and not is_valid_label(inst["label"]))
        or (inst["statementType"] == "Goto" and inst.get("targetLabel") and not is_valid_label(inst["targetLabel"]))
        for inst in instructions
    )
    if has_invalid_label:
        touched = True
        render_instructions()
        return
    set_encode_result(encode_program(instructions))


def handle_decode(event=None):
    global decode_result, decode_error
    raw = document.getElementById("decode-input").value.strip()
    decode_error = ""
    try:
        decode_result = decode_q(int(raw))
    except Exception:
        decode_result = None
        decode_error = "invalid input — enter a non-negative integer"
    render_decode_output()


def switch_tab(mode):
    document.getElementById("tab-encode").className = "active" if mode == "encode" else ""
    document.getElementById("tab-decode").className = "active" if mode == "decode" else ""
    document.getElementById("encode-section").hidden = mode != "encode"
    document.getElementById("decode-section").hidden = mode != "decode"


def init():
    listen(document.getElementById("tab-encode"), "click", lambda e: switch_tab("encode"))
    listen(document.getElementById("tab-decode"), "click", lambda e: switch_tab("decode"))
    listen(document.getElementById("add-btn"), "click", add_instruction)
    listen(document.getElementById("encode-btn"), "click", handle_encode)
    listen(document.getElementById("decode-btn"), "click", handle_decode)
    render_instructions()
    render_encode_output()
    render_decode_output()
    switch_tab("encode")


init()
