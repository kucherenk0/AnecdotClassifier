# AnecdotClassifier

Simple text classifier for humorous stories, that returns the most appropriate tag to given text

### Installing

Download or clone files from repository 
```
>> https://github.com/kucherenk0/AnecdotClassifier.git
```
make new virtual environment with
```
>> virtualenv env
>> source env/bin/activate
```
install requirements.txt
```
>> pip install -r src/requirements.txt
```
## Running 

If you running AnecdotClassifier for the first time then you need to train classification model.
In order to do this you need to collect dataset from http://anekdot.ru

```
>> python AnecdotClassifier 
```
It might take some time

```
Downloading anecdotes...
Done!
Training model...
Done!
```
As a result you will see new files in your directory 
```
>> tree -L 1
├── README.md
├── classifier.mdl
├── html_source
├── pca.mdl
├── requirements.txt
├── vect.mdl
└── venv
```
**html_source/** directory will contain html pages from  http://anekdot.ru that you'll need to collect a dataset <br>
**pca.mdl, vect.mdl, classifier.mdl** are files that are needed for the classifier<br>
Then input the story you need to be classified
```
So i'm ready to read your story!
"Пришли как-то Пупа и Лупа получать зарплату. Но в бухгалтерии всё перепутали и Лупа получил зарплату за Пупу, а Пупа за Лупу."
```
Then you'll recive the result
```
Looks like this is about: Деньги
```

## Authors

Alexander Kucherenko kucherenko.av@physhtech.edu

