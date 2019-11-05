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
        alg = cv2.KAZE_create()
        # Dinding image keypoints
        kps = alg.detect(image)
        # Getting first 32 of them. 
        # Number of keypoints is varies depend on image size and color pallet
        # Sorting them based on keypoint response value(bigger is better)
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
        # getting cosine distance between search image and images database
        v = vector.reshape(1, -1)
        return scipy.spatial.distance.cdist(self.matrix, v, 'cosine').reshape(-1)
    
    def euclid_dist(self, vector):
        # getting euclid distance between query image and images database
        # determining whether database vector and query vector
        v_database = self.matrix # length(v_database) = banyak data, dimensi matriks 86x2048
        v_query = vector # length(v_query) = 2048
        # array of euclidean distance without square rooting
        sum = [0 for n in range(self.number_of_photos)]
        squared = [0 for l in range(self.number_of_photos)]
        # for query
        # counting euclidean distance without square rooting
        #for i in range(self.number_of_photos) :
         #   for j in range(2048) :
          #      euclid_dist_not_squared[j][i] += (v_query[j]-v_database[i][j])**2
        # summing all elmts without squaring root
        for i in range(self.number_of_photos) :
            for j in range(2048) :
                sum[i] += (v_query[j]-v_database[i][j])**2
        for k in range(self.number_of_photos) :
            squared[k] = sum[k]**(1/2)
        #for l in range(self.number_of_photos) :
         #   for m in range(2048) :
          #      sum[l] += euclid_dist_not_squared[m][l]
        # squaring root
        #squared = 0
        #for o in range(self.number_of_photos):
         #   squared += sum[o]
        return squared

    def match(self, image_path, topn=5):
        features = extract_features(image_path)
        img_distances = self.euclid_dist(features)
        img_distances_arr = np.array(img_distances)
        # getting top 5 records
        nearest_ids = np.argsort(img_distances_arr)[:topn]
        nearest_img_paths = self.names[nearest_ids].tolist()
        print(nearest_ids)
        return nearest_img_paths, img_distances_arr[nearest_ids].tolist()

def show_img(path):
    img = imread(path, mode="RGB")
    plt.imshow(img)
    plt.show()
    
def run():
    images_path_query = r'C:\Users\windows\Desktop\query_db\PINS\pins_query'
    images_path_database = r'C:\Users\windows\Desktop\query_db\PINS\pins_query'
    files = [os.path.join(images_path_query, p) for p in sorted(os.listdir(images_path_query))]
    # getting 3 random images 
    sample = random.sample(files, 1)
    
    #batch_extractor(images_path_database)

    ma = Matcher('features.pck')
    
    for s in sample:
        print ('Query image ==========================================')
        show_img(s)
        names, match = ma.match(s, topn=5)
        print ('Result images ========================================')
        for i in range(5):
            # we got the top less euclidean distance
            # so we show the real euclidean distance (without 1-)
            print ('Match %s' % (match[i]))
            show_img(os.path.join(images_path_database, names[i]))

run()