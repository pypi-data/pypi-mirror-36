# Pyforms Generic Editor Terminal Plugin

Adds a terminal window to execute commands to control the GUI interface.

## How to install:

1. Clone the repository and project folder using the terminal.
2. Install the plugin by running the next command in the terminal:
```shell
    sudo pip3 install . --upgrade
```
3. Open GUI
4. Select Options > Edit user settings
5. Add the following info:

```python
    GENERIC_EDITOR_PLUGINS_LIST = [
        (...other plugins...),
        'pge_welcome_plugin',
    ]    
```
6. Save
7. Restart GUI



![screenshot](docs/imgs/window.png)