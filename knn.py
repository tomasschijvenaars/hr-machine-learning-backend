import numpy as np

class KNN:
  # Function to compute Euclidean distance between two points
  def compute_distance(self, sollicitant, data_point):
      return np.linalg.norm(np.array(sollicitant) - np.array(data_point))

  # Function to find the k nearest neighbors
  def find_k_nearest_neighbors(self, hasjob_data, sollicitant, k):
      distances = []
      for data_point in hasjob_data:
          distance = self.compute_distance(sollicitant, data_point[:-1])
          distances.append((data_point, distance))
      distances.sort(key=lambda x: x[1])
      neighbors = [distances[i][0] for i in range(k)]
      return neighbors

  #Hoofdfunctie voor het calculeren van de KNN, KNN staat op 3
  def classify_point(self, hasjob_data, sollicitant):
      neighbors = self.find_k_nearest_neighbors(hasjob_data, sollicitant, 3)
      labels = [neighbor[-1] for neighbor in neighbors]
      prediction = max(set(labels), key=labels.count)
      return prediction, neighbors

  # Main execution block
  if __name__ == "__main__":
      # Dataset moet uit de database komen. Deze dataset moet aangevult kunnen worden met een [70, 70, 1]
      data = [
          [80, 85, 1],
          [90, 90, 1],
          [80, 80, 1],
          [40, 40, 0],
          [45, 40, 0]
      ]

      # Parameters
      k = 3  #Number of neighbors
      new_point = [60, 60]  #New data point to classify

      # Prediction
      predicted_label, nearest_neighbors = classify_point(data, new_point)

      print(f'Data={new_point}, Predicted: {predicted_label}')
