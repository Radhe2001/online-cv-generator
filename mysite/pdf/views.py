from django.shortcuts import render
# from django.urls import reverse
from .models import Profile
# import pdfkit
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
# import io
from xhtml2pdf import pisa



def accept(request):
    if request.method == 'POST':
        name = request.POST.get('name',"")
        email = request.POST.get('email',"")
        phone = request.POST.get('phone',"")
        summary = request.POST.get('summary',"")
        degree = request.POST.get('degree',"")
        school = request.POST.get('school',"")
        university = request.POST.get('university',"")
        previous_work = request.POST.get('previous_work',"")
        skills = request.POST.get('skills',"")
        
        profile = Profile(name=name,email=email,phone=phone,summary=summary,degree=degree,school=school,
                          previous_work=previous_work,skills=skills,university=university)
        
        profile.save()
        return HttpResponseRedirect('/list/')
        
    return render(request,"pdf/form.html")



    
def resume(request,id):
    profile = Profile.objects.get(id=id)
    template = get_template('pdf/resume.html')
    html = template.render({'profile':profile})

    # Create a PDF file using xhtml2pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return render(request,"pdf/resume.html",{'profile':profile})

    return response

def list(request):
    profile = Profile.objects.all()
    return render(request,"pdf/list.html",{'profile':profile})