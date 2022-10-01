#from time import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from numpy import dtype
from .models import Post
from .forms import PostForm
from django.views.generic import UpdateView
from django.urls import reverse
from django.contrib.auth.models import User

from janome.tokenizer import Tokenizer
from wordcloud import WordCloud

def wordcloudmake(text, pk):
    lines = text.split("\r\n")
    words_list = []
    # tk = Tokenizer(wakati=True)
    for line in lines:
    # tk = Tokenizer()
        tokens = Tokenizer().tokenize(line)
        stop_words = ["あなた","私","こと","人","よう","もの","これ", "いま","の","時","それ","ところ"]
        for token in tokens:
            token_list = token.part_of_speech.split(",")[0]
            if token_list in ["名詞"]:
                if token.surface not in stop_words:
                    words_list.append(token.base_form)
    
    words = ' '.join(words_list)
    # words = " ".join(tokens)
    font_path=r'C:\Windows\Fonts\Meiryo.ttc'
    wordcloud = WordCloud(background_color=(240,255,255),
                          font_path=font_path,
                          width=800,
                          height=400,
                        #   mask = msk,
                        #   contour_width=1,
                        #   contour_color="black",
                          stopwords=set(stop_words)).generate(words)
    # wordcloud = WordCloud(font_path=r'C:\Windows\Fonts\Meiryo.ttc').generate(words)
    fn = "./media/wordcloud"+str(pk)+".png"
    wordcloud.to_file(fn)
    return fn
    # wordcloud.to_file('./media/wordcloud'+str(pk)+'.png')



# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html',{'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html',{'post': post})

# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form})

def post_wc(request, pk):
    post = get_object_or_404(Post, pk=pk)
    txt = post.text
    wordcloudmake(txt, pk)
    fn = "wordcloud"+str(pk)+".png"
    post.thumb = fn
    post.save()
    return render(request, 'blog/post_detail.html',{'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})

class PostUpdate(UpdateView):
    template_name = 'blog/post_edit.html'
    model = Post
    fields = ["title","text","thumb"]
    
    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk":self.object.pk})
