### Task 2
---
**1. Create a new database named website.**
```sql
mysql > CREATE DATABASE website;
```
![GitHub](/task2/)

**2. Create a new table named member, in the website database.**
```sql
mysql > USE website;

mysql > CREATE TABLE member(
id BIGINT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(255) NOT NULL,
username VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
follower_count INT UNSIGNED NOT NULL DEFAULT 0,
time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```
![](/task2/2-2.jpg)

### Task 3
---
**1. INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data.**
```sql
mysql > INSERT INTO member(name, username, password, follower_count) VALUES('test', 'test', 'test', 5);
mysql > INSERT INTO member(name, username, password, follower_count) VALUES('a', 'a', 'a', 20);
mysql > INSERT INTO member(name, username, password, follower_count) VALUES('b', 'b', 'b', 15);
mysql > INSERT INTO member(name, username, password, follower_count) VALUES('c', 'c', 'c', 8);
mysql > INSERT INTO member(name, username, password, follower_count) VALUES('d', 'd', 'd', 2);
```
![](/task3/3-1、3-2.jpg)

**2. SELECT all rows from the member table.**
```sql
mysql > SELECT * FROM member;
```
![](/task3/3-1、3-2.jpg)

**3. SELECT all rows from the member table, in descending order of time.**
```sql
mysql > SELECT * FROM member ORDER BY time DESC;
```
![](/task3/3-3.jpg)

**4. SELECT total 3 rows, second to fourth, from the member table, in descending order of time. Note: it does not mean SELECT rows where id are 2, 3, or 4.**
```sql
mysql > SELECT * FROM member ORDER BY time DESC LIMIT 3 OFFSET 1;
```
![](/task3/3-4.jpg)

**5. SELECT rows where username equals to test.**
```sql
mysql > SELECT * FROM member WHERE username='test';
```
![](/task3/3-5.jpg)

**6. SELECT rows where name includes the es keyword.**
```sql
mysql > SELECT * FROM member WHERE name LIKE '%es%';
```
![](/task3/3-6.jpg)

**7. SELECT rows where both username and password equal to test.**
```sql
mysql > SELECT * FROM member WHERE username='test' AND password='test';
```
![](/task3/3-7.jpg)

**8. UPDATE data in name column to test2 where username equals to test.**
```sql
mysql > UPDATE member SET name=’test2’ WHERE username='test';
```
![](/task3/3-8.jpg)

### Task 4
---
**1. SELECT how many rows from the member table.**
```sql
mysql > SELECT COUNT(*) FROM member;
```
![](/task4/4-1.jpg)

**2. SELECT the sum of follower_count of all the rows from the member table.**
```sql
mysql > SELECT SUM(follower_count) FROM member;
```
![](/task4/4-2.jpg)

**3. SELECT the average of follower_count of all the rows from the member table.**
```sql
mysql > SELECT AVG(follower_count) FROM member;
```
![](/task4/4-3.jpg)

**4. SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.**
```sql
mysql > SELECT AVG(follower_count) 
        FROM (SELECT follower_count FROM member ORDER BY follower_count DESC LIMIT 2)
        AS top_followers;
```
![](/task4/4-4.jpg)

### Task 5
---
**1. Create a new table named message, in the website database.**
```sql
mysql > USE website;

mysql > CREATE TABLE message(
id BIGINT PRIMARY KEY AUTO_INCREMENT,
member_id BIGINT NOT NULL,
content VARCHAR(255) NOT NULL,
like_count INT UNSIGNED NOT NULL DEFAULT 0,
time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY(member_id) REFERENCES member(id)
);
```
![](/task5/5-1.jpg)

**2. SELECT all messages, including sender names. We have to JOIN the member table to get that.**
```sql
先新增 message 表格資料
mysql > INSERT INTO message(member_id, content, like_count) VALUES(1, 'Hello test', 30);
mysql > INSERT INTO message(member_id, content, like_count) VALUES(2, 'Hello a', 20);
mysql > INSERT INTO message(member_id, content, like_count) VALUES(3, 'Hello b', 55);
mysql > INSERT INTO message(member_id, content, like_count) VALUES(4, 'Hello c', 10);
mysql > INSERT INTO message(member_id, content, like_count) VALUES(5, 'Hello d', 5);
mysql > INSERT INTO message(member_id, content, like_count) VALUES(1, '你好 test', 10);
mysql > INSERT INTO message(member_id, content, like_count) VALUES(2, '你好 a', 40);
mysql > INSERT INTO message(member_id, content, like_count) VALUES(3, '你好 b', 20);
mysql > INSERT INTO message(member_id, content, like_count) VALUES(4, '你好 c', 5);
mysql > INSERT INTO message(member_id, content, like_count) VALUES(5, '你好 d', 25);

再合併兩個表格
mysql > SELECT * FROM message INNER JOIN member ON member.id=message.member_id;
```
![](/task5/5-2.jpg)

**3. SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that.**
```sql
mysql > SELECT * FROM message 
        INNER JOIN member ON member.id=message.member_id 
        WHERE member.username='test';
```
![](/task5/5-3.jpg)

**4. Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to test.**
```sql
mysql > SELECT AVG(message.like_count) FROM message 
        INNER JOIN member ON member.id=message.member_id 
        WHERE member.username='test';
```
![](/task5/5-4.jpg)

**5. Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username.**
```sql
mysql > SELECT member.username, AVG(message.like_count) FROM message 
        INNER JOIN member ON member.id=message.member_id 
        GROUP BY member.username;
```
![](/task5/5-5.jpg)
