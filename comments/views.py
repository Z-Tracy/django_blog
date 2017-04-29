from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm


# Create your views here.
def post_comment(request, post_pk):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来
    # 这里我们使用了django提供的一个快捷函数 get_object_or_404
    # 这个函数的作用是当获取的文章（POST）存在时，则获取，否则返回404
    post = get_object_or_404(Post, pk=post_pk)
    #
    # http请求有get和post两种方法，一般用户通过变动提交数据都通过post请求
    # 因此只有当用户的请求为post时才需要处理表单数据
    if request.method == 'POST':

        # 利用这些数据构造了CommentForm的实例，这样django的表单就生成了
        form = CommentForm(request.POST)

        # 当调用form.is_valid()方法时，django自动帮我们检查表单的数据是否符合格式要求
        if form.is_valid():
            # 检查数据是否合法，调用save方法保存数据到数据库
            # commit=False的作用是仅仅利用表单的数据生成Comment的模型类的实例但还不保存到数据库
            comment = form.save(commit=False)
            # 将评论和被评论的文章关联起来
            comment.post = post
            # 最终将评论数据保存到数据库，调用模型实例的save方法
            comment.save()

        else:
            # 检查数据不合法，重新渲染详情页，并且渲染表单的错误
            # 因此我们传了三个模型变量给detali.html,一个是文章（Post），一个是表单 form，一个是评论列表
            # 注意这里我们用到了 post.comment_set.all() 方法,其作用是获取这篇 post 下的的全部评论
            # 因为 Post 和 Comment 是 ForeignKey 关联的， 因此使用 post.comment_set.all() 反向查询全部评论，正向查询就直接是 comment.post
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            return render(request,'blog/detail.html', context=context)
    # 不是post请求的话，说明用户没有提交评论，重定向到文章详情页
    return redirect(post)

