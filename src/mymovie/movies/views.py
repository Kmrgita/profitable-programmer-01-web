from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os

AIRTABLE_MOVIESTABLE_BASE_ID = "appOhpRxIqWI8YcHD"
AIRTABLE_API_KEY = "keyAzZ6cA8E1P4Ly1"


AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID', AIRTABLE_MOVIESTABLE_BASE_ID),
              'Movies', api_key=os.environ.get('AIRTABLE_API_KEY', AIRTABLE_API_KEY))


# Create your views here.
def home_page(request):
    # print(str(request.GET.get('query', '')))
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(
        formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)

#


def create(request):
    if request.method == 'POST':
        try:
            data = {
                'Name': request.POST.get('name'),
                'Pictures': [{'url': request.POST.get('url') or 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ3--VuoJd0jfplzxXvzNnbemdD5CyBNxqN14yBLwRKDrWO0vewOw&s'}],
                'Rating': int(request.POST.get('rating')),
                'Notes': request.POST.get('notes')
            }

            response = AT.insert(data)

            # notify on create
            messages.success(request, 'New Movie {}'.format(
                response['fields'].get('Name') + ' Added Successfully !'))
        except Exception as e:
            messages.warning(
                request, 'Got an error when trying to create new movie: {}'.format(e))

    return redirect('/')

# notify on create


def edit(request, movie_id):
    if request.method == 'POST':
        try:
            data = {
                'Name': request.POST.get('name'),
                'Pictures': [{'url': request.POST.get('url') or 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ3--VuoJd0jfplzxXvzNnbemdD5CyBNxqN14yBLwRKDrWO0vewOw&s'}],
                'Rating': int(request.POST.get('rating')),
                'Notes': request.POST.get('notes')
            }
            response = AT.update(movie_id, data)

            # notify on update
            messages.info(request, 'Movie {}'.format(
                response['fields'].get('Name') + ' Successfully Updated !'))
        except Exception as e:
            messages.warning(
                request, 'Got an error when trying to update movie: {}'.format(e))

    return redirect('/')


def delete(request, movie_id):
    try:
        movie_name = AT.get(movie_id)['fields'].get('Name')
        response = AT.delete(movie_id)

        # notify on delete
        messages.warning(request, 'Movie {}'.format(
            movie_name) + ' DELETED !!!')
    except Exception as e:
        messages.warning(
            request, 'Got an error while trying delete the movie: {}'.format(e))

    return redirect('/')
