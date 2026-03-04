const logEl = document.getElementById('log');
const runBtn = document.getElementById('runBtn');
const statusEl = document.getElementById('status');
const chainEl = document.getElementById('chain');
const refreshBtn = document.getElementById('refreshChain');

function setStatus(state, text) {
  statusEl.className = `status ${state}`;
  statusEl.textContent = text;
}

function appendLine(text) {
  const p = document.createElement('div');
  p.className = 'line';
  const lower = text.toLowerCase();
  if (lower.includes('step')) p.classList.add('step');
  if (lower.includes('[chain]')) p.classList.add('chain');
  if (lower.includes('[private')) p.classList.add('private');
  p.textContent = text;
  logEl.appendChild(p);
  logEl.scrollTop = logEl.scrollHeight;
}

async function loadChain() {
  chainEl.innerHTML = '<div class="muted">Loading chain…</div>';
  try {
    const res = await fetch('/api/chain');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const blocks = await res.json();
    if (!Array.isArray(blocks) || blocks.length === 0) {
      chainEl.innerHTML = '<div class="muted">No blocks yet. Run the demo.</div>';
      return;
    }
    const rows = blocks.map(b => `
      <tr>
        <td class="num">#${String(b.block_num).padStart(2,'0')}</td>
        <td class="rt">${b.record_type}</td>
        <td class="summary">${b.summary}</td>
        <td class="hash">${b.block_hash.slice(0,16)}…</td>
      </tr>`).join('');
    chainEl.innerHTML = `
      <table>
        <thead><tr><th>#</th><th>Type</th><th>Summary</th><th>Hash</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>`;
  } catch (err) {
    chainEl.innerHTML = `<div class="error">Chain load failed: ${err.message}</div>`;
  }
}

function runDemo() {
  logEl.innerHTML = '';
  setStatus('running', 'Running');
  runBtn.disabled = true;

  const src = new EventSource('/api/run');
  src.onmessage = (ev) => {
    appendLine(ev.data);
  };
  src.addEventListener('end', async () => {
    src.close();
    setStatus('done', 'Done');
    runBtn.disabled = false;
    await loadChain();
  });
  src.onerror = (err) => {
    appendLine('[error] stream interrupted');
    setStatus('fail', 'Error');
    runBtn.disabled = false;
    src.close();
  };
}

runBtn.addEventListener('click', runDemo);
refreshBtn.addEventListener('click', loadChain);

setStatus('idle', 'Idle');
loadChain();
