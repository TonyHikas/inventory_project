from starlette.config import Config

from framework.utils.constants import Duration

config = Config('.env')

# Database config
DB_ADDRESS = config('DB_ADDRESS', cast=str, default='')
DB_USER = config('DB_USER', cast=str, default='')
DB_PASSWORD = config('DB_PASSWORD', cast=str, default='')
DB_PORT = config('DB_PORT', cast=str, default='')
DB_NAME = config('DB_NAME', cast=str, default='')
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}'

# JWT
JWT_SECRET = config('JWT_SECRET', cast=str, default='NMZIY4IAPqOTH3T3T-YF37DLBfVPfN_QgzKkrt0y9Zk')
JWT_ALGORITHM = config('JWT_ALGORITHM', cast=str, default='HS256')
ACCESS_TOKEN_EXPIRE_SECONDS = Duration.DAY
REFRESH_TOKEN_EXPIRE_SECONDS = Duration.MONTH

# Logging config
