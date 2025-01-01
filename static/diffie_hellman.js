document.getElementById('encryption-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    
    fetch('/generate_encryption', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        let resultDiv = document.getElementById('results');
        resultDiv.innerHTML = '';

        if (data.result) {
            for (const key in data.result) {
                const resultDiv = document.createElement('div');
                resultDiv.innerHTML = `<strong>${key}:</strong> ${data.result[key]}`;
                resultDiv.classList.add('result');
                resultDiv.appendChild(resultDiv);
            }
        }
    })
    .catch(error => {
        console.error(error);
        alert('Error processing encryption/decryption');
    });
});
