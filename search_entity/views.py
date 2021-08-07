import PyPDF2
import spacy
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PDF

nlp = spacy.load('en_core_web_sm')

def upload_file(request):
    if request.method == 'POST':
        pdf_file = request.FILES['file_upload']
        pdf_name = pdf_file.name

        pdf_object = PDF.objects.filter(file_name=pdf_name)

        if pdf_object.exists():
            messages.info(request, 'File already exist.')

            return redirect('search_entity:search_entity')
        else:
            read_pdf = PyPDF2.PdfFileReader(pdf_file, strict=False)
            number_of_pages = read_pdf.getNumPages()

            content = ''
            for page in range(number_of_pages if number_of_pages < 50 else 50):
                read = read_pdf.getPage(page)
                page_content = read.extractText()
                content += page_content.encode('utf-8').decode().strip()

            document = nlp(content)

            entities = list()
            for entity in document.ents:
                entities.append(entity.text.lower())
        
            PDF.objects.update_or_create(
                file_name=pdf_file.name,
                file=pdf_file,
                entity=entities
            )

            messages.info(request, 'File successfully uploaded.')

            return redirect("search_entity:search_entity")

def search_entity(request):
    suggestions = list()

    if request.method == 'POST':
        content = request.POST['search']
        document = nlp(content)

        # entities = content.split()
        entities = list()
        for entity in document.ents:
            # print(entity.text, entity.label_)
            entities.append(entity.text)
        
        pdf_files = PDF.objects.all()
        for pdf_file in pdf_files:
            for entity in entities:
                if entity.lower() in pdf_file.entity:
                    if pdf_file not in suggestions:
                        suggestions.append(pdf_file)

    return render(request, 'search_entity/index.html', {
        'suggestions': suggestions
    })