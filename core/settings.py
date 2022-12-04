from functools import cached_property

from pydantic import BaseSettings

from framework.utils.constants import Duration


class Settings(BaseSettings):
    POSTGRES_RW_DNS: str
    POSTGRES_RO_DNS: str
    POSTGRES_PASSWORD_SECRET: str

    JWT_SECRET: str
    JWT_ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_SECONDS: int = Duration.DAY
    REFRESH_TOKEN_EXPIRE_SECONDS: int = Duration.MONTH

    @cached_property
    def postgres_full_rw_dns(self):
        """Read and write dns include password."""
        return self.__add_password_to_dns(self.POSTGRES_RW_DNS, self.POSTGRES_PASSWORD_SECRET)

    @cached_property
    def postgres_full_ro_dns(self):
        """Read only dns include password."""
        return self.__add_password_to_dns(self.POSTGRES_RO_DNS, self.POSTGRES_PASSWORD_SECRET)

    @staticmethod
    def __add_password_to_dns(dns: str, password: str):
        """Add password to dns without password."""
        dns_parts = dns.split('@')
        return f'{dns_parts[0]}:{password}{dns_parts[1]}'


settings = Settings()
