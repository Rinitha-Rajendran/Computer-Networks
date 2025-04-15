
import socket
import requests

def countryweb(url):
    try:
        domain = url.split("//")[-1].split("/")[0]
        Ipaddr=socket.gethostbyname(domain)
        response = requests.get(f"https://ipapi.co/{Ipaddr}/json/")
        data = response.json()
        j=data.get("country_name")
        return f"The website {url} is located in: {j}"
    except Exception as e:
        return str(e)
