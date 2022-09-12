# API Design

## Table of Content
- Register Account /Email confirmation (/register)
- Login(ผิด,ถูก,ถูกแต่ยังไม่ยืนยันอีเมล) (/logout /login)
- ส่งรายการ โรงเรียนหรือคอร์สตาม คำเสริชและ filter ไปที่หน้าค้นหา
- ดู/ลบ/แก้ไข  profile ของแต่ละ account
- สร้าง/ดู/ลบ/แก้ไข คอร์ส
- แสดงครูที่สอนในคอร์สหนึ่งๆทั้งหมด
- แสดงนักเรียนที่จองคอร์สทั้งหมด
- เพิ่ม/ลบ ครูที่สอนในคอร์สเรียน
- สร้าง/ดู/ลบ/แก้ไข/โรงเรียน
- เพิ่ม/ดู/ลบ ครูในโรงเรียน
- เพิ่ม/ลบ/สร้าง/แก้ไขห้องเรียน
- ดูวันเวลาการใช้ห้องรายห้อง
- สร้างคำขอ
- ดูรายการคำขอ
- ยืนยัน/ปฏิเสธคำขอ
- จองคอร์ส
- ดูรายการจองทั้งหมดในแต่ละคอร์ส
- ยืนยัน/ปฏิเสธการจองคอร์ส
- ดึงรายการจองทั้งหมด
- ดึงรายการเรียนที่สมัครไว้ทั้งหมดรายบุคคล
- ดึงรายการสอนที่ต้องสอนทั้งหมดรายบุคคล
- ดึงวัน/เวลาที่เรียน/สอนทั้งหมดรายบุคคล
- ดึงรายการโรงเรียนที่เป็นสมาชิกรายบุคคล
- ดึงรายการโรงเรียนที่เป็นเจ้าของรายบุคคล
- ??แจ้งเตือนในเว็บ/เมลแก่เจ้าของคอร์สว่ามีคนจองคอร์ส
- ??แจ้งเตือนในเว็บ/เมลเมื่อถึงเวลาเรียน 
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
        "status" : string,
        "logo_url" : string,
        "banner_url" : string 
    }
```
## **4. Room object**
```
    {
        "room_id" : number,
        "room_name" : string,
        "school_id" : number,
        "maximum_seat" : number
    }
```
## **5. Request object**
```
    {
        "request_id" : number,
        "account_id" : number,
        "school_id" : number,
        "document_url" : string,
        "proof_of_payment_url" : string,
        "request_status" : string
    }
```
## **6. Reservation**
```
    {
        reservation_id : number,
        course_id : number,
        account_id : number,
        payment_url : string,
        status : string,
        reservation_datetime : string,
        expire_datetime : string,
    }
```
## **7. Study time object**
```
    "course_id" : number,
    "day" : string,
    "start_time" : string,
    "end_time" : string
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
### Query Parameters
| Query   |      Type      |  Default |
|---------|-------------|------|
| user_id | NUMBER | None |
| is_verified | BOOLEAN | *True* |
| user_status | STRING | None |
| year_of_birth | NUMBER | None |

### Response
`200` Get successfully
```
    {
        "metadata" : {
             "count": number,
             "offset" : number, 
             "limit" : number
        },
        "results" : [All match account objects]
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
### Query Parameters
| Query   |      Type      |  Default |
|---------|-------------|------|
| type | STRING |None |
| course_name | STRING | None |
| course_id | NUMBER | None |
| school_id| NUMBER| None|
| max_price |    NUMBER   |   None |
| max_student | NUMBER| None|
| start_date | STRING | None|
| end_date | STRING | None |
| is_deleted | BOOLEAN | *False* |
| offset | NUMBER |    None |
| limit | NUMBER |    None |

### Example
```
    /courses?type=math&max_price=2000
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
### Query Parameters
| Query   |      Type      |  Default |
|---------|-------------|------|
| school_name | STRING | None |
| school_id | NUMBER | None |
| type | STRING | None |
| address** | STRING | None |
| offset | NUMBER | None |
| limit | NUMBER | None | 
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
### `GET` /courses/<course_ id>
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
        "room_id" : number,
        "course_description" : string,
        "reserve_open_date" : string,
        "reserve_close_date" : string,
        "start_date" : string,
        "end_date" : string,
        "course_period" : number,
        "course_student" : number,
        "teachers_id" : [<account_id>,..],
        "payment_text" : string,
        "payment_picture_url" : string,
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
## 3.5 แสดงครูทั้งหมดที่สอนในคอร์ส
### Permission : All users
### `GET` /courses/<course_id>/teachers
### Response
`200` Get successfully
```
    {
        "teachers" : [
            <teachers>,
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
        "students" : [
            <account object>,
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
## 3.8 ลบครูที่สอนในคอร์ส
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
### Permission : User ที่ login แล้วเท่านั้น หรือ System Admin
### `POST` /schools
### Request
```
    {
        "owner_id" : number,
        "name" : string,
        "description" : string,
        "address" : string,
        "logo_url" : string,
        "banner_url" : string,
        "school_type_id" : [<type_id>, . .]
    }
```
### Response
`201` Created
```
    Return newly created school object
```
## 4.2 เรียกดู single school
### Permission : All users
### `GET` /schools/<school_id>
### Response
`200` Get successfully
```
    Return single school object
```
## 4.3 ลบ School 
### Permission : System Admin only
### `DELETE` /schools/<school_id>
### Response
`204` Deleted
```
    Return none
```
## 4.4 แก้ไขข้อมูล school (ยกเว้น status)
### Permission : Userที่loginแล้วและเป็นเจ้าของ school นั้น หรือ System Admin
### `PUT` /schools/<school_id>
### Request
```
    {
        <update field> : <update value>,
        .
        .
    
    }
```
### Response
`200` Update correctly
```
    Return single school object
```
`400`  Incorrect parameters
```
    Return error messages
```
## 4.5 ดูครูทั้งหมดในโรงเรียน
### Permission : All users
### `GET` /schools/<school_id>/teachers
### Response
`200` Get correctly
```
    {
        "teachers" : [
            <teacher object>, 
            . 
            . 
            .
        ]
    }
```
** กรณีไม่มี teacher เลยจะ return list ว่าง<br>
`404` schools doesn't not exist
```
    Return none
```
## 4.6 เพิ่มครูในโรงเรียน (ถ้ามีอยู่แล้วไม่มีผล)
### Permission : Userที่loginแล้วและเป็นเจ้าของโรงเรียนนั้น หรือ System Admin
### `PUT` /schools/<school_id>/teachers 
### Request
```
    //list of teachers_id that want to add
    {
        "teachers" : [
            <teacher object>,
            . 
            . 
            .
        ]    
    }
```
### Response
`200` Add correctly
```
    Same as GET /schools/<school_id>/teachers
```
## 4.6 ลบครูในโรงเรียน
### Permission : User ที่ login แล้วและเป็นเจ้าของโรงเรียนนั้น หรือ System Admin 
### `DELETE` /schools/<school_id>/terchers
### Request 
```
    {
        "teachers" : [
            <teacher object>,
            . 
            . 
            .
        ] 
    }
```
### Response
`200` update successfully
```
    Same as GET /schools/<school_id>/teachers
```
`400` invalid delete
```
    Return error message
```
## **5. Rooms**
## 5.1 เพิ่ม/สร้าง/แก้ไขห้องเรียนในโรงเรียน
### Permission : User ที่ loginแล้วและเป็นเจ้าของโรงเรียนนั้น หรือ System Admin
### `PUT` /schools/<school_id>/rooms
### Request
```
    {
        "room_name" : string,
        "maximum_seat" : number,
    }
```
`201` Created
```
    Return newly created room object
```
`200` Update successfully
```
    Return updated room
```
## 5.2 ดูห้องเรียนในโรงเรียน
### Permission : User ที่ loginแล้วและเป็นเจ้าของโรงเรียนนั้น หรือ System Admin
### `GET` /schools/<school_id>/rooms?\<query_parameters>
**ถ้าไม่ใส่ ?\<query_params> คือเรียกทั้งหมด
### Query Parameters
| Query   |      Type      |  Default |
|---------|-------------|------|
| max_seat | NUMBER | None |
| available_in | [DATETIME,DATETIME] | None |

### Response
`200` Get successfully
```
    Return list of rooms object that match the parameters
```
`404` Room does not exist
```
    Return none
```
## 5.3 ดู single room
### Permission : User ที่ loginแล้วและเป็นเจ้าของโรงเรียนนั้น หรือ System Admin
### `GET` /schools/<school_id>/rooms/<room_id>
`200` Get successfully
```
    Return single room object
```
`404` Room does not exist
```
    Return none
```
## 5.4 ลบห้องเรียนในโรงเรียน
### Permission : User ที่ loginแล้วและเป็นเจ้าของโรงเรียนนั้น หรือ System Admin
### `DELETE` /schools/<school_id>/rooms/<room_id>
### Response
`204` Deleted
```
    Return none
```
## 5.5 ดูเวลาการใช้ห้องรายห้อง
### Permission :User ที่ loginแล้วและเป็นสมาชิกของโรงเรียนที่เป็นเจ้าของห้องนั้น หรือ System Admin
### `GET` /rooms/<room_id>/usages
### Response
`200` Get sucessfully
```
    {
        "count" : number,
        "usages" :[
            {"date" : string, "start_time" : string, "end_time" : string},
            .
            .
            .
        ] 
    }
```

## **6. คำขอเปิดโรงเรียน**
## 6.1 สร้างคำขอ(ต้องทำหลังสร้างโรงเรียนทันที)
### Permission :User ที่ login แล้ว หรือ System Admin
### `POST` /requests
### Request
```
    {
        "account_id" : number,
        "school_id" : number,
        "document_url" : string,
        "proof_pay_ment_url" : string
    }
```
### Response
`201` Created
```
    Return newly created request object
```
## 6.2 เรียกดูคำขอเดียว
### Permission : User ที่เป็นเจ้าของ Request นั้นๆ หรือ System admin
### `GET` /requests/<request_id>
### Response
`200` Get sucessfully
```
    Return signle matched request
```
## 6.3 เรียกดูตำขอแบบใช้เงื่อนไข
### Permission : System Admin เท่านั้น
### `GET` /requests?\<query_parameters>
### Query Parameters
| Query   |      Type      |  Default |
|---------|-------------|------|
| request_id | NUMBER | None |
| accound_id | NUMBER | None |
| school_id | NUMBER | None |
| request_status | STRING | None |

`200` Get sucessfully
### Response
```
    {
        "count" : number,
        "requests" : [
            <matched request object>,
            .
            .
            .
        ]
    }
```
## 6.4 ลบคำขอ
### Permission : System Admin only
### `DELETE` /requests/<request_id>
`204` Deleted
```
    Return none
```
## 6.5 แก้ไขสถานะคำขอ
### Permission : System Admin only
### `PUT` /requests/<request_id>/request_status
### Request
```
    {
        "request_status" : string 
    }
```
### Response
`200` Update successfully
```
    Return updated request object
```
`404` request not exist
```
    Return none
```
## 7. **การจองคอร์ส**
## 7.1 จองคอร์ส
### Permission : User ที่ Login แล้ว
### `POST` /reservations`
## Request
```
    {
        "course_id" : string,
        "account_id" : string,
        "payment_url" : string,
    }
```
### Response
`200` Reserve successfully
```
    Return newly create reservation object
```
## 7.2 ดูข้อมูลการจองทั้งหมดในคอร์ส
### Permission : User ที่ login แล้วและเป็นเจ้าของคอร์สนั้น หรือ System Admin
### `GET` /courses/<course_id>/reservations
## Response
`200` Get succesfully
```
    {
        "reservations" : [
            <reservation object>,
            .
            .
            .
        ]
    }
```
## 7.3 เปลี่ยนสถานะการจองคอร์ส
### Permission : User ที่ login แล้วและเป็นครูเจ้าของคอร์สนั้น
### `PUT` /reservations/<reservation_id>/status
## Request
```
    {
        "reservation_status" : string
    }
```
### Response
`200` Updated
```
    Return updated reservation object
```
## 7.4 ลบการจองคอร์ส
### Permission : System Admin only
### `DELETE` /reservations/<reservation_id>
## Response
`204` Deleted
```
    Return none
```
## **8. Personal Management**
## 8.1 ดึงรายการจองทั้งหมดของตนเอง
### Permission : User ที่ loginแล้วเท่านั้นและเป็นเจ้าของ account นั้น หรือ System Admin
### `GET` /users/<user_id>/reservations
### Response
`200` Get succesfully
```
    {
        "reservations" : [
            <reservation object>,
            .
            .
            .
        ]
    }
```
## 8.2 ดึงรายการเรียนทั้งหมด(คอร์สที่จองและได้รับการยืนยันแล้ว)
### Permission : User ที่ loginแล้วเท่านั้นและเป็นเจ้าของ account นั้น หรือ System Admin
### `GET` /users/<user_id>/courses
### Response
`200` Get successfully
```
    {
        "courses" : [
            <course object>,
            .
            .
            .
        ]
    }
```
## 8.3 ดึงรายการสอนทั้งหมด
### Permission : User ที่ loginแล้วเท่านั้นและเป็นเจ้าของ account นั้น หรือ System Admin 
### `GET` /users/<user_id>/teachings
### Response
`200` Get sucessfully
```
    {
        "courses" : [
            <course object>,
            .
            .
            .
        ]
    }
```
## 8.4 ดึงวันเวลาที่เรียนสอนทั้งหมด
### Permission : User ที่ loginแล้วเท่านั้นและเป็นเจ้าของ account นั้น หรือ System Admin 
### `GET` /users/<user_id>/times
### Response
`200` Get successfully
```
    {
        "teachings" : [
            <study time object>,
            .
            .
            .
        ],
        "studyings" : [
            <study time object>,
            .
            .
            .
        ]
    }
```
## 8.5 ดึงรายการโรงเรียนที่เป็นสมาชิกทั้งหมด
### Permission : User ที่ loginแล้วเท่านั้นและเป็นเจ้าของ account นั้น หรือ System Admin
### `GET` /users/<user_id>/schools
### Response
`200` Get successfully 
```
    {
        "schools" : [
            <school object>,
            .
            .
            .
        ]
    }
```
## 8.6 ดีงรายการโรงเรียนที่เป็นเจ้าของทั้งหมด
### Permission : User ที่ loginแล้วเท่านั้นและเป็นเจ้าของ account นั้น หรือ System Admin 
### `GET` /users/<user_id>/owners
### Response
```
    {
        "schools" : [
            <school object>,
            .
            .
            .
        ]
    }
```




