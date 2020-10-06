from django.shortcuts import render
from django.http.response import HttpResponse
from django.db import connection
from backend.model.company import COMPANY

class companycontroller:
    def __init__(self):
        return

    def showcompanylist(request):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
                backend_company.code,
                front_company.address,
                front_company.built_date,
                front_company.company_name,
                front_company.class_name,
                front_company.monitor_flag,
                front_company.related_bussiness
            FROM
                backend_company
            LEFT JOIN
                front_company
            on backend_company.code=front_company.company_code
            order by front_company.monitor_flag desc,front_company.class_name desc
            """)
        results = cursor.fetchall()
        companylist =[]

        for temp in results:
            com ={}
            com['company_code']         =temp[0]
            com['address']              =temp[1]
            com['built_date']           =temp[2]
            com['company_name']         =temp[3]
            com['class_name']           =temp[4]
            com['monitor_flag']         =temp[5]
            com['related_bussiness']    =temp[6]
            companylist.append(com)
        context ={
            'resultlist'        :companylist,

        }
        return render(request, 'company/companylist.html', context)


    def addNewCompany(request):
        cursor = connection.cursor()
        cursor.execute(
            """
                select back.code
                from
                backend_company back
                where back.code not in
                (select
                company_code from front_company
                );
            """)
        results = cursor.fetchall()
        companylist =[]
        for temp in results:
            com ={}
            com['company_code']         =temp[0]
            companylist.append(com)
        context ={
            'resultlist'        :companylist,

        }

        return render(request, 'company/getnewcompany.html', context)


