#! /usr/bin/env python3
import xml.etree.ElementTree as ET
import urllib3
import io, re, codecs, csv
import nltk
import sys, os
import shutil
import certifi

from bs4 import BeautifulSoup
import lxml

if len(sys.argv) != 3:
    print("This program allows you to download audio files likes concerts etc " +
        "from the website archive.org.\nUsage in cli is :\n" +
        "\"./archive-download.py 'url' 'directory'\" with :\n" +
        "\t- url : the url of the files you want to download\n" +
        "\t- directory : a path where you want to folder to be created" +
        " e.g '~/Downloads'"
        )    
    sys.exit()

def getHTML(URL):
    """Return a html document from a URL link."""
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
    r = http.request('GET',URL)
    if r == urllib3.exceptions.SSLError:
        print("Unable to establish connection.")
        os.exit()
    return r.data
    

def getTracks(URL):
    """Return a dictionnary with key = track_names and values = track_links."""
    soup = BeautifulSoup(getHTML(URL), features="lxml")
    bloc = soup.find("div", {"class":"container container-ia width-max"})
    raw_names = bloc.find_all("meta", {"itemprop":"name"})
    raw_links = bloc.find_all("link", {"itemprop":"associatedMedia"})
    track_names = []
    track_links = []
    i = 0
    for raw_name in raw_names:
            i += 1
            if i < 10:
                nb = "0" + str(i)
            else:
                nb = str(i)
            track_names.append(nb + " - " + raw_name.get('content') + ".mp3")
    for i in range(len(raw_links)//2):
        track_links.append(raw_links[i*2].get('href'))
    tracks = {}
    for track in range(len(track_names)):
        tracks[track_names[track]] = track_links[track]
    return tracks

def getFolderName(URL):
    """
    Return a string representing the name of the folder wich will be
    created to store all tracks.
    """
    soup = BeautifulSoup(getHTML(URL), features="lxml")
    folderName = soup.find("h1", {"class":"sr-only"})
    folderName = folderName.get_text()
    folderName = re.sub('\n','',folderName)
    folderName = re.sub(' +', '_', folderName)
    folderName = re.sub('^_+','',folderName)
    folderName = re.sub('_+$','',folderName)
    
    return folderName
    
    
def writeTrack(track_name, track_link):
    """Writes out a track in the current directory."""
    url = track_link
    c = urllib3.PoolManager()

    with c.request('GET',url, preload_content=False) as resp, open(track_name, 'wb') as out_file:
        shutil.copyfileobj(resp, out_file)


def writeAll(URL):
    tracks = getTracks(URL)
    print("Successfully located track links and names.")
    folder = getFolderName(URL)
    os.mkdir(folder) # creates a sub-directory in current directory to store the live
    os.chdir(folder) # making the created folder the current working folder
    print("Successfully created a sub-directory to download tracks in.")
    n = len(tracks)
    i = 0
    print("Downloading tracks, this might take a while depending on your connection and the size of your resquest.")
    for track_name, track_link in tracks.items():
        i += 1
        writeTrack(track_name, track_link)
        print("Wrote {}/{} tracks".format(i,n)) # to know how the progress    
    print("All tracks successfully written. Bye")

if __name__ == "__main__":

    #url = "https://archive.org/details/gd72-08-27.sbd.orf.3328.sbeok.shnf/gd1972-08-27d1t01-orf.shn"
    url = sys.argv[1] # url of the live to download
    path = sys.argv[2] # path where to create folder containing the tracks

    os.chdir(os.path.expanduser(path)) # set path as the current folder

    writeAll(url) # create directory to put tracks, download tracks

