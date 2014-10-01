:: ecoReleve-Sensor installation script
:: Requires Python 3.4.1, conda and conda-build

conda install sqlalchemy

conda install zope.interface

conda skeleton pypi transaction
conda build transaction
conda install --use-local transaction

conda skeleton pypi zope.deprecation
conda build zope.deprecation
conda install --use-local zope.deprecation

conda skeleton pypi zope.sqlalchemy
conda build zope.sqlalchemy
conda install --use-local zope.sqlalchemy

conda skeleton pypi waitress
conda build waitress
conda install --use-local waitress

conda skeleton pypi translationstring
conda build translationstring
conda install --use-local translationstring

conda install -c https://conda.binstar.org/Trentonoliphant pyramid_tm

conda build ecorelevesensor
conda install --use-local ecorelevesensor