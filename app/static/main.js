document.getElementById('chat-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const input = document.getElementById('prompt');
    const prompt = input.value;
    if(!prompt) return;
    addMessage('user', prompt);
    input.value='';
    const res = await fetch('/api/chat', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({prompt})
    });
    const data = await res.json();
    addMessage('assistant', data.response);
});

function addMessage(role, text){
    const div = document.createElement('div');
    div.classList.add('message', role);
    div.textContent = text;
    document.getElementById('messages').appendChild(div);
}
