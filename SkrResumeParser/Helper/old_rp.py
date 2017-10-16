import requests
def basic(fname):
    url = "http://35.192.156.244/Project/resume/registration/"+fname

    files = {'file': open('/home/sumit/Desktop/project17/ResumeParser/Data/resume_samples/pdfs/samples/'+fname, 'rb')}
    r = requests.post(url, files=files)

    return r.text
print basic("sample1.pdf")
