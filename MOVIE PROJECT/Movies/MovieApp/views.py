
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from pymongo import MongoClient
from  uuid import uuid4
from django.core.files.storage import FileSystemStorage

# Create your views here.

def Movies(request):
    if request.method =="GET":
        client = MongoClient("mongodb://127.0.0.1:27017")
        db = client.MovieDb
        col = db["MovieDetails"]
        moviesdata = col.find()
        col1 = db["ActorDetails"]
        actorsdata= col1.find()
        return render(request,"movies.html", {"drop": actorsdata,"result":moviesdata})


def AddMovie(request):
    if request.method == "POST":
        client = MongoClient("mongodb://127.0.0.1:27017")
        db = client.MovieDb
        col = db["MovieDetails"]
        movieid =  str(uuid4())
        moviename = request.POST["moviename"]
        year = request.POST["year"]
        plot = request.POST["plot"]  
        image = request.FILES["image"]
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        actors = request.POST.getlist('actors[]')
        ac = []
        for a in actors:
            ac.append(a)
        col.insert_one({
                "movieid":movieid,
                "moviename": moviename,
                "year": year,
                "plot": plot,
                "poster":filename,
                "actors":ac
        })
        return HttpResponseRedirect('/MovieApp/moviemessage')

  
        
 
def AddActor(request):
    if request.method == "POST":
        client = MongoClient("mongodb://127.0.0.1:27017")
        db = client.MovieDb
        col = db["ActorDetails"]
        actorid =  str(uuid4())
        actorname = request.POST["actorname"]
        sex = request.POST["sex"]
        dob = request.POST["dob"]  
        bio =request.POST["bio"]
        col.insert_one({
                "actorid":actorid,
                "actorname": actorname,
                "sex": sex,
                "dob": dob,
                "bio":bio,
        })
    return HttpResponseRedirect('/MovieApp/actormessage/')
    
def EditMovie(request):
    if request.method =="GET":
        movieid = request.GET.get("id")
        client = MongoClient("mongodb://127.0.0.1:27017")
        db = client.MovieDb
        col = db["MovieDetails"]
        data = col.find_one({"movieid":movieid})
        col1 = db["ActorDetails"]
        actorsdata= col1.find()
        return render(request,"editmovie.html",{"editdata":data,"drop": actorsdata})
    if request.method =="POST":
        client = MongoClient("mongodb://127.0.0.1:27017")
        db = client.MovieDb
        col = db["MovieDetails"]
        movieid = request.POST["hidden"]
   
        moviename = request.POST["moviename"]
        year = request.POST["year"]
        plot = request.POST["plot"]  
        actors = request.POST.getlist('actors[]')
        ac = []
        for a in actors:
            ac.append(a)
     
        col.find_one_and_update(
            {"movieid":movieid},
                {
                   '$set':
                   {
                    "moviename": moviename,
                    "year": year,
                    "plot": plot,
                    "actors":ac
                    
                   }
            
                })
        return HttpResponseRedirect('/MovieApp/actormessage/')

def actormessage(request):
    if request.method=="GET":
        return render(request,"actorsuccess.html")


def moviemessage(request):
    if request.method=="GET":
        return render(request,"moviesuccess.html")

def editmessage(request):
     if request.method=="GET":
        return render(request,"editsuccess.html")

def search(request):
    if request.method =="POST":
        client = MongoClient("mongodb://127.0.0.1:27017")
        db = client.MovieDb
        coll = db["MovieDetails"]
        search = request.POST["search"].title()
        da = []
        data = coll.find({"moviename":search})
        if data != None:
            for i in data:
                da.append(i)
            if len(da) == 0:
                return render(request,"search.html",{"result": "No Results!!!"})
            else:
                return render(request,"search.html",{"result": da})
    if request.method=="GET":
        return HttpResponseRedirect('/MovieApp/Movie')