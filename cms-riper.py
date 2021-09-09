import requests
import time
from config_file import ConfigFile
config = ConfigFile("apis.ini")
API_KEY = config.get('keys.api_key', parse_types=True)

#SEND_REQUESTS_TO_API
def getCMSResults(url,verbose=False):
    try:        
        res=requests.get(f"https://whatcms.org/API/Tech?key={API_KEY}&url={url}")
    except requests.exceptions.ConnectionError:
        print("Unable To Connect To the Internet.")
        exit(1)
########       
    if res.status_code==200:
        if res.json()["result"]["code"]==101:
            print("INVALID API KEY!.")
            exit(1)
########
        if res.json()["result"]["code"]==120:
            WAIT=float(res.json()["retry_in_seconds"])
            if verbose:
                print(f"Rate limit reached. Trying Again in {WAIT} seconds.  ")
            time.sleep(WAIT)
            return getCMSResults(url,verbose)
        if verbose:
            print(res.text)
        cms=None
        for data in res.json()["results"]:
            if "CMS" in data["categories"]:
                cms=data["name"]
        return {
            'cms':cms,
        }
    else:
        print("Unknown Error Occured.")
        exit(1)
#########
#SCAN_URLS_CREATE_AND_WRITE_IN_FILES
def multiScan(url):
    cmsresults=getCMSResults(url)
    print(f"====================")
    print(f"For: {url}")
    print(f"The cms is: {cmsresults['cms'] or 'Unknown'}")
    print(f"====================")
    cmsresultsname = ({cmsresults['cms'] or 'Unknown'})
    for cmstype in cmsresultsname:
        with open("{}.txt".format(cmstype), "a") as filo:
            filo.writelines(url+'\n')
   
if __name__=="__main__":    
     input_file = input('INPUT  YOUR LIST NAME:  ')
     if input_file:
        with open(input_file,'r') as urls:
            durl = [url.strip('\n') for url in urls]
            for url in durl:
             multiScan(url)
             
