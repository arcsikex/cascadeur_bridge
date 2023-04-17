# Files required for the addon to work

## Files for the socket module to work:
- _socket.pyd
- select.pyd

These files should be copied to *CASCADEUR PATH\python\DLLs*

## Commands that are used by the addon
The whole *external* folder should be copied to the commands folder.
By default the commands path is *CASCADEUR PATH\resources\scripts\python\commands*.
But it can be changed by defining a path in *CASCADEUR PATH\resources\settings.ini*.

```python
# Cascadeur root folder from .exe path
import os
root_folder = os.path.dirname(program_path)

# Get commands path from config
import configparser

config = configparser.ConfigParser()
config.read(os.path.join(root_folder, "resources", 'settings.ini'))

path = config.get('section_name', 'ScriptsDir')

if path:
    return path
else:
    return os.path.join(root_folder, "resources", "scripts", "python", "commands")
