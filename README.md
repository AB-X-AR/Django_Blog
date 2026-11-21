# A2Z Blog Project

## 1. Project overview

We'll build a Django Blog Application with the following features:
![[Pasted image 20261121191933.png]]


## 2. Technologies we'll use

|Technology|Purpose|
|---|---|
|Python|Programming language|
|Django|Backend framework|
|SQLite|Database initially|
|HTML5|Structure|
|CSS3|Styling|
|Bootstrap 5|Responsive UI|
|JavaScript|Interactivity|

## 3. Project structure

Our project will eventually look something like this:

text

```
blog_project/
│
├── manage.py
│
├── blog_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── blog/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│       └── blog/
│           ├── home.html
│           ├── post_detail.html
│           └── create_post.html
│
├── accounts/
│   ├── views.py
│   └── urls.py
│
├── static/
├── media/
└── requirements.txt
```