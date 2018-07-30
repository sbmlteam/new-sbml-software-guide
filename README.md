## Installation

Python 3 is highly recommended for this installation! If you're using Python 2, it'll function but be harder.

### Get the Code

First, open a command prompt.

*Important!* Give the code a short file path with no spaces!

Either clone the repository to your computer using
```
git clone https://github.com/sbmlteam/new-sbml-software-guide.git
```
or download the ZIP and unzip to your computer.

Navigate to your new-sbml-software-guide folder. 

### Python 3 Virtual Environments

*Note: These instructions are for Python 3; if you're on Python 2, see [these instructions](#python-2-virtual-environments) instead.*

Create and activate the virtual environment.

On Windows:
```
py -3 -m venv venv
```

Everything else:
```
python3 -m venv venv
```

### Install Flask
On Windows:
```
venv\Scripts\activate
```

Everything else:
```
. venv/bin/activate
```

You'll know this succeeded if `(venv)` appears at the front of your shell prompt.

Now, install Flask to the virtual environment using
```
pip install Flask
```

If you get errors about not being able to find pip, your file path is too long or contains spaces. You'll need to relocate the folder; then try again. If it still doesn't work, make sure the new-sbml-software-guide folder is in your `$PYTHONPATH` (or `%PYTHONPATH%` on Windows).

### Running the Code
Double-check you're in your virtual environment (ie: `(venv)` precedes your shell prompt) and you're in new-sbml-software-guide!

Then run these commands (for Windows):

```
export FLASK_APP="flaskr:start()"
export FLASK_ENV=development
```

Everything else:
```
set FLASK_APP="flaskr:start()"
set FLASK_ENV=development
```

To run the code, use:
```
python flaskr\__init__.py -i
```
The `-i` option initializes the database and must be run each time `schema.sql` is changed. Use `CTRL+C` to exit that process, then run:

```
python flaskr\__init__.py
```
Then navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) and you should see the software guide!

### Python 2 Virtual Environments
Virtual environment support isn't a built-in module in Python 2, so you need to download it yourself. 

If you're on Mac OS X or Windows, first download get-pip.py [here](https://bootstrap.pypa.io/get-pip.py). 

On Mac OS X:
```
sudo python2 Downloads/get-pip.py # or wherever you saved it
sudo python2 -m pip install virtualenv
```

On Windows, as an administrator:
```
\Python27\python.exe Downloads\get-pip.py # or wherever you saved it
\Python27\python.exe -m pip install virtualenv
```

If you're on Linux, get virtualenv using the appropriate command:
```
sudo apt-get install python-virtualenv # Debian, Ubuntu
sudo yum install python-virtualenv # CentOS, Fedora
sudo pacman -S python-virtualenv #Arch
```

Create and activate the virtual environment.

On Windows:
```
\Python27\Scripts\virtualenv.exe venv
```

Everything else:
```
virtualenv venv
```

Now you can return to [Install Flask](#install-flask) above!
