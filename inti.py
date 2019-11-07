# Kelompok : Kusuma Istimewa
# Nama / NIM :
# 1. Felix Setiawan / 13518078
# 2. Fakhrurrida Clarendia Widodo / 13518091
# 3. Stefanus Gusega Gunawan / 13518149

import cv2
import numpy as np
import scipy
from scipy.misc import imread
import pickle
import random
import os
import matplotlib.pyplot as plt

# Feature extractor
def extract_features(image_path, vector_size=32):
    image = imread(image_path, mode="RGB")
    try:
        # Using KAZE, cause SIFT, ORB and other was moved to additional module
        # which is adding addtional pain during install
        alg = cv2.AKAZE_create()
        # Dinding image keypoints
        kps = alg.detect(image)
        # Getting first 32 of them. 
        # Number of keypoints is varies depend on image size and color pallet
        # Sorting them based on keypoint response value(bigger Istimewa better)
        kps = sorted(kps, key=lambda x: -x.response)[:vector_size]
        # computing descriptors vector
        kps, dsc = alg.compute(image, kps)
        # Flatten all of them in one big vector - our feature vector
        dsc = dsc.flatten()
        # Making descriptor of same size
        # Descriptor vector size is 64
        needed_size = (vector_size * 64)
        if dsc.size < needed_size:
            # if we have less the 32 descriptors then just adding zeros at the
            # end of our feature vector
            dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])
    except cv2.error as e:
        print ('Error: ', e)
        return None

    return dsc


def batch_extractor(images_path, pickled_db_path="features.pck"):
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]

    result = {}
    for f in files:
        print ('Extracting features from image %s' % f)
        name = f.split('/')[-1].lower()
        result[name] = extract_features(f)
    
    # saving all our feature vectors in pickled file
    with open(pickled_db_path, 'wb') as fp:
        pickle.dump(result, fp)

class Matcher(object):

    def __init__(self, pickled_db_path="features.pck"):
        with open(pickled_db_path, 'rb') as fp:
            self.data = pickle.load(fp)
        self.names = []
        self.matrix = []
        self.number_of_photos = 0
        for k, v in self.data.items():
            self.names.append(k)
            self.matrix.append(v)
            self.number_of_photos += 1
        self.matrix = np.array(self.matrix)
        self.names = np.array(self.names)

    def cos_cdist(self, vector):
        # getting cosine similarity between query image and images database
        # determining whether database vector and query vector
        v_database = self.matrix # length(v_database) = banyak data, dimensi matriks 86x2048
        v_query = vector # length(v_query) = 2048
        dot_product = [0 for n in range(self.number_of_photos)]
        dist_query = 0
        dist_db = [0 for n in range(self.number_of_photos)]
        dist = [0 for n in range(self.number_of_photos)]
        final = [0 for z in range(self.number_of_photos)]
        # pengisian array dot_product dan array dist_db (|y| untuk vektor y)
        for i in range(self.number_of_photos) :
            for j in range(2048) :
                dot_product[i] += ((v_query[j])*(v_database[i][j]))
                dist_db[i] += ((v_database[i][j])**2)
            dist_db[i] = (dist_db[i])**(1/2)
        # pengisian array dist_query (|x| untuk vektor x)
        for l in range(2048) :
            dist_query += ((v_query[l])**2)
        dist_query = (dist_query)**(1/2)
        # pengisian array dist (|x| * |y| untuk dua vektor x dan y) dan array final
        for o in range(self.number_of_photos) :
            dist[o] = dist_query*dist_db[o]
            final[o] = -dot_product[o]/dist[o] # make it negative so we can sort them ascending
        return final
    
    def euclid_dist(self, vector):
        # getting euclid distance between query image and images database
        # determining whether database vector and query vector
        v_database = self.matrix # length(v_database) = banyak data, dimensi matriks 86x2048
        v_query = vector # length(v_query) = 2048
        sum = [0 for n in range(self.number_of_photos)] # akan diisi oleh euclidean^2 dr setiap pencocokan
        squared = [0 for l in range(self.number_of_photos)] # akan terisi oleh euclidean dr setiap pencocokan (sudah diakar)
        # pengisian array sum
        for i in range(self.number_of_photos) :
            for j in range(2048) :
                sum[i] += (v_query[j]-v_database[i][j])**2
        # pengisian array squared
        for k in range(self.number_of_photos) :
            squared[k] = sum[k]**(1/2)
        return squared

    def match(self, image_path, topn):
        features = extract_features(image_path)
        img_distances = self.euclid_dist(features)  # bentuk list
        img_distances_arr = np.array(img_distances) # bentuk numpy array
        # getting top 5 records (tergantung sih mau ditampilin brp foto)
        nearest_ids = np.argsort(img_distances_arr)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()
        return nearest_img_paths, img_distances_arr[nearest_ids].tolist()

    def match2(self, image_path, topn=5): # matcher dengan metode cosine similarity
        features = extract_features(image_path)
        img_distances = self.cos_cdist(features)  # bentuk list
        img_distances_arr = np.array(img_distances) # bentuk numpy array
        # getting top 5 records (tergantung sih mau ditampilin brp foto)
        nearest_ids = np.argsort(img_distances_arr)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()
        return nearest_img_paths, img_distances_arr[nearest_ids].tolist()

def show_img(path):
    img = imread(path, mode="RGB")
    plt.imshow(img)
    plt.show()

def show_filename(path) :
    # to show the filename of path
    return os.path.basename(path)
    
def run_euclid(images_path_query, sumphotos):
    # database for checking
    images_path_database = r'C:\Users\MEGA LIS SETIYAWATI\Documents\evan\tugas\algeo\PINS\pins_Aaron Paul'   
    # extract all features of all database to features.pck 
    batch_extractor(images_path_database)
    ma = Matcher('features.pck')
    # mengembalikan array foto paling mirip dari yg paling mirip sampai yg paling tidak mirip
    # disimpan pada array names (berisi file path dari foto-foto)
    # menggunakan match (menggunakan Metode Euclidean)
    names, match = ma.match(images_path_query, sumphotos) 
    return names
def run_cosine(images_path_query,sumphotos):
    # database for checking
    images_path_database = r'C:\Users\MEGA LIS SETIYAWATI\Documents\evan\tugas\algeo\PINS\pins_Aaron Paul'
    # extract all features of all database to features.pck
    batch_extractor(images_path_database)
    ma = Matcher('features.pck')
    # mengembalikan array foto paling mirip dari yg paling mirip sampai yang paling tidak mirip
    # disimpan pada array names (berisi file path dari foto-foto)
    # menggunakan match2 (menggunakan Metode Cosine Similarity)
    names, match = ma.match2(images_path_query, sumphotos)
    return names

