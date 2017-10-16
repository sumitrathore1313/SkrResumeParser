import os
import re

def get_data(input_path):
    '''
    this file take whole manual labeled resumes from file path given and convert into data used for gram sentence vector like
         all.txt
    :param input_path: path of resumes file
    :return: return data
    '''
    ends = ['<ba>', '<we>', '<ed>', '<ca>', '<ex>', '<sk>', '<pr>', '<su>', '<mi>']
    end = ['<ba>', '<we>', '<ed>', '<ca>', '<ex>', '<sk>', '<pr>', '<su>', '<mi>', '</ba>', '</we>', '</ed>', '</ca>','</ex>', '</sk>', '</pr>', '</su>', '</mi>']

    sentence = []
    with open(input_path, 'rb') as f:
        contents = f.readlines()
        token = 0
        for line in contents:
            if line.rstrip() == '<ba>' or token == 1:
                if line.rstrip() not in end:
                    sentence.append([line, 0])
                if token != 1:
                    token = 1
                elif line.rstrip() in ends:
                    token = 0

            if line.rstrip() == '<we>' or token == 2:
                if line.rstrip() not in end:
                    sentence.append([line, 1])
                if token != 2:
                    token = 2
                elif line.rstrip() in ends:
                    token = 0

            if line.rstrip() == '<ed>' or token == 3:
                if line.rstrip() not in end:
                    sentence.append([line, 2])
                if token != 3:
                    token = 3
                elif line.rstrip() in ends:
                    token = 0


            if line.rstrip() == '<ca>' or token == 4:
                if line.rstrip() not in end:
                    sentence.append([line, 3])
                if token != 4:
                    token = 4
                elif line.rstrip() in ends:
                    token = 0


            if line.rstrip() == '<ex>' or token == 5:
                if line.rstrip() not in end:
                    sentence.append([line, 4])
                if token != 5:
                    token = 5
                elif line.rstrip() in ends:
                    token = 0


            if line.rstrip() == '<sk>' or token == 6:
                if line.rstrip() not in end:
                    sentence.append([line, 5])
                if token != 6:
                    token = 6
                elif line.rstrip() in ends:
                    token = 0


            if line.rstrip() == '<pr>' or token == 7:
                if line.rstrip() not in end:
                    sentence.append([line, 6])
                if token != 7:
                    token = 7
                elif line.rstrip() in ends:
                    token = 0


            if line.rstrip() == '<su>' or token == 8:
                if line.rstrip() not in end:
                    sentence.append([line, 7])
                if token != 8:
                    token = 8
                elif line.rstrip() in ends:
                    token = 0


            if line.rstrip() == '<mi>' or token == 9:
                if line.rstrip() not in end:
                    sentence.append([line, 8])
                if token != 9:
                    token = 9
                elif line.rstrip() in ends:
                    token = 0

    return sentence

def generate_data(dir_path, output_path):
    '''
    this funtion take all labeled resume and combine to form all.txt
    NOTE - delete all file if already exist beacuse it will not overwrite
    :param dir_path: path of resume dir
    :param output_path : path of output file
    :return: generate segments file for level
    '''
    # select only dir not file
    filelist = os.walk(dir_path).next()[2]
    for file in filelist:
            with open(dir_path+file, 'r') as f:
                contents = f.read()
            with open(output_path, 'a') as f:
                f.write(contents)
    return 0

#generate_data("/home/sumit/Desktop/project17/ResumeParser/Data/resume_samples/txts/all/", "/home/sumit/Desktop/project17/ResumeParser/Data/resume_segments/Level0/all.txt")
#sen2vec = get_data("/home/sumit/Desktop/project17/ResumeParser/Data/resume_segments/Level0/all.txt")
#print sen2vec[-5:-1], len(sen2vec), len(sen2vec[0])