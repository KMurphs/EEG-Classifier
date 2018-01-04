import requests
from bs4 import BeautifulSoup
import urllib
import os

EEGFiles_url = 'https://physionet.org/physiobank/database/sleep-edfx/'


#gets the list of files from the url address 
def Get_Files_List(url):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    files = list()
    for item in soup.find('pre').find_all('a'):
        item_str = str(item)
        if(('.edf' in item_str) and ('.hyp') not in item_str):
            file = item_str[item_str.find('href="') + 6:item_str.find('">')]
            files.append(file)
    return files			
	


#downloads a file in the data directory at the same level as this python file
def Download_File(file):
    try: 
        link = EEGFiles_url + file
        downloader = urllib.URLopener()
    #    downloader.retrieve(link, '..\\Data\\' + file)
        downloader.retrieve(link, 'Data\\' + file)
    except:
        print('Error Occured while downloading %s'%file)
        pass


#downloads a file in the data directory at the same level as this python file
def Download_EDF_Files(EEGFiles_url):
    print('\n\nDownloading EDF Files:')
    files = Get_Files_List(EEGFiles_url)
    
    counter = 0
    for file in files:
        counter += 1
        print('%d out of %d: File: %s'%(counter, len(files),file))
        if file in os.listdir('Data'):
#        if file in os.listdir('..\\Data'):
            continue
        Download_File(file)
    
    
    
    
    
    
    
if __name__ == '__main__':
    Download_EDF_Files(EEGFiles_url)
		