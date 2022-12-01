from logging import getLogger
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import GameRank1, Profile
from .forms import GameRankForm, SingUpForm
LOGGER = getLogger()

def gamerank_list(request):
    ranking = GameRank1.objects.values('username','ranking')
    return render(request, 'gamerank_list.html', {'rankinglist': ranking})

# def update_game_rank(request):
#     game_rank: QuerySet = GameRank1.objects.all()
#     print(game_rank.values())
#     return HttpResponse(game_rank)

class GameRankCreateView(CreateView):

    template_name = 'form.html'
    form_class = GameRankForm
    success_url = reverse_lazy('gamerank_create')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class GameRankUpdateView(UpdateView):

    template_name = 'form.html'
    model = GameRank1
    form_class = GameRankForm
    success_url = reverse_lazy('gamerank')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a GameRank.')
        return super().form_invalid(form)


class RankDeleteView(DeleteView):
    template_name = 'delete.html'
    model = GameRank1
    success_url = reverse_lazy('gamerank')


class GameRankListView(LoginRequiredMixin, ListView):
    template_name = 'gamerank_list.html'
    model = GameRank1

class SignUpView(CreateView):
    template_name = 'form.html'
    form_class = SingUpForm
    success_url = reverse_lazy('gamerank')

class GameRankView(LoginRequiredMixin, View):
   def get(self, request):
       print(request.username)
       profile = Profile.objects.get(user=request.username)
       if profile.clicks_left > 0:
           profile.clicks_left -= 1
           profile.save()
           return render(
               request, template_name='gamerank_list.html',
               context={'GameRank': GameRank1.objects.all()}
           )
       else:
           return render(request, template_name='no_clicks.html')


