from django.shortcuts import render,get_object_or_404,get_list_or_404
from .models import FinanceReviews,ProductReviews,QuestionAnswers,Comments
from .serializers import FinanceReviewSerializer,ProductReviewSerializer,CommentSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
# 회원간 소통 할 수 있는 커뮤니티 기능(게시판)을 구현합니다.
# • 게시글 조회, 생성, 삭제, 수정 및 댓글 생성, 삭제 기능은 필수로 구현합니다.
# • 회원의 권한에 따라 다른 동작을 하도록 구성합니다.
# • 예시: 본인이 작성한 게시글 및 댓글만 삭제, 수정 가능하도록 구성합니다.
# • 소통 방식은 자유롭게 구성합니다.
# • 예시: 금융 상품 리뷰 게시판, 내가 가입한 상품 자랑 게시판 등
# 각 게시판 종류별 전체 조회/생성 + 단일 게시판 조회/수정/삭제 구현


#@@@@@@@@@@@@@@@@@@@@@@@게시판 종류별 전체 조회/생성 + 단일 게시판 상세 조회/수정/삭제 구현 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# 필요한 데코레이터 추가하기

@csrf_exempt
@api_view(['GET', 'POST'])
def finance(request):
    if request.method == 'GET':
        financeBoards = FinanceReviews.objects.all().order_by('-created_at')
        serializer = FinanceReviewSerializer(financeBoards, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FinanceReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 필요한 데코레이터 추가하기
@api_view(['GET', 'DELETE', 'PUT'])
def finance_detail(request, finance_pk):
    financeBoard = get_object_or_404(FinanceReviews, pk=finance_pk)

    if request.method == 'GET':
        serializer = FinanceReviewSerializer(financeBoard)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = FinanceReviewSerializer(financeBoard, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author = request.user)
            return Response(serializer.data)
        
    elif request.method == 'DELETE':
        financeBoard.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 필요한 데코레이터 추가하기
@api_view(['GET', 'POST'])
def product(request):
    if request.method == 'GET':
        productBoards = ProductReviews.objects.all().order_by('-created_at')
        serializer = ProductReviewSerializer(productBoards, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'PUT'])
def product_detail(request, product_pk):
    productBoard = get_object_or_404(ProductReviews, pk=product_pk)

    if request.method == 'GET':
        serializer = ProductReviewSerializer(productBoard)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProductReviewSerializer(productBoard, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author = request.user)
            return Response(serializer.data)

    elif request.method == 'DELETE':
        productBoard.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

#@@@@@@@@@@@@@@@@@@@@@@좋아요 기능 구현@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@api_view(['POST'])
def finance_like(request, finance_pk):
    financeBoard = get_object_or_404(FinanceReviews, pk=finance_pk)

    if request.user in financeBoard.like_users.all():
        financeBoard.like_users.remove(request.user)
    else:
        financeBoard.like_users.add(request.user)

    financeBoard.save()
    return Response({'status': 'ok'})


@api_view(['POST'])
def product_like(request, product_pk):
    productBoard = get_object_or_404(ProductReviews, pk=product_pk)

    if request.user in productBoard.like_users.all():
        productBoard.like_users.remove(request.user)
    else:
        productBoard.like_users.add(request.user)

    productBoard.save()
    return Response({'status': 'ok'})


#@@@@@@@@@@@@@@@@@@@@@@댓글 구현@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@api_view(['GET', 'POST'])
def finance_comments(request, finance_pk):
    finance = get_object_or_404(FinanceReviews,pk=finance_pk)
    if request.method == 'GET':
        comments = finance.finance_comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, finance=finance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def product_comments(request, product_pk):
    product = get_object_or_404(ProductReviews,pk=product_pk)
    if request.method == 'GET':
        comments = product.product_comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def comments_detail(request, comment_pk):
    comment = get_object_or_404(Comments, pk=comment_pk)

    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)