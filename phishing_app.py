from flask import Blueprint, request, render_template
import re
import spacy
import dns.resolver

phishing_app = Blueprint('phishing_app', __name__)

# Load SpaCy model for text analysis
nlp = spacy.load("en_core_web_sm")

# Function to check for phishing keywords and patterns
def is_phishing_content(email_body):
    phishing_keywords = ["urgent", "verify your account", "click here", "account suspended", "free", "claim now", "password", "security"]
    suspicious_phrases = any(keyword in email_body.lower() for keyword in phishing_keywords)

    doc = nlp(email_body)
    for ent in doc.ents:
        if ent.label_ == "MONEY":
            suspicious_phrases = True

    return suspicious_phrases

# Function to validate sender's email domain (using DNS)
def check_email_domain_validity(email):
    domain = email.split('@')[-1] if '@' in email else None
    if not domain:
        return False

    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        return False
    except Exception as e:
        print(f"Unexpected error while validating domain: {e}")
        return False

# Function to check for suspicious URLs in email body
def check_urls_in_email(email_body):
    urls = re.findall(r'(https?://\S+)', email_body)
    for url in urls:
        if "bit.ly" in url or "goo.gl" in url:
            return True
    return False

@phishing_app.route('/', methods=['GET', 'POST'])
def check_phishing_email():
    if request.method == 'POST':
        sender_email = request.form['sender_email']
        email_body = request.form['email_body']

        valid_sender_domain = check_email_domain_validity(sender_email)
        phishing_content = is_phishing_content(email_body)
        suspicious_urls = check_urls_in_email(email_body)
        is_phishing = phishing_content or not valid_sender_domain or suspicious_urls

        return render_template(
            'phishing_result.html',
            result=is_phishing,
            phishing_content=phishing_content,
            valid_sender_domain=valid_sender_domain,
            suspicious_urls=suspicious_urls,
            sender_email=sender_email,
            email_body=email_body
        )

    return render_template('phishing_index.html')
