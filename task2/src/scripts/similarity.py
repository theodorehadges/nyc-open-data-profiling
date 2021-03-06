import re
import csv
import numpy as np
import scipy
import pandas as pd
import json
import math
from scipy.cluster.hierarchy import linkage, fcluster
from nltk.util import ngrams
from collections import Counter
#from similarity import *

# set ngrams here
NGRAMS = 3


# note: cosine similarity function is from:
# https://gist.github.com/gaulinmp/da5825de975ed0ea6a24186434c24fe4
def cosine_similarity_ngrams(a, b):
    vec1 = Counter(a)
    vec2 = Counter(b)
    
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    return float(numerator) / denominator

def compute_jaccard_similarity(s1, s2):
    numerator = len(set(s1).intersection(set(s2)))
    denominator = len(set(s1).union(set(s2)))
    if denominator is 0:
        return(0.0)
    return(numerator/denominator)

def write_to_json(cluster_id_dic):
    with open('../../resources/filename_clusters.json', 'w') as fp:
        json.dump(cluster_id_dic, fp, sort_keys=True, indent=4)

def write_list_to_txt(file_list, dest_filename):
    with open('../../resources/'+dest_filename, 'w') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow(file_list)

def write_matrix_to_csv(M):
    np.savetxt('../../resources/filename_similarity_matrix.csv', M, delimiter=',')

def clean_string(s):
    s = s.lower()
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
    return(s)

def get_ngram_list_from_string(s):
    clean_s = clean_string(s)
    tokens = [token for token in s]
    output = list(ngrams(tokens, NGRAMS)) 
    return(output)

if __name__ == "__main__":

    filelist = "../cluster3.txt"
    
    with open(filelist, 'r') as f:
        raw_list = f.read().split(",")

    raw_list = raw_list = [re.sub("\[|\]|\'|\'|" "", "", item)for item in raw_list]
    raw_list = [re.sub(" " "", "", item)for item in raw_list] 
    
    raw_list = list(set(raw_list)) # remove duplicate filenames 
   
    clean_list = [x.split(".")[1] for x in raw_list] 
    clean_list = [re.sub("_", "", item)for item in raw_list] 


    # Use this small sample set for sanity check
    #test_list = ["hello", "hi", "cool", "school"]
    #axis_len = len(test_list)
    
    axis_len = len(clean_list)
    M = np.empty((axis_len, axis_len)) # init an empty matrix 
        
    for i, name_x in enumerate(clean_list):
        for j, name_y in enumerate(clean_list):
            a = get_ngram_list_from_string(name_x)
            b = get_ngram_list_from_string(name_y)

            #M[i][j] = compute_jaccard_similarity(a, b)
            M[i][j] = cosine_similarity_ngrams(a, b)


    linkage_matrix = scipy.cluster.hierarchy.linkage(M)
    fcluster = fcluster(linkage_matrix, t=0.9)

    cluster_id_dic = {'cluster'+str(x): [] for x in fcluster}

    df = pd.DataFrame()
    df['filename'] = raw_list
    df['cluster_id'] = fcluster

    for index, row in df.iterrows():
        cluster_id_dic['cluster'+str(row['cluster_id'])].append(row['filename'])

    # Areas of study (interests) filelist to text file
    aos_filelist = []
    for filename in cluster_id_dic['cluster7']:
        aos_filelist.append(filename)
    write_list_to_txt(aos_filelist, 'area_of_study_filelist')

    # Parks and playgrounds file list to text file
    park_playground_filelist = []
    for filename in cluster_id_dic['cluster35']:
        park_playground_filelist.append(filename)
    write_list_to_txt(park_playground_filelist, 'park_playground_filelist')

    # Agency file list to text file
    agency_filelist = []
    for filename in cluster_id_dic['cluster11']:
        agency_filelist.append(filename)
    for filename in cluster_id_dic['cluster32']:
        agency_filelist.append(filename)
    write_list_to_txt(agency_filelist, 'agency_filelist')


    # Neighborhood file list to text file
    neighborhood_filelist = []
    for filename in cluster_id_dic['cluster5']:
        neighborhood_filelist.append(filename)
    for filename in cluster_id_dic['cluster62']:
        neighborhood_filelist.append(filename)
    for filename in cluster_id_dic['cluster63']:
        neighborhood_filelist.append(filename)
    write_list_to_txt(neighborhood_filelist, 'neighborhood_filelist')

    # Location type file list to text file
    location_type_filelist = []
    for filename in cluster_id_dic['cluster42']:
        if 'PREM' in filename:
            location_type_filelist.append(filename)
    write_list_to_txt(location_type_filelist, 'location_type_filelist')


    # 15 22 26
    # School name (sn) type file list to text file
    sn_filelist = []
    for filename in cluster_id_dic['cluster15']:
        sn_filelist.append(filename)
    for filename in cluster_id_dic['cluster22']:
        sn_filelist.append(filename)
    for filename in cluster_id_dic['cluster26']:
        sn_filelist.append(filename)
    write_list_to_txt(sn_filelist, 'school_name_type_filelist')


    # 1 2 3 4
    # School subject (ss) type file list to text file
    ss_filelist = []
    for filename in cluster_id_dic['cluster1']:
        ss_filelist.append(filename)
    for filename in cluster_id_dic['cluster2']:
        ss_filelist.append(filename)
    for filename in cluster_id_dic['cluster3']:
        ss_filelist.append(filename)
    for filename in cluster_id_dic['cluster4']:
        ss_filelist.append(filename)
    write_list_to_txt(ss_filelist, 'school_subject_type_filelist')


    
    # write cluster dic to json
    write_to_json(cluster_id_dic)

    # write similarity matrix to csv
    write_matrix_to_csv(M)

    # write file list to text file (the list represents the axes of the sim matrix)
    write_list_to_txt(clean_list, 'filelist_axis_sim_matrix')

