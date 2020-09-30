from datetime import datetime

def readURL():
    urls = open('url_list.txt','r').read()
    urls = str(urls).split('\n')
    return urls

def writeResults(url,results):
    f= open(str(datetime.now()),"w+")
    f.write(url+'\n')
    for i in results:
        i = i.replace('{','').replace('}','').replace(',','').replace("'",'')
        f.write(str(i)+'\n')
    f.close()