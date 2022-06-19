class Config(object):

    DEBUG = False
    TESTING = False

class DevConfig(Config):

    DATABASE_URI = 'dev_db.json'
    DEBUG = True

class ProdConfig(Config):

    DATABASE_URI = 'prod_db.json'    

class TestConfig(Config):

    DATABASE_URI = 'test_db.json'
    TESTING = True


config = {
    'development': DevConfig,
    'production': ProdConfig,
    'testing': TestConfig
}