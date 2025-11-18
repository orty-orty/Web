# 🚀 Introduction
This space is dedicated to **SQL injections**. I'll gradually add more exercises to help anyone who wants to improve their skills on this topic.  

After each challenge, you will retrieve a flag like `HackUTT{README}` that confirms you have solved it.  

---

# 📖 Principle  
First of all, **what is a SQL injection?**  
It occurs when a user's input is not properly prepared, allowing us to inject arbitrary SQL queries that will be executed by the server. Using these queries, you might be able to:  
- Bypass authentication without a password  
- Leak information from databases  
- Read and write files on the server  

---

# ✏️ Exercises  

## 🔰 ./intro  
This exercise demonstrates the results of different SQL queries on a small database.  
Initially, it offers options such as **register**, **login**, and **modify password**, similar to a real web application.  
It is primarily designed for beginners, but it can also help you stay sharp and challenge yourself by crafting complex queries.  

---

## 🥇 ./ex_1  
**Your first bypass!**  
The goal of this challenge is to show you how to log into an account **without using a password**.  

---

## 🔍 ./ex_2  
Your first **data leak**!  
Try experimenting with a **UNION-based SQL injection** to retrieve the admin’s password.  

---

## 🪲 ./ex_3  
Here, your objective is to provoke meaningful **SQL errors** and read the clues they expose.  
Follow the trail to the admin password.  

---

## 🧩 ./ex_4  
Connecting to the admin account was easy, but what if the first query is completely secure?  
Learn how to exploit a **second‑order SQL injection** to retrieve the flag from the `/admin` endpoint.  

---

## 📂 ./ex_5  
Leaking the database is fun, but reading files is even better.  
Let’s see how you can access information on the server using SQL queries.  
**The flag is located in the `/shared` directory.**  

---

## ⏳ Next exercise coming soon...  

---

### ⚠️ Disclaimer  
Remember that these exercises are provided for **educational purposes only**.  
**Do not attempt to reproduce them on any infrastructure without explicit authorization. Unauthorized testing is illegal and unethical.**

---
