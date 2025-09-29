import whois
import ssl
import socket
def get_domain_from_url(url):
    # Extract domain from URL
    import tldextract
    ext = tldextract.extract(url)
    domain = f"{ext.domain}.{ext.suffix}" if ext.domain and ext.suffix else url
    return domain

def get_domain_info(domain):
    # WHOIS lookup
    import os
    import requests
    api_key = os.environ.get('WHOISXMLAPI_KEY')
    if api_key:
        try:
            print(f"[DEBUG] WhoisXMLAPI lookup for domain: {domain}")
            url = f"https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={api_key}&domainName={domain}&outputFormat=JSON"
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            whois_record = data.get('WhoisRecord', {})
            registrar = whois_record.get('registrarName', 'N/A')
            creation_date = whois_record.get('createdDate')
            if creation_date:
                from datetime import datetime
                try:
                    creation_dt = datetime.strptime(creation_date[:10], "%Y-%m-%d")
                    age_years = (datetime.now() - creation_dt).days // 365
                    age = f"{age_years} years"
                except Exception as date_exc:
                    print(f"[DEBUG] Date parse error: {date_exc}")
                    age = 'N/A'
            else:
                age = 'N/A'
            print(f"[DEBUG] Registrar: {registrar}, Age: {age}")
        except Exception as e:
            import traceback
            print(f"[DEBUG] WhoisXMLAPI lookup failed: {e}")
            traceback.print_exc()
            registrar = 'N/A'
            age = 'N/A'
    else:
        try:
            print(f"[DEBUG] WHOIS lookup for domain: {domain}")
            w = whois.whois(domain)
            print(f"[DEBUG] WHOIS raw result: {w}")
            registrar = w.registrar or 'N/A'
            creation_date = w.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            if creation_date:
                from datetime import datetime
                age_years = (datetime.now() - creation_date).days // 365
                age = f"{age_years} years"
            else:
                age = 'N/A'
            print(f"[DEBUG] Registrar: {registrar}, Age: {age}")
        except Exception as e:
            import traceback
            print(f"[DEBUG] WHOIS lookup failed: {e}")
            traceback.print_exc()
            registrar = 'N/A'
            age = 'N/A'
    # SSL check
    ssl_valid = False
    try:
        print(f"[DEBUG] SSL check for domain: {domain}")
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(3)
            s.connect((domain, 443))
        ssl_valid = True
        print(f"[DEBUG] SSL valid: {ssl_valid}")
    except Exception as e:
        print(f"[DEBUG] SSL check failed: {e}")
        ssl_valid = False
    return {
        'age': age,
        'registrar': registrar,
        'ssl': ssl_valid
    }
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import re
from pydantic import BaseModel
from typing import List, Optional
import os
# Hugging Face integration
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Define request models
class EmailAnalysisRequest(BaseModel):
    email_text: str

class URLAnalysisRequest(BaseModel):
    url: str

# Define response models
class ThreatIndicator(BaseModel):
    description: str
    severity: str

class AnalysisResult(BaseModel):
    classification: str
    confidence: float
    threats: List[ThreatIndicator]
    analysis: str
    domain_info: Optional[dict] = None

app = FastAPI(title="PhishShield ML API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000", "http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML models and vectorizers

# Load Hugging Face phishing email detection model
try:
    hf_tokenizer = AutoTokenizer.from_pretrained("cybersectony/phishing-email-detection-distilbert_v2.4.1")
    hf_model = AutoModelForSequenceClassification.from_pretrained("cybersectony/phishing-email-detection-distilbert_v2.4.1")
    print("✅ Hugging Face phishing email model loaded successfully")
except Exception as e:
    print(f"❌ Error loading Hugging Face model: {e}")
    hf_tokenizer = None
    hf_model = None





# Local sklearn URL phishing classifier integration
# Hugging Face URL phishing classifier integration (original model)
from transformers import BertTokenizerFast, BertForSequenceClassification, pipeline
import torch
urlbert_model_name = "CrabInHoney/urlbert-tiny-v4-phishing-classifier"
urlbert_tokenizer = BertTokenizerFast.from_pretrained(urlbert_model_name)
urlbert_model = BertForSequenceClassification.from_pretrained(urlbert_model_name)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
urlbert_model.to(device)
url_classifier = pipeline(
    "text-classification",
    model=urlbert_model,
    tokenizer=urlbert_tokenizer,
    device=0 if torch.cuda.is_available() else -1,
    return_all_scores=True
)
url_label_mapping = {"LABEL_0": "safe", "LABEL_1": "phishing"}

# Email preprocessing function
def preprocess_email(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Enhanced email feature extraction
def extract_email_features(email_text):
    features = []
    # Basic text features
    features.append(len(email_text))
    features.append(email_text.count('@'))
    features.append(email_text.count('http'))
    features.append(email_text.count('www'))
    features.append(email_text.count('!'))
    features.append(email_text.count('$'))
    features.append(email_text.count('%'))
    features.append(email_text.count('?'))
    features.append(email_text.count('click'))
    features.append(email_text.count('link'))
    features.append(email_text.count('reward'))
    features.append(email_text.count('gift'))
    features.append(email_text.count('card'))
    features.append(email_text.count('claim'))
    features.append(email_text.count('win'))
    features.append(email_text.count('prize'))
    features.append(email_text.count('congratulations'))
    features.append(email_text.count('amazon'))
    features.append(email_text.count('expires'))
    features.append(email_text.count('urgent'))
    features.append(email_text.count('verify'))
    features.append(email_text.count('update'))
    features.append(email_text.count('account'))
    features.append(email_text.count('password'))
    features.append(email_text.count('support'))
    features.append(email_text.count('team'))
    # Sender domain suspicious pattern
    sender_match = re.search(r'from:\s*"?[^"]*"?\s*<([^>]*)>', email_text)
    sender_domain = sender_match.group(1) if sender_match else ''
    features.append(int('amazon' in sender_domain and 'amaz0n' in sender_domain))
    features.append(int('prizes' in sender_domain or 'support' in sender_domain))
    # Link detection
    features.append(int('http' in email_text or 'https' in email_text))
    # Urgency phrases
    urgency_keywords = ['hurry', 'expires', 'urgent', 'limited', 'now', 'immediately', '24 hours']
    features.append(int(any(kw in email_text for kw in urgency_keywords)))
    return np.array(features).reshape(1, -1)

# URL feature extraction function
def extract_url_features(url):
    suspicious_keywords = [
    'login', 'secure', 'verify', 'account', 'update', '极ree', 'paypal', 'bank', 'iphone', 'signin', 'password', 'ebay', 'amazon', 'admin', 'confirm', 'webscr', 'redirect', 'submit', 'id', 'user', 'client', 'auth', 'pay', 'refund', 'win', 'bonus', 'prize', 'alert', 'urgent', 'limited', 'risk', 'protection', 'safe', 'device', 'remove', 'register', 'reset', 'unlock', 'activate', 'support', 'help', 'service', 'access', 'direct', 'deposit', 'royalbank', 'rbc', 'halifax', 'lloyds', 'interac', 'apple', 'google', 'microsoft', 'outlook', 'office', 'mail', 'email', 'sms', 'whatsapp', 'facebook', 'instagram', 'twitter', 'linkedin', 'cloud', 'azure', 'aws', 'netlify', 'xyz', 'online', 'digital', 'site', 'web', 'host', 'domain', 'ssl', 'cert', 'whois', 'registrar', 'phish', 'scam', 'fraud', 'fake', 'malicious', 'danger', 'threat', 'attack', 'hack', 'steal', 'harvest', 'spoof', 'phishing'
]
    keyword_features = [int(kw in url.lower()) for kw in suspicious_keywords]
    return [
        len(url),
        sum(c.isdigit() for c in url),
        sum(not c.isalnum() for c in url),
        url.count('.'),
        int('@' in url),
        url.count('-'),
        len(url.split('/')[2]) if url.startswith('http') and len(url.split('/')) > 2 else 0,  # domain length
        int(url.startswith('https')),  # uses HTTPS
    ] + keyword_features

@app.get("/")
async def root():
    return {"message": "PhishShield ML API is running"}

@app.post("/api/analyze/email", response_model=AnalysisResult)
async def analyze_email(request: EmailAnalysisRequest):
    if not hf_model or not hf_tokenizer:
        raise HTTPException(status_code=500, detail="Hugging Face model not loaded")
    try:
        email_text = request.email_text
        # Extract sender domain for whitelisting
        import re
        sender_match = re.search(r'from:\s*"?[^"\n]*"?\s*<([^>]+)>', email_text, re.IGNORECASE)
        if not sender_match:
            sender_match = re.search(r'from:\s*([^\s]+)', email_text, re.IGNORECASE)
        sender_email = sender_match.group(1).strip() if sender_match else ''
        sender_domain = sender_email.split('@')[-1].lower() if '@' in sender_email else ''
        # Whitelist
        email_whitelist = [
            'company.com', 'gmail.com', 'outlook.com', 'yahoo.com', 'apple.com', 'microsoft.com',
            'icloud.com', 'protonmail.com', 'zoho.com', 'hotmail.com', 'aol.com', 'pm.me'
        ]
        if sender_domain in email_whitelist:
            classification = 'ham'
            confidence = 99.99
            threats = []
            analysis = "Sender domain is trusted. No phishing indicators detected."
            return AnalysisResult(
                classification=classification,
                confidence=confidence,
                threats=threats,
                analysis=analysis
            )

        inputs = hf_tokenizer(email_text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = hf_model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        probs = predictions[0].tolist()
        labels = {
            "legitimate_email": probs[0],
            "phishing_url": probs[1],
            "legitimate_url": probs[2],
            "phishing_url_alt": probs[3]
        }
        print(f"[DEBUG][EMAIL] Raw model probs: {probs}")
        print(f"[DEBUG][EMAIL] Label mapping: {labels}")
        max_label = max(labels.items(), key=lambda x: x[1])
        prediction = max_label[0]
        confidence = float(max_label[1] * 100)

        # Confidence threshold
        threshold = 80.0
        if "phishing" in prediction and confidence > threshold:
            classification = "phishing"
            threats = [ThreatIndicator(description="Phishing indicators detected", severity="high")]
            analysis = "This email is likely a phishing attempt."
        else:
            classification = "ham"
            threats = []
            analysis = "Email content appears legitimate with no suspicious indicators detected."

        return AnalysisResult(
            classification=classification,
            confidence=confidence,
            threats=threats,
            analysis=analysis
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing email: {str(e)}")



@app.post("/api/analyze/url", response_model=AnalysisResult)
async def analyze_url(request: URLAnalysisRequest):
    import traceback

    try:
        url = request.url.strip()
        # Optionally preprocess URL (lowercase, remove protocol)
        url_for_model = url.lower().replace('http://', '').replace('https://', '')

        # Whitelist for trusted domains
        trusted_domains = [
            'google.com', 'gmail.com', 'microsoft.com', 'outlook.com', 'apple.com', 'icloud.com',
            'yahoo.com', 'amazon.com', 'facebook.com', 'twitter.com', 'linkedin.com', 'github.com',
            'youtube.com', 'wikipedia.org', 'instagram.com', 'whatsapp.com', 'netflix.com', 'office.com',
            'mail.google.com', 'mail.yahoo.com', 'mail.outlook.com', 'mail.microsoft.com'
        ]
        # Extract the domain from the URL
        try:
            import tldextract
            ext = tldextract.extract(url)
            domain = f"{ext.domain}.{ext.suffix}" if ext.domain and ext.suffix else url
        except Exception:
            domain = url

        if domain in trusted_domains:
            print(f"[WHITELIST] Domain '{domain}' is trusted. Forcing classification to 'safe'.")
            classification = 'safe'
            confidence = 99.99
            threats = []
            analysis = "This is a well-known trusted domain. No phishing indicators detected."
            # Still get domain info
            domain_info = get_domain_info(domain)
            return AnalysisResult(
                classification=classification,
                confidence=confidence,
                threats=threats,
                analysis=analysis,
                domain_info=domain_info
            )

        # Step 1: Run the classifier, catch errors
        try:
            results = url_classifier(url_for_model)
            print(f"[DEBUG][URL] Raw model output for URL '{url}': {results}")
            # Print all label/score pairs for clarity
            for r in results[0]:
                print(f"[DEBUG][URL] Label: {r['label']}, Score: {r['score']}")
            # If unsure, pick the label with the highest score
            best = max(results[0], key=lambda x: x['score'])
            print(f"[DEBUG][URL] Chosen label: {best['label']} (score: {best['score']})")
            confidence = float(best['score'] * 100)
            threshold = 80.0
            if best['label'] == 'LABEL_1' and confidence > threshold:
                classification = 'phishing'
            else:
                classification = 'safe'
        except Exception as model_exc:
            print(f"Model prediction failed: {model_exc}")
            import traceback
            traceback.print_exc()
            return AnalysisResult(
                classification="error",
                confidence=0.0,
                threats=[],
                analysis=f"Model prediction failed: {str(model_exc)}",
                domain_info=None
            )

        # Fallback rule-based detection for obvious phishing patterns
        phishing_keywords = [
            'login', 'secure', 'verify', 'account', 'update', 'paypal', 'bank', 'signin', 'password', 'ebay', 'amazon', 'admin', 'confirm', 'webscr', 'redirect', 'submit', 'id', 'user', 'client', 'auth', 'pay', 'refund', 'win', 'bonus', 'prize', 'alert', 'urgent', 'limited', 'risk', 'protection', 'safe', 'device', 'remove', 'register', 'reset', 'unlock', 'activate', 'support', 'help', 'service', 'access', 'direct', 'deposit', 'royalbank', 'rbc', 'halifax', 'lloyds', 'interac', 'apple', 'google', 'microsoft', 'outlook', 'office', 'mail', 'email', 'sms', 'whatsapp', 'facebook', 'instagram', 'twitter', 'linkedin', 'cloud', 'azure', 'aws', 'netlify', 'xyz', 'online', 'digital', 'site', 'web', 'host', 'domain', 'ssl', 'cert', 'whois', 'registrar', 'phish', 'scam', 'fraud', 'fake', 'malicious', 'danger', 'threat', 'attack', 'hack', 'steal', 'harvest', 'spoof', 'phishing'
        ]
        suspicious = any(kw in url.lower() for kw in phishing_keywords)
        if suspicious and classification == 'safe':
            classification = 'phishing'
            confidence = max(confidence, 80.0)
            print(f"[DEBUG] Fallback rule-based detection triggered for URL: {url}")

        # Step 2: Threat indicators
        threats = []
        if classification == "phishing":
            threats = [ThreatIndicator(description="Phishing indicators detected", severity="high")]
            analysis = "This URL is likely a phishing site."
        elif classification == "safe":
            analysis = "URL appears to be legitimate."
        else:
            analysis = "Unable to classify URL."

        # Step 3: Domain info extraction, catch errors
        domain_info = None
        try:
            try:
                import tldextract
            except ImportError:
                import sys
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", "tldextract"])
                import tldextract
            # Extract domain from the original URL (remove protocol and path)
            import re
            url_for_domain = url
            if '://' in url_for_domain:
                url_for_domain = url_for_domain.split('://', 1)[1]
            url_for_domain = url_for_domain.split('/', 1)[0]
            domain = get_domain_from_url(url_for_domain)
            print(f"[DEBUG] Extracted domain for info: {domain}")
            domain_info = get_domain_info(domain)
        except Exception as domain_exc:
            print(f"Domain info extraction failed: {domain_exc}")
            traceback.print_exc()
            domain_info = None

        return AnalysisResult(
            classification=classification,
            confidence=confidence,
            threats=threats,
            analysis=analysis,
            domain_info=domain_info
        )
    except Exception as e:
        print(f"Error analyzing URL: {e}")
        traceback.print_exc()
        return AnalysisResult(
            classification="error",
            confidence=0.0,
            threats=[],
            analysis=f"Internal error: {str(e)}",
            domain_info=None
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
