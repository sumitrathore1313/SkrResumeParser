from VectorProcessing import GloveSentenceVector

Vector_class = GloveSentenceVector('/home/sumit/PycharmProjects/ResumeParser/Data/resume_segments/Level0/',
                                       save_model_path='/home/sumit/PycharmProjects/ResumeParser/Data/resume_segments/Test/')
sen2vec = Vector_class.get_avg_sentenceVector()
print len(sen2vec)