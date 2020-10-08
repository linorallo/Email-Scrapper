from datetime import datetime
import boto3
import credentials


def readURL():
    urls = open('url_list.txt', 'r').read()
    urls = str(urls).split('\n')
    return urls


def writeResults(url, results):
    f = open(str(datetime.now())+'.txt', "w+")
    f.write(url+'\n')
    for i in results:
        f.write(str(i)+'\n')
    f.close()


def defineBucket():
    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-2',
        aws_access_key_id = credentials.get_s3_key(),
        aws_secret_access_key='mysecretkey'
    )

def read_cities():
    urls = open('cities_list.csv', 'r').read()
    urls = str(urls).split('\n')
    return urls

def save_results(results):
    f = open('results/'+str(datetime.now())+'.txt', "w+")
    f.write('----------------------'+'\n')
    for i in results:
        f.write(str(i)+'\n')
    f.close()