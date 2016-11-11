# SinopacAPI ![永豐金證券LOGO](http://www.sinotrade.com.tw/Images/logo.png)


[![Coverage Status](https://coveralls.io/repos/github/ypochien/SinopacAPI/badge.svg)](https://www.alvin.tw/cover/)


#### Sinopac Securities Order API Wrapper by Python.

ref : [永豐金API元件下單](http://www.sinotrade.com.tw/ec/eleader1/API.htm)

###Usage
1. Download T4 API.
1. Download this project with T4 Path 
1. modify config.json

        {
            "UserId": "",   #T4_User_ID
            "Password": "", #T4_User_Password
            "eKey": "C:/ekey/551/", #CA Key Path
            "eKeyPassword": "" #CA Key Password
        }
1. import SinopacAPI
1. .....
 
 
###Todolist
* 委託下單封裝
* 回報處理
* 委託刪除封裝
* 研究一下，Windows版本可否使用線上CI與測試的玩具

###Run Test
        $ nosetests --with-coverage --cover-package=SinopacAPI --cover-html --cover-erase
**Any Question?**

    mail me : 
        ypochien (at) gmail.com

