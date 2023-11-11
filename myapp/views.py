from datetime import datetime
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from .models import User, category, articles, comments, role
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage


# Create your views here.


def index(request):
    cats = category.objects.all()
    return render(request, 'index.html', {
        'cats': cats,
    })


def dashboard_articles(request):
    cats = category.objects.all()
    us = User.objects.all().order_by('-pk')
    if request.user.roles or request.user.is_superuser:
        arts = articles.objects.all().order_by('-createdAt')
        return render(request, 'dashboard_articles.html', {
            'cats': cats,
            'articles': arts,
            'us': us
        })
    else:
        return HttpResponseRedirect(reverse(index))


def dashboard_categories(request):
    cats = category.objects.all().order_by('-pk')
    us = User.objects.all().order_by('-pk')

    if request.user.roles or request.user.is_superuser:
        arts = articles.objects.all().order_by('-createdAt')
        return render(request, 'dashboard_categories.html', {
            'cats': cats,
            'arts': arts,
            'us': us
        })
    else:
        return HttpResponseRedirect(reverse(index))


def dashboard_users(request):

    cats = category.objects.all()
    us = User.objects.all().order_by('-pk')
    paginator = Paginator(us, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.roles or request.user.is_superuser:
        arts = articles.objects.all().order_by('-createdAt')
        return render(request, 'dashboard_user.html', {
            'cats': cats,
            'us': page_obj,
        })
    else:
        return HttpResponseRedirect(reverse(index))


def editUser(request, user_id):
    cats = category.objects.all()
    roles = role.objects.all()
    us = User.objects.get(pk=user_id)
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        username = request.POST.get('username')
        email = request.POST.get('email')
        RoleText = request.POST.get('roles')
        if RoleText == "":
            Role = role.objects.get(role=RoleText)

        us.first_name = first_name
        us.last_name = last_name
        us.email = email
        us.username = username
        if RoleText == "":
            us.roles = Role
        us.save()
        return HttpResponseRedirect(reverse('dashboard_users'))
    else:
        return render(request, 'editUser.html', {
            'cats': cats,
            'us': us,
            'roles': roles
        })


def sendEmail(request, user_id):
    cats = category.objects.all()
    us = User.objects.get(pk=user_id)
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_email = settings.EMAIL_HOST_USER
        recipient_list = []
        recipient_list.append(us.email)
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponseRedirect(reverse('dashboard_users'))
    else:
        return render(request, 'sendEmail.html', {
            'cats': cats,
        })


def news(request):
    cats = category.objects.all()
    art = articles.objects.all().order_by('-createdAt')

    paginator = Paginator(art, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news.html', {
        'cats': cats,
        'articles': page_obj
    })


def subscribe(request, category_id):
    cats = category.objects.all()
    currentUser = User.objects.get(pk=request.user.id)
    currentUser.categories.add(category_id)

    return HttpResponseRedirect(reverse('categories'))


def unsubscribe(request, category_id):
    cats = category.objects.all()
    currentUser = User.objects.get(pk=request.user.id)
    currentUser.categories.remove(category_id)

    return HttpResponseRedirect(reverse('categories'))


def subscribeD(request, category_id):
    cats = category.objects.all()
    currentUser = User.objects.get(pk=request.user.id)
    currentUser.categories.add(category_id)

    return HttpResponseRedirect(reverse('category', kwargs={'category_id': category_id}))


def unsubscribeD(request, category_id):
    cats = category.objects.all()
    currentUser = User.objects.get(pk=request.user.id)
    currentUser.categories.remove(category_id)

    return HttpResponseRedirect(reverse('category', kwargs={'category_id': category_id}))


def signOut(request):
    cats = category.objects.all()
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def article(request, article_id):
    cats = category.objects.all()
    article = articles.objects.get(pk=article_id)
    article_comments = comments.objects.filter(
        article=article_id).order_by('-date_modified')
    return render(request, 'article.html', {
        'cats': cats,
        'article': article,
        'comments': article_comments
    })


def articleActive(request, article_id):
    article = articles.objects.get(pk=article_id)
    cats = category.objects.all()
    if request.user.roles or request.user.is_superuser:
        if article.isActive == False:
            article.isActive = True
            article.save()
        else:
            article.isActive = False
            article.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def deleteComment(request, comment_id):
    cats = category.objects.all()
    comment = comments.objects.get(pk=comment_id)
    article = comment.article
    if comment.user.pk == request.user.pk:
        comment.delete()
    return HttpResponseRedirect(reverse('article', kwargs={'article_id': article.id}))


def deleteArticle(request, article_id):
    cats = category.objects.all()
    article = articles.objects.get(pk=article_id)
    if request.user.roles or request.user.is_superuser:
        article.delete()
    return HttpResponseRedirect(reverse('news'))


def dashboardDeleteArticle(request, article_id):
    if request.user.roles or request.user.is_superuser:
        cats = category.objects.all()
        article = articles.objects.get(pk=article_id)
        article.delete()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseRedirect(reverse('index'))


def deleteCategory(request, category_id):
    cats = category.objects.all()
    cat = category.objects.get(pk=category_id)
    if request.user.roles or request.user.is_superuser:
        cat.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def profile(request):
    cats = category.objects.all()
    user = User.objects.get(pk=request.user.id)
    subs = user.categories
    commentsFiltered = comments.objects.filter(user=user).count()
    return render(request, 'profile.html', {
        'cats': cats,
        'subs': subs,
        'commentsFiltered': commentsFiltered
    })


def passwordRecover(request, user_id):
    cats = category.objects.all()
    passwordUser = User.objects.get(pk=user_id)
    if passwordUser.id == request.user.id:
        if request.method == 'POST':
            currentPassword = request.POST.get('password')
            newPassword = request.POST.get('newpassword')
            confirm_password = request.POST.get('confirm-password')
            user = authenticate(
                username=request.user.username, password=currentPassword)
            if user is not None:
                if newPassword == confirm_password:
                    user.set_password(newPassword)
                    user.save()
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'passwordChange.html', {
                        'cats': cats,
                        'message': 'Passwords must match.'
                    })
            else:
                return render(request, 'passwordChange.html', {
                    'cats': cats,
                    'message': 'Password incorrect.'
                })
        else:
            return render(request, 'passwordChange.html', {
                'userC': passwordUser,
                'cats': cats,
            })
    else:
        return HttpResponseRedirect(reverse('index'))


def contactUs(request):
    cats = category.objects.all()
    if request.user.is_authenticated:
        if request.method == 'POST':
            message_email = request.POST['email']
            message_subject = request.POST['subject']
            message = request.POST['message']

            send_mail(
                message_subject,
                'email from : ' + message_email + ' ---- message :' + message,
                message_email,
                ['hubnews000@gmail.com'],
            )
            return render(request, 'contact.html', {
                'cats': cats,
                'message': True
            })
        else:
            return render(request, 'contact.html', {
                'cats': cats,
            })
    else:
        return HttpResponseRedirect(reverse(index))


def editProfile(request):
    cats = category.objects.all()
    currentUser = User.objects.get(pk=request.user.pk)
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            confirmation = request.POST['confirmation']
            user = authenticate(
                username=request.user.username, password=password)
            if 'uploadlogo' in request.FILES:
                drr = FileSystemStorage()
                picture = request.FILES['uploadlogo']
                file = drr.save(picture.name, picture)
                file_url = drr.url(file)

                if user is not None:
                    if password == confirmation:
                        currentUser.username = username
                        currentUser.email = email
                        currentUser.picture = picture
                        currentUser.save()
                        return HttpResponseRedirect(reverse('profile'))
                    else:
                        return render(request, "editProfile.html", {
                            "message": "Passwords must match."
                        })
                else:
                    return render(request, 'editProfile.html', {
                        'cats': cats,
                        'message': 'Password incorrect.'
                    })
            else:
                if user is not None:
                    if password == confirmation:
                        currentUser.username = username
                        currentUser.email = email
                        currentUser.save()
                        return HttpResponseRedirect(reverse('profile'))
                    else:
                        return render(request, "editProfile.html", {
                            "message": "Passwords must match."
                        })

                else:
                    return render(request, 'editProfile.html', {
                        'cats': cats,
                        'message': 'Password incorrect.'
                    })

        else:
            return render(request, 'editProfile.html', {
                'cats': cats,
            })
    else:
        return HttpResponseRedirect(reverse('index'))


def signup(request):
    cats = category.objects.all()
    if not request.user.is_authenticated:
        if request.method == "POST" and request.FILES['uploadLogo']:
            drr = FileSystemStorage()
            picture = request.FILES['uploadLogo']
            file = drr.save(picture.name, picture)
            file_url = drr.url(file)
            username = request.POST.get("username")
            email = request.POST.get("email")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            # Ensure password matches confirmation
            password = request.POST.get("password")
            confirmation = request.POST.get("confirmation")
            if password != confirmation:
                return render(request, "signup.html", {
                    "message": "Passwords must match."
                })
            # Attempt to create new user
            try:
                newuser = User.objects.create_user(
                    username=username, email=email, password=password, first_name=first_name, last_name=last_name, picture=picture)
                newuser.save()
                newuser = authenticate(username=username, password=password)

            except IntegrityError:
                return render(request, "signup.html", {
                    "cats": cats,
                    "message": "Username already taken."
                })
            if newuser is not None:
                login(request, newuser)
            return HttpResponseRedirect(reverse('signIn'))
        else:
            return render(request, 'signup.html', {
                'cats': cats,
            })
    else:
        return HttpResponseRedirect(reverse('index'))


def addComment(request, article_id):
    cats = category.objects.all()
    mainArticle = articles.objects.get(pk=article_id)
    content = request.POST.get('comment')
    article = mainArticle
    user = request.user
    b = comments(content=content, user=user, article=article,
                 date_modified=datetime.now())
    b.save()
    return HttpResponseRedirect(reverse('article', kwargs={'article_id': article_id}))


def editArticle(request, article_id):
    cats = category.objects.all()
    article = articles.objects.get(pk=article_id)
    if request.user.roles or request.user.is_superuser:
        if request.method == 'POST':
            articleTitle = request.POST.get('articleTitle')
            articleImage = request.POST.get('articleImage')
            articleTime = request.POST.get('articleTime')
            articleDate = request.POST.get('articleDate')
            articleLocation = request.POST.get('articleLocation')
            articleUpperContent = request.POST.get('articleUpperContent')
            articleUnderContent = request.POST.get('articleUnderContent')
            articleSmallContent = request.POST.get('articleSmallContent')
            articleCategoryText = request.POST['articleCategory']
            articleCategory = category.objects.get(title=articleCategoryText)
            articleSecondImage = request.POST.get('articleSecondImage')
            article.title = articleTitle
            article.image = articleImage
            article.content = articleSmallContent
            article.upperContent = articleUpperContent
            article.underContent = articleUnderContent
            if articleSecondImage:
                article.secondImage = articleSecondImage
            article.location = articleLocation
            article.category = articleCategory
            article.articleTime = articleTime
            article.articleDate = articleDate
            article.save()
            return HttpResponseRedirect(reverse('article', kwargs={'article_id': article_id}))
        else:
            return render(request, 'editArticle.html', {
                'cats': cats,
                'article': article
            })
    else:
        HttpResponseRedirect(reverse('index'))


def newArticle(request):
    cats = category.objects.all()
    arts = articles.objects.all()
    if request.user.roles or request.user.is_superuser:
        if request.method == 'POST':
            articleTitle = request.POST.get('articleTitle')
            articleImage = request.POST.get('articleImage')
            articleTime = request.POST.get('articleTime')
            articleDate = request.POST.get('articleDate')
            articleLocation = request.POST.get('articleLocation')
            articleUpperContent = request.POST.get('articleUpperContent')
            articleUnderContent = request.POST.get('articleUnderContent')
            articleSmallContent = request.POST.get('articleSmallContent')
            articleCategoryText = request.POST['articleCategory']
            articleCategory = category.objects.get(title=articleCategoryText)
            articleSecondImage = request.POST.get('articleSecondImage')
            if articleSecondImage:
                newArticle = articles(title=articleTitle, image=articleImage, category=articleCategory,
                                      content=articleSmallContent, upperContent=articleUpperContent,
                                      secondImage=articleSecondImage, underContent=articleUnderContent,
                                      location=articleLocation, articleTime=articleTime, articleDate=articleDate)
            else:
                newArticle = articles(title=articleTitle, image=articleImage, category=articleCategory,
                                      content=articleSmallContent, upperContent=articleUpperContent, underContent=articleUnderContent,
                                      location=articleLocation, articleTime=articleTime, articleDate=articleDate)
            newArticle.save()
            recipient_list = []
            subject = f" there was a new article HUB200 newslettters"
            art = articles.objects.get(
                title=articleTitle, image=articleImage, category=articleCategory)
            message = f" there was a new article in {articleCategoryText} Category, press here to go to the new article http://127.0.0.1:8000/article/{art.pk}"
            from_email = settings.EMAIL_HOST_USER
            for us in User.objects.all():
                if articleCategory in us.categories.all():
                    recipient_list.append(us.email)
            send_mail(subject, message, from_email, recipient_list)

            return HttpResponseRedirect(reverse('dashboard_articles'))
        else:
            return render(request, 'newArticle.html', {
                'cats': cats,
            })
    else:
        HttpResponseRedirect(reverse('index'))


def editComment(request, comment_id):
    cats = category.objects.all()
    comment = comments.objects.get(pk=comment_id)
    newContent = request.POST.get('newComment')
    if comment.user.pk == request.user.pk:
        comment.content = newContent
        comment.save()
    article = comment.article
    return HttpResponseRedirect(reverse('article', kwargs={'article_id': article.id}))


def newCategory(request):
    if request.user.roles or request.user.is_superuser:
        if request.method == 'POST':
            title = request.POST.get('title')
            image = request.POST.get('image')
            content = request.POST.get('content')
            catSave = category.objects.create(
                title=title, image=image, content=content)
            catSave.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseRedirect(reverse('index'))


def editCategory(request, category_id):
    cats = category.objects.all()
    cat = category.objects.get(pk=category_id)
    if request.user.roles or request.user.is_superuser:
        if request.method == 'POST':
            categoryTitle = request.POST.get('categoryTitle')
            categoryImage = request.POST.get('categoryImage')
            categoryContent = request.POST.get('categoryContent')
            cat.title = categoryTitle
            cat.image = categoryImage
            cat.content = categoryContent
            cat.save()
            return HttpResponseRedirect(reverse('category', kwargs={'category_id': category_id}))
        else:
            return render(request, 'editCategory.html', {
                'cats': cats,
                'category': cat
            })
    else:
        HttpResponseRedirect(reverse('index'))


def archives(request):
    cats = category.objects.all()
    art = articles.objects.filter(isActive=False).order_by('-createdAt')
    return render(request, 'archives.html', {
        'cats': cats,
        'articles': art
    })


def category_page(request, category_id):
    cats = category.objects.all()
    cat = category.objects.get(pk=category_id)
    arts = articles.objects.filter(category=cat).order_by('-createdAt')

    paginator = Paginator(arts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'category.html', {
        'cats': cats,
        'category': cat,
        'articles': page_obj
    })


def categories(request):
    cats = category.objects.all()
    return render(request, 'categories.html', {
        'cats': cats,
    })


def signIn(request):
    cats = category.objects.all()
    if not request.user.is_authenticated:
        if request.method == 'POST':
            user = authenticate(
                username=request.POST['username'], password=request.POST['password'])

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, "signIn.html", {
                    "message": "Invalid username and/or password."
                })
        else:
            return render(request, 'signIn.html', {
                'cats': cats,
            })
    else:
        return HttpResponseRedirect(reverse("index"))
