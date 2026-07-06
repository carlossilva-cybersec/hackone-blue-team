import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "raw_xml", "registry_persistance.xml")


def get_child_text(parent, tag_name):
    for child in parent:
        if child.tag.split("}")[-1] == tag_name:
            return (child.text or "").strip()
    return ""


def get_child_attr(parent, tag_name, attr_name):
    for child in parent:
        if child.tag.split("}")[-1] == tag_name:
            return (child.attrib.get(attr_name) or "").strip()
    return ""


def load_events(file_path=DATA_PATH):
    tree = ET.parse(file_path)
    root = tree.getroot()
    events = []

    for event_elem in root.findall(".//{*}Event"):
        system = event_elem.find("{*}System")
        event_data = event_elem.find("{*}EventData")

        data_map = {}
        if event_data is not None:
            for data in event_data.findall("{*}Data"):
                name = data.attrib.get("Name")
                if name:
                    data_map[name] = (data.text or "").strip()

        event = {
            "event_id": int(get_child_text(system, "EventID") or 0),
            "utc_time": data_map.get("UtcTime") or get_child_attr(system, "TimeCreated", "SystemTime") or "",
            "channel": get_child_text(system, "Channel"),
            "computer": get_child_text(system, "Computer"),
            "provider": get_child_attr(system, "Provider", "Name"),
            "event_type": data_map.get("EventType", ""),
            "image": data_map.get("Image", ""),
            "target_object": data_map.get("TargetObject", ""),
            "details": data_map.get("Details", ""),
            "rule_name": data_map.get("RuleName", ""),
            "user": data_map.get("User", ""),
            "process_id": int(data_map.get("ProcessId") or 0),
            "raw_log": ET.tostring(event_elem, encoding="unicode"),
        }
        events.append(event)

    return events


def evaluate_condition(event, expression):
    expression = expression.strip()
    match = re.match(r"^([A-Za-z_]+)\s*(==|!=|contains|startswith)\s*(.+)$", expression)
    if not match:
        raise ValueError("Consulta inválida. Use algo como: event_id == 13")

    field = match.group(1).lower().replace("-", "_")
    operator = match.group(2).lower()
    raw_value = match.group(3).strip()

    if raw_value.startswith(("'", '"')) and raw_value.endswith(("'", '"')):
        value = raw_value[1:-1]
    else:
        try:
            value = int(raw_value)
        except ValueError:
            value = raw_value

    actual = event.get(field, "")
    if operator == "contains":
        return str(actual).lower().find(str(value).lower()) != -1
    if operator == "startswith":
        return str(actual).lower().startswith(str(value).lower())
    if operator == "==":
        return actual == value
    if operator == "!=":
        return actual != value
    raise ValueError("Operador não suportado")


def search_events(events, query):
    query = (query or "").strip()
    if not query:
        return events[:50]

    try:
        blocks = re.split(r"\s+(and|or)\s+", query, flags=re.IGNORECASE)
        if len(blocks) == 1:
            return [event for event in events if evaluate_condition(event, query)]

        results = [event for event in events if evaluate_condition(event, blocks[0])]
        index = 1
        while index < len(blocks):
            operator = blocks[index].lower()
            next_block = blocks[index + 1]
            next_results = [event for event in events if evaluate_condition(event, next_block)]

            if operator == "and":
                results = [event for event in results if event in next_results]
            elif operator == "or":
                results = results + [event for event in next_results if event not in results]
            index += 2

        return results
    except ValueError:
        return []


def build_metrics(events, results):
    counts = {}
    for event in results:
        event_type = event.get("event_type") or "Sem tipo"
        counts[event_type] = counts.get(event_type, 0) + 1

    chart = []
    for name, value in sorted(counts.items(), key=lambda item: item[1], reverse=True)[:6]:
        chart.append({"name": name, "value": value})

    return {
        "total_events": len(events),
        "filtered_events": len(results),
        "chart": chart,
        "top_event_type": chart[0]["name"] if chart else "Nenhum",
    }


@app.route("/", methods=["GET", "POST"])
def index():
    query = "event_id == 13"
    results = []
    selected_event = None
    examples = [
        "event_id == 13",
        "image contains 'svchost'",
        "event_type == 'SetValue'",
        "target_object contains 'Services'",
        "image contains 'cmd' or event_type == 'SetValue'",
    ]

    events = load_events(DATA_PATH)

    if request.method == "POST":
        query = request.form.get("query", "") or query
    else:
        query = request.args.get("query", query)

    results = search_events(events, query)[:50]
    metrics = build_metrics(events, results)
    selected_event_id = request.args.get("event_id", type=int)
    if selected_event_id is not None:
        selected_event = next((event for event in results if event["event_id"] == selected_event_id), None)
    if selected_event is None and results:
        selected_event = results[0]

    if request.method == "POST":
        return render_template(
            "results.html",
            query=query,
            results=results,
            examples=examples,
            total_events=len(events),
            selected_event=selected_event,
            metrics=metrics,
        )

    if query != "event_id == 13" or request.args.get("query") is not None or request.args.get("event_id") is not None:
        return render_template(
            "results.html",
            query=query,
            results=results,
            examples=examples,
            total_events=len(events),
            selected_event=selected_event,
            metrics=metrics,
        )

    return render_template("index.html", query=query, examples=examples, metrics=metrics)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
