from pyramid.config import Configurator
from sqlalchemy import engine_from_config, create_engine

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    #engine = create_engine("mssql+pyodbc://eReleveApplication:123456@localhost\\SQLSERVER2008/ECWP_eReleve_Sensor?driver=SQL SERVER")
    print engine
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('weekData', '/weekData')
    config.scan()
    return config.make_wsgi_app()
