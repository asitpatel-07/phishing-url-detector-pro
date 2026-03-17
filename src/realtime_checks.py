import socket
import requests


def check_domain_resolution(url):
    try:
        host = url.split("//", 1)[-1].split("/", 1)[0].split(":")[0]
        socket.gethostbyname(host)
        return True
    except Exception:
        return False


def check_http_response(url):
    try:
        response = requests.get(
            url,
            timeout=5,
            allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        return response.status_code
    except Exception:
        return None


def run_realtime_checks(url):
    return {
        "domain_resolves": check_domain_resolution(url),
        "http_status": check_http_response(url)
    }


if __name__ == "__main__":
    test_url = input("Enter URL: ").strip()
    print(run_realtime_checks(test_url))