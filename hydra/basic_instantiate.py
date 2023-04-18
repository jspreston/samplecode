from dataclasses import dataclass

import hydra
from hydra.utils import instantiate
from omegaconf import MISSING, DictConfig


class AbstractTypeA:
    def __init__(self, param1: str, param2: int):
        self.param1 = param1
        self.param2 = param2

class TypeA1(AbstractTypeA):
    def __init__(self, param1: str, param2: int):
        super().__init__(param1, param2)

class TypeA2(AbstractTypeA):
    def __init__(self, param1: str, param2: int, param3: float):
        super().__init__(param1, param2)
        self.param3 = param3

class TypeB:
    def __init__(self, type_a: AbstractTypeA, an_int: int):
        self.type_a = type_a
        self.an_int = an_int

# reads the config from conf/config.yaml
@hydra.main(config_path="conf", config_name="config", version_base="1.3")
def my_app(cfg: DictConfig) -> None:
    print(f"Config type: {type(cfg)}")
    the_ob: TypeB = instantiate(cfg)
    print(f"{type(the_ob)} vs. {TypeB}")
    assert type(the_ob) is TypeB
    print(vars(the_ob))
    assert isinstance(the_ob.type_a, AbstractTypeA)
    print(vars(the_ob.type_a))

if __name__ == "__main__":
    my_app()