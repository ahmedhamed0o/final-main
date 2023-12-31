from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", views.index, name="index"),
    path("news", views.news, name="news"),
    path("signIn", views.signIn, name="signIn"),
    path("signOut", views.signOut, name="signOut"),
    path("newCategory", views.newCategory, name="newCategory"),
    path("addComment/<int:article_id>", views.addComment, name="addComment"),
    path("archives", views.archives, name="archives"),
    path("newArticle", views.newArticle, name="newArticle"),
    path("article/<int:article_id>", views.article, name="article"),
    path("signup", views.signup, name="signup"),
    path("profile", views.profile, name="profile"),
    path("editProfile", views.editProfile, name="editProfile"),
    path("editArticle/<int:article_id>", views.editArticle, name="editArticle"),
    path("subscribe/<int:category_id>", views.subscribe, name="subscribe"),
    path("subscribeD/<int:category_id>", views.subscribeD, name="subscribeD"),
    path('articleActive/<int:article_id>',
         views.articleActive, name="articleActive"),
    path("passwordRecover/<int:user_id>",
         views.passwordRecover, name="passwordRecover"),
    path("editComment/<int:comment_id>", views.editComment, name="editComment"),
    path("unsubscribeD/<int:category_id>",
         views.unsubscribeD, name="unsubscribeD"),
    path("unsubscribe/<int:category_id>",
         views.unsubscribe, name="unsubscribe"),
    path("editCategory/<int:category_id>",
         views.editCategory, name="editCategory"),
    path("deleteCategory/<int:category_id>",
         views.deleteCategory, name="deleteCategory"),
    path("deleteArticle/<int:article_id>",
         views.deleteArticle, name="deleteArticle"),
    path("dashboardDeleteArticle/<int:article_id>",
         views.dashboardDeleteArticle, name="dashboardDeleteArticle"),
    path("deleteComment/<int:comment_id>",
         views.deleteComment, name="deleteComment"),
    path("categories", views.categories, name="categories"),
    path("contactUs", views.contactUs, name="contactUs"),
    path("category/<int:category_id>", views.category_page, name="category"),
    path("editUser/<int:user_id>", views.editUser, name="editUser"),
    path("sendEmail/<int:user_id>", views.sendEmail, name="sendEmail"),
    path("dashboard/articles", views.dashboard_articles, name="dashboard_articles"),
    path("dashboard/users", views.dashboard_users, name="dashboard_users"),
    path("dashboard/categories", views.dashboard_categories,
         name="dashboard_categories"),

]
