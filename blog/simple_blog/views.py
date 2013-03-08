# Create your views here.
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response

from django.forms import ModelForm
from django.core.context_processors import csrf
from simple_blog.models import *

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ["post"]


def add_comment(request, pk):
	"""Add a new comment"""
	p = request.POST

	if p.has_key("body") and p["body"]:
		author = "Anonymous"
		if p["author"]: author = p["author"]
		comment = Comment(post=Post.objects.get(pk=pk))
		cf = CommentForm(p, instance=comment)
		cf.fields["author"].required = False

		comment = cf.save(commit=False)
		comment.author = author
		comment.save()
	return HttpResponseRedirect(reverse("simple_blog.views.post", args=[pk]))

def post(request, pk):
    """Single post with comments and a comment form."""
    post = Post.objects.get(pk=int(pk))
    comments = Comment.objects.filter(post=post)
    d = dict(post=post, comments=comments, form=CommentForm(), user=request.user)
    d.update(csrf(request))
    return render_to_response("blog/post.html", d)

def delete_comment(request, post_pk, pk=None):
	"""Delete comments with primary key """
	if not pk: pklst = request.POST.getlist("delete")
	else: pklst = [pk]

	for pk in pklst:
	    Comment.objects.get(pk=pk).delete()
	return HttpResponseRedirect(reverse("simple_blog.views.post", args=[post_pk])) 

def main(request):
    """Main listing."""
    posts = Post.objects.all().order_by("-created")
    paginator = Paginator(posts, 2)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    return render_to_response("blog/list.html", dict(posts=posts, user=request.user))