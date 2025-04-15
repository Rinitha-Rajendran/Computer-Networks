from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
def externllinks(url):
    try:
        response=requests.get(url)
        soup=BeautifulSoup(response.text,'html.parser')
        links=soup.find_all('a',href=True)
        externllinks=[]
        basedomain=urlparse(url).netloc
        for link in links:
            linkurl=link['href']
            if urlparse(linkurl).netloc and urlparse(linkurl).netloc!=basedomain:
                externllinks.append(linkurl)
        extcount=len(externllinks)
        return f"There are {extcount} external links on the website:\n"+"\n".join(externllinks)
    except Exception as e:
        return f"Error while counting exteranl links : {str(e)}"