import requests

SITES = [
    # Pagini obisnuite (Partile 2, 3 si 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care esueaza
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Raspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    # Returneaza o adresa completa, de exemplu https://example.com/login.
    # lstrip('/') face sa mearga si cu path "login", si cu "/login".
    return f"https://{host}/{path.lstrip('/')}"


def is_https(url):
    # Returneaza True daca adresa incepe cu https://, altfel False.
    return url.startswith("https://")


def show_response(url):
    # Trimite un GET la url si afiseaza statusul si Content-Type.
    r = requests.get(url, timeout=5)
    print("Status:", r.status_code)
    print("Content-Type:", r.headers.get("Content-Type", "unknown"))


def check_site(url):
    # Returneaza un dictionar cu: status, content_type, length, server.
    # Nu se opreste niciodata cu eroare: la esec intoarce status None si un mesaj.
    try:
        r = requests.get(url, timeout=5)
    except requests.RequestException as e:
        return {"status": None, "error": str(e)}
    return {
        "status": r.status_code,
        # pastram doar tipul (fara "; charset=...")
        "content_type": r.headers.get("Content-Type", "unknown").split(";")[0].strip(),
        "length": len(r.content),
        # daca lipseste antetul Server, folosim "unknown"
        "server": r.headers.get("Server", "unknown"),
    }


def scan_sites():
    # Verifica toate site-urile din SITES, afiseaza doar cele cu status 200 si un rezumat.
    rezultate = [(url, check_site(url)) for url in SITES]
    ok = [(url, r) for url, r in rezultate if r["status"] == 200]
    # sortare dupa length, cel mai mare primul
    ok.sort(key=lambda pereche: pereche[1]["length"], reverse=True)
    for url, r in ok:
        print(f"{url} -> {r['status']}, {r['length']} octeti")
    print(f"Reusite: {len(ok)} | Esuate: {len(rezultate) - len(ok)}")


def check_headers(url):
    # Returneaza un dictionar cu: present, missing, score.
    # La esec intoarce status None si un mesaj.
    try:
        r = requests.get(url, timeout=5)
    except requests.RequestException as e:
        return {"status": None, "error": str(e)}
    # r.headers e insensibil la majuscule, deci "in" potriveste indiferent de caz.
    present = [h for h in SECURITY_HEADERS if h in r.headers]
    missing = [h for h in SECURITY_HEADERS if h not in r.headers]
    return {
        "present": present,
        "missing": missing,
        # scor = procent intreg al antetelor prezente (1/4=25, 2/4=50, 4/4=100)
        "score": int(len(present) / len(SECURITY_HEADERS) * 100),
    }


def retry_check(url, attempts=3):
    # Incearca de cel mult `attempts` ori; returneaza status si attempts (cereri reale).
    status = None
    error = None
    facute = 0
    for _ in range(attempts):
        facute += 1
        try:
            r = requests.get(url, timeout=5)
        except requests.RequestException as e:
            # eroare de conexiune/timeout -> mai incercam
            status, error = None, str(e)
            continue
        status, error = r.status_code, None
        # status sub 500 (inclusiv 404): ne oprim imediat
        if status < 500:
            break
        # status 500+: lasam bucla sa mai incerce
    rezultat = {"status": status, "attempts": facute}
    # cheia "error" doar daca toate incercarile au esuat cu eroare de conexiune
    if status is None and error is not None:
        rezultat["error"] = error
    return rezultat
