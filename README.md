sample code for pyside6

# How to setup environment
To setup the environment, run the following commands in the root folder of the repository.

```
python -m venv env
env\scripts\activate
pip install -r .\requirements.txt
```

# How to create executable
To package this program into an executable, run the following command in the root folder of the repository.
```
pyinstaller main.spec
```
The resultant executable file will be in the `dist` folder. Please be aware that the program requires images to be put into the `data/images` directory to work.