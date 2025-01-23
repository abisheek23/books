from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import  User
from django.contrib import messages  # For displaying feedback messages to the user
from .models import *
from datetime import date, timedelta
from django.db.models import Q



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

            return redirect(add_generes)
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
            copies = req.POST.get('available_copies')
            file = req.FILES.get('image', None)

            # Validate required fields
            if not all([bname, aname, description, pdate, loca, genre,copies, file]):
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
                available_copies=copies,
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


def edit_book(req,id):
    if req.method=='POST':
        bname = req.POST.get('title', '').strip().upper()
        aname = req.POST.get('auther', '').strip().upper()
        description = req.POST.get('description', '').strip()
        pdate = req.POST.get('date', None)
        loca = req.POST.get('location', None)
        genre = req.POST.get('generes', None)
        copies = req.POST.get('available_copies')
        file = req.FILES.get('image', None)

        
        if file:
            gen = genres.objects.get(pk=genre)
            books.objects.filter(pk=id).update(title=bname,
                auther=aname,
                description=description,
                publication_date=pdate,
                location=loca,
                genre=gen,
                available_copies=copies,
                cover_image=file,)
            data=books.objects.get(pk=id)
            data. cover_image=file
            data.save()
        else:
            books.objects.filter(pk=id).update(title=bname,
                auther=aname,
                description=description,
                
            )
        return redirect(admin_home)
        

    else:
         data=books.objects.get(pk=id)
         return  render(req,'admin/edit_book.html',{'data':data})
    
def delet_book(req,id):
    data=books.objects.get(pk=id)
    file=data.cover_image.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(admin_home)

    
def view_book(req):
    cate_name = req.GET.get('category', None)
    cate = Category.objects.all()  # Fetch all categories
    
    if cate_name:  # If category filter is applied
        Book = books.objects.filter(name=cate_name)  # Filter products based on the category ID
    else:  # If no category filter is provided
        Book =books.objects.all()  # Fetch all products

    # Render the products and categories on the template
    return render(req, 'admin/view_books.html', {'Books': Book, 'cate': cate})


def view_user(req):

    user =User.objects.all()  # Fetch all products

    # Render the products and categories on the template
    return render(req, 'admin/user.html', {'user': user,})

# def view_reanted_books(req):
#     data=Borrow.objects.all()
    
#     return render (req,'admin/view_reanted_book.html',{'borrows':data})

def display_contacts(request):
    # Fetch all contact form submissions from the database
    contacts = Contact.objects.all().order_by('-created_at')  # Orders by latest submissions
    return render(request, "admin/display_contacts.html", {"contacts": contacts})

def book_request(req, id):
    # Get the book object
    book = books.objects.get(pk=id)
    
    # Get the user object
    user = User.objects.get(username=req.session.get('user'))

    # Check if the user has already requested or borrowed this book (any status)
    if Borrow.objects.filter(book=book, user=user).exists():
        messages.error(req, f"You have already requested or borrowed '{book.title}'.")
        return redirect(view_borrow)

    # Create a borrow request with a 'Pending' status
    Borrow.objects.create(book=book, user=user, status='Pending')
    messages.success(req, f"Your request to borrow '{book.title}' has been sent.")
    return redirect(view_borrow)


def manage_borrow_requests(req):
    # Get all pending borrow requests
    borrow_requests = Borrow.objects.filter(status='Pending')
   
    return render(req, 'admin/manage_borrow_requests.html', {'requests': borrow_requests})

def approve_request(req, borrow_id):
    borrow = Borrow.objects.get(pk=borrow_id)
    if borrow.book.available_copies > 0:
        # Approve the request
        borrow.status = 'Approved'
        borrow.approval_date = date.today()  
        borrow.r_date=borrow.approval_date + timedelta(days=30)
        borrow.book.available_copies -= 1
        borrow.book.save()
        borrow.save()
        messages.success(req, f"Request for '{borrow.book.title}' has been approved.")
    else:
        messages.error(req, f"Cannot approve. No copies available for '{borrow.book.title}'.")
    return redirect(manage_borrow_requests)



def reject_request(req, borrow_id):
    # Get the borrow record
    borrow = Borrow.objects.get(pk=borrow_id)
    # Default rejection without reason (GET request)
    borrow.status = 'Rejected'
    borrow.save()
    messages.info(req, f"Request for '{borrow.book.title}' has been rejected.")
    return redirect(manage_borrow_requests)

def delete_all_rejected(req):
    # Filter and delete all records with 'Rejected' status
    rejected_requests = Borrow.objects.filter(status='Rejected')
    count = rejected_requests.count()
    rejected_requests.delete()
    messages.success(req, f"Successfully deleted {count} rejected requests.")
    return redirect(manage_borrow_requests)

def view_rejucted(req):
    # Get all pending borrow requests
    data= Borrow.objects.filter(status='Rejected')
    return render(req, 'admin/rejected.html', {'reject': data})
def view_rented_books(req):
    # Get all pending borrow requests
    borrow= Borrow.objects.filter(status='Approved')
    return render(req, 'admin/view_rented_books.html', {'rented': borrow})

def manage_returns(req):
    # Fetch all return requests
    return_requests = Borrow.objects.filter(status='Return Requested')
    return render(req, 'admin/manage_returns.html', {'return_requests': return_requests})

def approve_return(req, borrow_id):
    borrow = Borrow.objects.get(pk=borrow_id)

    # Ensure the book is in the 'Return Requested' state
    if borrow.status != 'Return Requested':
        messages.error(req, "Invalid action. The return request is not in the correct state.")
        return redirect('manage_returns')

    # Approve the return
    borrow.status = 'Returned'
    borrow.return_approval_date = date.today()

    book = borrow.book
    book.available_copies += 1
    book.save()
    borrow.save()

    messages.success(req, f"Return request for '{borrow.book.title}' has been approved.")
    return redirect('manage_returns')


def manage_extension_requests(req):
    # Fetch all pending extension requests
    extension_requests = Borrow.objects.filter(extension_status='Pending')
    return render(req, 'admin/manage_extension_requests.html', {'requests': extension_requests})


def approve_extension(req, borrow_id):
    borrow = Borrow.objects.get(pk=borrow_id)

    if borrow.extension_status != 'Pending':
        messages.error(req, "This extension request has already been processed.")
        return redirect('manage_extension_requests')

    # Approve the extension
    borrow.r_date = borrow.new_return_date  # Update the return date
    borrow.extension_status = 'Approved'
    borrow.save()

    messages.success(req, f"Extension for '{borrow.book.title}' has been approved.")
    return redirect('manage_extension_requests')


def reject_extension(req, borrow_id):
    borrow = Borrow.objects.get(pk=borrow_id)

    if borrow.extension_status != 'Pending':
        messages.error(req, "This extension request has already been processed.")
        return redirect('manage_extension_requests')

    # Reject the extension
    borrow.extension_status = 'Rejected'
    borrow.save()

    messages.info(req, f"Extension request for '{borrow.book.title}' has been rejected.")
    return redirect('manage_extension_requests')


def returned_book(req):
    
    borrow = Borrow.objects.filter(status='Returned')
    return render(req, 'admin/returned_books.html', {'borrow': borrow})

#user
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
    search_query = req.GET.get('q', '').upper()  # Default to an empty string if no search query is provided
    
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

#

def Books(req):
    # Get genre filter from query parameters
    genre_id = req.GET.get('genres', None)
    
    # Get search query from query parameters
    search_query = req.GET.get('q', '').upper()

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
    if Borrow.objects.filter(book=book, user=user,status='pending').exists():
        # Send a message that the book is already borrowed
        messages.error(req, f"You have already borrowed '{book.title}'. You cannot borrow it again.")
    
 
    req_date = date.today()
    
    # Create the Borrow record
    Borrow.objects.create(
        book=book,
        user=user,
        request_date=req_date
    )
    # return render(req,'user/borrow.html',{'book': book})
    return redirect(view_borrow)





def view_borrow_req(req):
   user=User.objects.get(username=req.session['user'])
    # Get all pending borrow requests
   borrow_requests = Borrow.objects.filter(user=user).filter(Q(status='Pending') | Q(status='Rejected'))

   return render(req, 'user/requests.html', {'requests': borrow_requests})

            
def view_borrow(req):
   user=User.objects.get(username=req.session['user'])
    # Get all pending borrow requests
   borrowd = Borrow.objects.filter(user=user,status='Approved')
   return render(req, 'user/borrowed.html', {'borrow':borrowd})  

def request_return(req, borrow_id):
    user = User.objects.get(username=req.session['user'])
    # Use get() instead of filter() to retrieve a single object
    try:
        borrow = Borrow.objects.get(pk=borrow_id, user=user)

        # Ensure the book is already borrowed and not already returned
        if borrow.status != 'Approved':
            messages.error(req, "You cannot request a return for this book.")
            return redirect('view_borrow')

        # Update borrow status to 'Return Requested'
        borrow.status = 'Return Requested'
        borrow.return_request_date = date.today()
        borrow.save()

        messages.success(req, f"Return request for '{borrow.book.title}' has been sent.")
    except Borrow.DoesNotExist:
        messages.error(req, "Borrow record not found.")
    
    return redirect('view_borrow')  # Note: Changed to use string name instead of function reference
     
def about(req):
    
       return render(req,'user/about.html')
def contact(req):
    
       return render(req,'user/contact.html')

def submit_contact_form(req):
    if req.method == "POST":
        name = req.POST.get("name")
        email = req.POST.get("email")
        message = req.POST.get("message")

        # Save the data to the Contact model
        Contact.objects.create(name=name, email=email, message=message)

        # Provide feedback to the user
        messages.success(req, "Your message has been sent successfully!")
        return redirect(contact)  # Replace with the name of your contact page URL
    return render(req, "user/contact.html")
    
def request_extension(req, borrow_id):
    user = User.objects.get(username=req.session['user'])
    borrow = Borrow.objects.get(pk=borrow_id, user=user)

    # Check if the borrow status is valid for an extension request
    if borrow.status != 'Approved':
        messages.error(req, "You cannot request an extension for this book.")
        return redirect('view_borrow')

    # Check if the user has already requested an extension
    if borrow.extension_status == 'Pending':
        messages.warning(req, "You have already requested an extension for this book.")
        return redirect('view_borrow')

    if req.method == 'POST':
        # Fetch the new return date from the form
        new_date = req.POST.get('new_return_date')
        if not new_date:
            messages.error(req, "Please provide a valid new return date.")
            return redirect('view_borrow')

        new_return_date = date.fromisoformat(new_date)

        # Ensure the requested date is valid
        if new_return_date <= borrow.r_date:
            messages.error(req, "The new return date must be after the current return date.")
            return redirect('view_borrow')

        # Update the borrow record
        borrow.extension_requested_date = date.today()
        borrow.new_return_date = new_return_date
        borrow.extension_status = 'Pending'
        borrow.save()

        messages.success(req, f"Extension request submitted for '{borrow.book.title}'.")
        return redirect('view_borrow')

    return render(req, 'user/request_extension.html', {'borrow': borrow})

def borrow_history(req):
    user = User.objects.get(username=req.session['user'])
    borrow = Borrow.objects.filter(status='Returned', user=user)
    return render(req, 'user/borrow_history.html', {'borrow': borrow})