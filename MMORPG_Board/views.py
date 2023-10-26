from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView, FormView
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Post, Response
from .forms import PostForm, RespondForm, ResponsesFilterForm
from .task_manager import send_response_email, send_acceptance_email

class Index(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

class PostItem(DetailView):
    model = Post
    template_name = 'publish_item.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Response.objects.filter(author_id=self.request.user.id).filter(post_id=self.kwargs.get('pk')):
            context['respond'] = "Откликнулся"
        elif self.request.user == Post.objects.get(pk=self.kwargs.get('pk')).author:
            context['respond'] = "Мое_объявление"
        return context

class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'create_publication.html'
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm('MMORG_Board.add_post'):
            return HttpResponseRedirect(reverse('account_profile'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return redirect(f'/post/{post.id}')

class EditPost(PermissionRequiredMixin, UpdateView):
    permission_required = 'MMORPG_Board.change_post'
    template_name = 'edit_publication.html'
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        author = Post.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Вы не имеете прав для редактирования объявления!!!!")

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/post/' + str(self.kwargs.get('pk')))

class DeletePost(PermissionRequiredMixin, DeleteView):
    permission_required = 'MMORPG_Board.delete_post'
    template_name = 'delete_publication.html'
    queryset = Post.objects.all()
    success_url = '/index'

    def dispatch(self, request, *args, **kwargs):
        author = Post.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Удалять объявление может только его автор")

class Responses(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'responses.html'
    context_object_name = 'responses'

    def get_context_data(self, **kwargs):
        context = super(Responses, self).get_context_data(**kwargs)
        title = self.request.GET.get('title')
        context['form'] = ResponsesFilterForm(self.request.user, initial={'title': title})
        context['title'] = title

        if title:
            post_id = Post.objects.get(title=title)
            context['filter_responses'] = list(Response.objects.filter(post_id=post_id).order_by('-dateCreation'))
            context['response_post_id'] = post_id.id
        else:
            context['filter_responses'] = list(Response.objects.filter(post_id__author=self.request.user).order_by('-dateCreation'))

        context['myresponses'] = list(Response.objects.filter(author=self.request.user).order_by('-dateCreation'))
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

@login_required
def response_accept(request, pk):
    response = Response.objects.get(id=pk)
    response.status = True
    response.save()
    send_acceptance_email.delay(response_id=pk)
    return HttpResponseRedirect('/responses')

@login_required
def response_delete(request, pk):
    response = Response.objects.get(id=pk)
    response.delete()
    return HttpResponseRedirect('/responses')

class Respond(LoginRequiredMixin, CreateView):
    model = Response
    template_name = 'respond.html'
    form_class = RespondForm

    def form_valid(self, form):
        respond = form.save(commit=False)
        respond.author = self.request.user
        respond.post = Post.objects.get(id=self.kwargs.get('pk'))
        respond.save()
        send_response_email.delay(respond_id=respond.id)
        return redirect(f'/post/{self.kwargs.get("pk")}')
