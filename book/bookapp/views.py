from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import  User
from django.contrib import messages  # For displaying feedback messages to the user
from .models import *
from datetime import date, timedelta
import os
# Create your views here.
def u_login(req):
    if 'admin' in req.session:
        return redirect(admin_home)
    if 'user' in req.session:
        return redirect (user_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        data=authenticate(username=uname,password=password)
        if data:
            login(req,data)
            if data.is_superuser:
              req.session['admin']=uname   #create session 
              return redirect(admin_home)
            else:
                req.session['user']=uname
                return redirect(user_home)
        else:
            messages.warning(req, " invalid user name or password")
            return redirect(login)
    else:
        return render(req,'login.html')
def u_logout(req):
     logout(req)
     req.session.flush()
     return redirect(u_login)

def admin_home(req):
     if 'admin' in req.session:
       return render(req,'admin/admin_home.html')
     else:
        return redirect(u_login)

def add_location(req):
    if 'admin' in req.session:
        if req.method == 'POST':
            name = req.POST['location']
            locations.objects.create(location_name=name.lower())
            location = locations.objects.all()
            return render(req, 'admin/add_location.html', {'locations': location})
        else:
            location = locations.objects.all()
            return render(req, 'admin/add_location.html', {'locations': location})
    else:
          return redirect(u_login)
    
def delete_location(req, id):
    if 'admin' in req.session:
        try:
            location = locations.objects.get(id=id)
            location.delete()
        except locations.DoesNotExist:
            print(f"Location with id {id} does not exist.")
        return redirect(add_location)  # Use the URL name
    else:
        return redirect(u_login)
     
def add_cateogory(req):
    if 'admin' in req.session:
        if req.method == 'POST':
            name = req.POST['name']
            Category.objects.create(name=name.lower())
            categorys = Category.objects.all()

            return render(req, 'admin/add_category.html', {'categorys': categorys})
        else:
            categorys= Category.objects.all()
            return render(req, 'admin/add_category.html', {'categorys':categorys})
    else:
          return redirect(u_login)
    
def delete_category(req, id):
    if 'admin' in req.session:
        try:
            location = Category.objects.get(id=id)
            location.delete()
        except Category.DoesNotExist:
            print(f"cateogory with id {id} does not exist.")
        return redirect(add_cateogory)  # Use the URL name
    else:
        return redirect(u_login)
def add_generes(req):
    if 'admin' in req.session:
        if req.method == 'POST':
            name = req.POST['generes']
            print(name)
            cate=req.POST['category']
            cat=Category.objects.get(pk=cate)
            data=genres.objects.create(ge_name=name,cat_name=cat)
            data.save()
            
            genre = genres.objects.all()

            return render(req, 'admin/add_genres.html', {'genres':genre,'cate':cate})
        else:
            cate=Category.objects.all()
            genre= genres.objects.all()
            return render(req, 'admin/add_genres.html', {'genres': genre,'cate':cate})
    else:
          return redirect(u_login)
    
def delete_generes(req, id):
    if 'admin' in req.session:
        try:
            location = genres.objects.get(id=id)
            location.delete()
        except genres.DoesNotExist:
            print(f"cateogory with id {id} does not exist.")
        return redirect(add_generes)  # Use the URL name
    else:
        return redirect(u_login)
     
def add_books(req):
    if 'admin' in req.session:  # Check if admin is logged in
        if req.method == 'POST':
            # Safely retrieve data from the request
            bname = req.POST.get('title', '').strip().upper()
            aname = req.POST.get('auther', '').strip().upper()
            description = req.POST.get('description', '').strip()
            pdate = req.POST.get('date', None)
            loca = req.POST.get('location', None)
            genre = req.POST.get('generes', None)
            file = req.FILES.get('image', None)

            # Validate required fields
            if not all([bname, aname, description, pdate, loca, genre, file]):
                gene = genres.objects.all()
                loc = locations.objects.all()
                return render(req, 'admin/add_book.html', {
                    'geners': gene,
                    'location': loc,
                    'error': 'All fields are required.'
                })

            try:
                # Fetch genre and location objects
                gen = genres.objects.get(pk=genre)
                loca = locations.objects.get(pk=loca)
            except (genres.DoesNotExist, locations.DoesNotExist):
                gene = genres.objects.all()
                loc = locations.objects.all()
                return render(req, 'admin/add_book.html', {
                    'geners': gene,
                    'location': loc,
                    'error': 'Invalid genre or location selection.'
                })

            # Create and save the book object
            books.objects.create(
                title=bname,
                auther=aname,
                description=description,
                publication_date=pdate,
                location=loca,
                genre=gen,
                cover_image=file,
            )
            return redirect(admin_home)  # Redirect to admin home after saving

        else:
            # Render form with genres and locations
            gene = genres.objects.all()
            loc = locations.objects.all()
            return render(req, 'admin/add_book.html', {'geners': gene, 'location': loc})
    else:
        return redirect(admin_home)  # Redirect to admin home if not logged in
    
def view_book(req):
    cate_name = req.GET.get('category', None)
    cate = Category.objects.all()  # Fetch all categories
    
    if cate_name:  # If category filter is applied
        Book = books.objects.filter(name=cate_name)  # Filter products based on the category ID
    else:  # If no category filter is provided
        Book =books.objects.all()  # Fetch all products

    # Render the products and categories on the template
    return render(req, 'admin/view_books.html', {'Books': Book, 'cate': cate})
def delet_book(req,pk):
    data=books.objects.get(pk=pk)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(admin_home)

def view_user(req):

    user =User.objects.all()  # Fetch all products

    # Render the products and categories on the template
    return render(req, 'admin/user.html', {'user': user,})

def view_reanted_books(req):
    data=Borrow.objects.all()
    
    return render (req,'admin/view_reanted_book.html',{'borrows':data})

# def returns(req):



def reg(req):
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        pswd=req.POST['pswd']
        # print(email)
        # send_mail('account created', 'you created a account in e_com', settings.EMAIL_HOST_USER, [email])

        try:
          data=User.objects.create_user(first_name=uname, username=email,email=email,password=pswd)
          data.save()
          return redirect (req,login)
        except:
           messages.warning(req, " already used ")
           return redirect(reg)
    else:
        return render(req,'user/registration.html')

def user_home(req):
    search_query = req.GET.get('q', '')  # Default to an empty string if no search query is provided
    
    # Filter Borrow records based on the search query
    if search_query:
        book = books.objects.filter(
             title=search_query  # You can search by book title
        )
    else:
        book = books.objects.all()  #
    if 'user' in req.session:
        return render(req,'user/user.html', { 'BOOKS': book,'search_query': search_query})
    else:
        return redirect (u_login)

# def Books(req):
#     id = req.GET.get('genres', None)
   
#     gen = genres.objects.all()  
    
#     if id:  # If category filter is applied
#        BOOKS = books.objects.filter(id=gen_id)  
#     else:
#         BOOKS = books.objects.all()[::-1]
#     # 
#     search_query = req.GET.get('q', '')  # Default to an empty string if no search query is provided
    
#     # Filter Borrow records based on the search query
#     if search_query:
#         BOOKS = books.objects.filter(
#              title=search_query,  # You can search by book title
#         )
#     else:  
#           BOOKS = books.objects.all()[::-1]  
#     if 'user' in req.session:
#         return render(req,'user/view_book.html', {'book': BOOKS,'search_query': search_query ,'gen': gen})
#     else:
#         return redirect (u_login)
def Books(req):
    # Get genre filter from query parameters
    genre_id = req.GET.get('genres', None)
    
    # Get search query from query parameters
    search_query = req.GET.get('q', '')

    # Fetch all genres for the dropdown or filtering options
    gen = genres.objects.all()

    # Initialize the books queryset
    BOOKS = books.objects.all()

    # Filter by genre if a genre ID is provided
    if genre_id:
        BOOKS = BOOKS.filter(genre_id=genre_id)

    # Filter by search query if provided
    if search_query:
        BOOKS = BOOKS.filter(title__icontains=search_query)

    # Reverse the queryset for latest books first
    BOOKS = BOOKS[::-1]

    # Check if the user is logged in
    if 'user' in req.session:
        return render(req, 'user/view_book.html', {'book': BOOKS, 'search_query': search_query, 'gen': gen})
    else:
        return redirect(u_login)

    
def viewbook(req,id):
    book=books.objects.get(pk=id)
    if 'user' in req.session:
       return render(req,'user/book.html',{'Book':book})

def book_reant(req, id):
    # Get the book object
    book =books.objects.get(pk=id)
    # Get the user object
    user = User.objects.get (username=req.session.get('user'))

        # Check if the user has already borrowed this book
    if Borrow.objects.filter(book=book, user=user).exists():
        # Send a message that the book is already borrowed
        messages.error(req, f"You have already borrowed '{book.title}'. You cannot borrow it again.")
        # return render(req, 'user/borrow.html', {'book': book})
        return redirect(view_borrow)


    
    # Calculate the return date (10 days from today)
    return_date = date.today() + timedelta(days=10)
    
    # Create the Borrow record
    Borrow.objects.create(
        book=book,
        user=user,
        r_date=return_date
    )
    print(book.id)
    # return render(req,'user/borrow.html',{'book': book})
    return redirect(view_borrow)



def view_borrow(req):
   user=User.objects.get(username=req.session['user'])
   data=Borrow.objects.filter(user=user)[::-1] 
   return render (req,'user/borrow.html',{'borrows':data})

            
   
     
def about(req):
    
       return render(req,'user/about.html')
def contact(req):
    
       return render(req,'user/contact.html')
    