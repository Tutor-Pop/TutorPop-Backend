# API Design

## Table of Content
1) Register Account /Email confirmation (/register)
2) Login(ผิด,ถูก,ถูกแต่ยังไม่ยืนยันอีเมล) (/logout /login)
3) ส่งรายการ โรงเรียนหรือคอร์สตาม คำเสริชและ filter ไปที่หน้าค้นหา
4) ดู/ลบ/แก้ไข  profile ของแต่ละ account
5) สร้าง/ดู/ลบ/แก้ไข คอร์ส
6) แสดงครูที่สอนในคอร์สหนึ่งๆทั้งหมด
7) ดูวันเวลาการใช้ห้องรายห้อง
8) สร้างคำขอ
9) ดูรายการคำขอ
10) ยืนยัน/ปฏิเสธคำขอ
11) สร้าง/ดู/ลบ/แก้ไข/โรงเรียนแสดงรายการ user ตาม username/userid
12) เพิ่ม/ดู/ลบ ครูในโรงเรียน
13) จองคอร์ส
14) ดูรายการจองทั้งหมดในแต่ละคอร์ส
15) ยืนยัน/ปฏิเสธการจองคอร์ส
16) ดึงรายการเรียนที่สมัครไว้ทั้งหมดรายบุคคล
17) ดึงรายการสอนที่ต้องสอนทั้งหมดรายบุคคล
18) ดึงวัน/เวลาที่เรียน/สอนทั้งหมดรายบุคคล
19) ดึงรายการโรงเรียนที่เป็นสมาชิกรายบุคคล
20) ดึงรายการโรงเรียนที่เป็นเจ้าของรายบุคคล
21) แจ้งเตือนในเว็บ/เมลแก่เจ้าของคอร์สว่ามีคนจองคอร์ส
22) แจ้งเตือนในเว็บ/เมลเมื่อถึงเวลาเรียน
# Common Objects
## **1. User object**
```
    {
        "user_id" : number,
        "username" : string,
        "firstname" : string,
        "lastname" : string,
        "email" : string,
        "year_of_birth" : number,
        "description" : string,
        "is_verified" : boolean,
        "picture_url" : string,
        "user_status" : string
    }
```
## **2. Course object**
```
    {
        "course_id" : number,
        "school_id" : number,
        "course_name" : string,
        "course_description" : string,
        "reserve_open_date" : string,
        "reserve_close_date" : string,
        "start_date" : string,
        "end_date" : string,
        "course_period" : number,
        "course_price" : number,
        "maximum_student" : number,
        "reserved_student" : number,
        "payment_method_text_url" : string,
        "payment_method_picture_url" : string
        "is_delete" : boolean
    }
```
# Endpoint 
** รูปแบบอื่นที่ไม่ได้กำหนดเฉพาะให้เป็น Response เป็น default errorทั้งหมด
## **1. Account**

## 1.1 เรียกดูข้อมูลของ User
### `GET` /users/<user_id>  
### Response  	
`200` User exist
```
    Return single user object
```
`404` User not exist
```
    Return message “User not exist”
```	
## 1.2 ลบ User
### `DELETE` /users/<user_id>
### Response
`204`  Deleted
``` 
	Return none
```
## 1.3 แก้ไข User 
### `PUT` /users/<user_id>  
### Request Body 
```
    {
        <Update field> : <Update data>,
        .
        .
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
`200` Update correctly

```
    Return user object
```
`400` Incorrect parameters
```
    Return error messages
```
`403` No permission
```
    Return error messages
```

## 1.4 เรียกดู User ทั้งหมด  
### `GET` /users

### Response

`200` Get correctly
```
    Return all user objects
```

---
## **2. Course & School Searching**
## 2.1 search & filter courses
### `GET` /courses?\<query paremeters>
### Example
```
    /courses?type=math&price_max=2000
```
### Response
`200` Search successfully
```
    {
        "metadata" : {
            "count": number,
             "offset" : number, 
             "limit" : number
        },
        "results" : [All match course objects]
    }
```
## 2.2 search & filter schools
### `GET` /schools?\<query paremeters>
### Example
```
    /schools?name=Hogwarts&type=Magic_school
```
### Response
`200` Search successfully
```
    {
        "metadata" : {
            "count": number,
             "offset" : number, 
             "limit" : number
        },
        "results" : [All match school objects]
    }
```
---

## **3. Course**
## 3.1 ดูข้อมูลของแต่ละคอร์ส
### `GET` /courses/<course_ id>
### Response
`200` Course exist
```
    Return single course object
```
`404` Course not exist
```
    Return message "Course not exist"
```
## 3.2 สร้างคอร์ส
### `POST` /courses
### Request
```
    {
        "school_id" : number,
        "course_name" : string,
        "type_id" : number,
        "course_description" : string,
        "reserve_open_date" : string,
        "reserve_close_date" : string,
        "start_date" : string,
        "end_date" : string,
        "course_period" : number,
        "course_student" : number,
        "teachers_id" : [<account_id>,..],
        "payment_text" : string,
        "payment_picture_url" : string
    }
```
### Response
`201` create course successfully
```
    Return newly create course object
```
## 3.3 ลบคอร์ส
### `DELETE` /courses/<course_id>
### Response
`204` deleted
```
    Return none
```
## 3.4 แก้ไขคอร์ส
### `PUT` /courses/<course_id>
### Request
```
    {
        <update field> : <update value>,
        .
        .
    }
```
Example
```
    {
        "course_name" : "Software Engineering",
        "end_date" : "11-11-2011"
    } 
```
### Response
`200` Update correctly

```
    Return course object
```
`400`  Incorrect parameters
```
    Return error messages
```
`403` No permission
```
    Return error messages
```
## 3.5 ดูครูทั้งหมดที่สอนในคอร์ส
### `GET` /courses/<course_id>/teachers
### Response
`200` Get successfully
```
    {
    	"metadata" : {
	    "count" : number
	},
        "teachers_id" : [
            <account_id>,
            .
            .
        ]
    }
```
** กรณีไม่มี teacher เลยจะ return list ว่าง<br>
`404` Course Not exist
```
    Return none
```
