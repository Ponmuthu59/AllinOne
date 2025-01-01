<script>
    document.addEventListener("DOMContentLoaded", function() {
        const algorithmSelect = document.getElementById('algorithm');
        const textInput = document.getElementById('text');
        const keyInput = document.getElementById('key');
        const ivInput = document.getElementById('iv');
        const ciphertextInput = document.getElementById('ciphertext');

        // Event listener for algorithm change
        algorithmSelect.addEventListener('change', function() {
            // Hide all optional fields
            keyInput.classList.add('optional-field');
            ivInput.classList.add('optional-field');
            ciphertextInput.classList.add('optional-field');
            
            // Show only the required fields based on selected algorithm
            if (algorithmSelect.value === 'aes_encrypt') {
                keyInput.classList.remove('optional-field');
                ivInput.classList.remove('optional-field');
            } else if (algorithmSelect.value === 'aes_decrypt') {
                keyInput.classList.remove('optional-field');
                ivInput.classList.remove('optional-field');
                ciphertextInput.classList.remove('optional-field');
            } else if (algorithmSelect.value === 'base64_encrypt' || algorithmSelect.value === 'base64_decrypt') {
                textInput.classList.remove('optional-field');
            }
        });

        // Trigger change event to hide fields initially
        algorithmSelect.dispatchEvent(new Event('change'));
    });
</script>
