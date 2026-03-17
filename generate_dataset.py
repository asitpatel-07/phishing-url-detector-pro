import os
import random
import pandas as pd

TOTAL_LEGIT = 3000
TOTAL_PHISH = 3000

legit_domains = [
    "google.com", "youtube.com", "facebook.com", "instagram.com", "wikipedia.org",
    "amazon.in", "amazon.com", "microsoft.com", "apple.com", "github.com",
    "linkedin.com", "netflix.com", "paypal.com", "flipkart.com", "stackoverflow.com",
    "openai.com", "chatgpt.com", "adobe.com", "canva.com", "whatsapp.com",
    "telegram.org", "reddit.com", "quora.com", "coursera.org", "udemy.com",
    "geeksforgeeks.org", "hackerrank.com", "leetcode.com", "oracle.com", "ibm.com",
    "intel.com", "samsung.com", "nvidia.com", "hp.com", "dell.com",
    "lenovo.com", "cisco.com", "zoho.com", "infosys.com", "tcs.com",
    "wipro.com", "accenture.com", "irctc.co.in", "hdfcbank.com", "icicibank.com",
    "axisbank.com", "sbi.co.in", "onlinesbi.sbi", "yahoo.com", "bing.com"
]

legit_paths = [
    "", "/home", "/about", "/services", "/contact", "/blog", "/help",
    "/support", "/pricing", "/dashboard", "/profile", "/settings",
    "/products", "/shop", "/signin", "/account", "/security", "/careers",
    "/docs", "/learn", "/courses/python", "/news", "/updates"
]

legit_queries = [
    "", "", "", "?ref=home", "?page=1", "?lang=en", "?utm_source=web",
    "?category=tech", "?session=abc123", "?id=102"
]

brands = [
    "google", "paypal", "amazon", "microsoft", "apple", "facebook",
    "instagram", "netflix", "bankofindia", "sbi", "hdfc", "icici",
    "axisbank", "flipkart", "linkedin", "telegram", "whatsapp", "adobe"
]

phish_words = [
    "login", "verify", "update", "secure", "account", "bank", "payment",
    "bonus", "gift", "reset", "password", "confirm", "wallet", "suspended",
    "recover", "urgent", "alert", "signin", "validation", "authentication"
]

bad_tlds = [".xyz", ".ru", ".tk", ".ml", ".ga", ".cf", ".top", ".click", ".buzz", ".gq"]
shorteners = ["bit.ly", "tinyurl.com", "goo.gl", "t.co", "cutt.ly"]

def random_legit_url():
    protocol = random.choice(["https://", "https://", "https://", "http://"])
    add_www = random.choice([True, True, False])
    domain = random.choice(legit_domains)
    host = f"www.{domain}" if add_www else domain
    path = random.choice(legit_paths)
    query = random.choice(legit_queries)
    return f"{protocol}{host}{path}{query}"

def random_ip_url():
    ip = ".".join(str(random.randint(11, 240)) for _ in range(4))
    path = random.choice([
        "/login", "/verify", "/secure/update", "/account/reset", "/banking/signin"
    ])
    return f"http://{ip}{path}"

def random_phish_url():
    style = random.randint(1, 8)
    brand = random.choice(brands)
    w1 = random.choice(phish_words)
    w2 = random.choice(phish_words)
    tld = random.choice(bad_tlds)

    if style == 1:
        return f"http://{brand}-{w1}-{w2}{tld}"
    elif style == 2:
        return f"http://secure-{brand}-{w1}-{w2}{tld}/verify"
    elif style == 3:
        return f"http://{brand}.secure-{w1}-{w2}{tld}/login"
    elif style == 4:
        return f"http://www.{brand}-{w1}-account-alert{tld}/update?session={random.randint(1000,9999)}"
    elif style == 5:
        short = random.choice(shorteners)
        return f"http://{short}/{brand}{random.randint(100,999)}{w1}"
    elif style == 6:
        return random_ip_url()
    elif style == 7:
        return f"http://{brand}-{w1}-{w2}-bonus-freegift{tld}/signin?user={brand}&id={random.randint(100,999)}"
    else:
        return f"http://{w1}-{brand}-security-check{tld}/confirm-password"

def generate_dataset():
    rows = []

    for _ in range(TOTAL_LEGIT):
        rows.append({"url": random_legit_url(), "label": 0})

    for _ in range(TOTAL_PHISH):
        rows.append({"url": random_phish_url(), "label": 1})

    random.shuffle(rows)
    df = pd.DataFrame(rows)

    os.makedirs("dataset", exist_ok=True)
    df.to_csv("dataset/urls.csv", index=False)

    print("Dataset generated successfully.")
    print("Saved to dataset/urls.csv")
    print("Total rows:", len(df))
    print("Legitimate:", (df["label"] == 0).sum())
    print("Phishing:", (df["label"] == 1).sum())

if __name__ == "__main__":
    generate_dataset()