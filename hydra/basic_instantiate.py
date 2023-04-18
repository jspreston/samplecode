from dataclasses import dataclass

import hydra
from hydra.utils import instantiate
from omegaconf import MISSING


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
    def __init__(self, param1: AbstractTypeA, param2: int):
        self.param1 = param1
        self.param2 = param2

@dataclass
class AbstractTypeAConfig:
    param1: str = MISSING
    param2: int = 1

@dataclass
class TypeA1Config(AbstractTypeAConfig):
    _target_: str = "basic_instantiate.TypeA1"
    param1: str = "param1"
    param2: int = 2

@dataclass
class TypeA2Config(AbstractTypeAConfig):
    _target_: str = "basic_instantiate.TypeA2"
    param1: str = "param1"
    param2: int = 2
    param3: float = 3.0

# this class uses an AbstractTypeA, can be TypeA1 or TypeA2
@dataclass
class TypeBConfig:
    _target_: str = "basic_instantiate.TypeB"
    param1: AbstractTypeAConfig = MISSING
    param2: int = 3

# reads the config from conf/config.yaml
@hydra.main(config_path="conf", config_name="config", version_base="1.3")
def my_app(cfg: TypeBConfig) -> None:
    the_ob: TypeB = instantiate(cfg)
    print(type(the_ob))
    print(vars(the_ob))
    print(type(the_ob.param1))
    print(vars(the_ob.param1))

if __name__ == "__main__":
    my_app()