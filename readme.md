# ABOUT THIS APP

This is an Email Scheduler App that send message on scheduled time, email will be received based on event, you must add your email to an event to receive email. written in Python using flask framework, Using simple GUI to input data and registering email recevier

I also implement Multithreading for faster computation and to handle coccurent task/function, as Database I am using [PostgreSQL as a Service](https://elephantsql.com/)

# INSTALATION

First install necessary package

```
pip install -r requirement.txt
```
Install & make sure your reddis server running

[Installing Redis](https://redis.io/docs/getting-started/installation/)

Run Program With

```
python run.py
```

Open in your browser

http://localhost:5000

# TEST CASE

You can run test case using 

```
python -m pytest
```
# NOTE

Currently username & password in .env file is empty, please use your own. To create your own password using gmail please refer [HERE](https://support.google.com/accounts/answer/185833?hl=en)