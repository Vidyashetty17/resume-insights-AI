document.getElementById('uploadForm')?.addEventListener('submit',async e=>{
    e.preventDefault();document.getElementById('loading').textContent='Analyzing...';});