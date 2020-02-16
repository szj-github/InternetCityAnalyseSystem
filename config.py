DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'Mayuhao187,.'
HOST = 'cn-huaihuai.club'
PORT = '3306'
DATABASE = 'Job_DB'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False