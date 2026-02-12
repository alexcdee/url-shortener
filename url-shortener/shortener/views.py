from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count

from shortener.forms import UrlForm
from .models import UrlData
from .serializers import UrlDataSerializer

@api_view(['GET', 'POST'])
def url_list_create(request):
    if request.method == 'GET':
        qs = UrlData.objects.all().order_by('-created')
        total = UrlData.objects.count()
        serializer = UrlDataSerializer(qs, many=True, context={'request': request})
        return Response({'total': total, 'items': serializer.data})

    original = request.data.get('url')
    if not original:
        return Response({'error': 'url is required'}, status=status.HTTP_400_BAD_REQUEST)

    UrlData.objects.create(url=original)
    total = UrlData.objects.count()
    latest = UrlData.objects.latest('id')
    out = UrlDataSerializer(latest, context={'request': request})
    return Response({'total': total, 'latest': out.data}, status=status.HTTP_201_CREATED)






def home(request):
    latest = None
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            latest = UrlData.objects.create(url=form.cleaned_data['url'])
            form = UrlForm()
    else:
        form = UrlForm()
    data = UrlData.objects.all().order_by('-created')
    return render(request, 'home.html', {'form': form, 'data': data, 'latest': latest})

def redirect_view(request, slug):
    url_data = get_object_or_404(UrlData, slug=slug)
    return redirect(url_data.url)

