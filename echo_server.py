from flask import Flask, render_template, abort, request, make_response, json, Response
import csv

app = Flask(__name__)

data = {}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    if path == '':
        return render_template('index.html')
    elif path == 'endpoints':
        return Response(json.dumps(data.keys()))
    else:
        if request.method == 'POST':
            file = request.files.get('upload_file', None)
            if not file is None:
                contents = decode_file(file, path)
            else:
                contents = json.loads(request.data)

            data[path] = contents
            return make_response('{"test": "ok"}')
        else:
            contents = data.get(path, None)
            if not contents is None:
                return Response(json.dumps(contents))
            else:
                abort(404)


def decode_file(file, path):
    if file.content_type == 'application/json':
        return json.load(file.stream)
    elif file.content_type == 'text/csv':
        reader = csv.DictReader(file.stream, delimiter=',')
        return [line for line in reader]


if __name__ == '__main__':
    app.run()
