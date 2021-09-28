from flask import request, Response, jsonify, render_template

from quick_api import app
app.url_map.strict_slashes = False
backend = app.config["BACKEND"]


@app.route('/')
def root():
    if app.config["STATIC_ENTRY_POINT"]:
        return app.send_static_file(app.config["STATIC_ENTRY_POINT"])
    else:
        return ""


@app.route("/api", methods=["GET", "POST"])
def api_root():
    return render_template("api_root.html", datasets=backend.datasets())


@app.route("/api/<dataset>", methods=["GET", "POST"])
def posts(dataset):

    if request.method == "GET":
        sort = request.args.get("_sort")
        order = request.args.get("_order") or "asc"
        try:
            records = backend.get_all(dataset, sort, order)
        except KeyError:
            return Response("{}", mimetype="application/json"), 404

        return Response(records, mimetype="application/json")
    elif request.method == "POST":

        if request.mimetype != "application/json":
            return jsonify({}), 415
        data = request.json
        try:
            record = backend.post(dataset, data)
        except KeyError:
            return Response("{}", mimetype="application/json"), 404

        return Response(record, mimetype="application/json"), 201


@app.route("/api/<dataset>/<record_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def post(dataset, record_id):

    try:
        record_id = int(record_id)
    except ValueError:
        return Response("{}", mimetype="application/json"), 404

    if request.method == "GET":
        try:
            record = backend.get_record(dataset, record_id)
        except KeyError:
            return Response("{}", mimetype="application/json"), 404

        return Response(record, mimetype="application/json")

    elif request.method == "DELETE":
        try:
            record = backend.delete(dataset, record_id)
        except KeyError:
            return Response("{}", mimetype="application/json"), 404

        return Response(record, mimetype="application/json")

    else:
        if request.content_type != "application/json":
            return jsonify({}), 415
        data = request.json

        if request.method == "PUT":
            try:
                record = backend.put(dataset, record_id, data)
            except KeyError:
                return Response("{}", mimetype="application/json"), 404

            return Response(record, mimetype="application/json"), 201

        elif request.method == "PATCH":
            try:
                record = backend.patch(dataset, record_id, data)
            except KeyError:
                return Response("{}", mimetype="application/json"), 404

            return Response(record, mimetype="application/json"), 201





@app.route("/restore")
def restore():
    with open("test_data.json", "w") as orig:
        with open("test_data_bak.json", "r") as bak:
            orig.write(bak.read())
    backend.update_json_data()
    return ""
