from flask import Flask, request, Response, jsonify
import requests
import socket

app = Flask(__name__)

@app.route('/proxy', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No url provided'}), 400

    try:
        # Forward the request to the target url
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            params=request.args,
            cookies=request.cookies,
            allow_redirects=True
        )

        # Return the response
        headers = [(name, value) for (name, value) in resp.raw.headers.items()]
        response = Response(resp.content, resp.status_code, headers)
        return response

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dns_lookup', methods=['GET'])
def dns_lookup():
    hostname = request.args.get('hostname')
    try:
        ip_address = socket.gethostbyname(hostname)
        return jsonify({'hostname': hostname, 'ip_address': ip_address})
    except socket.gaierror as e:
        return jsonify({'error': str(e), 'hostname': hostname}), 400

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
