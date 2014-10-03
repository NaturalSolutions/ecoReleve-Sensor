:: ecoReleve-Sensor installation script
:: Requires Python 3.4.1, conda and conda-build

conda install pandas
conda install pyodbc
conda install reportlab
conda install scikit-learn
conda install sqlalchemy
conda install zope.interface

python setup.py install