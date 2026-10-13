from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check

# Partea 1: apeluri pentru build_url si is_https
print("Partea 1, build_url:", build_url("example.com", "login"))
print("Partea 1, build_url:", build_url("example.com", "/login"))
print("Partea 1, is_https:", is_https("https://example.com"))
print("Partea 1, is_https:", is_https("http://example.com"))

# Partea 2: apeluri pentru show_response (se afiseaza singur)
print("Partea 2, show_response (example.com):")
show_response("https://example.com")
print("Partea 2, show_response (httpbin.org/json):")
show_response("https://httpbin.org/json")

# Partea 3: apeluri pentru check_site (caz care merge + caz care esueaza)
print("Partea 3, check_site (merge):", check_site("https://example.com"))
print("Partea 3, check_site (inexistent):", check_site("http://this-site-does-not-exist.invalid"))

# Partea 4: apelul scan_sites()
print("Partea 4, scan_sites:")
scan_sites()

# Partea 5: apeluri pentru check_headers (cu antete + fara antete + inaccesibil)
print("Partea 5, check_headers (cu antete):",
      check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
print("Partea 5, check_headers (fara antete):", check_headers("https://example.com"))
print("Partea 5, check_headers (inaccesibil):", check_headers("http://this-site-does-not-exist.invalid"))

# Partea 6: apeluri pentru retry_check (200, 404, 500, inaccesibil)
print("Partea 6, retry_check (200):", retry_check("https://httpbin.org/status/200"))
print("Partea 6, retry_check (404):", retry_check("https://httpbin.org/status/404"))
print("Partea 6, retry_check (500):", retry_check("https://httpbin.org/status/500"))
print("Partea 6, retry_check (inaccesibil):", retry_check("http://this-site-does-not-exist.invalid"))

