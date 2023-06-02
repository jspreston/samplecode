from dataclasses import dataclass
import subprocess
from typing import List, Optional, Tuple
from textwrap import dedent

import os
import tempfile
import yaml


def _normalize_config_hierarchy(config_hierarchy: dict) -> dict:
    """Normalize the config hierarchy by removing indentation"""
    output = {}
    for key, value in config_hierarchy.items():
        if isinstance(value, str):
            output[key] = dedent(value)
        elif isinstance(value, dict):
            output[key] = _normalize_config_hierarchy(value)
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    return output


def _create_config_hierarchy(config_hierarchy: dict, parent_dir: str):
    """Create the directory structure specified in config_hierarchy within
    "parent_dir"."""
    for key, value in config_hierarchy.items():
        if isinstance(value, str):
            with open(os.path.join(parent_dir, key), "w") as f:
                f.write(value)
        elif isinstance(value, dict):
            new_dir = os.path.join(parent_dir, key)
            os.makedirs(new_dir, exist_ok=True)
            _create_config_hierarchy(value, new_dir)
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    return parent_dir


def _get_files(config_hierarchy: dict, cur_dir: str) -> List[Tuple[str, str]]:
    """Get a list of files and their contents from the config hierarchy."""
    files: List[Tuple[str, str]] = []
    for key, value in config_hierarchy.items():
        if isinstance(value, str):
            files.append((os.path.join(cur_dir, key), value))
        elif isinstance(value, dict):
            new_dir = os.path.join(cur_dir, key)
            files.extend(_get_files(value, new_dir))
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    return files


def _run_shell_command(cmd, cwd: Optional[str] = None) -> str:
    """Run a command in a shell and return the output as a string."""
    result = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd
    )

    # If the command returned a non-zero exit code, raise an error
    if result.returncode != 0:
        raise Exception(
            f"Command '{cmd}' failed with error code {result.returncode} and error"
            f" message '{result.stderr.decode('utf-8')}'"
        )

    return result.stdout.decode("utf-8").strip()


def _draw_hierarchy(config_hierarchy, prefix=""):
    result = ""

    items = list(config_hierarchy.items())
    for i, (key, value) in enumerate(items):
        is_last = i == len(items) - 1
        if isinstance(value, str):
            if is_last:
                result += f"{prefix}└── {key}\n"
            else:
                result += f"{prefix}├── {key}\n"
        elif isinstance(value, dict):
            if is_last:
                result += f"{prefix}└── {key}\n"
                result += _draw_hierarchy(value, prefix + "    ")
            else:
                result += f"{prefix}├── {key}\n"
                result += _draw_hierarchy(value, prefix + "│   ")
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    return result


DEFAULT_MAIN_FILE = """
import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg : DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
"""


MARKDOWN_FILE_FORMAT = """
**{file_name}**
```{file_type}
{file_contents}
```
"""


@dataclass
class ExHydraConfig:
    config_hierarchy: dict
    name: str = "Hydra Example"
    description: str = ""
    command_line_args: str = ""
    main_file: str = DEFAULT_MAIN_FILE
    main_file_name: str = "my_app.py"
    config_dir_name = "conf"
    _result: Optional[str] = None

    def __post_init__(self):
        self.config_hierarchy = _normalize_config_hierarchy(self.config_hierarchy)

    def _cmd(self):
        cmd = f"python {self.main_file_name}"
        if self.command_line_args:
            cmd += f" {self.command_line_args}"
        return cmd

    def _run(self):
        parent_dir = tempfile.mkdtemp()
        config_dir = os.path.join(parent_dir, self.config_dir_name)
        os.makedirs(config_dir, exist_ok=True)
        _create_config_hierarchy(self.config_hierarchy, config_dir)
        with open(os.path.join(parent_dir, self.main_file_name), "w") as f:
            f.write(self.main_file)
        cmd = self._cmd()
        result = _run_shell_command(cmd, cwd=parent_dir)
        self._result = result

    def draw_hierarchy(self) -> str:
        return _draw_hierarchy(self.config_hierarchy)

    def get_files(self) -> List[Tuple[str, str]]:
        return _get_files(self.config_hierarchy, self.config_dir_name)

    def to_markdown(self):
        if self._result is None:
            self._run()

        config_dir_diagram = self.draw_hierarchy()
        config_files = self.get_files()

        formatted_config_files = "\n\n".join(
            [
                MARKDOWN_FILE_FORMAT.format(
                    file_name=file_name, file_type="yaml", file_contents=file_contents
                )
                for file_name, file_contents in config_files
            ]
        )

        formatted_main_file = MARKDOWN_FILE_FORMAT.format(
            file_name=self.main_file_name,
            file_type="py",
            file_contents=self.main_file,
        )
        formatted_config_dir_diagram = MARKDOWN_FILE_FORMAT.format(
            file_name="Config Directory Structure",
            file_type="",
            file_contents=config_dir_diagram,
        )
        formatted_command_line = MARKDOWN_FILE_FORMAT.format(
            file_name="Command Line",
            file_type="sh",
            file_contents=self._cmd(),
        )
        formatted_result = MARKDOWN_FILE_FORMAT.format(
            file_name="Output",
            file_type="",
            file_contents=self._result,
        )

        return f"""
        # {self.name}
        {self.description}
        
        {formatted_main_file}

        {formatted_config_dir_diagram}

        {formatted_config_files}

        {formatted_command_line}

        {formatted_result}
        """
