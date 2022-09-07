# API Design

## Table of Content
1. Register Account /Email confirmation (/register)
2. Login(ผิด,ถูก,ถูกแต่ยังไม่ยืนยันอีเมล) (/logout /login)
3. ส่งรายการ โรงเรียนหรือคอร์สตาม คำเสริชและ filter ไปที่หน้าค้นหา
4. ดู/ลบ/แก้ไข  profile ของแต่ละ account
5. สร้าง/ดู/ลบ/แก้ไข คอร์ส
6. แสดงครูที่สอนในคอร์สหนึ่งๆทั้งหมด
7. แสดงนักเรียนที่จองคอร์สทั้งหมด
8. เพิ่ม/ลบ ครูที่สอนในคอร์สเรียน
9. สร้าง/ดู/ลบ/แก้ไข/โรงเรียน
10. เพิ่ม/ดู/ลบ ครูในโรงเรียน
11. ดูวันเวลาการใช้ห้องรายห้อง
12. สร้างคำขอ
13. ดูรายการคำขอ
14. ยืนยัน/ปฏิเสธคำขอ
15. จองคอร์ส
16. ดูรายการจองทั้งหมดในแต่ละคอร์ส
17. ยืนยัน/ปฏิเสธการจองคอร์ส
18. ดึงรายการเรียนที่สมัครไว้ทั้งหมดรายบุคคล
19. ดึงรายการสอนที่ต้องสอนทั้งหมดรายบุคคล
20. ดึงวัน/เวลาที่เรียน/สอนทั้งหมดรายบุคคล
21. ดึงรายการโรงเรียนที่เป็นสมาชิกรายบุคคล
22. ดึงรายการโรงเรียนที่เป็นเจ้าของรายบุคคล
23. แจ้งเตือนในเว็บ/เมลแก่เจ้าของคอร์สว่ามีคนจองคอร์ส
24. แจ้งเตือนในเว็บ/เมลเมื่อถึงเวลาเรียน 
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
## **3. School object**
```
    {
        "school_id" : number,
        "owner_id"  : number,
        "name" : string,
        "description" : string,
        "address" : string,
        "status" : string 
    }
```
# Endpoint 
- รูปแบบอื่นที่ไม่ได้กำหนดเฉพาะให้เป็น Response เป็น default errorทั้งหมด
- ทุก Reponse จะมี `status code` คืนมาเป็น Field แรกทั้งหมด
## **1. Account**

## 1.1 เรียกดูข้อมูลของ User
### Permission : All users
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
## 1.2 เรียกดู Users ตามเงื่อนไข  
### Permission : All users
### `GET` /users?\<query parematers>
### Response
`200` Get successfully
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
## 1.3 ลบ User
### Permission : System admin only
### `DELETE` /users/<user_id>
### Response
`204`  Deleted
``` 
	Return none
```
## 1.4 แก้ไข User 
### Permission : Userที่ login แล้วและเป็นเจ้าของ หรือ System Admin
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
---
## **2. Course & School Searching**
## 2.1 Search & Filter Courses
### Permission : All users
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
## 2.2 Search & Filter Schools
### Permission : All users
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
### Permission : All users
### `GET` /courses/<course_ id>?\<query parameters>

### Response
`200` Course exist
```
    Return single course object that matched course_id and query parameters
```
`404` Course not exist
```
    Return message "Course not exist"
```
## 3.2 สร้างคอร์ส
### Permission : User ที่ login แล้วและเป็นครูในโรงเรียนใดๆ
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
### Permission : User ที่ login แล้วและเป็นเจ้าของคอร์สนั้น หรือ System Admin
### `DELETE` /courses/<course_id>
### Response
`204` Course deleted
```
    Return deleted course object(which is_delate = true)
```
## 3.4 แก้ไขคอร์ส
### Permission : User ที่ login แล้วและเป็นเจ้าของคอร์สนั้น หรือ System Admin 
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
## 3.5 แสดงครูทั้งหมดที่สอนในคอร์ส
### Permission : All users
### `GET` /courses/<course_id>/teachers
### Response
`200` Get successfully
```
    {
        "teachers_id" : [
            <account_id>,
            .
            .
        ]
    }
```
** กรณีไม่มี teacher เลยจะ return list ว่าง<br>
`404` Course doesn't not exist
```
    Return none
```
## 3.6 แสดงนักเรียนทั้งหมดที่จองคอร์ส
### Permission : User ที่ login แล้วและเป็นเจ้าของคอร์สนั้น หรือ System Admin
### `GET` /courses/<course_id>/students
### Response
`200` Get successfully
```
    {
        "students_id" : [
            <account_id>,
            .
            .
        ]
    }
```
## 3.7 เพิ่มครูที่สอนในคอร์ส (ถ้ามีอยู่แล้วไม่มีผล)
### Permission : User ที่ login แล้วและเป็นเจ้าของคอร์สนั้น หรือ System Admin 
### `PUT` /courses/<course_id>/teachers
### Request
```
    {
        "teachers_id" : [
            <account_id>,
            .
            .
        ] //list id ของ teacher ที่จะเพิ่ม
    }
```
### Response
`200` update successfully
```
    Same as GET /courses/<course_id>/teachers
```
`400` invalid update
```
    Return error message
```
### 3.8 ลบครูที่สอนในคอร์ส
### Permission : User ที่ login แล้วและเป็นเจ้าของคอร์สนั้น หรือ System Admin 
### `DELETE` /courses/<course_id>/terchers
### Request 
```
    {
        "teachers_id" : [
            <account_id>,
            .
            .
        ] //list id ของ teacher ที่จะลบ
    }
```
### Response
`200` update successfully
```
    Same as GET /courses/<course_id>/teachers
```
`400` invalid delete
```
    Return error message
```
## **4. School**
## 4.1 สร้าง School
### `POST` /schools

