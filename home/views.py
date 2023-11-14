from django.shortcuts import render, get_object_or_404, redirect

from home.models import Assessment, Response


def index(request):
    return render(request, 'home/index.html', context={})


def assessment(request, assessment_id, response_id):
    # obj = get_object_or_404(Assessment, id=assessment_id)
    #
    # if response_id == -1:
    #     resp = Response(assessment=obj)
    #     resp.current_page = obj.formpage_set.first()
    #     resp.save()
    #
    #     return redirect('assessment', assessment_id=obj.id, response_id=resp.id)
    #
    # resp = get_object_or_404(Response, id=response_id)
    # page_titles = [page.title for page in obj.formpage_set.all()]
    # title = resp.current_page.title
    # page_index = page_titles.index(title)
    # description = resp.current_page.description
    # questions = resp.current_page.questions.all()

    context = {
        # 'id': resp.id,
        # 'page_index': page_index,
        # 'page_titles': page_titles,
        # 'title': title,
        # 'description': description,
        # 'questions': questions,
    }

    return render(request, 'home/assessment.html', context=context)
