async function askQuestion() {
  const q = document.getElementById("question").value;
  const resEl = document.getElementById("answer");
  resEl.textContent = "...thinking...";
  try {
    const resp = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: q }),
    });

    // Handle non-JSON responses gracefully to avoid JSON.parse errors.
    const contentType = resp.headers.get('content-type') || '';
    if (!resp.ok) {
      // Try parse JSON error payload, otherwise show text
      if (contentType.includes('application/json')) {
        const err = await resp.json();
        resEl.textContent = 'Error: ' + (err.error || JSON.stringify(err));
      } else {
        const txt = await resp.text();
        resEl.textContent = 'Error: ' + txt;
      }
      return;
    }

    if (contentType.includes('application/json')) {
      const data = await resp.json();
      if (data.error) {
        resEl.textContent = 'Error: ' + data.error;
      } else {
        resEl.textContent = data.answer;
      }
    } else {
      // Fallback: display raw text
      const txt = await resp.text();
      resEl.textContent = txt;
    }
  } catch (err) {
    resEl.textContent = 'Request failed: ' + err;
  }
}

document.getElementById('ask').addEventListener('click', askQuestion);


async function uploadPdf() {
  const input = document.getElementById('pdf');
  const status = document.getElementById('upload-status');
  if (!input.files || input.files.length === 0) {
    status.textContent = 'No file selected';
    return;
  }
  const file = input.files[0];
  status.textContent = 'Uploading...';
  const form = new FormData();
  form.append('file', file, file.name);

  try {
    const resp = await fetch('/api/ingest', { method: 'POST', body: form });
    const contentType = resp.headers.get('content-type') || '';
    if (!resp.ok) {
      if (contentType.includes('application/json')) {
        const err = await resp.json();
        status.textContent = 'Upload error: ' + (err.error || JSON.stringify(err));
      } else {
        status.textContent = 'Upload error: ' + await resp.text();
      }
      return;
    }

    if (contentType.includes('application/json')) {
      const data = await resp.json();
      status.textContent = 'Uploaded: ' + (data.filename || 'ok');
    } else {
      status.textContent = await resp.text();
    }
  } catch (err) {
    status.textContent = 'Upload failed: ' + err;
  }
}

document.getElementById('upload').addEventListener('click', uploadPdf);
