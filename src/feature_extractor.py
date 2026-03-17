import re
import math
import ipaddress
from urllib.parse import urlparse
import tldextract

SHORTENERS = {
    "bit.ly", "goo.gl", "tinyurl.com", "ow.ly", "t.co", "is.gd",
    "buff.ly", "adf.ly", "bit.do", "cutt.ly", "rb.gy", "shorturl.at"
}

SUSPICIOUS_WORDS = [
    "login", "verify", "update", "secure", "account", "bank", "banking",
    "confirm", "free", "gift", "bonus", "password", "signin",
    "wallet", "pay", "payment", "alert", "suspended", "reset",
    "urgent", "recover", "authentication", "validate"
]

TRUSTED_BRANDS = [
    "google", "paypal", "amazon", "microsoft", "apple", "facebook",
    "instagram", "netflix", "sbi", "hdfc", "icici", "axisbank", "flipkart"
]


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        return url
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url


def shannon_entropy(text: str) -> float:
    if not text:
        return 0.0
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    entropy = 0.0
    length = len(text)
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)
    return round(entropy, 4)


def is_ip_address(domain: str) -> int:
    try:
        ipaddress.ip_address(domain)
        return 1
    except ValueError:
        return 0


def count_digits(text: str) -> int:
    return sum(ch.isdigit() for ch in text)


def count_letters(text: str) -> int:
    return sum(ch.isalpha() for ch in text)


def count_special_chars(text: str) -> int:
    return sum(not ch.isalnum() for ch in text)


def count_suspicious_words(url: str) -> int:
    u = url.lower()
    return sum(word in u for word in SUSPICIOUS_WORDS)


def has_suspicious_word(url: str) -> int:
    return int(count_suspicious_words(url) > 0)


def get_subdomain_count(subdomain: str) -> int:
    if not subdomain:
        return 0
    return len([p for p in subdomain.split(".") if p.strip()])


def has_brand_misuse(url: str, domain: str) -> int:
    u = url.lower()
    d = domain.lower()
    for brand in TRUSTED_BRANDS:
        if brand in u and brand not in d:
            return 1
    return 0


def extract_url_features(url: str) -> dict:
    url = normalize_url(url)

    parsed = urlparse(url)
    extracted = tldextract.extract(url)

    subdomain = extracted.subdomain or ""
    domain = extracted.domain or ""
    suffix = extracted.suffix or ""
    full_domain = parsed.netloc.split(":")[0]
    path = parsed.path or ""
    query = parsed.query or ""

    digit_count = count_digits(url)
    letter_count = count_letters(url)
    special_char_count = count_special_chars(url)

    features = {
        "url_length": len(url),
        "domain_length": len(full_domain),
        "path_length": len(path),
        "query_length": len(query),
        "dot_count": url.count("."),
        "hyphen_count": url.count("-"),
        "underscore_count": url.count("_"),
        "slash_count": url.count("/"),
        "question_count": url.count("?"),
        "equal_count": url.count("="),
        "at_count": url.count("@"),
        "ampersand_count": url.count("&"),
        "percent_count": url.count("%"),
        "digit_count": digit_count,
        "letter_count": letter_count,
        "special_char_count": special_char_count,
        "digit_ratio": round(digit_count / max(len(url), 1), 4),
        "special_char_ratio": round(special_char_count / max(len(url), 1), 4),
        "has_https": int(parsed.scheme == "https"),
        "has_http": int(parsed.scheme == "http"),
        "has_ip_address": is_ip_address(full_domain),
        "subdomain_count": get_subdomain_count(subdomain),
        "has_www": int("www" in subdomain.lower() or full_domain.lower().startswith("www")),
        "has_suspicious_word": has_suspicious_word(url),
        "suspicious_word_count": count_suspicious_words(url),
        "is_shortened": int(full_domain.lower() in SHORTENERS),
        "domain_entropy": shannon_entropy(full_domain),
        "url_entropy": shannon_entropy(url),
        "has_login_word": int("login" in url.lower()),
        "has_verify_word": int("verify" in url.lower()),
        "has_secure_word": int("secure" in url.lower()),
        "has_bank_word": int("bank" in url.lower()),
        "has_update_word": int("update" in url.lower()),
        "has_free_word": int("free" in url.lower()),
        "has_bonus_word": int("bonus" in url.lower()),
        "has_confirm_word": int("confirm" in url.lower()),
        "tld_length": len(suffix),
        "domain_token_count": len([x for x in re.split(r"[-._]", domain) if x]),
        "path_token_count": len([x for x in re.split(r"[/._\-]", path) if x]),
        "query_token_count": len([x for x in re.split(r"[=&_\-]", query) if x]),
        "has_brand_misuse": has_brand_misuse(url, domain),
        "is_long_url": int(len(url) > 75),
        "is_very_long_url": int(len(url) > 120),
        "has_multiple_hyphens": int(url.count("-") >= 2),
    }

    return features


if __name__ == "__main__":
    test_url = input("Enter URL: ").strip()
    print(extract_url_features(test_url))