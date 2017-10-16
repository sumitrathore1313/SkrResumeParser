from nltk.tag import StanfordNERTagger
st = StanfordNERTagger('/home/sumit/stanford-nlp/ner-api/classifiers/english.muc.7class.distsim.crf.ser.gz', '/home/sumit/stanford-nlp/ner-api/stanford-ner.jar')

def getNER(data):
    return st.tag(data.split())


f = open('/home/sumit/PycharmProjects/ResumeParser/Data/resume_segments/Test/sample.txt', 'r')
data = f.readlines()
f.close()
for line in data:
    print getNER(line)