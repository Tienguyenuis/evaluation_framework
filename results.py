import os
import json
import csv

def resultslp_to_list():
    all_datasets = os.listdir('/home/congttn/badne/data/')
    #Open file and copy lines
    with open('/home/congttn/badne/embeddings/LP/lp-results.txt', 'r') as f:
        raw_data = [line.strip() for line in f]

    output = []
    #Identify where the relevant data lies in each line from the file and filter out duplicates
    for i in (range(len(raw_data))):
        replace = raw_data[i].replace('_train_0.5.embeddings-', " ")
        replaced = replace.replace('_train_0.6.embeddings-', " ")
        line = replaced.split()
        if "F=" in line[2]:
            line.insert(2, "")
        compare = [' ', ' ', ' ', ' ', ' ']
        for dataset in all_datasets:
            if "-" + dataset in line[1]:
                split = line[1].split("-" + dataset)
                try:
                    compare[0] = split[0]
                    compare[1] = dataset
                    compare[2] = line[2]
                    compare[3] = line[3]
                    compare[4] = line[4]
                except:
                    pass
                if compare not in output:
                    output.append(compare)
                    break
         
    return output


def listlp_to_json():
    #convert list of lists to dict of dicts
    result = resultslp_to_list()
    new_dict = {}
    for i in range(len(result)):
        new_dict[i]= {
                'method':'met',
                'dataset':'data',
                'size':'size',
                'F':'f',
                'score':'score'
                }
        new_dict[i]['method'] = result[i][0]
        new_dict[i]['dataset'] = result[i][1] 
        new_dict[i]['size'] = result[i][2] 
        new_dict[i]['F'] = result[i][3] 
        new_dict[i]['score'] = result[i][4]

    with open('/home/congttn/badne/web/json_files/resultlp.json', 'w') as fp: 
        json.dump(new_dict, fp)
    
    return new_dict


def resultsnc_to_list():
    all_datasets = os.listdir('/home/congttn/badne/data/')
    output = []
    #Open the tsv file and append each row to a list
    with open('/home/congttn/badne/embeddings/NC/nc-results.tsv', 'r') as fd:
        rd = csv.reader(fd, delimiter="\t")
        for row in rd:
            metdata_size = str(row[1]).replace('-edgelist.txt.embeddings-', " ")
            #Use the lists to identify relevant data for each line.
            compare = [' ', ' ', ' ', ' ']
            for dataset in all_datasets:
                if "-" + dataset in row[1]:
                    find_method = str(metdata_size).split("-" + dataset)
                    if "-edgelist.txt" in find_method[1]:
                        find_method[1] = ""
                    compare[0] = find_method[0]
                    compare[1] = dataset
                    compare[2] = find_method[1]
                    compare[3] = row[2]
                    if compare not in output:
                        output.append(compare)
                        break
    return output


def listnc_to_json():
    #Scores for node classification are stored as 'max&min' in the same table entry, so they are separated:
    result = resultsnc_to_list()
    split_minmax = []
    for row in result:
        find_max_min = row[3].replace("&", " ")
        found_max_min = find_max_min.split()
        data = [row[0], row[1], row[2], found_max_min[0], found_max_min[1]]
        split_minmax.append(data)
    
    #Same approach as converting to json for link prediction
    new_dict = {}
    for i in range(len(split_minmax)):
        new_dict[i]={
                'method':'met',
                'dataset':'data',
                'size':'size',
                'macro':'macro',
                'micro':'micro'
                }
        new_dict[i]['method'] = split_minmax[i][0]
        new_dict[i]['dataset'] = split_minmax[i][1]
        new_dict[i]['size'] = split_minmax[i][2].strip()
        new_dict[i]['macro'] = split_minmax[i][3]
        new_dict[i]['micro'] = split_minmax[i][4]

    with open('/home/congttn/badne/web/json_files/resultnc.json', 'w') as fp:
            json.dump(new_dict, fp)

    return new_dict

