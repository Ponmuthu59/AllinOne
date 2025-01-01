from flask import Blueprint, request, render_template, jsonify
import hashlib
import base64

crypto_blueprint = Blueprint('encryption', __name__, template_folder='templates', static_folder='static')

# Helper Methods

# MD5 and SHA256 Hashing
def md5(text):
    return hashlib.md5(text.encode()).hexdigest()

def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

# Binary Conversion
def to_binary(text):
    return ' '.join(format(ord(c), 'b') for c in text)

def from_binary(binary_text):
    return ''.join(chr(int(b, 2)) for b in binary_text.split())

# Base64 Encoding and Decoding
def base64_encrypt(text):
    return base64.b64encode(text.encode()).decode()

def base64_decrypt(encoded_text):
    try:
        return base64.b64decode(encoded_text).decode()
    except Exception as e:
        return str(e)

# Octal Conversion
def to_octal(text):
    return ' '.join(oct(ord(c))[2:] for c in text)

def from_octal(octal_text):
    return ''.join(chr(int(o, 8)) for o in octal_text.split())

@crypto_blueprint.route('/encryption')
def encryption():
    return render_template('crypto.html')

@crypto_blueprint.route('/generate_encryption', methods=['POST'])
def generate_encryption():
    algorithm = request.form.get('algorithm')
    text = request.form.get('text')
    result = None
    error = None

    try:
        if algorithm == 'md5' and text:
            result = md5(text)
        elif algorithm == 'sha256' and text:
            result = sha256(text)
        elif algorithm == 'binary_convert' and text:
            result = to_binary(text)
        elif algorithm == 'binary_decode' and text:
            result = from_binary(text)
        elif algorithm == 'base64_encrypt' and text:
            result = base64_encrypt(text)
        elif algorithm == 'base64_decrypt' and text:
            result = base64_decrypt(text)
        elif algorithm == 'octal_convert' and text:
            result = to_octal(text)
        elif algorithm == 'octal_decode' and text:
            result = from_octal(text)
        else:
            error = "Invalid input or missing required fields"
    except Exception as e:
        error = str(e)

    return render_template('crypto_results.html', result=result, error=error)
