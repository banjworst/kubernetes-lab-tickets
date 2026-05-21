import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ticket_manager import GitHubTicketManager

app = Flask(__name__, static_folder='.')
CORS(app)

# ── Load credentials from environment variables ──────────────
token = os.getenv("GITHUB_TOKEN")
owner = os.getenv("GITHUB_OWNER")
repo  = os.getenv("GITHUB_REPO")

if not all([token, owner, repo]):
    print("ERROR: Missing environment variables.")
    print("Set them with:")
    print("  export GITHUB_TOKEN='ghp_your_token'")
    print("  export GITHUB_OWNER='your-github-username'")
    print("  export GITHUB_REPO='your-repo-name'")
    exit(1)

tm = GitHubTicketManager(token, owner, repo)

# ── Serve the UI ─────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('.', 'ticket_ui.html')

# ── Create a ticket ──────────────────────────────────────────
@app.route('/api/ticket/create', methods=['POST'])
def create_ticket():
    data        = request.get_json()
    title       = data.get('title', '').strip()
    description = data.get('description', '').strip()
    labels      = data.get('labels', [])

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    # FIX: handle labels whether they arrive as a string or a list
    # ticket.sh sends ["kubernetes,aws,eks"] — one string inside a list
    if isinstance(labels, str):
        labels = [l.strip() for l in labels.split(',') if l.strip()]
    elif isinstance(labels, list):
        expanded = []
        for item in labels:
            expanded.extend([l.strip() for l in str(item).split(',') if l.strip()])
        labels = expanded

    print(f"DEBUG: title={title!r} labels={labels!r}")

    result = tm.create_ticket(title=title, description=description, labels=labels)

    if result['success']:
        return jsonify({
            'number':  result['ticket_number'],
            'url':     result['url'],
            'message': result['message']
        }), 201
    else:
        print(f"DEBUG: GitHub error: {result['error']}")
        return jsonify({'error': result['error']}), 500

# ── List tickets ─────────────────────────────────────────────
@app.route('/api/ticket/list', methods=['GET'])
def list_tickets():
    state  = request.args.get('state', 'open')
    result = tm.list_tickets(state=state)

    if result['success']:
        tickets = []
        for t in result['tickets']:
            tickets.append({
                'number': t['number'],
                'title':  t['title'],
                'state':  t['state'],
                'body':   t.get('body', ''),
                'labels': [l['name'] for l in t.get('labels', [])]
            })
        return jsonify({'tickets': tickets}), 200
    else:
        return jsonify({'error': result['error']}), 500

# ── Get a single ticket ──────────────────────────────────────
@app.route('/api/ticket/<int:number>', methods=['GET'])
def get_ticket(number):
    result = tm.get_ticket(number)

    if result['success']:
        t = result['ticket']
        return jsonify({
            'number':      t['number'],
            'title':       t['title'],
            'state':       t['state'],
            'description': t.get('body', ''),
            'labels':      [l['name'] for l in t.get('labels', [])]
        }), 200
    else:
        return jsonify({'error': result['error']}), 404

# ── Close a ticket ───────────────────────────────────────────
@app.route('/api/ticket/<int:number>/close', methods=['POST'])
def close_ticket(number):
    data   = request.get_json()
    note   = data.get('resolution_note', '')
    result = tm.close_ticket(number, solution_comment=note)

    if result['success']:
        return jsonify({'message': result['message']}), 200
    else:
        return jsonify({'error': result['error']}), 500

# ── Run ──────────────────────────────────────────────────────
if __name__ == '__main__':
    print(f"\n  Lab Manager running at http://localhost:5001")
    print(f"  GitHub: {owner}/{repo}\n")
    app.run(host='0.0.0.0', port=5001, debug=False)