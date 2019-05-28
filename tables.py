import json
from pprint import pprint
import os


undirected_data = ['BlogCatalog', 'Youtube-labelled', 'Reddit', 'dblp-coauthor', 'Flickr-labelled']
directed_data = ['Cora', 'Twitter', 'dblp-cite', 'Epinions']
nc_data = ['BlogCatalog', 'PubMed', 'Cora', 'Reddit', 'Flickr-labelled', 'Youtube', 'CoCit']

undirected_restricted= ["HOPE"]
directed_restricted = ["NetMF"]
nc_restricted = []

undirected_sizes = ["small.npy", "128.tgt", "", "p1-q1.embeddings"]
directed_sizes = ["128.src", "large.npy", "", "p1-q1.embeddings"]
nc_sizes = ["64.tgt", "large.npy", "", "p1-q1.embeddings"]

all_datasets = os.listdir('/home/congttn/badne/data/')
all_methods = os.listdir('/home/congttn/badne/code/methods/')

def filter_methods(restricted):
    methods = all_methods
    for restrict in restricted:
        try:
            methods.remove(restrict)
        except:
            pass
    
    return methods


def format_undirectedlp(methods, datasets, size):
    with open('/home/congttn/badne/web/json_files/resultlp.json') as f:
        data = json.load(f)

    the_dict = {}
    #Create empty values for all method-dataset combination
    for method in methods:
        for dataset in datasets:
            the_dict[method + "_" + dataset] = ""


    for i in range(len(data)):
        try:
            method_data = data[str(i)]['method'] + "_" + data[str(i)]['dataset']
            if data[str(i)]['size'] in size and data[str(i)]['dataset'] in datasets:
                the_dict[method_data] = data[str(i)]['score']
        except:
            pass
    return the_dict

def format_directedlp(methods, datasets, size):
    with open('/home/congttn/badne/web/json_files/resultlp.json') as f:
        data = json.load(f)
    the_dict = {}
    #Create empty values for all method-dataset combination
    for method in methods:
        for dataset in datasets:
            the_dict[method + "_" + dataset] = ""


    for i in range(len(data)):
        try:
            method_data = data[str(i)]['method'] + "_" + data[str(i)]['dataset']
            if data[str(i)]['size'] in size and data[str(i)]['dataset'] in datasets:
                if not the_dict[method_data]:
                    the_dict[method_data] = {
                        'F=0.0':' ',
                        'F=0.5':' ',
                        'F=1.0':' '
                    }
                if data[str(i)]['F'] == 'F=0.0':
                    the_dict[method_data]['F=0.0'] = data[str(i)]['score']
                elif data[str(i)]['F'] == 'F=0.5':
                    the_dict[method_data]['F=0.5'] = data[str(i)]['score']
                elif data[str(i)]['F'] == 'F=1.0':
                    the_dict[method_data]['F=1.0'] = data[str(i)]['score']
        except:
            pass
    return the_dict


def format_entriesnc(methods, datasets, size):
    with open('/home/congttn/badne/web/json_files/resultnc.json') as f:
        data = json.load(f)

    the_dict = {}
    #Create empty values for all method-dataset combination
    for method in methods:
        for dataset in datasets:
            the_dict[method + "_" + dataset] = ""
    
    for i in range(len(data)):
        try:
            method_data = data[str(i)]['method'] + "_" + data[str(i)]['dataset']
            if data[str(i)]['size'] in size and data[str(i)]['dataset'] in datasets:
                the_dict[method_data] = [data[str(i)]['macro'], data[str(i)]['micro']]
        except:
            pass
    return the_dict


def undirected_resultslp():
    data = format_undirectedlp(all_methods, undirected_data, undirected_sizes)
    undirected_score = []
    undirected_methods = filter_methods(undirected_restricted)
    for i in range(len(undirected_methods)):
        row = []
        row.append(undirected_methods[i])
        for dat_met, value in data.items():
            if undirected_methods[i] + "_" in dat_met:
                row.append(value)

        undirected_score.append(row)
    return undirected_score


def directed_resultslp():
    data = format_directedlp(all_methods, directed_data, directed_sizes)
    directed_score = []
    directed_methods = filter_methods(directed_restricted)
    for i in range(len(directed_methods)):
        row = []
        row.append(directed_methods[i])
        for dat_met, value in data.items():
            if directed_methods[i] + "_" in dat_met:
                try:
                    row.append(value['F=0.0'])
                    row.append(value['F=0.5'])
                    row.append(value['F=1.0'])
                except:
                    row.append("")
                    row.append("")
                    row.append("")
        directed_score.append(row)
    return directed_score


def resultsnc():
    data = format_entriesnc(all_methods, nc_data, nc_sizes)
    nc_score = []
    nc_methods = filter_methods(nc_restricted)
    for i in range(len(nc_methods)):
        row = []
        row.append(nc_methods[i])
        for dat_met, value in data.items():
            if nc_methods[i] + "_" in dat_met:
                try:
                    row.append(value[0])
                    row.append(value[1])
                except:
                    row.append("")
                    row.append("")
        nc_score.append(row)
    
    return nc_score

