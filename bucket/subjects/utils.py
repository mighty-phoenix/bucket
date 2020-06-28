# helper functions

def filter_and_search_queryset(qs, request):
    books = request.GET.get('books')
    movies = request.GET.get('movies')
    documentaries = request.GET.get('documentaries')
    websites = request.GET.get('websites')
    youtube_channels = request.GET.get('youtube_channels')
    social_media = request.GET.get('social_media')
    others = request.GET.get('others')
    types = [books, movies, documentaries, websites, youtube_channels, social_media, others]
    if '' in types:
        if books == None:
            qs = qs.exclude(type='book')
        if movies == None:
            qs = qs.exclude(type='movie')
        if documentaries == None:
            qs = qs.exclude(type='documentary')
        if websites == None:
            qs = qs.exclude(type='website')
        if youtube_channels == None:
            qs = qs.exclude(type='youtube_channel')
        if social_media == None:
            qs = qs.exclude(type='social_media')
        if others == None:
            qs = qs.exclude(type='other')
    search_query = request.GET.get('search')
    if search_query != '' and search_query is not None:
        qs = qs.filter(title__icontains=search_query).order_by('title')
    return qs
