# Introduction 
This space is dedicated to SQL injections. I'll gradually add more exercises to help anyone who wants to improve their skills on this topic.
After each challenge, you will retrieve a flag like `HackUTT{README}` that confirms you have solved it.\
<br>
  

# Principle 📖
First of all, what is a SQL injection?
It occurs when a user's input is not properly prepared, allowing us to inject arbitrary SQL queries that will be executed by the server. Using these new queries, you might be able to bypass authentication without a password, leak information from databases, or even read and write files on the server.\
<br>

# Exercices ✏️
## Intro
This exercise demonstrates the results of different SQL queries on a small database.
Initially, it will offer a few options such as register, login, and modify password, similar to what you would find in a real web application.
It is primarily designed for beginners, but it can also help you stay sharp in this programming language and challenge yourself by crafting complex queries.

## Ex_1
Your first bypass !\
The goal of this challenge is to show you how to log into an account without using a password

## Ex_2
This challenge is designed for your first data leak. Try experimenting with a UNION-based SQL injection to retrieve the admin’s password.

## Ex_3
Here, your objective is to provoke meaningful SQL errors and read the clues they expose. Follow the trail to the admin password.

## Ex_4
Connecting to the admin account was easy, but what if the first query is completely secure? Learn how to exploit a second‑order SQL injection to retrieve the flag from the `/admin` endpoint.

## Ex_5
Leaking the database is fun, but reading files is even better. Let’s see how you can access information on the server using SQL queries.\
<br>
## Next exercise coming soon ...
