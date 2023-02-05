# ABOUT THIS APP

This is an Email Scheduler App that send message on scheduled time, email will be received based on event, you must add your email to an event to receive email. written in Python using flask framework, Using simple GUI to input data and registering email recevier

I also implement Multithreading for faster computation and to handle coccurent task/function, as Database we use [PostgreSQL as a Service](https://elephantsql.com/)

# INSTALATION

First install necessary package

```
pip install -r requirement.txt
```
Install & make sure your reddis server running

[Installing Redis](https://redis.io/docs/getting-started/installation/)

Run Program With

```
python -m flask run
```

Open in your browser

http://localhost:5000