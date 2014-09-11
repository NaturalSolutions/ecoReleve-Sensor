import numpy as np
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Numeric, DateTime
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from math import pow
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import normalize

def periodic_behaviour(connection, id):
   return True

def load_data(id):
   engine = create_engine('mssql+pyodbc://eReleveApplication:123456@.\\SQLSERVER2008/ecoReleve_Data')
   metadata = MetaData()
   V_Individuals_LatLonDate = Table('V_Individuals_LatLonDate', metadata,
      Column('ind_id', Integer),
      Column('lat', Numeric),
      Column('lon', Numeric),
      Column('date', DateTime)
   )
   metadata.create_all(engine)
   data = engine.execute(V_Individuals_LatLonDate.select().where(V_Individuals_LatLonDate.c['ind_id'] == id)).fetchall()
   return np.array([(row['lon'], row['lat']) for row in data], dtype=float)


def compute_density(X, grid, extent):
   n = X.shape[1] 
   x_min, x_max, y_min, y_max = extent
   var_x, var_y = np.var(X, axis = 0)
   gamma2 = .25 * (var_x + var_y) * pow(n, -1./3)
   factor = 1./(2*n*np.pi*gamma2)
   nb_x, nb_y = grid   
   X_norm_2 = np.square(X).sum(axis = 1)
   xx, yy = np.meshgrid(np.linspace(x_min, x_max, nb_x), np.linspace(y_min, y_max, nb_y))
   centers = np.vstack([xx.ravel(), yy.ravel()]).T
   dist = euclidean_distances(X, centers, (centers**2).sum(axis = 1), squared = True)
   density = factor * np.exp(-dist/(2.*gamma2)).sum(axis = 0).reshape((nb_y, nb_x))
   return density

if  __name__ == '__main__':
   id = 5263
   X = load_data(id)
   x_min, x_max = X[:,0].min(), X[:,0].max()
   y_min, y_max = X[:,1].min(), X[:,1].max()
   db = DBSCAN(eps=0.01, min_samples=100)
   density = db.fit(X)
   core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
   core_samples_mask[db.core_sample_indices_] = True
   labels = db.labels_
   unique_labels = set(labels)
   colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
   for k, col in zip(unique_labels, colors):
      if k == -1:
        # Black used for noise.
        col = 'w'
      else:
         class_member_mask = (labels == k)
         xy = X[class_member_mask & core_samples_mask]
         plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)

         xy = X[class_member_mask & ~core_samples_mask]
         plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=6)
   """
   X = normalize(X)
   density = compute_density(X, (250, 250), (x_min, x_max, y_min, y_max))
   plt.figure()
   plt.imshow(density, cmap='hot', origin='lower', extent=(x_min, x_max, y_min, y_max))
   plt.colorbar()
   """
   plt.show()
