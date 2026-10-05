from django.shortcuts import render
from django.http import HttpResponse, request
from myapp.models import *
from django.forms.models import model_to_dict
from django.shortcuts import redirect
from django.http import JsonResponse

def search_list(request):

    # ============================================================
    # 初始化變數
    # 避免網址沒有 cname 參數時，
    # resultlist、data_count、status 等變數不存在
    # ============================================================
    resultlist = []
    errormessage = ""
    status = False
    data_count = 0

    # ============================================================
    # ORM 語法
    # 判斷網址是否有 cname 參數
    # 例如：
    # /search_list/?cname=潘
    # ============================================================
    if 'cname' in request.GET:

        # 取得使用者輸入的姓名
        cname = request.GET['cname']

        # ========================================================
        # 模糊比對（比照首頁搜尋）：
        # 先移除頭尾空白，再依空白切成多個關鍵字，
        # 每個關鍵字都用 icontains 對姓名、生日、電子郵件、
        # 電話、地址進行模糊搜尋，關鍵字之間、欄位之間都是 OR。
        # 並依 cid 由大到小排序
        # ========================================================
        from django.db.models import Q
        keywords = cname.strip().split()

        query = Q()
        for keyword in keywords:
            query |= (
                Q(cname__icontains=keyword) |
                Q(cbirthday__icontains=keyword) |
                Q(cemail__icontains=keyword) |
                Q(cphone__icontains=keyword) |
                Q(caddr__icontains=keyword)
            )

        resultlist = Student.objects.filter(query).order_by('-cid')

        # ========================================================
        # 將查詢到的學生資料印到 VS Code Terminal
        # ========================================================
        for student in resultlist:
            print(model_to_dict(student))

        # ========================================================
        # 計算查詢結果筆數
        # ========================================================
        data_count = resultlist.count()

        # ========================================================
        # 測試「查無資料」時，可以暫時取消下面這行註解
        #
        # 注意：
        # 一旦設成 []，就會故意把真正查到的資料清掉
        # ========================================================
        # resultlist = []

        # ========================================================
        # 判斷查詢結果是否為空
        # ========================================================
        if not resultlist:
            errormessage = "查無資料."
            status = False
            data_count = 0
        else:
            # 有找到資料
            errormessage = ""
            status = True

    else:
        # ========================================================
        # 使用者還沒有送出 cname 查詢參數
        # ========================================================
        errormessage = "請輸入姓名進行搜尋。"

    # ============================================================
    # locals() 將目前函式內的變數傳給 search_list.html
    # 包括：
    # resultlist
    # errormessage
    # status
    # data_count
    # cname（有搜尋時）
    # ============================================================
    return render(request, 'search_list.html', locals())

def api_search_list(request):
    data = list(Student.objects.values())
    return JsonResponse(data, safe=False)
def search_name(request):

    # 顯示搜尋學生頁面
    return render(request, 'search_name.html')


def index(request):
    if 'site_search' in request.GET:
        site_search = request.GET['site_search']
        search_list = site_search.strip()      #remove leading and trailing spaces
        keywords = search_list.split()
        print(f"keywords: {keywords}")

        # 根據關鍵字進行查詢cnaem , birthday, email, phone, address
        from django.db.models import Q
        query = Q()
        for keyword in keywords:   #|=相似 (OR)   i=i+1
            query |= (
                Q(cname__icontains=keyword) |
                Q(cbirthday__icontains=keyword) |
                Q(cemail__icontains=keyword) |
                Q(cphone__icontains=keyword) |
                Q(caddr__icontains=keyword)
            )

        resultlist = Student.objects.filter(query).order_by('cid')
    else:
        resultlist = Student.objects.all().order_by('cid')

    #分頁設定
    from django.core.paginator import Paginator
    paginator = Paginator(resultlist, 3)  # 每頁顯示 3 筆資料
    page_number = request.GET.get('page')
    resultlist = paginator.get_page(page_number)
    page_obj = resultlist

     # 說明:
    # page_obj 是一個包含該頁資料的物件
    # page_obj.number 目前頁碼
    # page_obj.paginator.num_pages 總頁數
    # page_obj.paginator.page_range 所有可用的頁碼（從 1 開始）
    # page_obj.previous_page_number 上一頁的頁碼
    # page_obj.next_page_number 下一頁的頁碼

    # page_obj.has_next 是否有下一頁
    # page_obj.has_previous 是否有上一頁
    # page_obj.object_list 該頁的資料
    

    # 將資料印到 VS Code Terminal
    for student in resultlist:
        print(model_to_dict(student))

    # 計算目前學生總筆數
    # data_count = resultlist.count()
    data_count = paginator.count    #要改成使用分頁器的總筆數

    # 顯示首頁
    return render(request, 'index.html', locals())  # page_obj is available in the template as resultlist

def post(request):

    if request.method == "POST":
        # 在這裡處理 POST 請求的邏輯
        cname = request.POST.get('cname')
        csex = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr = request.POST.get('caddr')
        print(f"cname: {cname}, csex: {csex}, cbirthday: {cbirthday}, cemail: {cemail}, cphone: {cphone}, caddr: {caddr}")

        # 建立新的學生資料
        Student.objects.create(
            cname=cname,
            csex=csex,
            cbirthday=cbirthday,
            cemail=cemail,
            cphone=cphone,
            caddr=caddr
        )
        return redirect('index')  # 新增資料後導向首頁
   

    # 顯示表單頁面
    return render(request, 'post.html')

# def edit(request, id):

#     # ==========================================================
#     # POST：之後用來接收「修改後」的學生資料
#     # ==========================================================
#     if request.method == 'POST':

#         return HttpResponse(
#             f"This is a POST request for editing student"
#         )

#     # ==========================================================
#     # GET：使用者第一次按「編輯」時
#     # 依照 cid 找出該學生資料，送到 edit.html
#     # ==========================================================
#     else:

#         print(f"id: {id}")

#         # ★ 注意：你的 Model 是 Student，不是 students
#         # 依照網址傳進來的 id 查詢學生
#         obj_data = Student.objects.get(cid=id)

#         # 在 Terminal 印出資料，方便確認
#         print(model_to_dict(obj_data))

#         # 將 obj_data 傳給 edit.html
#         return render(
#             request,
#             'edit.html',
#             locals()
#         )

def edit(request, id):

    # =========================================================
    # POST：按下修改按鈕
    # =========================================================
    if request.method == 'POST':
        #GPT Version:
        # # =====================================================
        # # ★ 1. 先取得要修改的學生物件
        # #
        # # 例如：
        # # /edit/16/
        # #
        # # id = 16
        # # =====================================================
        # obj_data = students.objects.get(cid=id)


        # # =====================================================
        # # ★ 2. 把 POST 過來的新資料
        # #    放進 obj_data
        # # =====================================================
        # obj_data.cname = request.POST.get('cname')
        # obj_data.csex = request.POST.get('csex')
        # obj_data.cbirthday = request.POST.get('cbirthday')
        # obj_data.cemail = request.POST.get('cemail')
        # obj_data.cphone = request.POST.get('cphone')
        # obj_data.caddr = request.POST.get('caddr')


        # # =====================================================
        # # ★ 3. 儲存
        # #
        # # Django 會把 obj_data 的修改寫回資料庫
        # # =====================================================
        # obj_data.save()
        
        # ----------------------------------------------------------#

        #Teacher Version:
        # =====================================================
        # 取得 edit.html POST 過來的資料
        # =====================================================
        cname = request.POST.get('cname')
        csex = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr = request.POST.get('caddr')


        # =====================================================
        # Terminal 顯示收到的資料
        # =====================================================
        print(f'id: {id}')

        print(
            f'cname: {cname}, '
            f'csex: {csex}, '
            f'cbirthday: {cbirthday}, '
            f'cemail: {cemail}, '
            f'cphone: {cphone}, '
            f'caddr: {caddr}'
        )


        # =====================================================
        # ★ 老師的 UPDATE 寫法
        #
        # 找到 cid=id 的學生
        # 然後直接 UPDATE
        # =====================================================
        Student.objects.filter(cid=id).update(
            cname=cname,
            csex=csex,
            cbirthday=cbirthday,
            cemail=cemail,
            cphone=cphone,
            caddr=caddr
        )


        # =====================================================
        # ★ UPDATE 完成後重新查一次
        #
        # 因為上面使用的是 .update()
        # 並沒有建立 obj_data
        #
        # 如果想 print(model_to_dict(obj_data))
        # 就必須重新 get()
        # =====================================================
        obj_data = Student.objects.get(cid=id)

        print("修改成功：")

        print(model_to_dict(obj_data))


        # =====================================================
        # ★ 修改完成後回首頁
        #
        # 例如：
        # /index/?updated=16
        #
        # index.html 就會讓第 16 Row 執行 Fade 效果
        # =====================================================
        return redirect(f'/index/?updated={id}')


    # =========================================================
    # GET：從首頁按「編輯」
    # =========================================================
    else:

        print(f'id: {id}')


        # =====================================================
        # 取得要編輯的學生資料
        # =====================================================
        obj_data = Student.objects.get(cid=id)


        # Terminal 顯示目前學生資料
        print(model_to_dict(obj_data))


        # =====================================================
        # 顯示 edit.html
        # =====================================================
        return render(
            request,
            'edit.html',
            locals()
        )

from django.db import connection
from django.http import JsonResponse

def delete(request, id):
    # 原本
    obj_data = Student.objects.get(cid=id)

    if request.method == "POST":

        # ★ 只新增這段：先清除 Scorelist
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM myapp_scorelist WHERE cID_id = %s",
                [id]
            )

        # 原本
        obj_data.delete()

        # 原本
        return redirect(f'/index/?deleted={id}')

    # ★ 保持你原本寫法，不要改成 {"student": obj_data}
    return render(request, 'delete.html', locals())
 

def api_search_list(request):
    resultList = Student.objects.all().order_by('cid')
    for item in resultList:
        print(model_to_dict(item))

    dataresultList = list(resultList.values()) # queriset 轉成 list，以便JsonResponse使用
    return JsonResponse(dataresultList, safe=False)   #safe=False 表示可以傳回非字典型態的資料
                                                      #safe=True 只允許傳回字典型態的資料


def getItem(request, id):
    print(f'id: {id}')
    try:
        obj_data = Student.objects.get(cid=id) # 取得指定 ID 的學生資料
        data = model_to_dict(obj_data)     # 將 Django 模型物件轉換成字典，以便 JsonResponse 使用
        return JsonResponse(data, safe=True)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, safe=True)


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

#取消CSRF驗證
@csrf_exempt
def createItem(request):
    try:

        # ============================================================
        # 只允許 GET / POST
        # ============================================================
        if request.method not in ('GET', 'POST'):
            return JsonResponse(
                {'error': 'Method not allowed'},
                status=400
            )

        # ============================================================
        # 用 Postman 送 POST 時，如果參數是寫在網址的 Query String
        # (例如：http://xxx/createItem/?cname=bill&cex=M&birthday=2026-09-18)
        # 這種參數只會出現在 request.GET，不會出現在 request.POST
        # (request.POST 只有 Body 是 form-data / x-www-form-urlencoded 時才有值)
        # 所以這裡優先讀 request.POST，沒有的話再退回 request.GET
        # 欄位名稱同時支援完整名稱(csex/cbirthday)及簡寫(cex/birthday)
        # ============================================================
        params = request.POST if request.POST else request.GET

        cname = params.get('cname', '')
        csex = params.get('csex') or params.get('cex', '')
        cbirthday = params.get('cbirthday') or params.get('birthday', '')
        cemail = params.get('cemail', '')
        cphone = params.get('cphone', '')
        caddr = params.get('caddr', '')

        print(f".......{request.method}.......")

        print(
            f'cname: {cname}, '
            f'csex: {csex}, '
            f'cbirthday: {cbirthday}, '
            f'cemail: {cemail}, '
            f'cphone: {cphone}, '
            f'caddr: {caddr}'
        )

        # ============================================================
        # cname 為必填欄位，沒有的話直接回傳錯誤
        # ============================================================
        if not cname:
            return JsonResponse(
                {'error': 'cname is required'},
                status=400
            )

        # ============================================================
        # 建立新的學生資料並寫入資料庫
        # ============================================================
        obj_data = Student.objects.create(
            cname=cname,
            csex=csex,
            cbirthday=cbirthday or None,
            cemail=cemail,
            cphone=cphone,
            caddr=caddr
        )

        data = model_to_dict(obj_data)

        print("新增成功：")
        print(data)

        return JsonResponse(data, safe=True, status=201)

    except Exception as e:

        # 開發階段把真正錯誤印出來，比較容易除錯
        print(f"createItem error: {e}")

        return JsonResponse(
            {
                'error': 'Invalid request',
                'detail': str(e)
            },
            status=400
        )

@csrf_exempt
def updateItem(request, id):
    try:
        obj_data = Student.objects.get(cid=id)
        if request.method == 'GET':
            cname = request.GET.get('cname', '')
            csex = request.GET.get('csex') or request.GET.get('cex', '')
            cbirthday = request.GET.get('cbirthday') or request.GET.get('birthday', '')
            cemail = request.GET.get('cemail', '')
            cphone = request.GET.get('cphone', '')
            caddr = request.GET.get('caddr', '')

            obj_data.cname = cname
            obj_data.csex = csex
            obj_data.cbirthday = cbirthday or None
            obj_data.cemail = cemail
            obj_data.cphone = cphone
            obj_data.caddr = caddr
            print(f"cname: {cname}, csex: {csex}, cbirthday: {cbirthday}, cemail: {cemail}, cphone: {cphone}, caddr: {caddr}")
            obj_data.save()

            # data = model_to_dict(obj_data)

            # print("更新成功：")
            # print(data)

            # return JsonResponse(data, safe=True, status=200)
            return JsonResponse(
                            {'success': 'Item updated successfully'},
                            status=200
                        )

        elif request.method == 'POST':
            cname = request.POST.get('cname', '')
            csex = request.POST.get('csex') or request.POST.get('cex', '')
            cbirthday = request.POST.get('cbirthday') or request.POST.get('birthday', '')
            cemail = request.POST.get('cemail', '')
            cphone = request.POST.get('cphone', '')
            caddr = request.POST.get('caddr', '')

            obj_data.cname = cname
            obj_data.csex = csex
            obj_data.cbirthday = cbirthday or None
            obj_data.cemail = cemail
            obj_data.cphone = cphone
            obj_data.caddr = caddr
            print(f"cname: {cname}, csex: {csex}, cbirthday: {cbirthday}, cemail: {cemail}, cphone: {cphone}, caddr: {caddr}")
            obj_data.save()

            return JsonResponse(
                            {'success': 'Item updated successfully'},
                            status=200
                        )
        else:
            return JsonResponse(
                {'error': 'Method not allowed'},
                status=400
            )
    except Exception as e:
        print(f"updateItem error: {e}")
        return JsonResponse(
            {
                'error': 'Invalid request',
                'detail': str(e)
            },
            status=400
        )
@csrf_exempt
def deleteItem(request, id):
    try:
        obj_data = Student.objects.get(cid=id)  #指定id學生
        obj_data.delete()
        return JsonResponse(
            {'success': 'Item deleted successfully'},
            status=200
        )
    except Exception as e:
        print(f"deleteItem error: {e}")
        return JsonResponse(
            {
                'error': 'Invalid request',
                'detail': str(e)
            },
            status=400
        )