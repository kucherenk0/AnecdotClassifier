# AnecdotClassifier

Simple text classifier for humorous stories, that returns the most appropriate tag to given text

### Installing

Download or clone files from repository 
```
>> https://github.com/kucherenk0/AnecdotClassifier.git
```
make new virtual environment with
```
virtualenv env
source env/bin/activate
```
install requirements.txt
```
pip install -r src/requirements.txt
```
## Running 

#Trainig model
If you running AnecdotClassifier for the first time then you need to train classification model 
In order to do this you need to collect dataset from http://anekdot.ru

```
python AnecdotClassifier train 
```
It might take some time
As a result you will see new files in your directory 

### Running using echo

Aslo you can run it using echo tool

```
>> echo "123 текст 12!" | java SubstringFinder "12"
```
Then you'll recive the result
```
12*3 текст 12*!
```

## Authors

Alexander Kucherenko kucherenko.av@physhtech.edu

