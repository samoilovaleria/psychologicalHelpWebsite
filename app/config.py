class DatabaseConfig:
    HOST: str = "localhost"
    PORT: int = 5432
    USER: str = "admin"
    PASS: str = "pass"
    NAME: str = "polytech"

    @property
    def URI(self) -> str:
        return f"postgresql://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"
