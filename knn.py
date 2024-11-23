import numpy as np

class KNN:
  #Euclidean afstand tussen 2 punten
  def compute_distance(self, point1, point2):
      return np.linalg.norm(np.array(point1) - np.array(point2))

  #functie om KNN te vinden
  def find_k_nearest_neighbors(self, job_data, sollicitant, k):
      distances = []
      for data_point in job_data:
          distance = self.compute_distance(sollicitant, data_point[:-1])
          distances.append((data_point, distance))
      distances.sort(key=lambda x: x[1])
      neighbors = [distances[i][0] for i in range(k)]
      return neighbors

  #Hoofdfunctie voor het calculeren van de KNN, KNN staat op 3
  #job_data = array van de %vaardigheden, %ervaring en goed/slecht die mensen hadden wanneer ze aan een vacature werden gekoppeld.
  #sollicitant = array van %vaardigheden, %ervaring vergeleken met de huidige vacature
  def classify_point(self, job_data, sollicitant):
      neighbors = self.find_k_nearest_neighbors(job_data, sollicitant, 3)
      labels = [neighbor[-1] for neighbor in neighbors]
      prediction = max(set(labels), key=labels.count)
      return prediction