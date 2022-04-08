# This Code was written with reference to the content covered in UBC's CPSC 340 Course

import numpy as np

class OutlierDetection:
    # Initial data is expected to be an nx2 numpy array, where n is the length of initial data
    # and for some point i, initial_data[i,0] is the time  and initial_data[i,1] is the day
    def __init__(self, num_neighbors, max_ratio, min_data_len, max_data_len, initial_data=None):

        assert(min_data_len > num_neighbors)
        
        self.num_neighbors = num_neighbors
        self.max_ratio = max_ratio
        self.min_data_len = min_data_len
        self.max_data_len = max_data_len
        if initial_data is None:
            self.data = np.array([[]])
        else:
            self.data = initial_data
    # Add point as a 1x2 numpy array - it must be a two dimensional array!
    # Returns true if the point is an outlier
    def add(self, point, debug=False):

        if len(self.data) < self.min_data_len:
            #We don't have enough data to make determine any outlier behaviour
            self.data = np.append(self.data, point, axis=0)
            return False
        distances = np.linalg.norm(self.data - point, axis=1)
        nearest_points = np.argsort(distances)[:self.num_neighbors]
        avg_distance = np.sum(distances[nearest_points])/self.num_neighbors
        if debug:
            print("---(new add)---")
            print("point added: ", point)
            print("average distance: ", avg_distance)
            print("nearest points: ", self.data[nearest_points])
        nbor_avg_distance = 0
        
        for index in nearest_points:
            n_point = self.data[index]
            data = np.delete(self.data, index, axis=0)
            nbor_avg_distance += np.sum(np.sort(np.linalg.norm(data - n_point, axis=1))[:self.num_neighbors])/self.num_neighbors
            if debug:
                print("---")
                print("     Neighboring Point")
                print("     Index: ", index)
                print("     Neighbours: ", data[np.argsort(np.linalg.norm(data - n_point, axis=1))[:self.num_neighbors]])
                print("     Distances: ", np.sort(np.linalg.norm(data - n_point, axis=1))[:self.num_neighbors])
                print("     Print Curr Avg Dist: ", nbor_avg_distance)
                print("---")
        if (len(self.data) == self.max_data_len):
            self.data = np.delete(self.data, 0, axis=0)
        self.data = np.append(self.data, point, axis=0)
        if debug:
            print("Ratio: ", avg_distance/nbor_avg_distance)
            print("---(end add)---")
        return avg_distance/nbor_avg_distance > self.max_ratio