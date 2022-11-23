#from time import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from dg.settings import MEDIA_ROOT, MEDIA_URL
from .models import Post, Simg
from .forms import PostForm, SimgForm
from django.views.generic import UpdateView
from django.urls import reverse
from django.contrib.auth.models import User

from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
from django.conf import settings
import os
import cv2
from tensorflow.python.keras.models import load_model
import numpy as np

if settings.DEBUG:
    font_path=r'C:\Windows\Fonts\Meiryo.ttc'
    media_path = MEDIA_ROOT
else:
    font_path=r'/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'
    media_path = "/home/dpcob/dpcob.pythonanywhere.com/media/"

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
    # if settings.DEBUG:
    #     font_path=r'C:\Windows\Fonts\Meiryo.ttc'
    # else:
    #     font_path=r'/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'
    wordcloud = WordCloud(background_color=(240,255,255),
                          font_path=font_path,
                          width=800,
                          height=400,
                        #   mask = msk,
                        #   contour_width=1,
                        #   contour_color="black",
                          stopwords=set(stop_words)).generate(words)
    # wordcloud = WordCloud(font_path=r'C:\Windows\Fonts\Meiryo.ttc').generate(words)
    fn = "wordcloud"+str(pk)+".png"
    # fnp = os.path.join(MEDIA_ROOT, fn)
    fnp = os.path.join(media_path, fn)
    wordcloud.to_file(fnp) # ローカルで使うときはパスが必要
    # post.thumb = fnp
    # post.save()
    # return fnp
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
    # fnp = os.path.join(media_path, fn)
    post.thumb = fn # DB登録はパスを省く
    # post.thumb = fnp
    post.save()
    return render(request, 'blog/post_detail.html',{'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})

def souun_new(request):
    # simg = Simg(updated_by=request.user)
    if request.method == "POST":
        form = SimgForm(request.POST, request.FILES)
        if form.is_valid():
            simg = form.save(commit=False)
            # post.author = request.user
            # post.published_date = timezone.now()
            simg.save()
            return redirect('souun')
    else:
        form = SimgForm()
    return render(request, 'blog/souun_new.html', {'form': form})

def souun(request):
    simg = Simg.objects.all()
    return render(request, 'blog/souun.html', {'simg': simg})

def tfjdg(imgf, jdg):
    IS = 224
    classes = ["双雲", "パンピー"]
    
    fnp = os.path.join(media_path, "souun.h5")
    #modelへ保存データを読み込み
    model = load_model(fnp)

    model.summary()

    fnp = os.path.join(media_path, str(imgf))
    iarry = cv2.imread(fnp, cv2.IMREAD_GRAYSCALE)
    iarry_resize = cv2.resize(iarry, (IS, IS))

    X = []
    X.append(iarry_resize)
    X = np.array(X)

    result = model.predict([X])[0]
    predicted = result.argmax()
    percentage = int(result[predicted] * 100)
    print(predicted)
    jdg = '{0}({1}%)'.format(classes[predicted], percentage)

    # jdg = "Change String"
    return jdg

def jdg_souun(request, pk):
    simg = get_object_or_404(Simg, pk=pk)
    simg.jdg = tfjdg(simg.imgf, simg.jdg)
    simg.save()
    simg = Simg.objects.all()
    return render(request, 'blog/souun.html', {'simg': simg})
    # return render(request, 'blog/souun_jdg.html', {'simg': simg})

# def souun_detail(request, pk):
#     simg = get_object_or_404(Simg, pk=pk)
#     return render(request, 'blog/souun_detail.html', {'simg': simg})

class PostUpdate(UpdateView):
    template_name = 'blog/post_edit.html'
    model = Post
    fields = ["title","text","thumb"]
    
    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk":self.object.pk})
