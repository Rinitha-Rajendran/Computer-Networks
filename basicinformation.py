from bs4 import BeautifulSoup
import requests
def extracttext(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        if soup.title:
            title = soup.title.string
        else:
            title = "No title found"
        headers = []
        for h in soup.find_all(['h1','h2']):
            headers.append(h.get_text())
        headerstext = '\n'.join(headers) if headers else "no headers found"
        reply = (
            f"=== Website Information ===\n"
            f"URL: {url}\n"
            f"Title: {title}\n"
            f"\n=== Headers ===\n"
            f"{headerstext}\n"
            f"============================\n"
        )
        return reply
    except requests.RequestException as e:
        return f"Error fetching URL: {str(e)}\n"
