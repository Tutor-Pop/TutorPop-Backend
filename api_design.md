# API Design

## Table of Content
1) Register Account /Email confirmation (/register)
2) Login(ผิด,ถูก,ถูกแต่ยังไม่ยืนยันอีเมล) (/logout /login)
3) ส่งรายการ โรงเรียนหรือคอร์สตาม คำเสริชและ filter ไปที่หน้าค้นหา
4) ดู/ลบ/แก้ไข  profile ของแต่ละ account
5) สร้าง/ดู/ลบ/แก้ไข คอร์ส
6) ดูวันเวลาการใช้ห้องรายห้อง
7) สร้างคำขอ
8) ดูรายการคำขอ
9) ยืนยัน/ปฏิเสธคำขอ
10) สร้าง/ดู/ลบ/แก้ไข/โรงเรียนแสดงรายการ user ตาม username/userid
11) เพิ่ม/ดู/ลบ ครูในโรงเรียน
12) จองคอร์ส
13) ดูรายการจองทั้งหมดในแต่ละคอร์ส
14) ยืนยัน/ปฏิเสธการจองคอร์ส
15) ดึงรายการเรียนที่สมัครไว้ทั้งหมดรายบุคคล
16) ดึงรายการสอนที่ต้องสอนทั้งหมดรายบุคคล
17) ดึงวัน/เวลาที่เรียน/สอนทั้งหมดรายบุคคล
18) ดึงรายการโรงเรียนที่เป็นสมาชิกรายบุคคล
19) ดึงรายการโรงเรียนที่เป็นเจ้าของรายบุคคล
20) แจ้งเตือนในเว็บ/เมลแก่เจ้าของคอร์สว่ามีคนจองคอร์ส
21) แจ้งเตือนในเว็บ/เมลเมื่อถึงเวลาเรียน

# Endpoint

## **1. Account**

## 1.1 เรียกดูข้อมูลของ User
## `GET` /users/<user_id>  

### Response  	
`200` if user exist
```
    Return User object
```
`404` if user not exist
```
    Return message “User not exist”
```	
else
```
    default
```
## 1.2 ลบ User
## `DELETE` /users/<user_id>
### Response
`204` if deleted
``` 
	Return none
```
else
```
	default
```

## 1.3 แก้ไข User 
## `PUT` /users/<user_id>  
### Request Body 
```
    {
        <field> : <Update data>,
        ……
    }
```
### Example
```json
    {
        "firstname" : "hello",
        "lastname" : "world"
    }
```
### Response
`200` if update correctly

```
    Return user object
```
`400` if incorrect parameters
```
    Return error messages
```
`403` if no permission
```
    Return error messages
```
else
```
    Default
```

## 1.4 เรียกดู User ทั้งหมด  
## `GET` /users

### Response

`200` if get all users correctly
```
    Return all user objects
```
else
```
    Default
```

---
## **2. Course & School Searching**
## `GET` /search

### Request
```
    {
		"search" : string,
		"type" : string //school or course,
		"filter" : {
			[filter field] : string,
			….
		}
	{
```
### Example
```json
    {
		"search" : "ไสยศาสตร์เบื้องต้น",
		"type" : "course",
		"filter" : {
			"tag" : "magic",
			"max_price" : 5000
		}	
    }
```
### Response
`200` Search successfully
```
    Return all match school/course objects
```
else
``` 
    default
```

---

## **3. Course**
## `GET` /courses/<course_ id>

เดะทำต่อ