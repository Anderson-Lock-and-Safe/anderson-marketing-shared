#!/bin/bash
# Send a Google Chat message via the bot service account
# Usage: ./tools/send_gchat.sh "Your message here"

MESSAGE="$1"
SPACE="spaces/AAQAaZSXewI"
SERVER="/Users/gpoole_anderson/claude_marketing/google-chat-plugin/servers/google-chat-mcp.js"
KEY="/Users/gpoole_anderson/claude_marketing/google-chat-plugin/servers/service-account-key.json"

if [ -z "$MESSAGE" ]; then
  echo "Usage: $0 \"message text\""
  exit 1
fi

# Escape quotes in message for JSON
ESCAPED=$(echo "$MESSAGE" | sed 's/"/\\"/g')

GOOGLE_SERVICE_ACCOUNT_KEY_FILE="$KEY" node -e "
const { spawn } = require('child_process');
const proc = spawn('node', ['$SERVER'], {
  env: { ...process.env, GOOGLE_SERVICE_ACCOUNT_KEY_FILE: '$KEY' }
});
let output = '';
proc.stdout.on('data', d => { output += d.toString(); });
const msgs = [
  JSON.stringify({jsonrpc:'2.0',id:1,method:'initialize',params:{protocolVersion:'2024-11-05',capabilities:{},clientInfo:{name:'test',version:'1.0'}}}),
  JSON.stringify({jsonrpc:'2.0',method:'notifications/initialized'}),
  JSON.stringify({jsonrpc:'2.0',id:2,method:'tools/call',params:{name:'google_chat_api',arguments:{method:'POST',path:'/$SPACE/messages',body:{text:'$ESCAPED'}}}})
];
proc.stdin.write(msgs.join('\n') + '\n');
setTimeout(() => { proc.stdin.end(); console.log('Message sent'); process.exit(0); }, 5000);
" 2>/dev/null
