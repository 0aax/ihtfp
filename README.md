# ihtfp
> *Which ihtfp describes today's mood?*

<p align='center'>
<img src="example/example-term.gif" width="500">
</p>

> *Plot mood charts!*

<p align='center'>
<img src="example/example_mood_plot.png" width="600">
</p>

## Installation
Clone repository.
```
git clone https://github.com/0aax/ihtfp.git
```
(Optional) Create and activate a virtual environment.
```
virtualenv -p python3 venv
source venv/bin/activate
```
Install package.
```
pip install path/to/ihtfp
```
## Usage
```
ihtfp                               log daily mood

ihtfp daily                         log daily mood
ihtfp plot                          generate and save mood chart

ihtfp add "MEANING" RATING          add new ihtfp meaning and mood rating
ihtfp del "MEANING"                 delete all instances of a particular meaning
ihtfp export VAR VAL                edit config variables
```