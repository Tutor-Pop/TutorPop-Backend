# API Design

## Table of Content
### 1.Account
- 1.1 เรียกดูข้อมูลของ Account
- 1.2 เรียกดู Accounts ตามเงื่อนไข
- 1.3 ลบ Account
- 1.4 แก้ไข Account
### 2.Course & School Searching
- 2.1 Search & Filter Courses
- 2.2 Search & Filter Schools
### 3.Course
- 3.1 ดูข้อมูลของคอร์ส
- 3.2 สร้างคอร์ส
- 3.3 ลบคอร์ส
- 3.4 แก้ไขคอร์ส
- 3.5 แสดงครูทั้งหมดที่สอนในคอร์ส
- 3.6 แสดงนักเรียนทั้งหมดที่สอนคอร์ส
- 3.7 เพิ่มครูที่สอนในคอร์ส
- 3.8 ลบครูที่สอนในคอร์ส
- 3.9 อัพโหลดรูปช่องทางการชำระเงิน
### 4.School
- 4.1 สร้าง School
- 4.2 เรียกดู Single School
- 4.3 ลบ School
- 4.4 แก้ไขข้อมูล School (ยกเว้น status)
- 4.5 ดูครูทั้งหมดในโรงเรียน
- 4.6 เพิ่มครูในโรงเรียน (ถ้ามีอยู่แล้วไม่มีผล)
- 4.7 ลบครูในโรงเรียน
- 4.8 แก้ไขสถานะโรงเรียน
- 4.9 ดูคอร์สทั้งหมดในโรงเรียน
- 4.10 ดูผู้ใช้คนอื่นที่ไม่ได้อยู่ในโรงเรียน
### 5.Room
- 5.1 เพิ่ม/สร้าง/แก้ไขห้องเรียนในโรงเรียน
- 5.2 ดูห้องเรียนในโรงเรียน
- 5.3 ดูข้อมูล Single room
- 5.4 ลบห้องเรียนในโรงเรียน
- 5.5 ลบห้องหลายห้องในโรงเรียน
- 5.6 ดูเวลาการใช้ห้องรายห้อง
### 6.Open Request
- 6.1 สร้างคำขอ
- 6.2 เรียกดูคำขออันเดียว
- 6.3 เรียกดูคำขอแบบใช้เงื่อนไข
- 6.4 ลบคำขอ
- 6.5 แก้ไขข้อมูลคำขอ (ยกเว้น status)
- 6.6 แก้ไขสถานะคำขอ
- 6.7 ส่งหลักฐานการชำระเงินของการจอง
### 7.Course Reservation
- 7.1 การจองคอร์ส
- 7.2 ดูข้อมูลการจองทั้งหมดในคอร์ส
- 7.3 แก้ไขสถานะการจองคอร์ส
- 7.4 ลบการจองคอร์ส
- 7.5 อัพโหลดหลักฐานการจ่ายเงินในการจอง
### 8.Personal Management
- 8.1 เรียกรายการจองทั้งหมดของตนเอง
- 8.2 เรียกรายการเรียนทั้งหมด
- 8.3 เรียกรายการจองทั้งหมด
- 8.4 เรีียกวันเวลาเรียน/สอนทั้งหมด
- 8.5 เรียกรายการโรงเรียนที่เป็นสมาชิกทั้งหมด
- 8.6 เรียกรายการโรงเรียนที่เป็นเจ้าของทั้งหมด
### 9. Login/Register
### 10. Notification Message
- 10.1 สร้าง notification message
- 10.2 เรียก notification message ทั้งหมดของ account หนึ่งๆ
- 10.3 เรียก notification message เฉพาะที่ยังไม่ expire ของ account หนึ่งๆ
### 11. Statistics
- 11.1 เรียกดูข้อมูลจำนวน Accounts, Schools, Courses ที่ Active ในปัจจุบัน
- 11.2 เรียกดูข้อมูลจำนวน School Open Request ที่ยังไม่เสร็จสิ้น
## **1. Account object**
```
    {
        "account_id" : number,
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
        "owner_id" : number,
        "course_name" : string,
        "type" : string,
        "course_description" : string,
        "reserve_open_date" : string,
        "reserve_close_date" : string,
        "start_date" : string,
        "end_date" : string,
        "course_period" : number,
        "course_price" : number,
        "maximum_student" : number,
        "reserved_student" : number,
        "payment_method_text" : string,
        "payment_method_pic" : image,
        "is_deleted" : boolean
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
        "document" : File,
        "paymeny_pic" : Image,
        "request_status" : string
    }
```
## **6. Reservation**
```
    {
        "reservation_id" : number,
        "course_id" : number,
        "account_id" : number,
        "payment_pic" : Image,
        "status" : string,
        "reservation_datetime" : string,
        "expire_datetime" : string,
    }
```
## **7. Study time object**
```
    {
        "course_id" : number,
        "day" : string,
        "start_time" : string,
        "end_time" : string
    }
```
## **8. Notification object**
```
    {
        "account_id" : number,
        "message_noti" : string,
        "create_time" : string,
        "expire_date" : string
        }
```

## **9. Study time record object**
```
    {
        "course_id" : number,
        "study_date" : string,
        "start_time" : string,
        "end_time" : string
    }
```
# Endpoint 
- รูปแบบอื่นที่ไม่ได้กำหนดเฉพาะให้เป็น Response เป็น default errorทั้งหมด
- ทุก Reponse จะมี `status code` คืนมาเป็น Field แรกทั้งหมด
## **1. Account**

## 1.1 เรียกดูข้อมูลของ Account
### Permission : All users
### `GET` /account/\<id>  
### Response  	
`200` Account exist
```
    Return single Account object
```
`404` Account not exist
```
    Return message "Account not exist"
```
## 1.2 เรียกดู Accounts ตามเงื่อนไข  
### Permission : All users
### `GET` /accounts?\<query parematers>
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
        },
        "results" : [All match account objects]
    }
```
## 1.3 ลบ Account
### Permission : System admin only
### `DELETE` /account/\<id>
### Response
`204`  Deleted
``` 
	Return none
```
## 1.4 แก้ไข Account 
### Permission : User ที่ login แล้วและเป็นเจ้าของ หรือ System Admin
### `PUT` /account/\<id> 
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
    Return Account object
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
### `GET` /courses/search?\<query paremeters>
### Query Parameters
| Query   |      Type      |  Default | Note
|---------|-------------|------| --------|
| search  | STRING | None | Partial match from fields(course_name, course description, school_name) |
| type | STRING |None |
| min_price | NUMBER | None | course.price >= query.min_price
| max_price |    NUMBER   |   None | course.price <= query.max_price
| max_student | NUMBER| None| 
| start_date | STRING | None| course.start_date >= query.start_date |
| end_date | STRING | None | course.end_date <= query.end_date |
| is_deleted | BOOLEAN | *False* |
| address | STRING | None |


### Example
```
    /courses?search=KU&type=math&max_price=2000
```
### Response
`200` Search successfully
```
    {
        "count" : number
        "results" : [All match course objects]
    }
```
## 2.2 Search & Filter Schools
### Permission : All users
### `GET` /schools/search?\<query paremeters>
### Query Parameters
| Query   |      Type      |  Default | Note |
|---------|-------------|------| ----- |
| search | STRING | None | Partial match from fields(school_name, description)
| type | STRING | None |
| address | STRING | None |
| status | STRING | OPEN | 

### Example
```
    /schools?search=Hogwarts&type=Magic_school
```
### Response
`200` Search successfully
```
    {
        "count" : number,
        "results" : [All match school objects]
    }
```
---

## **3. Course**
## 3.1 ดูข้อมูลของแต่ละคอร์ส
### Permission : All users
### `GET` /schools/<school_id>/courses/<course_ id>
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
### `POST` /schools/<school_id>/courses
### Request
```
    {
        "school_id" : number,
        "owner_id" : number,
        "course_name" : string,
        "type" : string,
        "room_id" : number,
        "course_description" : string,
        "reserve_open_date" : string,
        "reserve_close_date" : string,
        "start_date" : string,
        "end_date" : string,
        "course_period" : number,
        "course_price" : number,
        "maximum_student" : number,
        "payment_method_text" : string,
        "payment_method_pic" : image
        "study_time" : [<study time object>, ...],
        "teachers" : [<teacher_id> , ...]
    }
```
### Response
`201` create course successfully
```
    Return newly create course object
```
## 3.3 ลบคอร์ส
### Permission : User ที่ login แล้วและเป็นเจ้าของคอร์สนั้น หรือ System Admin
### `DELETE` /schools/<school_id>/courses/<course_id>
### Response
`204` Course deleted
```
    Return deleted course object(which is_delate = true)
```
## 3.4 แก้ไขคอร์ส
### Permission : User ที่ login แล้วและเป็นเจ้าของคอร์สนั้น หรือ System Admin 
### `PUT` /schools/<school_id>/courses/<course_id>
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
### `GET` /schools/<school_id>/courses/<course_id>/teachers
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
### `GET` /schools/<school_id>/courses/<course_id>/students
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
### `PUT` /schools/<school_id>/courses/<course_id>/teachers
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
### `DELETE` /schools/<school_id>/courses/<course_id>/terchers
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
## 3.9 อัพโหลดรูปช่องทางการชำระเงิน
### Permission : User ที่เป็นเจ้าของคอร์ส
### `PUT`
### Request
```
    HTML Form:
        payment_method_pic : image
```
### Response
`200` Upload complete
```
    return uploaded course object
```

## **4. School**
## 4.1 สร้าง School 
### Permission : User ที่ login แล้วเท่านั้น หรือ System Admin
### `POST` /schools
### Request
```
    HTML Form:
        "owner_id" : number,
        "name" : string,
        "description" : string,
        "address" : string,
        "logo_pix" : File,
        "banner_pic" : File,
        "school_type_id" : [<type_id>, . .]
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
    HTML Form:
        <update field> : <update value>,
        .
        .
    
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
## 4.7 ลบครูในโรงเรียน
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
## 4.8 แก้ไขสถานะของโรงเรียน
### Permission : System Admin only
### `PUT` /schools/<school_id>/status
### Request
```
    {
        "status" : <update status>
    }
```
### Response
`200` Update correctly
```
    Return updated school object
```
`404` School not exist
## 4.9 ดูคอร์สทั้งหมดในโรงเรียน
### Permission : All users
### `GET` /schools/<school_id>/courses
### Response
`200` Get successfully
```
    {
        'count' : number,
        'result' : [
            <course object>,
        ]
    }
```
`404` School not exist
## 4.10 เรียกดูผู้ใช้ที่ไม่ได้อยู่ในโรงเรียน
### Permission : All User
### `GET` /schools/<school_id>/others
### Response
`200` Get successfully
```
    {
        'others' : [
            <school_id>,
        ]
    }
```
`404` School not exist
## **5. Rooms**
## 5.1 เพิ่ม/สร้าง/แก้ไขห้องเรียนในโรงเรียน
### Permission : User ที่ loginแล้วและเป็นเจ้าของโรงเรียนนั้น หรือ System Admin
### `PUT` /schools/<school_id>/rooms/<room_id>
### Request
```
    {
        "room_name" : string,
        "maximum_seat" : number,
        "description" : string
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
## 5.2 ดูข้อมูลห้องเรียน
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
## 5.3 ดูห้องเรียนในโรงเรียนทั้งหมด
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

## 5.4 ลบห้องเรียนในโรงเรียน
### Permission : User ที่ loginแล้วและเป็นเจ้าของโรงเรียนนั้น หรือ System Admin
### `DELETE` /schools/<school_id>/rooms/<room_id>
### Response
`204` Deleted
```
    Return none
```
## 5.5 ลบห้องหลายห้องในโรงเรียน
### Permission : เจ้าของ School
### `DELETE` /schools/<school_id>/rooms
### Request
```
    {
        "rooms_id" : [
            room_id1,
            room_id2,
            ...
        ]
    }
```
### Response
`204` Deleted
```
    Return none
``` 
## 5.6 ดูเวลาการใช้ห้องรายห้อง
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

## **6. Open Request**
## 6.1 สร้างคำขอ(ต้องทำหลังสร้างโรงเรียนทันที)
### Permission :User ที่ login แล้ว หรือ System Admin
### `POST` /requests
### Request
```
    HTML Form:
        "account_id" : number,
        "school_id" : number,
        "document" : File,
        "payment_pic" : Image
    
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
| account_id | NUMBER | None |
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
## 6.5 แก้ไขข้อมูลคำขอ(ยกเว้นสถานะคำขอ)
### Permission : User ที่เป็นเจ้าของ คำขอนั้น
### `PUT` /requests/<request_id>
### Request
```
    HTML Form:
        "update field" : update data,
        .
        .
        .
    
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
## 6.6 แก้ไขสถานะคำขอ
### Permission : System Admin only
### `PUT` /requests/<request_id>/status
### Request
```
    {
        "status" : <update status>
    }
```
### Response
`200` Update correctly
```
    Return updated request object
```
`404` Request not exist
## 6.7 ส่งหลักฐานการชำระเงินของการจอง
### Permission : User ที่ login แล้ว
### `PUT` /request/<request_id>/upload_payment
### Request
```
    HTML Form:
        'payment_pic' : image
```
### Response
`200` Update correctly
```
    Return uploaded request
```
`404` Request not exist
## 7. **Course Reservation**
## 7.1 จองคอร์ส
### Permission : User ที่ Login แล้ว
### `POST` /reservations
## Request
```
    HTML Form:
        "course_id" : string,
        "account_id" : string,
        "payment_pic" : string,
    
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
        "status" : string
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
## 7.5 อัพโหลดหลักฐานการจ่ายเงินสำหรับการจองคอร์ส
### Permission : เจ้าของการจองนั้น
### `PUT` /reservations/<reservation_id>/payment
## Request
```
    HTML Form:
        payment_pic : <Upload Picture>
```
## Response
`200` Upload succesfully
```
    Return updated reservation object
```
`400` No Upload file
```
    message : Upload file not included
```
`401` Unautorized
```
    message : Unauthorized
```
`404` Reservation not found
```
    message : Reservation not found
```
## **8. Personal Management**
## 8.1 เรียกรายการจองทั้งหมดของตนเอง
### Permission : User ที่ loginแล้วเท่านั้นและเป็นเจ้าของ account นั้น หรือ System Admin
### `GET` /accounts/<user_id>/reservations
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
## 8.2 เรียกรายการเรียนทั้งหมด(คอร์สที่จองและได้รับการยืนยันแล้ว)
### Permission : User ที่ loginแล้วเท่านั้นและเป็นเจ้าของ account นั้น หรือ System Admin
### `GET` /accounts/<user_id>/courses
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
## 8.3 เรียกรายการสอนทั้งหมด
### Permission : User ที่ loginแล้วเท่านั้นและเป็นเจ้าของ account นั้น หรือ System Admin 
### `GET` /accounts/<user_id>/teachings
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
## 8.4 เรียกวันเวลาที่เรียนสอนทั้งหมด
### Permission : User ที่ loginแล้วเท่านั้นและเป็นเจ้าของ account นั้น หรือ System Admin 
### `GET` /accounts/<user_id>/times
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
## 8.5 เรียกรายการโรงเรียนที่เป็นสมาชิกทั้งหมด
### Permission : User ที่ loginแล้วเท่านั้นและเป็นเจ้าของ account นั้น หรือ System Admin
### `GET` /accounts/<user_id>/schools
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
## 8.6 เรียกรายการโรงเรียนที่เป็นเจ้าของทั้งหมด
### Permission : User ที่ loginแล้วเท่านั้นและเป็นเจ้าของ account นั้น หรือ System Admin 
### `GET` /accounts/<user_id>/owners
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
## **9. Login/Register**
## **10. Notification message**
## 10.1 สร้าง Notification message
### Permission : System Admin
### `POST` /messages
### Request
```
    {
        "account_id" : number,
        "message_noti" : string,
        "expire_date" : string
    }
```
### Response
`200` Created
```
    Return created message
```
## 10.2 เรียก Notification message ทั้งหมดของ account 
### Permission : System Admin และเจ้าของ account
### `GET` /accounts/<account_id>/messages
### Response
`200`
```
    "count" : number,
    "messages" : {
        <notification>,
    }
```
## 10.2 เรียก Notification message เฉพาะที่ยังไม่ expire ของ account 
### Permission : System Admin และเจ้าของ account
### `GET` /accounts/<account_id>/messages_nxp
### Response
`200`
```
    {
    "count" : number,
    "messages" : {
        <notification>,
    }
```
## **11. Statistics**
## 11.1 เรียกดูข้อมูลจำนวน Accounts, Schools, Courses ที่ Active ในปัจจุบัน
### Permission : All Accounts
### `GET` /stats/active
### Response
`200`
```
    {
        "accounts" : number,
        "courses" : number,
        "schools" : number
    }
``` 
## 11.2 เรียกดูข้อมูลจำนวน School Open Request ที่ยังไม่เสร็จสิ้น
### Permission : Admin Only
### `GET` /stats/pendingreq
### Response
`200`
```
    {
        "pending_req" : number
    }
``` 