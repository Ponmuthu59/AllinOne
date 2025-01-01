from flask import Blueprint, request, render_template, jsonify

diffie_hellman_blueprint = Blueprint('diffie_hellman', __name__, template_folder='templates', static_folder='static')

# Diffie-Hellman Algorithm Steps
def generate_diffie_hellman_steps(p, g, a, b):
    steps = [
        f"Step 1: Chosen prime number p = {p}",
        f"Step 2: Chosen primitive root modulo p, g = {g}",
        f"Step 3: Random private keys selected: a = {a}, b = {b}",
        f"Step 4: Compute public keys: A = g^a mod p, B = g^b mod p",
        f"Step 5: Compute shared keys: shared_key_A = B^a mod p, shared_key_B = A^b mod p",
        f"Final Step: Shared Key: {pow(pow(g, b, p), a, p)}"
    ]
    return steps

@diffie_hellman_blueprint.route('/')
def diffie_hellman():
    return render_template('diffie_hellman.html')  # HTML template for Diffie-Hellman

@diffie_hellman_blueprint.route('/generate_diffie', methods=['POST'])
def generate_diffie_hellman():
    try:
        p = int(request.form.get('p'))
        g = int(request.form.get('g'))
        a = int(request.form.get('a'))
        b = int(request.form.get('b'))

        steps = generate_diffie_hellman_steps(p, g, a, b)
        return jsonify({'steps': steps})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
