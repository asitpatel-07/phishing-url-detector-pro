import os


def load_report_template():
    file_path = os.path.join("templates", "report_template.html")
    if not os.path.exists(file_path):
        raise FileNotFoundError("report_template.html not found in templates folder")

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def generate_html_report(url, prediction_text, severity, risk_score, phishing_conf, legit_conf, reasons, features):
    template = load_report_template()

    reasons_html = "".join([f"<li>{reason}</li>" for reason in reasons]) if reasons else "<li>No strong suspicious indicator detected.</li>"

    important_features = {
        "URL Length": features["url_length"],
        "Domain Length": features["domain_length"],
        "Subdomain Count": features["subdomain_count"],
        "Suspicious Word Count": features["suspicious_word_count"],
        "Has HTTPS": features["has_https"],
        "Uses IP Address": features["has_ip_address"],
        "Shortened URL": features["is_shortened"],
        "Brand Misuse": features["has_brand_misuse"],
        "Digit Ratio": features["digit_ratio"],
        "Special Char Ratio": features["special_char_ratio"],
    }

    feature_rows = ""
    for key, value in important_features.items():
        feature_rows += f"<tr><td>{key}</td><td>{value}</td></tr>"

    features_table = f"""
    <table>
        <tr>
            <th>Feature</th>
            <th>Value</th>
        </tr>
        {feature_rows}
    </table>
    """

    html = template
    html = html.replace("{{url}}", str(url))
    html = html.replace("{{prediction}}", str(prediction_text))
    html = html.replace("{{severity}}", str(severity))
    html = html.replace("{{risk_score}}", str(risk_score))
    html = html.replace("{{phishing_confidence}}", f"{phishing_conf:.2f}")
    html = html.replace("{{legitimate_confidence}}", f"{legit_conf:.2f}")
    html = html.replace("{{reasons_list}}", reasons_html)
    html = html.replace("{{features_table}}", features_table)

    return html.encode("utf-8")