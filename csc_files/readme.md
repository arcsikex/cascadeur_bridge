# Cascadeur part of the add-on
For the addon to work properly the command files should be copied to the correct location. And for pythons socket module the _socket.pyd and select.pyd files are also needed.

## Files for the socket module to work:
- _socket.pyd
- select.pyd

These files should be copied to ***CASCADEUR PATH\python\DLLs***

## Commands that are used by the addon
The entire ***externals*** folder should be copied to the commands folder.
By default the commands path is ***CASCADEUR PATH\resources\scripts\python\commands***.

So the path of the command files should be '*.\commands\externals\temp_exporter.py*'
