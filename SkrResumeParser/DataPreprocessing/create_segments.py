import os
import re

def generate_level0_title_segments(input_path, output_path):
    '''
    this file take whole manual labeled resumes from dir path given and convert into segment like
         basic_info.txt
         education.txt
         extra.txt
         experience.txt
         skills.txt
         projects.txt
         certificates.txt
         summary.txt
    and save these file to output path given
    :param input_path: path of resumes dir
    :param output_path: path of output dir
    :return: generate file return 0
    '''
    ends = ['<ba>', '<we>', '<ed>', '<ca>', '<ex>', '<sk>', '<pr>', '<su>', '<mi>']
    basic_info = []
    education = []
    extra = []
    experience = []
    skills = []
    projects = []
    certificates = []
    summary = []
    mimc = []
    segments = [basic_info, education, extra, experience, skills, projects, certificates, summary, mimc]
    segments_label = ['basic_info', 'education', 'extra', 'experience', 'skills', 'projects', 'certificates', 'summary', 'mimc']
    all_files = os.listdir(input_path)
    for x in all_files:
        with open(input_path+x, 'rb') as f:
            contents = f.readlines()
            token = 0
            for line in contents:
                if line.rstrip() == '<ba>' or token == 1:
                    basic_info.append(line)
                    if token != 1:
                        token = 1
                    elif line.rstrip() in ends:
                        token = 0

                if line.rstrip() == '<we>' or token == 2:
                    experience.append(line)
                    if token != 2:
                        token = 2
                    elif line.rstrip() in ends:
                        token = 0

                if line.rstrip() == '<ed>' or token == 3:

                    education.append(line)
                    if token != 3:
                        token = 3
                    elif line.rstrip() in ends:
                        token = 0


                if line.rstrip() == '<ca>' or token == 4:

                    certificates.append(line)
                    if token != 4:
                        token = 4
                    elif line.rstrip() in ends:
                        token = 0


                if line.rstrip() == '<ex>' or token == 5:

                    extra.append(line)
                    if token != 5:
                        token = 5
                    elif line.rstrip() in ends:
                        token = 0


                if line.rstrip() == '<sk>' or token == 6:

                    skills.append(line)
                    if token != 6:
                        token = 6
                    elif line.rstrip() in ends:
                        token = 0


                if line.rstrip() == '<pr>' or token == 7:

                    projects.append(line)
                    if token != 7:
                        token = 7
                    elif line.rstrip() in ends:
                        token = 0


                if line.rstrip() == '<su>' or token == 8:
                    summary.append(line)
                    if token != 8:
                        token = 8
                    elif line.rstrip() in ends:
                        token = 0


                if line.rstrip() == '<mi>' or token == 9:
                    mimc.append(line)
                    if token != 9:
                        token = 9
                    elif line.rstrip() in ends:
                        token = 0

    ends = ['<ba>', '<we>', '<ed>', '<ca>', '<ex>', '<sk>', '<pr>', '<su>', '<mi>','</ba>', '</we>', '</ed>', '</ca>', '</ex>', '</sk>', '</pr>', '</su>', '</mi>']
    for c, output in enumerate(segments):
        with open(output_path+segments_label[c]+'.txt', 'wb') as f:
            for line in output:
                if line.rstrip() not in ends:
                    f.write(line)
    return 0

def generate_level_segment(dir_path):
    '''
    this funtion take all job title dir and combine to form level segment
    NOTE - delete all file if already exist beacuse it will not overwrite
    :param fname: path of level dir
    :return: generate segments file for level
    '''
    # select only dir not file
    dirlist = os.walk(dir_path).next()[1]
    for dir in dirlist:
        innerdir_list = os.listdir(dir_path+dir)
        for innerdir in innerdir_list:
            with open(dir_path+dir+'/'+innerdir, 'r') as f:
                contents = f.read()
            with open(dir_path+innerdir, 'a') as f:
                f.write(contents)
    return 0

def upgrade_level1(level0_dir_path = '/home/sumit/PycharmProjects/ResumeParser/Data/resume_segments/Level0/',
                   level1_dir_path='/home/sumit/PycharmProjects/ResumeParser/Data/resume_segments/Level1/'):
    '''
    this funtion upgrade level0 to level1
    :return:
    '''
    level0_dir_list = os.walk(level0_dir_path).next()[1]
    level0_files_list = os.walk(level0_dir_path).next()[2]

    level1_dir_list = os.walk(level0_dir_path).next()[1]
    for directory in level0_dir_list:
        for files in level0_files_list:
            data = open(level0_dir_path + directory + '/' + files, 'r').read()
            data = re.sub('[^A-Za-z0-9 \n.]+', ' ', data)
            data = list(data)
            pop_index = []
            for char in range(len(data)):
                if data[char] == '\n':
                    count = char + 1
                    if count < len(data) - 5:
                        while (not data[count].isalpha()):
                            pop_index.append(count)
                            count += 1
            count = 0
            for x in pop_index:
                x = x - count
                data.pop(x)
                count += 1
            for char in range(len(data)):
                if data[char] == '.':
                    if data[char + 1] == ' ':
                        data[char + 1] = '\n'
            for char in range(len(data) - 1):
                if data[char] == '\n':
                    if not data[char + 1].isupper():
                        data[char] = ' '
            data = "".join(data)
            data = re.sub('[^A-Za-z0-9 \n]+', '', data)
            data_lines = data.split('\n')
            new_data = []
            for line in data_lines:
                words = line.split()
                if len(words) >= 46:
                    for x in range(len(words) / 45):
                        words[(x + 1) * 45] = '\n'
                words.append('\n')
                new_data.append(" ".join(words))
            new_data = "".join(new_data)
            with open(level1_dir_path + directory + '/' + files, 'w') as f:
                f.write(new_data)



if __name__ =="__main__":
    #generate_level0_title_segments('../Data/resume_samples/txts/fresher/', '../Data/resume_segments/Level0/fresher/')
    generate_level_segment('/home/sumit/PycharmProjects/ResumeParser/Data/resume_segments/Level0/')
