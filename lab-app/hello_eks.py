from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <h1>Hello from Kubernetes! 🚀</h1>
    <p>Pod running successfully on AWS EKS</p>
    <p>Hostname: %s</p>
    ''' % os.getenv('HOSTNAME', 'unknown')

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
