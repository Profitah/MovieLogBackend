import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Movie

logger = logging.getLogger(__name__)

# get 요청 처리
def MovieList(request):
    if request.method == "GET":
        try:
            movies = Movie.objects.all().values()  
            return JsonResponse(list(movies), safe=False)
        except Exception as e:
            logger.error(f"[ERROR]  조회 오류 : {e}", exc_info=True)  
            return JsonResponse({"message": "오류가 발생했습니다. 관리자에게 문의하세요."}, status=500)  
        
# post 요청 처리
@csrf_exempt       
def AddMovie(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  
            if not data.get("title") or not data.get("release") or not data.get("description"):  
                return JsonResponse({"message": "데이터를 입력해주세요"}, status=400)

            movie = Movie.objects.create(
                title=data.get("title"),
                description=data.get("description", ""),  
                release=data.get("release"),
            )
            return JsonResponse({"message": "저장 되었습니다"}, status=201)

        except Exception as e:
            logger.error(f"[ERROR] 추가 오류 : {e}", exc_info=True)  
            return JsonResponse({"message": "오류가 발생했습니다. 관리자에게 문의하세요."}, status=500)
        
# delete 요청 처리
@csrf_exempt
def DeleteMovie(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            title = data.get("title")
            release = data.get("release")
            description = data.get("description")

            Movie.objects.filter(title=title, release=release, description=description).delete()
            return JsonResponse({"message": "삭제되었습니다."}, status=200)
        
        except Exception as e:
            logger.error(f"[ERROR] 삭제 오류 발생: {e}", exc_info=True)
            return JsonResponse({"message": "오류가 발생했습니다. 관리자에게 문의하세요."}, status=500)
        
#patch 요청 처리
@csrf_exempt
def UpdateMovie(request):
    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
            title = data.get("title")
            release = data.get("release")
            description = data.get("description")

            new_title = data.get("new_title", None) 
            new_release = data.get("new_release", None)  
            new_description = data.get("new_description", None) 

            movie = Movie.objects.filter(title=title, release=release, description=description).first()

            if new_title:
                movie.title = new_title
            if new_release:
                movie.release = new_release
            if new_description:
                movie.description = new_description

            movie.save()

            return JsonResponse({"message": "수정 되었습니다."}, status=200)
        
        except Exception as e:
            logger.error(f"수정 오류 : {e}", exc_info=True)
            return JsonResponse({"message": "오류가 발생했습니다. 관리자에게 문의하세요."}, status=500)