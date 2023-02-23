from restapi.models import Paper, Expression. Contact
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PaperSerializer, ExpressionSerializer
from .serializers import CommentSerializer, UserSerializer 
from taggit.models import Tag
from .forms import SearchForm, ExpressionForm
from .forms import CommentForm, LoginForm, UserRegistrationForm
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.core import serializers
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .math_logic.interpreter import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST


@api_view(['GET'])
def list_papers(request, tag_slug=None):

    if request.method == 'GET':
        paper_list = Paper.objects.all()
        tag = None

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            paper_list = paper_list.filter(tags__in=[tag])

        
        serializer = PaperSerializer(paper_list, many=True)

        return Response(serializer.data)

@api_view(['GET'])
def paper_detail(request, id):

    if request.method == 'GET':
        paper = Paper.objects.get(id=id)
        comments = paper.comments.filter(active=True)
        comments_serializer = serializers.serialize('json', comments)
        clean_comments = comments_serializer[1:-1]
        to_json = json.loads(clean_comments)
        serializer = PaperSerializer(paper)
       # serializer2 = CommentSerializer(comments)

        return Response({'paper':serializer.data, 'comments': to_json})
    return Response({'error': 'was not a GET request'}, status=400)


@api_view(['GET'])
def post_search(request):

    form = SearchForm()
    results = []
    
    if 'search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            results = Paper.objects.annotate(
                search=SearchVector('abstract', 'title')
                ).filter(search=form.cleaned_data['search'])
            serializer = PaperSerializer(results, many=True)
            return Response(serializer.data)
        return Response({'error': 'invalid search'}, status=400)
    return Response({'error': 'the term search was not in request'}, status=400)

@api_view(['POST'])
def paper_comment(request, paper_id):
    paper = get_object_or_404(Paper, id=paper_id)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment_data = form.cleaned_data
        comment = form.save(commit=False)
        comment.paper = paper
        comment.save()
        
        return Response(comment_data)
    return Response({'error': 'invalid form'})

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return Response({'login': 'Succesful'})
                else:
                    return Response({'login': 'Disabled'})
            else:
                return Response({'Invalid': 'login'})
    else:
        form = LoginForm()

    return Response({'test': 'hello'})

@api_view(['POST']) 
def register(request):
    form = UserRegistrationForm(request.POST)   
    if form.is_valid():
        new_user = form.save(commit=False)
        cd = form.cleaned_data    
        new_user.set_password(cd['password'])

        new_user.save()

        return Response({'account': 'created'}) 

    return Response({'form': 'invalid'})

@api_view(['POST'])
@login_required(login_url='/api/login/')
@csrf_exempt
def user_list(request):
    users = User.objects.filter(is_active=True)
    data_users = serializers.serialize('json', users)

    return Response(data_users)


@api_view(['POST'])
def compute_expression(request):
    form = ExpressionForm(request.POST)
    if form.is_valid():
        new_expr = form.save(commit=False)
        data_expr = form.cleaned_data
        data_expr = data_expr['expr']
        eval_data_expr = eval(data_expr)
        expr_model = Expression(expr=eval_data_expr)
        expr_model.save()
        serializer = ExpressionSerializer(expr_model)

        return Response(serializer.data)


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id in action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user)
            else:
                Contact.objects..filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({
                'status': 'ok'
            })
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})

    return JsonResponse({'status':'error'})
                