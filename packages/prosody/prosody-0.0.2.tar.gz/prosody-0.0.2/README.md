#  prosody

Generate voices using tts tool, called prosody

## How To Use
### Installing

Install prosody using pip
```
python -m pip install prosody
```

### Examples

Import package
```
from prosody import prosodyAPI 
```

Register valid user and password 

```
prosodyAPI.register_user('username', 'password')
```
Generate one voice using  **generate_voices**  function
```python
def generate_voices(emotionX, emotionY, actor, *texts):
	...
    return
    
generate_voices(0.1, 0.2, 'actor', 'text')
```
Also generate multiple voices at once 
```
generate_voices(0.1, 0.2, 'actor', 'text1', 'text2', 'text3', 'text4')
```
Then .wav files will be downloaded at root project directory



## Authors

* **Suwon Shin** - *Initial work* - [shh1574](https://github.com/shh1574)