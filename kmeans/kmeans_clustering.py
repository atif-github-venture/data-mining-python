import numpy as np
import matplotlib.pyplot as plt, mpld3
from matplotlib import style
import pandas as pd
import matplotlib.pyplot as plt
import os

style.use('ggplot')
path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                    'data', 'input')


class K_Means:
    def __init__(self, k=3, tolerance=0.0001, max_iterations=500):
        self.k = k
        self.tolerance = tolerance
        self.max_iterations = max_iterations

    def fit(self, data):

        self.centroids = {}

        # initialize the centroids, the first 'k' elements in the dataset will be our initial centroids
        # for i in range(self.k):
        #     self.centroids[i] = data[i]

        # initial centroid by kmeans++
        con = 0
        for item in self.initial_centroids(data, self.k):
            self.centroids[con] = item
            con += 1

        # begin iterations
        for i in range(self.max_iterations):
            self.classes = {}
            for i in range(self.k):
                self.classes[i] = []

            # find the distance between the point and cluster; choose the nearest centroid
            for features in data:
                distances = [np.linalg.norm(features - self.centroids[centroid]) for centroid in self.centroids]
                classification = distances.index(min(distances))
                self.classes[classification].append(features)

            previous = dict(self.centroids)

            # average the cluster datapoints to re-calculate the centroids
            for classification in self.classes:
                self.centroids[classification] = np.average(self.classes[classification], axis=0)

            isOptimal = True

            for centroid in self.centroids:

                original_centroid = previous[centroid]
                curr = self.centroids[centroid]

                if np.sum((curr - original_centroid) / original_centroid * 100.0) > self.tolerance:
                    isOptimal = False

            # break out of the main loop if the results are optimal, ie. the centroids don't change their positions much(more than our tolerance)
            if isOptimal:
                break

    def pred(self, data):
        distances = [np.linalg.norm(data - self.centroids[centroid]) for centroid in self.centroids]
        classification = distances.index(min(distances))
        return classification

    def initial_centroids(self, data, k):
        '''
        intialized the centroids for K-means++
        inputs:
            data - numpy array of data points having shape (200, 2)
            k - number of clusters
        '''
        ## initialize the centroids list and add
        ## a randomly selected data point to the list
        centroids = []
        centroids.append(data[np.random.randint(
            data.shape[0]), :])
        self.plot(data, np.array(centroids))

        ## compute remaining k - 1 centroids
        for c_id in range(k - 1):

            ## initialize a list to store distances of data
            ## points from nearest centroid
            dist = []
            for i in range(data.shape[0]):
                point = data[i, :]
                import sys
                d = sys.maxsize

                ## compute distance of 'point' from each of the previously
                ## selected centroid and store the minimum distance
                for j in range(len(centroids)):
                    temp_dist = self.distance(point, centroids[j])
                    d = min(d, temp_dist)
                dist.append(d)

                ## select data point with maximum distance as our next centroid
            dist = np.array(dist)
            next_centroid = data[np.argmax(dist), :]
            centroids.append(next_centroid)
            dist = []
            self.plot(data, np.array(centroids))
        return centroids

    def plot(self, data, centroids):
        plt.scatter(data[:, 0], data[:, 1], marker='.',
                    color='gray', label='data points')
        plt.scatter(centroids[:-1, 0], centroids[:-1, 1],
                    color='black', label='previously selected centroids')
        plt.scatter(centroids[-1, 0], centroids[-1, 1],
                    color='red', label='next centroid')
        plt.title('Select % d th centroid' % (centroids.shape[0]))

        plt.legend()
        plt.xlim(-5, 12)
        plt.ylim(-10, 15)
        plt.show()

    # function to compute euclidean distance
    def distance(self, p1, p2):
        return np.sum((p1 - p2) ** 2)


def main():
    df = pd.read_csv(path + '/places.txt', usecols=['long', 'lat'])

    # df = df[['long', 'lat']]
    # dataset = df.astype(float).values.tolist()

    X = df.values  # returns a numpy array

    km = K_Means(3)
    km.fit(X)

    # Plotting starts here
    colors = 10 * ["r", "g", "c", "b", "k"]

    for centroid in km.centroids:
        plt.scatter(km.centroids[centroid][0], km.centroids[centroid][1], s=130, marker="x")

    for classification in km.classes:
        color = colors[classification]
        for features in km.classes[classification]:
            plt.scatter(features[0], features[1], color=color, s=30)

    counter = 0
    for item in X:
        print(str(counter) + ' ' + str(km.pred(item)))
        counter += 1

    plt.show()
    print('done')


if __name__ == "__main__":
    main()

# http://madhugnadig.com/articles/machine-learning/2017/03/04/implementing-k-means-clustering-from-scratch-in-python.html


# # using sklearn
#
# import pandas as pd
# from sklearn.cluster import KMeans
# data = pd.read_csv('data/places.txt',  usecols=['long', 'lat'])
#
# km = KMeans(3, init='k-means++')
# km.fit(data)
# c = km.predict(data)
#
# counter = 0
# for item in c:
#     print(str(counter) + ' ' + str(item))
#     counter += 1
# print('done')
