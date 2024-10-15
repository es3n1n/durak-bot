from pydantic_settings import BaseSettings, SettingsConfigDict

from durak_bot.util.fs import ROOT_DIR


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    ENVIRONMENT: str = 'production'

    BOT_TOKEN: str

    @property
    def is_dev_env(self) -> bool:
        return 'dev' in self.ENVIRONMENT.lower()


config = Settings()  # type: ignore[call-arg]
