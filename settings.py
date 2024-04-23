from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    token: str
    adm_id: int


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            token=env.str("TOKEN"),
            adm_id=env.int("ADM_ID")
        )
    )


def settings_all():
    return get_settings('input')
