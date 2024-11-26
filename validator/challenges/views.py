from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import DefinedFile, Challenge, Level, Performance
from django.db.models import Count, Subquery, OuterRef, Q
from django.contrib.auth.decorators import login_required


def fetch_defined_files(request, challenge_slug):
    if request.method == 'GET':
        # Retrieve challenge based on the challenge_slug
        challenge = get_object_or_404(Challenge, slug=challenge_slug)
        level_id = request.GET.get('level_id')
        defined_files = DefinedFile.objects.filter(level__challenge=challenge, level_id=level_id)
        form_html = render_to_string('defined_file_form.html', {'defined_files': defined_files})
        return JsonResponse({'form_html': form_html})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def challenge_detail(request, challenge_slug=None):
    user = request.user
    if challenge_slug:
        challenge = get_object_or_404(Challenge, slug=challenge_slug)
        defined_files = DefinedFile.objects.filter(level__challenge=challenge).order_by('name')
        test_results = {defined_file.id: defined_file.get_test_result_for_user(request) for defined_file in defined_files}
        levels = Level.objects.filter(challenge=challenge).order_by('name')
        result = 'Upload your file first'

        # Vérifier si l'utilisateur a résolu tous les fichiers du challenge
        all_resolved = challenge.all_files_resolved_by_user(user)

        if request.method == 'POST':
            uploaded_file = request.FILES.get('uploaded_file')
            if uploaded_file:
                uploaded_content = uploaded_file.read().decode('utf-8')
                defined_file_name = request.POST.get('defined_file_name', None)

                if defined_file_name:
                    try:
                        defined_file = DefinedFile.objects.get(name=defined_file_name, level__challenge__name=challenge.name)
                        defined_content = defined_file.output_file.read().decode('utf-8')

                        if uploaded_content == defined_content:
                            # Create a Performance record
                            Performance.objects.create(user=user, definedfile=defined_file, solved=True)

                            # Check if all files are resolved
                            all_resolved = challenge.all_files_resolved_by_user(user)
                            result = 'VALID'
                            bonus_message = challenge.bonus_message if all_resolved else None
                        else:
                            result = 'INVALID'
                            bonus_message = None
                    except DefinedFile.DoesNotExist:
                        result = f'INVALID (No defined file named {defined_file_name} found for challenge: {challenge.name})'
                        bonus_message = None
                else:
                    result = 'INVALID (No defined file name provided)'
                    bonus_message = None
            else:
                result = 'INVALID (No file uploaded)'
                bonus_message = None

            # Return result and bonus message in JSON
            return JsonResponse({'result': result, 'bonus_message': bonus_message})


        return render(request, 'challenges/challenge_detail.html', {
            'defined_files': defined_files,
            'challenge': challenge,
            'levels': levels,
            'user': user,
            'test_results': test_results,
            'all_resolved': all_resolved,  # Passer l'état de validation
        })

    return render(request, 'challenges/challenge_list.html', {
        'challenges': Challenge.objects.all(),
        'user': user
    })


@login_required
def challenge_list(request):
    user = request.user
    # Sous-requête pour compter tous les fichiers définis pour chaque challenge
    defined_files_count = Challenge.objects.filter(
            pk=OuterRef('pk')
        ).annotate(
            count=Count('levels__defined_files')
        ).values('count')

    # Sous-requête pour compter les fichiers définis résolus par l'utilisateur courant pour chaque challenge
    resolved_files_count = Challenge.objects.filter(
            pk=OuterRef('pk')
        ).annotate(
            count=Count('levels__defined_files', filter=Q(levels__defined_files__performance__user=user, levels__defined_files__performance__solved=True))
        ).values('count')
    challenges = Challenge.objects.order_by('category', 'name').filter(published=True).annotate(
        num_defined_files=Subquery(defined_files_count),
        num_resolved_defined_files=Subquery(resolved_files_count)
        )
    return render(request, 'challenges/challenge_list.html', {'challenges': challenges})

