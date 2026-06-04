#!/bin/bash

# ============================================================
# ticket.sh — Lab Ticket Manager CLI
# ============================================================
# USAGE:
#   ./ticket.sh --browser "Title" "Description" "Body" "labels"
#   ./ticket.sh --curl    "Title" "Description" "Body" "labels"
# ============================================================

MODE=$1
TITLE=$2
DESCRIPTION=$3
BODY=$4
LABELS=$5

LAB_MANAGER_URL="http://localhost:5001"

# ── Validate mode flag ───────────────────────────────────────
if [[ "$MODE" != "--browser" && "$MODE" != "--curl" ]]; then
    echo ""
    echo "  ERROR: Missing or invalid mode flag."
    echo "  Usage:"
    echo "    ./ticket.sh --browser \"Title\" \"Description\" \"Body\" \"labels\""
    echo "    ./ticket.sh --curl    \"Title\" \"Description\" \"Body\" \"labels\""
    echo ""
    exit 1
fi

# ── Validate required fields ─────────────────────────────────
if [[ -z "$TITLE" || -z "$DESCRIPTION" ]]; then
    echo ""
    echo "  ERROR: Title and Description are required."
    echo ""
    exit 1
fi

# ── BROWSER MODE ─────────────────────────────────────────────
if [[ "$MODE" == "--browser" ]]; then
    echo ""
    echo "  Opening Lab Manager in browser..."

    TITLE_ENC=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$TITLE'''))")
    DESC_ENC=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$DESCRIPTION'''))")
    BODY_ENC=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$BODY'''))")
    LABELS_ENC=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$LABELS'''))")

    open "https://lab-ticket-manager.onrender.com/?title=$TITLE_ENCODED&description=$DESCRIPTION_ENCODED&body=$BODY_ENCODED&labels=$LABELS_ENCODED"

    echo "  Browser opened with pre-filled fields."
    echo ""
fi

# ── CURL MODE ────────────────────────────────────────────────
if [[ "$MODE" == "--curl" ]]; then
    echo ""
    echo "  Submitting ticket directly to Lab Manager..."
    echo ""

    # Write payload to a temp JSON file using Python
    # This safely handles multiline text, quotes, colons, and special characters
    TMPFILE=$(mktemp /tmp/ticket_payload.XXXXXX.json)

    python3 - "$TITLE" "$DESCRIPTION" "$BODY" "$LABELS" "$TMPFILE" << 'PYEOF'
import json, sys

payload = {
    'title': sys.argv[1],
    'description': sys.argv[2] + '\n\n' + sys.argv[3],
    'labels': [l.strip() for l in sys.argv[4].split(',') if l.strip()]
}

with open(sys.argv[5], 'w') as f:
    json.dump(payload, f)
PYEOF

    RESPONSE=$(curl -s -X POST "$LAB_MANAGER_URL/api/ticket/create" \
        -H "Content-Type: application/json" \
        -d @"$TMPFILE")

    rm -f "$TMPFILE"

    if echo "$RESPONSE" | python3 -m json.tool > /dev/null 2>&1; then
        ERROR=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('error',''))" 2>/dev/null)
        if [[ -z "$ERROR" ]]; then
            echo "  SUCCESS — Ticket created:"
            echo ""
            echo "$RESPONSE" | python3 -m json.tool
        else
            echo "  ERROR — GitHub rejected the ticket: $ERROR"
        fi
    else
        echo "  ERROR — Could not reach Lab Manager. Is ticketing_app.py running?"
        echo "  Raw response: $RESPONSE"
    fi
    echo ""
fi