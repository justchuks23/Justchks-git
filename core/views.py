from os.path import join

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TimeModel
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import View, ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from .cron import run_user_zoom_downloader
import logging
from .forms import AdminLoginForm, ZoomYoutubeUploadForm, UploadYoutubeForm
from .models import UserCredential, ZoomYouTubeFile, ZoomVideoCredential
from .tasks import upload_to_youtube_from_dir

from src.get_google_refresh_token import get_token
logger = logging.getLogger(__name__)
# Create your views here.


class AdminLoginView(View):

    def get(self, request):
        admin_user_form = AdminLoginForm()
        return render(request, 'forms/login.html', {'admin_user_form': admin_user_form})

    def post(self, request):
        admin_user_form = AdminLoginForm(request, data=request.POST)
        if admin_user_form.is_valid():
            username = admin_user_form.cleaned_data['username']
            password = admin_user_form.cleaned_data['password']
            admin = authenticate(request, username=username, password=password)

            if admin is not None and admin.is_staff:
                login(request, admin)
                return redirect('main:home', admin.id)
        messages.error(request, 'Invalid Password or Username')
        return redirect('main:admin_login')


class AdminLogoutView(LogoutView):
    next_page = reverse_lazy('main:admin_login')


class AdminPasswordResetView(PasswordResetView):
    template_name = 'forms/password_reset.html'
    success_url = reverse_lazy('main:password_reset_done')
    email_template_name = 'forms/password_email_reset_link.html'


class AdminPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'forms/reset_done.html'


class AdminPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'forms/reset_confirm.html'

    def get_success_url(self):
        return reverse_lazy('main:password_reset_complete')


class AdminPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'forms/reset_complete.html'


class ZoomVideoListView(LoginRequiredMixin, ListView):
    template_name = 'home/dashboard.html'
    context_object_name = 'zoom_files'
    paginate_by = 3
    model = ZoomYouTubeFile


class GetZoomVideoView(LoginRequiredMixin, View):
    Timeview = TimeModel
    def get(self, request, *args, **kwargs):
        return redirect('main:home', self.kwargs.get('pk'))
        
    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')
        try:
            official = UserCredential.objects.get(user=user_id)
            get_zoom = ZoomVideoCredential.objects.get(user=official.id)

            official_data = {
                'user': official.user.id,
                'zoom_client_id': official.zoom_client_id,
                'zoom_client_secret': official.zoom_client_secret,
                'zoom_account_id': official.zoom_account_id,
                'zoom_email': official.zoom_email,
                'min_duration': get_zoom.min_duration,
                'from_day_delta': get_zoom.start_date,
                'end_date': get_zoom.end_date,
                'page_size': get_zoom.page_size
            }

            run_user_zoom_downloader.delay(official_data)

            messages.success(request, 'Zoom video download started. Wait a minute to view all the videos')

        except UserCredential.DoesNotExist:
            MESSAGE = 'The user does not seem to be have the credentials for zoom. Please contact the admin'
            messages.error(request, MESSAGE)
            return redirect('main:home', user_id)

        return redirect('main:home', user_id)


class ZoomVideoDisplayView(LoginRequiredMixin, DetailView):
    model = ZoomYouTubeFile
    template_name = 'home/details.html'
    context_object_name = 'zoom_video'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        admin_user = self.kwargs.get('pk')
        zoom_video = self.get_object()

        initial_data = {
            'zoom_id': zoom_video.zoom_id
        }
        form = ZoomYoutubeUploadForm(initial=initial_data)
        context['admin'] = admin_user
        context['form'] = form
        return context


class ZoomVideoFormView(SingleObjectMixin, FormView):
    form_class = ZoomYoutubeUploadForm
    model = ZoomYouTubeFile
    template_name = 'forms/zoom-form.html'
    context_object_name = 'zoom_video'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance', None)
        return kwargs
      

    def form_valid(self, form):
        zoom_video = self.object
        official = UserCredential.objects.get(user=self.request.user.id)
        try:
            if official.google_refresh_token is None:
                # No refresh token exists
                result = get_token.delay(
                    user=official.user.id, code=official.google_code,
                    client_id=official.google_client_id, client_secret=official.google_client_secret
                )
                if result.get() and 'error_description' in result.get():
                    error_message = result.get().get('error_description')
                    messages.error(self.request, f'Sorry! could not process your request. Contact the Admin shortly. {error_message}')
                    return redirect(reverse('main:detail', kwargs={'slug': zoom_video.slug}))
                else:
                    zoom_video.appending_youtube_link_status = True
                    zoom_video.save()
                    messages.success(self.request, 'Success generating a token')
            else:
                zoom_video.appending_youtube_link_status = True
                zoom_video.save()

        except Exception as e:
            print(f"Error getting token {e}")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main:upload', kwargs={'pk': self.request.user.id, 'slug': self.object.slug})


class ZoomVideoDetailView(View):
    def get(self, request, *args, **kwargs):
        view = ZoomVideoDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ZoomVideoFormView.as_view()
        return view(request, *args, **kwargs)


class UploadDisplayView(LoginRequiredMixin, DetailView):
    model = ZoomYouTubeFile
    template_name = 'forms/confirm.html'
    context_object_name = 'zoom_video'

    def get_object(self, queryset=None):
        user = get_object_or_404(UserCredential, user=self.kwargs.get('pk'))
        zoom_video = get_object_or_404(ZoomYouTubeFile, slug=self.kwargs.get('slug'))
        return user, zoom_video

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user, zoom_video = self.get_object()

        initial_data = {
            'user_id': user.user.id,
            'zoom_id': zoom_video.zoom_name,
        }

        form = UploadYoutubeForm(initial=initial_data)
        context['form'] = form
        return context


class UploadFormView(SingleObjectMixin, FormView):
    form_class = UploadYoutubeForm
    model = ZoomYouTubeFile
    template_name = 'forms/confirm.html'
    context_object_name = 'zoom_video'

    def get_object(self, queryset=None):
        return get_object_or_404(ZoomYouTubeFile, slug=self.kwargs.get('slug'))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance', None)
        return kwargs

    def form_valid(self, form):
        zoom_video = self.object
        user_id = form.cleaned_data['user_id']
        zoom_id = form.cleaned_data['zoom_id']
        official = get_object_or_404(UserCredential, user=user_id)

        try:
            # uploading video to youtube
            video_file_path = join(settings.MEDIA_ROOT, zoom_id)
            # using the YouTube credentials and putting that in an instance
            youtube_url = upload_to_youtube_from_dir.delay(
                google_client_id=official.google_client_id,
                google_client_secret=official.google_client_secret,
                google_refresh_token=official.google_refresh_token,
                video_path=video_file_path, title=zoom_id)

            try:
                if youtube_url is None or youtube_url == '':
                    print(f'Error the youtube url is {youtube_url}')
                    messages.error(self.request, 'Error uploading the video')
                else:
                    # Update the database
                    zoom_video.youtube_video_file_url = youtube_url.get()
                    zoom_video.youtube_link_status = True
                    zoom_video.save()
                    messages.success(self.request, 'Video uploaded successfully to YouTube')
            except Exception as e:
                print(e)
                pass
        except Exception as e:
            print(e)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main:home', kwargs={'pk': self.request.user.id})


class UploadDetailView(View):
    def get(self, request, *args, **kwargs):
        view = UploadDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = UploadFormView.as_view()
        return view(request, *args, **kwargs)

