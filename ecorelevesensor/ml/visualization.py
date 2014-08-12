import numpy as np
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Numeric, DateTime
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from math import pow

def periodic_behaviour(connection, id):
   return True

if  __name__ == '__main__':
   engine = create_engine('mssql+pyodbc://eReleveApplication:123456@serveur2008\\SQLSERVER2008/ecoReleve_Data', echo=True)
   metadata = MetaData()
   V_Individuals_LatLonDate = Table('V_Individuals_LatLonDate', metadata,
      Column('indID', Integer),
      Column('lat', Numeric),
      Column('lon', Numeric),
      Column('date', DateTime)
   )
   metadata.create_all(engine)
   data = engine.execute(V_Individuals_LatLonDate.select().where(V_Individuals_LatLonDate.c.indID == 62559)).fetchall()
   X = np.array([(row['lon'], row['lat']) for row in data], dtype=float)
   n = X.shape[1]
   x_min, x_max = X[:,0].min(), X[:,0].max()
   y_min, y_max = X[:,1].min(), X[:,1].max()
   var_x, var_y = np.var(X, axis = 0)
   gamma2 = .25 * (var_x + var_y) * pow(n, -1./3)
   nb_x, nb_y = 100, 100
   density = np.zeros((nb_y, nb_x), dtype=float)
   x_values = np.linspace(x_min, x_max, nb_x)
   y_values = np.linspace(y_min, y_max, nb_y)
   for i in range( x_values.size ):
      x = x_values[i]
      for j in range( y_values.size ):
         y = y_values[j]
         c = np.array((x,y))
         dist2 = np.square(X - c).sum(axis = 1)
         density[j, i] = 1./(2*n*np.pi*gamma2) * np.exp(-dist2/(2.*gamma2)).sum()
   print np.mean(X, axis=0)
   clf = KMeans()
   clf.fit(X)
   plt.figure()
   plt.scatter(clf.cluster_centers_[:,0], clf.cluster_centers_[:,1])
   plt.figure()
   plt.imshow(density, cmap='hot', origin='lower', extent=(x_min, x_max, y_min, y_max))
   plt.show()