import tkinter as tk
from tkinter import ttk, messagebox
import random
import re
from PIL import Image, ImageTk, ImageDraw
import os
from tkinter import font as tkfont

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("800x600")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", foreground="#000000", font=("Helvetica", 11))
        self.style.configure("TButton",
            background="#fff",  # white background
            foreground="#000",  # black text
            borderwidth=1,
            focusthickness=1,
            focuscolor="#43b04a"
        )
        self.style.map("TButton",
            background=[("active", "#f0f0f0")],
            foreground=[("active", "#000")],
            bordercolor=[("active", "#43b04a"), ("!active", "#e0e0e0")]
        )
        self.style.configure("Header.TLabel", font=("Helvetica", 24, "bold"), foreground="#e74c3c", background="#f0f0f0")
        self.style.configure("Subheader.TLabel", font=("Helvetica", 16), foreground="#000000", background="#f0f0f0")
        
        # Configure card styles
        self.style.configure("Card.TFrame", background="white", relief="solid", borderwidth=1)
        self.style.configure("InfoCard.TLabelframe", background="white", foreground="#000000")
        self.style.configure("InfoCard.TLabelframe.Label", background="white", foreground="#000000", font=("Helvetica", 12, "bold"))
        self.style.configure("InfoCard.TFrame", background="white")
        self.style.configure("InfoCard.TLabel", background="white", foreground="#000000", font=("Helvetica", 11))
        
        # Configure treeview styles
        self.style.configure("Treeview", background="white", foreground="#000000", fieldbackground="white", font=("Helvetica", 11))
        self.style.configure("Treeview.Heading",
            background="#e74c3c",  # Strong red
            foreground="white",
            font=("Helvetica", 13, "bold")
        )
        self.style.map("Treeview.Heading",
            background=[("active", "#e74c3c"), ("pressed", "#e74c3c"), ("!active", "#e74c3c")],
            foreground=[("active", "white"), ("pressed", "white"), ("!active", "white")]
        )
        # Optionally, set row height for better spacing
        self.style.configure("Treeview", rowheight=28)
        
        # Configure button styles
        self.style.configure("Login.TButton", font=("Helvetica", 12, "bold"), background="#e74c3c", foreground="white", padding=10)
        self.style.configure("Logout.TButton", font=("Helvetica", 12, "bold"), background="#e74c3c", foreground="white", borderwidth=2, focusthickness=2, focuscolor="#c0392b", padding=8)
        self.style.map("Logout.TButton",
            background=[("active", "#c0392b")],
            foreground=[("active", "white")],
            bordercolor=[("active", "#c0392b"), ("!active", "#e74c3c")]
        )
        self.style.configure("EditProfile.TButton", font=("Helvetica", 12), background="#3498db", foreground="white", padding=5)
        self.style.configure("Calculate.TButton", font=("Helvetica", 12), background="#27ae60", foreground="white", padding=5)
        self.style.configure("Enroll.TButton", font=("Helvetica", 12, "bold"), background="#27ae60", foreground="white", padding=10)
        self.style.configure("Assign.TButton", font=("Helvetica", 12), background="#e74c3c", foreground="white", padding=5)
        
        # Configure combobox style
        self.style.configure("TCombobox", background="white", foreground="#000000", fieldbackground="white", font=("Helvetica", 11))
        self.style.map("TCombobox", fieldbackground=[("readonly", "white")], selectbackground=[("readonly", "#e74c3c")])
        
        # Configure entry style
        self.style.configure("TEntry", fieldbackground="white", foreground="#000000", font=("Helvetica", 11))
        
        # Configure notebook style
        self.style.configure("TNotebook", background="white")
        self.style.configure("TNotebook.Tab", font=("Helvetica", 14, "bold"), padding=[20, 10], foreground="#000")
        self.style.map("TNotebook.Tab",
            foreground=[("selected", "#000"), ("active", "#000"), ("!selected", "#000")],
            background=[("selected", "#fff"), ("active", "#e0e0e0"), ("!selected", "#f0f0f0")]
        )
        
        # Define a style for padded entry
        self.style.configure("Padded.TEntry", padding="8 4 8 4", foreground="#000", font=("Helvetica", 13), fieldbackground="#f5f5f5")
        
        # Create and set background image
        try:
            # Create background image if it doesn't exist
            if not os.path.exists("background1.jpg"):
                self.create_background_image()
            
            # Load the original image only once
            self.bg_image_original = Image.open("background1.jpg")
            # Initial resize
            self.bg_image = self.bg_image_original.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

            # Responsive background: update image on window resize
            def resize_bg(event):
                if hasattr(self, 'bg_label') and self.bg_label.winfo_exists():
                    w, h = max(1, event.width), max(1, event.height)
                    img = self.bg_image_original.resize((w, h), Image.Resampling.LANCZOS)
                    self.bg_photo = ImageTk.PhotoImage(img)
                    self.bg_label.config(image=self.bg_photo)
                    self.bg_label.image = self.bg_photo
            self.root.bind('<Configure>', resize_bg)
            self._resize_bg_handler = resize_bg  # Store handler for unbinding
        except Exception as e:
            print(f"Error loading background: {e}")
            # If image not found or error occurs, use a solid color
            self.root.configure(bg="#f0f0f0")
            self.bg_label = None
        
        # Dictionary databases
        self.users = {
            'admin1': {'password': 'admin123', 'type': 'admin'},
            'lecturer1': {'password': 'lecturer123', 'type': 'lecturer', 'suspended': False},
            'student1': {'password': 'student123', 'type': 'student', 'suspended': False}
        }
        
        self.students = {
            'S001': {'name': 'John Smith', 'course': 'Computer Science', 
                    'email': 'john.smith@example.com',
                    'phone': '123-456-7890',
                    'address': '123 College St',
                    'grades': {'CS101': 1.75, 'CS102': 2.0, 'CS103': 1.25},
                    'enrolled_subjects': ['CS101', 'CS102', 'CS103'],
                    'username': 'student1',
                    'suspended': False},
            'S002': {'name': 'Emma Johnson', 'course': 'Information Technology', 
                    'email': 'emma.johnson@example.com',
                    'phone': '098-765-4321',
                    'address': '456 University Ave',
                    'grades': {'IT101': 2.0, 'IT102': 1.5, 'CS101': 1.75},
                    'enrolled_subjects': ['IT101', 'IT102', 'CS101'],
                    'username': 'student2',
                    'suspended': False}
        }
        
        self.lecturers = {
            'L001': {'name': 'Dr. Brown', 'department': 'Computer Science', 
                    'email': 'dr.brown@example.com',
                    'phone': '111-222-3333',
                    'office': 'Building A, Room 101',
                    'courses': ['CS101', 'CS102'],
                    'username': 'lecturer1',
                    'suspended': False},
            'L002': {'name': 'Prof. Wilson', 'department': 'Information Technology', 
                    'email': 'prof.wilson@example.com',
                    'phone': '444-555-6666',
                    'office': 'Building B, Room 202',
                    'courses': ['IT101', 'IT102'],
                    'username': 'lecturer2',
                    'suspended': False}
        }
        
        self.courses = {
            'CS101': {'name': 'Introduction to Programming', 'lecturer': 'L001', 'department': 'CICS'},
            'CS102': {'name': 'Data Structures', 'lecturer': 'L001', 'department': 'CICS'},
            'IT101': {'name': 'Web Development', 'lecturer': 'L002', 'department': 'CICS'},
            'IT102': {'name': 'Database Systems', 'lecturer': 'L002', 'department': 'CICS'}
        }
        
        # Department and program structure based on the flowchart
        self.departments = {
            'CICS': {
                'name': 'College of Informatics and Computing Sciences',
                'programs': ['BS Information Technology']
            },
            'CABE': {
                'name': 'College of Accountancy, Business and Economics',
                'programs': ['Bachelor of Public Administration', 'Bachelor in Business Administration', 'Bachelor of Science in Management Accounting']
            },
            'CAS': {
                'name': 'College of Arts and Sciences',
                'programs': ['Bachelor of Science in Psychology', 'Bachelor of Arts in Communication']
            },
            'CTE': {
                'name': 'College of Teacher Education',
                'programs': ['Bachelor of Secondary Education Major in English', 'Bachelor of Secondary Education Major in Mathematics', 'Bachelor of Secondary Education Major in Sciences']
            },
            'CET': {
                'name': 'College of Engineering and Technology',
                'programs': ['Bachelor of Science in Computer Engineering Technology', 'Bachelor of Science in Electrical Engineering Technology']
            }
        }
        
        # Subjects by department and program (simplified from the flowchart)
        self.program_subjects = {
            'BS Information Technology': ['GEd 101', 'GEd 102', 'GEd 108', 'Fil 101', 'PATHFIT 1'],
            'Bachelor of Public Administration': ['GEd 101', 'GEd 102', 'GEd 108', 'PA 101', 'PA 102'],
            'Bachelor in Business Administration': ['GEd 101', 'GEd 102', 'GEd 103', 'ECO 101', 'MGT 101'],
            'Bachelor of Science in Management Accounting': ['GEd 101', 'GEd 102', 'GEd 103', 'ACC 101', 'MGT 203'],
            'Bachelor of Science in Psychology': ['GEd 101', 'GEd 108', 'GEd 109', 'PSY 101', 'PATHFIT 1'],
            'Bachelor of Arts in Communication': ['GEd 101', 'GEd 106', 'GEd 109', 'COMM 101', 'PATHFIT 1'],
            'Bachelor of Secondary Education Major in English': ['NSTP 111', 'PATHFIT 1', 'GEd 101', 'GEd 102', 'GEd 103', 'Fil 101', 'Ed 101'],
            'Bachelor of Secondary Education Major in Mathematics': ['NSTP 111', 'PATHFIT 1', 'GEd 101', 'GEd 102', 'GEd 103', 'MEd 111', 'MEd 112'],
            'Bachelor of Secondary Education Major in Sciences': ['NSTP 111', 'PATHFIT 1', 'GEd 101', 'GEd 102', 'GEd 103', 'SEd 111'],
            'Bachelor of Science in Computer Engineering Technology': ['CoE T140', 'CoE T141', 'GEd 101', 'GEd 102', 'GEd 103'],
            'Bachelor of Science in Electrical Engineering Technology': ['ELEX 141', 'ELEX 142', 'GEd 101', 'GEd 102', 'GEd 103']
        }
        
        # --- Apply Poppins font globally to major UI elements ---
        # Section headers and label frames
        self.style.configure("Section.TLabelframe.Label",
            font=("Poppins", 14, "bold"),
            foreground="#e74c3c",
            background="white",
            padding=8
        )
        self.style.configure("Section.TLabelframe",
            background="white",
            borderwidth=2,
            relief="solid"
        )
        # Treeview headers
        self.style.configure("Treeview.Heading",
            background="#e74c3c",
            foreground="white",
            font=("Poppins", 13, "bold")
        )
        # Buttons
        self.style.configure("TButton",
            font=("Poppins", 12, "bold"),
            background="#fff",
            foreground="#000",
            borderwidth=1,
            focusthickness=1,
            focuscolor="#43b04a"
        )
        self.style.configure("Login.TButton", font=("Poppins", 14, "bold"))
        self.style.configure("Logout.TButton", font=("Poppins", 14, "bold"))
        self.style.configure("EditProfile.TButton", font=("Poppins", 12))
        self.style.configure("Calculate.TButton", font=("Poppins", 12))
        self.style.configure("Enroll.TButton", font=("Poppins", 12, "bold"))
        self.style.configure("Assign.TButton", font=("Poppins", 12))
        # Notebook tabs
        self.style.configure("TNotebook.Tab", font=("Poppins", 14, "bold"))
        # Entry fields
        self.style.configure("Padded.TEntry", font=("Poppins", 13))
        self.style.configure("TEntry", font=("Poppins", 13))
        # Combobox
        self.style.configure("TCombobox", font=("Poppins", 13))
        
        # Create login page
        self.create_login_page()
    
    def create_background_image(self):
        """Create a gradient background image"""
        width = 1920
        height = 1080
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)

        # Create a gradient from light blue to white
        for y in range(height):
            r = int(240 + (255 - 240) * y / height)
            g = int(240 + (255 - 240) * y / height)
            b = int(255)
            for x in range(width):
                draw.point((x, y), fill=(r, g, b))

        # Save the image
        image.save('background.jpg')
    
    def create_login_page(self):
        # Clear the window
        for widget in self.root.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        # Add a semi-transparent overlay for contrast
        # (Removed overlay so only the image is shown)
        # if self.bg_label:
        #     overlay = tk.Label(self.root, bg='#000000', bd=0)
        #     overlay.place(x=0, y=0, relwidth=1, relheight=1)
        #     overlay.configure(bg='#000000')
        #     overlay.lower(self.bg_label)
        #     overlay.configure(bg='#000000', highlightthickness=0)
        #     overlay.lift(self.bg_label)

        # Centered card frame
        card = tk.Frame(self.root, bg='white', bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor='center', width=500, height=480)
        card.grid_propagate(False)
        card.update()
        card.configure(bg='white')
        card.tkraise()
        card.after(10, lambda: card.tkraise())

        # Shadow effect (simulate with extra frame)
        shadow = tk.Frame(self.root, bg='#d0d0d0', bd=0, highlightthickness=0)
        shadow.place(relx=0.5, rely=0.5, anchor='center', width=510, height=490)
        shadow.lower(card)

        # Logo (top right)
        try:
            logo_img = Image.open('logo.png').resize((64, 64), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(card, image=logo_photo, bg='white', bd=0)
            logo_label.image = logo_photo
            logo_label.place(x=410, y=30)
        except Exception:
            pass

        # Title and version
        title = tk.Label(
            card,
            text="Welcome to Student Management System",
            font=("Poppins", 22, "bold"),
            bg='white',
            fg='#000',
            wraplength=480,
            justify="center",
            anchor="center"
        )
        title.place(x=0, y=30, width=500, height=90)  # Increased height for Poppins

        # Subtext
        subtext = tk.Label(
            card,
            text="Enter your username and password to log in:",
            font=("Poppins", 12),
            bg='white',
            fg='#000',
            anchor="center",
            justify="center"
        )
        subtext.place(x=0, y=125, width=500, height=30)

        # Username entry with placeholder and modern style
        username_var = tk.StringVar()
        username_entry = ttk.Entry(
            card,
            textvariable=username_var,
            style="Padded.TEntry"
        )
        username_entry.place(x=30, y=160, width=440, height=44)
        username_entry.insert(0, "Enter your username")
        username_entry.config(foreground='#888', font=("Poppins", 13))
        def on_user_focus_in(e):
            if username_entry.get() == "Enter your username":
                username_entry.delete(0, tk.END)
                username_entry.config(foreground='#000', font=("Poppins", 13))
        def on_user_focus_out(e):
            if not username_entry.get():
                username_entry.insert(0, "Enter your username")
                username_entry.config(foreground='#888', font=("Poppins", 13))
        username_entry.bind("<FocusIn>", on_user_focus_in)
        username_entry.bind("<FocusOut>", on_user_focus_out)

        # Password field frame for better alignment
        pw_frame = tk.Frame(card, bg='white')
        pw_frame.place(x=30, y=220, width=440, height=44)

        # Password entry with modern style
        password_var = tk.StringVar()
        password_entry = ttk.Entry(
            pw_frame,
            textvariable=password_var,
            style="Padded.TEntry",
            show=''  # Start as visible for placeholder
        )
        password_entry.place(x=0, y=0, width=440, height=44)
        password_entry.insert(0, "Enter your password")
        password_entry.config(foreground='#888', font=("Poppins", 13))
        def on_pw_focus_in(e):
            if password_entry.get() == "Enter your password":
                password_entry.delete(0, tk.END)
                password_entry.config(foreground='#000', show='*' if show_btn.cget('text') == '👁' else '', font=("Poppins", 13))
        def on_pw_focus_out(e):
            if not password_entry.get():
                password_entry.insert(0, "Enter your password")
                password_entry.config(foreground='#888', show='', font=("Poppins", 13))
        password_entry.bind("<FocusIn>", on_pw_focus_in)
        password_entry.bind("<FocusOut>", on_pw_focus_out)

        # Show/Hide password button as a seamless overlay
        def toggle_password():
            if password_entry.cget('show') == '':
                password_entry.config(show='*')
                show_btn.config(text='👁')
            else:
                password_entry.config(show='')
                show_btn.config(text='🙈')
        show_btn = tk.Label(
            pw_frame,
            text='👁',
            font=("Poppins", 15),
            bg='white',
            fg='#000',
            cursor='hand2',
        )
        show_btn.place(x=400, y=6, width=32, height=32)
        show_btn.bind('<Button-1>', lambda e: toggle_password())
        show_btn.bind('<Enter>', lambda e: show_btn.config(fg='#000'))
        show_btn.bind('<Leave>', lambda e: show_btn.config(fg='#000'))

        # Login button
        def do_login():
            self.username_var = username_var
            self.password_var = password_var
            self.login()
        login_btn = tk.Button(
            card,
            text="Log In",
            font=("Poppins", 16, "bold"),
            bg="#43b04a",
            fg="#000",
            bd=0,
            relief='flat',
            activebackground="#388e3c",
            activeforeground="#000",
            command=do_login
        )
        login_btn.place(x=30, y=280, width=440, height=54)

        # Footer/help text
        # (Removed as per user request)
        # footer = tk.Label(
        #     card,
        #     text="Forgot your password? Contact admin.",
        #     font=("Helvetica", 10),
        #     bg='white',
        #     fg='#888'
        # )
        # footer.place(x=30, y=350)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        if username in self.users and self.users[username]['password'] == password:
            user_type = self.users[username]['type']
            
            # Check if user is suspended
            if user_type != 'admin' and self.users[username].get('suspended', False):
                messagebox.showerror("Access Denied", "Your account has been suspended. Please contact the administrator.")
                return
                
            self.current_user = username
            self.user_type = user_type
            
            # Unbind the resize event to prevent crashes after login
            if hasattr(self, '_resize_bg_handler'):
                self.root.unbind('<Configure>')
            
            if user_type == 'admin':
                self.create_admin_dashboard()
            elif user_type == 'lecturer':
                self.create_lecturer_dashboard()
            elif user_type == 'student':
                # Find student ID for this username
                student_id = None
                for sid, data in self.students.items():
                    if data.get('username') == username:
                        student_id = sid
                        break
                
                if not student_id:
                    student_id = 'S001'  # Default for demo
                self.create_student_dashboard(student_id)
                
            # Adjust the window to maximize after login
            self.root.state('zoomed')
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    def create_admin_dashboard(self):
        # Clear the window
        for widget in self.root.winfo_children():
            if widget != self.bg_label:
                widget.destroy()
            
        # Main frame with semi-transparent background (define first!)
        main_frame = ttk.Frame(self.root, padding=20, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # --- Modernized Admin Dashboard UI ---
        from PIL import Image, ImageTk
        header_frame = ttk.Frame(main_frame, style="Header.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        # Add icon to header (if logo.png exists)
        try:
            logo_img = Image.open('logo.png').resize((40, 40), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(header_frame, image=logo_photo, bg="#e74c3c", bd=0)
            logo_label.image = logo_photo
            logo_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        except Exception:
            pass
        ttk.Label(header_frame, text="Admin Dashboard", style="Header.TLabel").pack(side=tk.LEFT, padx=5, pady=5)
        # Logout button larger and with icon
        try:
            logout_img = Image.open('logout_icon.png').resize((20, 20), Image.Resampling.LANCZOS)
            logout_photo = ImageTk.PhotoImage(logout_img)
            logout_btn = tk.Button(
                header_frame,
                text=" Logout",
                font=("Helvetica", 14, "bold"),
                bg="#e74c3c",
                fg="white",
                activebackground="#c0392b",
                activeforeground="white",
                bd=2,
                relief="ridge",
                command=self.create_login_page,
                cursor="hand2",
                image=logout_photo,
                compound=tk.LEFT
            )
            logout_btn.image = logout_photo
        except Exception:
            logout_btn = tk.Button(
                header_frame,
                text="Logout",
                font=("Helvetica", 14, "bold"),
                bg="#e74c3c",
                fg="white",
                activebackground="#c0392b",
                activeforeground="white",
                bd=2,
                relief="ridge",
                command=self.create_login_page,
                cursor="hand2"
            )
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=8)

        # Notebook with icons and larger tabs
        self.style.configure("TNotebook.Tab", font=("Helvetica", 14, "bold"), padding=[20, 10])
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Always define the frames first, before icon logic
        students_frame = ttk.Frame(notebook, padding=10, style="Card.TFrame")
        lecturers_frame = ttk.Frame(notebook, padding=10, style="Card.TFrame")
        accounts_frame = ttk.Frame(notebook, padding=10, style="Card.TFrame")

        # Try to add icons if available, otherwise fall back to text
        try:
            student_icon = ImageTk.PhotoImage(Image.open('student_icon.png').resize((24, 24), Image.Resampling.LANCZOS))
            lecturer_icon = ImageTk.PhotoImage(Image.open('lecturer_icon.png').resize((24, 24), Image.Resampling.LANCZOS))
            user_icon = ImageTk.PhotoImage(Image.open('user_icon.png').resize((24, 24), Image.Resampling.LANCZOS))
            notebook.add(students_frame, text="  Manage Students", image=student_icon, compound=tk.LEFT)
            notebook.add(lecturers_frame, text="  Manage Lecturers", image=lecturer_icon, compound=tk.LEFT)
            notebook.add(accounts_frame, text="  User Accounts", image=user_icon, compound=tk.LEFT)
            notebook._student_icon = student_icon
            notebook._lecturer_icon = lecturer_icon
            notebook._user_icon = user_icon
        except Exception as e:
            # If any icon is missing or fails to load, just use text tabs
            notebook.add(students_frame, text="Manage Students")
            notebook.add(lecturers_frame, text="Manage Lecturers")
            notebook.add(accounts_frame, text="User Accounts")

        # Continue with the rest of the dashboard setup
        self.create_student_management(students_frame)
        self.create_lecturer_management(lecturers_frame)
        self.create_user_accounts_management(accounts_frame)
    
    def create_student_management(self, parent_frame):
        # Add student section
        add_frame = ttk.LabelFrame(parent_frame, text="Add New Student", padding=10, style="Section.TLabelframe")
        add_frame.pack(fill=tk.X, pady=10)
        
        # Grid for add student form
        ttk.Label(add_frame, text="Student ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.new_student_id = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_student_id, width=20, style="Padded.TEntry").grid(row=0, column=1, pady=5)
        
        ttk.Label(add_frame, text="Name:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=10)
        self.new_student_name = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_student_name, width=20, style="Padded.TEntry").grid(row=0, column=3, pady=5)
        
        ttk.Label(add_frame, text="Program:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.new_student_course = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_student_course, width=20, style="Padded.TEntry").grid(row=1, column=1, pady=5)
        
        ttk.Label(add_frame, text="Email:").grid(row=1, column=2, sticky=tk.W, pady=5, padx=10)
        self.new_student_email = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_student_email, width=20, style="Padded.TEntry").grid(row=1, column=3, pady=5)
        
        ttk.Label(add_frame, text="Phone:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.new_student_phone = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_student_phone, width=20, style="Padded.TEntry").grid(row=2, column=1, pady=5)
        
        ttk.Label(add_frame, text="Address:").grid(row=2, column=2, sticky=tk.W, pady=5, padx=10)
        self.new_student_address = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_student_address, width=20, style="Padded.TEntry").grid(row=2, column=3, pady=5)
        
        ttk.Label(add_frame, text="Department:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.new_student_dept = tk.StringVar()
        dept_combo = ttk.Combobox(add_frame, textvariable=self.new_student_dept, width=18)
        dept_combo['values'] = list(self.departments.keys())
        dept_combo.grid(row=3, column=1, pady=5)
        
        ttk.Button(add_frame, text="Save Student", command=self.add_student).grid(row=4, column=3, pady=10)
        
        # List student section
        list_frame = ttk.LabelFrame(parent_frame, text="Student List", padding=10, style="Section.TLabelframe")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview for student list
        columns = ('id', 'name', 'course', 'email', 'status')
        self.student_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Set column headings
        self.student_tree.heading('id', text='ID')
        self.student_tree.heading('name', text='Name')
        self.student_tree.heading('course', text='Program')
        self.student_tree.heading('email', text='Email')
        self.student_tree.heading('status', text='Status')
        
        # Set column widths
        self.student_tree.column('id', width=80)
        self.student_tree.column('name', width=150)
        self.student_tree.column('course', width=150)
        self.student_tree.column('email', width=180)
        self.student_tree.column('status', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.student_tree.yview)
        self.student_tree.configure(yscroll=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.student_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="View Details", command=self.view_student_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit", command=self.edit_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remove", command=self.remove_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Suspend/Unsuspend", command=self.toggle_student_suspension).pack(side=tk.LEFT, padx=5)
        
        # Populate treeview with data
        self.refresh_student_list()
    
    def toggle_student_suspension(self):
        selected_item = self.student_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a student to suspend/unsuspend")
            return
            
        # Get the student ID
        student_id = self.student_tree.item(selected_item, 'values')[0]
        name = self.students[student_id]['name']
        
        # Toggle suspension status
        username = self.students[student_id].get('username')
        if username and username in self.users:
            current_status = self.users[username].get('suspended', False)
            new_status = not current_status
            
            self.users[username]['suspended'] = new_status
            self.students[student_id]['suspended'] = new_status
            
            status_msg = "suspended" if new_status else "unsuspended"
            messagebox.showinfo("Success", f"Student {name} has been {status_msg}")
            self.refresh_student_list()
    
    def add_student(self):
        student_id = self.new_student_id.get()
        name = self.new_student_name.get()
        course = self.new_student_course.get()
        email = self.new_student_email.get()
        phone = self.new_student_phone.get()
        address = self.new_student_address.get()
        department = self.new_student_dept.get()
        
        if not (student_id and name and course and email):
            messagebox.showerror("Validation Error", "Student ID, Name, Course, and Email are required")
            return
        
        if student_id in self.students:
            messagebox.showerror("Validation Error", "Student ID already exists")
            return
            
        # Validate email format
        if not re.match(r"[^@]+@[^@]+.[^@]+", email):
            messagebox.showerror("Validation Error", "Invalid email format")
            return
        
        # Generate username and password for the new student
        username = f"student_{student_id.lower()}"
        password = f"pass_{student_id.lower()}"
        
        # Add to dictionaries
        self.students[student_id] = {
            'name': name,
            'course': course,
            'email': email,
            'phone': phone,
            'address': address,
            'grades': {},
            'enrolled_subjects': [],
            'username': username,
            'suspended': False,
            'department': department
        }
        
        # Add user account for login
        self.users[username] = {
            'password': password,
            'type': 'student',
            'suspended': False
        }
        
        messagebox.showinfo("Success", f"Student {name} added successfully\nUsername: {username}\nPassword: {password}")
        self.refresh_student_list()
        
        # Clear form
        self.new_student_id.set('')
        self.new_student_name.set('')
        self.new_student_course.set('')
        self.new_student_email.set('')
        self.new_student_phone.set('')
        self.new_student_address.set('')
        self.new_student_dept.set('')
    
    def view_student_details(self):
        selected_item = self.student_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a student to view")
            return
            
        # Get the student ID
        student_id = self.student_tree.item(selected_item, 'values')[0]
        student = self.students[student_id]
        
        # Create a new window to display details
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Student Details - {student['name']}")
        details_window.geometry("500x400")
        
        # Details frame
        details_frame = ttk.Frame(details_window, padding=20)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Display student details
        ttk.Label(details_frame, text=f"Student ID: {student_id}").pack(anchor=tk.W, pady=2)
        ttk.Label(details_frame, text=f"Name: {student['name']}").pack(anchor=tk.W, pady=2)
        ttk.Label(details_frame, text=f"Program: {student['course']}").pack(anchor=tk.W, pady=2)
        ttk.Label(details_frame, text=f"Email: {student['email']}").pack(anchor=tk.W, pady=2)
        ttk.Label(details_frame, text=f"Phone: {student.get('phone', 'N/A')}").pack(anchor=tk.W, pady=2)
        ttk.Label(details_frame, text=f"Address: {student.get('address', 'N/A')}").pack(anchor=tk.W, pady=2)
        
        # Status information
        status = "Suspended" if student.get('suspended', False) else "Active"
        ttk.Label(details_frame, text=f"Status: {status}").pack(anchor=tk.W, pady=2)
        
        # Username info
        if 'username' in student:
            ttk.Label(details_frame, text="Login Information:").pack(anchor=tk.W, pady=5)
            ttk.Label(details_frame, text=f"Username: {student['username']}").pack(anchor=tk.W, pady=2)
            username = student['username']
            if username in self.users:
                ttk.Label(details_frame, text=f"Password: {self.users[username]['password']}").pack(anchor=tk.W, pady=2)
        
        # Enrolled subjects
        ttk.Label(details_frame, text="Enrolled Subjects:").pack(anchor=tk.W, pady=5)
        subjects = student.get('enrolled_subjects', [])
        if subjects:
            for subject in subjects:
                subject_name = self.courses.get(subject, {}).get('name', subject)
                ttk.Label(details_frame, text=f"• {subject}: {subject_name}").pack(anchor=tk.W, pady=1)
        else:
            ttk.Label(details_frame, text="No subjects enrolled").pack(anchor=tk.W, pady=1)
            
        # Calculate GWA if grades exist
        if student.get('grades'):
            grades = student['grades']
            if grades:
                gwa = self.calculate_gwa(grades)
                ttk.Label(details_frame, text=f"General Weighted Average: {gwa:.2f}").pack(anchor=tk.W, pady=5)
        
        # Close button
        ttk.Button(details_frame, text="Close", command=details_window.destroy).pack(pady=10)
    
    def refresh_student_list(self):
        # Clear existing items
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
            
        # Add students to treeview
        for student_id, data in self.students.items():
            status = "Suspended" if data.get('suspended', False) else "Active"
            self.student_tree.insert('', tk.END, values=(student_id, data['name'], data['course'], data.get('email', 'N/A'), status))
    
    def edit_student(self):
        selected_item = self.student_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a student to edit")
            return
            
        # Get the student ID
        student_id = self.student_tree.item(selected_item, 'values')[0]
        student = self.students[student_id]
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Student - {student['name']}")
        edit_window.geometry("400x400")
        
        # Edit form
        form_frame = ttk.Frame(edit_window, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Student details form
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar(value=student['name'])
        ttk.Entry(form_frame, textvariable=name_var, width=30, style="Padded.TEntry").grid(row=0, column=1, pady=5)
        
        ttk.Label(form_frame, text="Program:").grid(row=1, column=0, sticky=tk.W, pady=5)
        course_var = tk.StringVar(value=student['course'])
        ttk.Entry(form_frame, textvariable=course_var, width=30, style="Padded.TEntry").grid(row=1, column=1, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        email_var = tk.StringVar(value=student.get('email', ''))
        ttk.Entry(form_frame, textvariable=email_var, width=30, style="Padded.TEntry").grid(row=2, column=1, pady=5)
        
        ttk.Label(form_frame, text="Phone:").grid(row=3, column=0, sticky=tk.W, pady=5)
        phone_var = tk.StringVar(value=student.get('phone', ''))
        ttk.Entry(form_frame, textvariable=phone_var, width=30, style="Padded.TEntry").grid(row=3, column=1, pady=5)
        
        ttk.Label(form_frame, text="Address:").grid(row=4, column=0, sticky=tk.W, pady=5)
        address_var = tk.StringVar(value=student.get('address', ''))
        ttk.Entry(form_frame, textvariable=address_var, width=30, style="Padded.TEntry").grid(row=4, column=1, pady=5)
        
        ttk.Label(form_frame, text="Status:").grid(row=5, column=0, sticky=tk.W, pady=5)
        status_var = tk.StringVar(value="Suspended" if student.get('suspended', False) else "Active")
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, width=28)
        status_combo['values'] = ["Active", "Suspended"]
        status_combo.grid(row=5, column=1, pady=5)
        status_combo.state(['readonly'])
        
        # Save function
        def save_changes():
            # Update student information
            self.students[student_id]['name'] = name_var.get()
            self.students[student_id]['course'] = course_var.get()
            self.students[student_id]['email'] = email_var.get()
            self.students[student_id]['phone'] = phone_var.get()
            self.students[student_id]['address'] = address_var.get()
            
            # Update suspension status
            new_suspended = (status_var.get() == "Suspended")
            self.students[student_id]['suspended'] = new_suspended
            
            # Update user account status too
            if 'username' in student:
                username = student['username']
                if username in self.users:
                    self.users[username]['suspended'] = new_suspended
            
            messagebox.showinfo("Success", "Student information updated")
            edit_window.destroy()
            self.refresh_student_list()
            
        # Reset password function
        def reset_password():
            if 'username' in student:
                username = student['username']
                if username in self.users:
                    new_password = f"reset_{student_id.lower()}"
                    self.users[username]['password'] = new_password
                    messagebox.showinfo("Success", f"Password has been reset to: {new_password}")
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Save Changes", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Reset Password", command=reset_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=edit_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def remove_student(self):
        selected_item = self.student_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a student to remove")
            return
            
        # Get the student ID
        student_id = self.student_tree.item(selected_item, 'values')[0]
        name = self.students[student_id]['name']
        
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to remove {name}?")
        if confirm:
            # Remove user account if exists
            if 'username' in self.students[student_id]:
                username = self.students[student_id]['username']
                if username in self.users:
                    del self.users[username]
            
            # Remove student record
            del self.students[student_id]
            messagebox.showinfo("Success", f"Student {name} removed successfully")
            self.refresh_student_list()
    
    def create_user_accounts_management(self, parent_frame):
        # Add user account section
        add_frame = ttk.LabelFrame(parent_frame, text="Create User Account", padding=10, style="Section.TLabelframe")
        add_frame.pack(fill=tk.X, pady=10)
        
        # Grid for add user form
        ttk.Label(add_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.new_username = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_username, width=20, style="Padded.TEntry").grid(row=0, column=1, pady=5)
        
        ttk.Label(add_frame, text="Password:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=10)
        self.new_password = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_password, width=20, style="Padded.TEntry").grid(row=0, column=3, pady=5)
        
        ttk.Label(add_frame, text="User Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.new_user_type = tk.StringVar(value="student")
        ttk.Combobox(add_frame, textvariable=self.new_user_type, 
                     values=["Student", "Lecturer", "Admin"], width=18).grid(row=1, column=1, pady=5)
        
        ttk.Button(add_frame, text="Create Account", command=self.add_user_account).grid(row=1, column=3, pady=5)
        
        # List accounts section
        list_frame = ttk.LabelFrame(parent_frame, text="User Accounts", padding=10, style="Section.TLabelframe")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview for user list
        columns = ('username', 'type', 'status')
        self.users_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Set column headings
        self.users_tree.heading('username', text='Username')
        self.users_tree.heading('type', text='User Type')
        self.users_tree.heading('status', text='Status')
        
        # Set column widths
        self.users_tree.column('username', width=200)
        self.users_tree.column('type', width=100)
        self.users_tree.column('status', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.users_tree.yview)
        self.users_tree.configure(yscroll=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Reset Password", command=self.reset_user_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Account", command=self.delete_user_account).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Suspend/Unsuspend", command=self.toggle_user_suspension).pack(side=tk.LEFT, padx=5)
        
        # Populate treeview with data
        self.refresh_users_list()
    
    def toggle_user_suspension(self):
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a user to suspend/unsuspend")
            return
            
        # Get the username and type
        username = self.users_tree.item(selected_item, 'values')[0]
        user_type = self.users_tree.item(selected_item, 'values')[1]
        
        # Don't allow suspending admin accounts
        if user_type == 'admin':
            messagebox.showerror("Error", "Admin accounts cannot be suspended")
            return
        
        # Toggle suspension status
        current_status = self.users[username].get('suspended', False)
        new_status = not current_status
        self.users[username]['suspended'] = new_status
        
        # Also update the corresponding student or lecturer record
        if user_type == 'student':
            for student_id, data in self.students.items():
                if data.get('username') == username:
                    self.students[student_id]['suspended'] = new_status
                    break
        elif user_type == 'lecturer':
            for lecturer_id, data in self.lecturers.items():
                if data.get('username') == username:
                    self.lecturers[lecturer_id]['suspended'] = new_status
                    break
        
        status_msg = "suspended" if new_status else "unsuspended"
        messagebox.showinfo("Success", f"User {username} has been {status_msg}")
        self.refresh_users_list()
    
    def add_user_account(self):
        username = self.new_username.get()
        password = self.new_password.get()
        user_type = self.new_user_type.get()
        
        if not (username and password):
            messagebox.showerror("Validation Error", "Username and Password are required")
            return
        
        if username in self.users:
            messagebox.showerror("Validation Error", "Username already exists")
            return
        
        # Add user account
        self.users[username] = {
            'password': password, 
            'type': user_type,
            'suspended': False
        }
        
        messagebox.showinfo("Success", f"User account {username} created successfully")
        self.refresh_users_list()
        
        # Clear form
        self.new_username.set('')
        self.new_password.set('')
    
    def refresh_users_list(self):
        # Clear existing items
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
            
        # Add users to treeview
        for username, data in self.users.items():
            status = "Suspended" if data.get('suspended', False) else "Active"
            self.users_tree.insert('', tk.END, values=(username, data['type'], status))
    
    def reset_user_password(self):
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a user to reset password")
            return
            
        # Get the username
        username = self.users_tree.item(selected_item, 'values')[0]
        
        # Create reset window
        reset_window = tk.Toplevel(self.root)
        reset_window.title(f"Reset Password for {username}")
        reset_window.geometry("300x150")
        
        # Reset form
        form_frame = ttk.Frame(reset_window, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text="New Password:").grid(row=0, column=0, sticky=tk.W, pady=5)
        new_password = tk.StringVar(value="newpass123")
        ttk.Entry(form_frame, textvariable=new_password, width=20, style="Padded.TEntry").grid(row=0, column=1, pady=5)
        
        # Save function
        def save_password():
            if username in self.users:
                self.users[username]['password'] = new_password.get()
                messagebox.showinfo("Success", "Password has been reset")
                reset_window.destroy()
            
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Save", command=save_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=reset_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def delete_user_account(self):
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a user to delete")
            return
            
        # Get the username
        username = self.users_tree.item(selected_item, 'values')[0]
        
        # Prevent deleting the current user
        if username == self.current_user:
            messagebox.showerror("Error", "You cannot delete your own account while logged in")
            return
            
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete the account {username}?")
        if confirm:
            del self.users[username]
            messagebox.showinfo("Success", f"User account {username} deleted successfully")
            self.refresh_users_list()
    
    def create_lecturer_management(self, parent_frame):
        # Add lecturer section
        add_frame = ttk.LabelFrame(parent_frame, text="Add New Lecturer", padding=10, style="Section.TLabelframe")
        add_frame.pack(fill=tk.X, pady=10)
        
        # Grid for add lecturer form
        ttk.Label(add_frame, text="Lecturer ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.new_lecturer_id = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_lecturer_id, width=20, style="Padded.TEntry").grid(row=0, column=1, pady=5)
        
        ttk.Label(add_frame, text="Name:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=10)
        self.new_lecturer_name = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_lecturer_name, width=20, style="Padded.TEntry").grid(row=0, column=3, pady=5)
        
        ttk.Label(add_frame, text="Department:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.new_lecturer_dept = tk.StringVar()
        dept_combo = ttk.Combobox(add_frame, textvariable=self.new_lecturer_dept, width=18) 
        dept_combo['values'] = list(self.departments.keys())
        dept_combo.grid(row=1, column=1, pady=5)
        
        ttk.Label(add_frame, text="Email:").grid(row=1, column=2, sticky=tk.W, pady=5, padx=10)
        self.new_lecturer_email = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_lecturer_email, width=20, style="Padded.TEntry").grid(row=1, column=3, pady=5)
        
        ttk.Label(add_frame, text="Phone:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.new_lecturer_phone = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_lecturer_phone, width=20, style="Padded.TEntry").grid(row=2, column=1, pady=5)
        
        ttk.Label(add_frame, text="Office:").grid(row=2, column=2, sticky=tk.W, pady=5, padx=10)
        self.new_lecturer_office = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_lecturer_office, width=20, style="Padded.TEntry").grid(row=2, column=3, pady=5)
        
        ttk.Button(add_frame, text="Save Lecturer", command=self.add_lecturer).grid(row=3, column=3, pady=10)
        
        # List lecturer section
        list_frame = ttk.LabelFrame(parent_frame, text="Lecturer List", padding=10, style="Section.TLabelframe")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview for lecturer list
        columns = ('id', 'name', 'department', 'email', 'status')
        self.lecturer_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Set column headings
        self.lecturer_tree.heading('id', text='ID')
        self.lecturer_tree.heading('name', text='Name')
        self.lecturer_tree.heading('department', text='Department')
        self.lecturer_tree.heading('email', text='Email')
        self.lecturer_tree.heading('status', text='Status')
        
        # Set column widths
        self.lecturer_tree.column('id', width=80)
        self.lecturer_tree.column('name', width=150)
        self.lecturer_tree.column('department', width=150)
        self.lecturer_tree.column('email', width=180)
        self.lecturer_tree.column('status', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.lecturer_tree.yview)
        self.lecturer_tree.configure(yscroll=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.lecturer_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="View Details", command=self.view_lecturer_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit", command=self.edit_lecturer).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remove", command=self.remove_lecturer).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Suspend/Unsuspend", command=self.toggle_lecturer_suspension).pack(side=tk.LEFT, padx=5)
        
        # Populate treeview with data
        self.refresh_lecturer_list()
    
    def toggle_lecturer_suspension(self):
        selected_item = self.lecturer_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a lecturer to suspend/unsuspend")
            return
            
        # Get the lecturer ID
        lecturer_id = self.lecturer_tree.item(selected_item, 'values')[0]
        name = self.lecturers[lecturer_id]['name']
        
        # Toggle suspension status
        username = self.lecturers[lecturer_id].get('username')
        if username and username in self.users:
            current_status = self.users[username].get('suspended', False)
            new_status = not current_status
            
            self.users[username]['suspended'] = new_status
            self.lecturers[lecturer_id]['suspended'] = new_status
            
            status_msg = "suspended" if new_status else "unsuspended"
            messagebox.showinfo("Success", f"Lecturer {name} has been {status_msg}")
            self.refresh_lecturer_list()
    
    def add_lecturer(self):
        lecturer_id = self.new_lecturer_id.get()
        name = self.new_lecturer_name.get()
        department = self.new_lecturer_dept.get()
        email = self.new_lecturer_email.get()
        phone = self.new_lecturer_phone.get()
        office = self.new_lecturer_office.get()
        
        if not (lecturer_id and name and department and email):
            messagebox.showerror("Validation Error", "Lecturer ID, Name, Department, and Email are required")
            return
        
        if lecturer_id in self.lecturers:
            messagebox.showerror("Validation Error", "Lecturer ID already exists")
            return
            
        # Validate email format
        if not re.match(r"[^@]+@[^@]+.[^@]+", email):
            messagebox.showerror("Validation Error", "Invalid email format")
            return
        
        # Generate username and password for the new lecturer
        username = f"lecturer_{lecturer_id.lower()}"
        password = f"pass_{lecturer_id.lower()}"
        
        # Add to dictionaries
        self.lecturers[lecturer_id] = {
            'name': name,
            'department': department,
            'email': email,
            'phone': phone,
            'office': office,
            'courses': [],
            'username': username,
            'suspended': False
        }
        
        # Add user account for login
        self.users[username] = {
            'password': password,
            'type': 'lecturer',
            'suspended': False
        }
        
        messagebox.showinfo("Success", f"Lecturer {name} added successfully\nUsername: {username}\nPassword: {password}")
        self.refresh_lecturer_list()
        
        # Clear form
        self.new_lecturer_id.set('')
        self.new_lecturer_name.set('')
        self.new_lecturer_dept.set('')
        self.new_lecturer_email.set('')
        self.new_lecturer_phone.set('')
        self.new_lecturer_office.set('')
    
    def view_lecturer_details(self):
        selected_item = self.lecturer_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a lecturer to view")
            return
            
        # Get the lecturer ID
        lecturer_id = self.lecturer_tree.item(selected_item, 'values')[0]
        lecturer = self.lecturers[lecturer_id]
        
        # Create a new window to display details
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Lecturer Details - {lecturer['name']}")
        details_window.geometry("400x400")
        
        # Details frame
        details_frame = ttk.Frame(details_window, padding=20)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Display lecturer details
        ttk.Label(details_frame, text=f"Lecturer ID: {lecturer_id}").pack(anchor=tk.W, pady=2)
        ttk.Label(details_frame, text=f"Name: {lecturer['name']}").pack(anchor=tk.W, pady=2)
        ttk.Label(details_frame, text=f"Department: {lecturer['department']}").pack(anchor=tk.W, pady=2)
        ttk.Label(details_frame, text=f"Email: {lecturer['email']}").pack(anchor=tk.W, pady=2)
        ttk.Label(details_frame, text=f"Phone: {lecturer.get('phone', 'N/A')}").pack(anchor=tk.W, pady=2)
        ttk.Label(details_frame, text=f"Office: {lecturer.get('office', 'N/A')}").pack(anchor=tk.W, pady=2)
        
        # Status information
        status = "Suspended" if lecturer.get('suspended', False) else "Active"
        ttk.Label(details_frame, text=f"Status: {status}").pack(anchor=tk.W, pady=2)
        
        # Courses taught
        ttk.Label(details_frame, text="Courses:").pack(anchor=tk.W, pady=5)
        courses_text = ", ".join(lecturer['courses']) if lecturer['courses'] else "None"
        ttk.Label(details_frame, text=courses_text).pack(anchor=tk.W, pady=2)
        
        # Username info
        if 'username' in lecturer:
            ttk.Label(details_frame, text="Login Information:").pack(anchor=tk.W, pady=5)
            ttk.Label(details_frame, text=f"Username: {lecturer['username']}").pack(anchor=tk.W, pady=2)
            username = lecturer['username']
            if username in self.users:
                ttk.Label(details_frame, text=f"Password: {self.users[username]['password']}").pack(anchor=tk.W, pady=2)
        
        # Close button
        ttk.Button(details_frame, text="Close", command=details_window.destroy).pack(pady=10)
    
    def refresh_lecturer_list(self):
        # Clear existing items
        for item in self.lecturer_tree.get_children():
            self.lecturer_tree.delete(item)
            
        # Add lecturers to treeview
        for lecturer_id, data in self.lecturers.items():
            status = "Suspended" if data.get('suspended', False) else "Active"
            self.lecturer_tree.insert('', tk.END, values=(lecturer_id, data['name'], data['department'], data.get('email', 'N/A'), status))
    
    def edit_lecturer(self):
        selected_item = self.lecturer_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a lecturer to edit")
            return
            
        # Get the lecturer ID
        lecturer_id = self.lecturer_tree.item(selected_item, 'values')[0]
        lecturer = self.lecturers[lecturer_id]
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Lecturer - {lecturer['name']}")
        edit_window.geometry("400x450")
        
        # Edit form
        form_frame = ttk.Frame(edit_window, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Lecturer details form
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar(value=lecturer['name'])
        ttk.Entry(form_frame, textvariable=name_var, width=30, style="Padded.TEntry").grid(row=0, column=1, pady=5)
        
        ttk.Label(form_frame, text="Department:").grid(row=1, column=0, sticky=tk.W, pady=5)
        dept_var = tk.StringVar(value=lecturer['department'])
        dept_combo = ttk.Combobox(form_frame, textvariable=dept_var, width=28)
        dept_combo['values'] = list(self.departments.keys())
        dept_combo.grid(row=1, column=1, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        email_var = tk.StringVar(value=lecturer.get('email', ''))
        ttk.Entry(form_frame, textvariable=email_var, width=30, style="Padded.TEntry").grid(row=2, column=1, pady=5)
        
        ttk.Label(form_frame, text="Phone:").grid(row=3, column=0, sticky=tk.W, pady=5)
        phone_var = tk.StringVar(value=lecturer.get('phone', ''))
        ttk.Entry(form_frame, textvariable=phone_var, width=30, style="Padded.TEntry").grid(row=3, column=1, pady=5)
        
        ttk.Label(form_frame, text="Office:").grid(row=4, column=0, sticky=tk.W, pady=5)
        office_var = tk.StringVar(value=lecturer.get('office', ''))
        ttk.Entry(form_frame, textvariable=office_var, width=30, style="Padded.TEntry").grid(row=4, column=1, pady=5)
        
        ttk.Label(form_frame, text="Status:").grid(row=5, column=0, sticky=tk.W, pady=5)
        status_var = tk.StringVar(value="Suspended" if lecturer.get('suspended', False) else "Active")
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, width=28)
        status_combo['values'] = ["Active", "Suspended"]
        status_combo.grid(row=5, column=1, pady=5)
        status_combo.state(['readonly'])
        
        # Courses section
        ttk.Label(form_frame, text="Courses:").grid(row=6, column=0, sticky=tk.W, pady=5)
        courses_text = tk.Text(form_frame, width=22, height=3)
        courses_text.grid(row=6, column=1, pady=5)
        courses_text.insert(tk.END, ", ".join(lecturer['courses']))
        
        # Save function
        def save_changes():
            # Update lecturer information
            self.lecturers[lecturer_id]['name'] = name_var.get()
            self.lecturers[lecturer_id]['department'] = dept_var.get()
            self.lecturers[lecturer_id]['email'] = email_var.get()
            self.lecturers[lecturer_id]['phone'] = phone_var.get()
            self.lecturers[lecturer_id]['office'] = office_var.get()
            
            # Update suspension status
            new_suspended = (status_var.get() == "Suspended")
            self.lecturers[lecturer_id]['suspended'] = new_suspended
            
            # Update user account status too
            if 'username' in lecturer:
                username = lecturer['username']
                if username in self.users:
                    self.users[username]['suspended'] = new_suspended
            
            # Update courses
            courses_raw = courses_text.get("1.0", tk.END).strip()
            if courses_raw:
                courses_list = [c.strip() for c in courses_raw.split(",")]
                self.lecturers[lecturer_id]['courses'] = courses_list
            else:
                self.lecturers[lecturer_id]['courses'] = []
            
            messagebox.showinfo("Success", "Lecturer information updated")
            edit_window.destroy()
            self.refresh_lecturer_list()
            
        # Reset password function
        def reset_password():
            if 'username' in lecturer:
                username = lecturer['username']
                if username in self.users:
                    new_password = f"reset_{lecturer_id.lower()}"
                    self.users[username]['password'] = new_password
                    messagebox.showinfo("Success", f"Password has been reset to: {new_password}")
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Save Changes", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Reset Password", command=reset_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=edit_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def remove_lecturer(self):
        selected_item = self.lecturer_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a lecturer to remove")
            return
            
        # Get the lecturer ID
        lecturer_id = self.lecturer_tree.item(selected_item, 'values')[0]
        name = self.lecturers[lecturer_id]['name']
        
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to remove {name}?")
        if confirm:
            # Remove user account if exists
            if 'username' in self.lecturers[lecturer_id]:
                username = self.lecturers[lecturer_id]['username']
                if username in self.users:
                    del self.users[username]
            
            # Remove lecturer record
            del self.lecturers[lecturer_id]
            messagebox.showinfo("Success", f"Lecturer {name} removed successfully")
            self.refresh_lecturer_list()
    
    def create_lecturer_dashboard(self):
        # Clear the window
        for widget in self.root.winfo_children():
            if widget != self.bg_label:
                widget.destroy()
            
        # Main frame with semi-transparent background
        main_frame = ttk.Frame(self.root, padding=20, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # Header with logo and logout button
        header_frame = ttk.Frame(main_frame, style="Header.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Add icon to header (if logo.png exists)
        try:
            logo_img = Image.open('logo.png').resize((40, 40), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(header_frame, image=logo_photo, bg="#e74c3c", bd=0)
            logo_label.image = logo_photo
            logo_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        except Exception:
            pass
            
        ttk.Label(header_frame, text="Lecturer Dashboard", style="Header.TLabel").pack(side=tk.LEFT, padx=5, pady=5)
        
        # Logout button with icon
        try:
            logout_img = Image.open('logout_icon.png').resize((20, 20), Image.Resampling.LANCZOS)
            logout_photo = ImageTk.PhotoImage(logout_img)
            logout_btn = tk.Button(
                header_frame,
                text=" Logout",
                font=("Helvetica", 14, "bold"),
                bg="#e74c3c",
                fg="white",
                activebackground="#c0392b",
                activeforeground="white",
                bd=2,
                relief="ridge",
                command=self.create_login_page,
                cursor="hand2",
                image=logout_photo,
                compound=tk.LEFT
            )
            logout_btn.image = logout_photo
        except Exception:
            logout_btn = tk.Button(
                header_frame,
                text="Logout",
                font=("Helvetica", 14, "bold"),
                bg="#e74c3c",
                fg="white",
                activebackground="#c0392b",
                activeforeground="white",
                bd=2,
                relief="ridge",
                command=self.create_login_page,
                cursor="hand2"
            )
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=8)

        # Get current lecturer info
        lecturer_id = None
        for lid, data in self.lecturers.items():
            if data.get('username') == self.current_user:
                lecturer_id = lid
                break
                
        if not lecturer_id:
            messagebox.showerror("Error", "Lecturer not found")
            self.create_login_page()
            return
            
        lecturer_info = self.lecturers[lecturer_id]
        
        # Display lecturer info in a styled card
        info_frame = ttk.LabelFrame(main_frame, text="Personal Information", 
                                  padding=10, style="Section.TLabelframe")
        info_frame.pack(fill=tk.X, pady=10)
        
        # Personal info with icons
        info_grid = ttk.Frame(info_frame, style="InfoCard.TFrame")
        info_grid.pack(fill=tk.X, pady=5)
        
        # Left column
        left_col = ttk.Frame(info_grid, style="InfoCard.TFrame")
        left_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        ttk.Label(left_col, text=f"Name: {lecturer_info['name']}", 
                 style="InfoCard.TLabel").pack(anchor=tk.W, pady=2)
        ttk.Label(left_col, text=f"Department: {lecturer_info['department']}", 
                 style="InfoCard.TLabel").pack(anchor=tk.W, pady=2)
        ttk.Label(left_col, text=f"Email: {lecturer_info.get('email', 'N/A')}", 
                 style="InfoCard.TLabel").pack(anchor=tk.W, pady=2)
        
        # Right column
        right_col = ttk.Frame(info_grid, style="InfoCard.TFrame")
        right_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        ttk.Label(right_col, text=f"Phone: {lecturer_info.get('phone', 'N/A')}", 
                 style="InfoCard.TLabel").pack(anchor=tk.W, pady=2)
        ttk.Label(right_col, text=f"Office: {lecturer_info.get('office', 'N/A')}", 
                 style="InfoCard.TLabel").pack(anchor=tk.W, pady=2)
        
        # Edit profile button with custom style
        ttk.Button(info_frame, text="Edit Profile", 
                  command=lambda: self.edit_lecturer_profile(lecturer_id),
                  style="EditProfile.TButton").pack(anchor=tk.W, pady=5)
        
        # Notebook with icons and larger tabs
        self.style.configure("TNotebook.Tab", font=("Helvetica", 14, "bold"), padding=[20, 10])
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Always define the frames first, before icon logic
        courses_frame = ttk.Frame(notebook, padding=10, style="Card.TFrame")
        grades_frame = ttk.Frame(notebook, padding=10, style="Card.TFrame")
        students_frame = ttk.Frame(notebook, padding=10, style="Card.TFrame")

        # Try to add icons if available, otherwise fall back to text
        try:
            course_icon = ImageTk.PhotoImage(Image.open('course_icon.png').resize((24, 24), Image.Resampling.LANCZOS))
            grade_icon = ImageTk.PhotoImage(Image.open('grade_icon.png').resize((24, 24), Image.Resampling.LANCZOS))
            student_icon = ImageTk.PhotoImage(Image.open('student_icon.png').resize((24, 24), Image.Resampling.LANCZOS))
            notebook.add(courses_frame, text="  Manage Courses", image=course_icon, compound=tk.LEFT)
            notebook.add(grades_frame, text="  Assign Grades", image=grade_icon, compound=tk.LEFT)
            notebook.add(students_frame, text="  View Students", image=student_icon, compound=tk.LEFT)
            notebook._course_icon = course_icon
            notebook._grade_icon = grade_icon
            notebook._student_icon = student_icon
        except Exception as e:
            # If any icon is missing or fails to load, just use text tabs
            notebook.add(courses_frame, text="Manage Courses")
            notebook.add(grades_frame, text="Assign Grades")
            notebook.add(students_frame, text="View Students")

        # Continue with the rest of the dashboard setup
        self.create_lecturer_courses_tab(courses_frame, lecturer_id)
        self.create_lecturer_grades_tab(grades_frame, lecturer_id)
        self.display_lecturer_students(students_frame, lecturer_id)
    
    def create_student_dashboard(self, student_id=None):
        # Clear the window
        for widget in self.root.winfo_children():
            if widget != self.bg_label:
                widget.destroy()
            
        # If no student_id provided, use the first student for demo
        if not student_id:
            student_id = 'S001'
            
        student_info = self.students[student_id]
        
        # Main frame with semi-transparent background
        main_frame = ttk.Frame(self.root, padding=20, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Header with logo and logout button
        header_frame = ttk.Frame(main_frame, style="Header.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Add icon to header (if logo.png exists)
        try:
            logo_img = Image.open('logo.png').resize((40, 40), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(header_frame, image=logo_photo, bg="#e74c3c", bd=0)
            logo_label.image = logo_photo
            logo_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        except Exception:
            pass
            
        ttk.Label(header_frame, text="Student Dashboard", style="Header.TLabel").pack(side=tk.LEFT, padx=5, pady=5)
        
        # Logout button with icon
        try:
            logout_img = Image.open('logout_icon.png').resize((20, 20), Image.Resampling.LANCZOS)
            logout_photo = ImageTk.PhotoImage(logout_img)
            logout_btn = tk.Button(
                header_frame,
                text=" Logout",
                font=("Helvetica", 14, "bold"),
                bg="#e74c3c",
                fg="white",
                activebackground="#c0392b",
                activeforeground="white",
                bd=2,
                relief="ridge",
                command=self.create_login_page,
                cursor="hand2",
                image=logout_photo,
                compound=tk.LEFT
            )
            logout_btn.image = logout_photo
        except Exception:
            logout_btn = tk.Button(
                header_frame,
                text="Logout",
                font=("Helvetica", 14, "bold"),
                bg="#e74c3c",
                fg="white",
                activebackground="#c0392b",
                activeforeground="white",
                bd=2,
                relief="ridge",
                command=self.create_login_page,
                cursor="hand2"
            )
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=8)
        
        # Display personal info in a styled card
        info_frame = ttk.LabelFrame(main_frame, text="Personal Information", 
                                  padding=10, style="Section.TLabelframe")
        info_frame.pack(fill=tk.X, pady=10)
        
        # Personal info with icons
        info_grid = ttk.Frame(info_frame, style="InfoCard.TFrame")
        info_grid.pack(fill=tk.X, pady=5)
        
        # Left column
        left_col = ttk.Frame(info_grid, style="InfoCard.TFrame")
        left_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        ttk.Label(left_col, text=f"Student ID: {student_id}", 
                 style="InfoCard.TLabel").pack(anchor=tk.W, pady=2)
        ttk.Label(left_col, text=f"Name: {student_info['name']}", 
                 style="InfoCard.TLabel").pack(anchor=tk.W, pady=2)
        ttk.Label(left_col, text=f"Course: {student_info['course']}", 
                 style="InfoCard.TLabel").pack(anchor=tk.W, pady=2)
        
        # Right column
        right_col = ttk.Frame(info_grid, style="InfoCard.TFrame")
        right_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        ttk.Label(right_col, text=f"Email: {student_info.get('email', 'N/A')}", 
                 style="InfoCard.TLabel").pack(anchor=tk.W, pady=2)
        ttk.Label(right_col, text=f"Phone: {student_info.get('phone', 'N/A')}", 
                 style="InfoCard.TLabel").pack(anchor=tk.W, pady=2)
        ttk.Label(right_col, text=f"Address: {student_info.get('address', 'N/A')}", 
                 style="InfoCard.TLabel").pack(anchor=tk.W, pady=2)
        
        # Edit profile button with custom style
        ttk.Button(info_frame, text="Edit Profile", 
                  command=lambda: self.edit_student_profile(student_id),
                  style="EditProfile.TButton").pack(anchor=tk.W, pady=5)
        
        # Notebook with icons and larger tabs
        self.style.configure("TNotebook.Tab", font=("Helvetica", 14, "bold"), padding=[20, 10])
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Always define the frames first, before icon logic
        grades_frame = ttk.Frame(notebook, padding=10, style="Card.TFrame")
        courses_frame = ttk.Frame(notebook, padding=10, style="Card.TFrame")
        enroll_frame = ttk.Frame(notebook, padding=10, style="Card.TFrame")

        # Try to add icons if available, otherwise fall back to text
        try:
            grade_icon = ImageTk.PhotoImage(Image.open('grade_icon.png').resize((24, 24), Image.Resampling.LANCZOS))
            course_icon = ImageTk.PhotoImage(Image.open('course_icon.png').resize((24, 24), Image.Resampling.LANCZOS))
            enroll_icon = ImageTk.PhotoImage(Image.open('enroll_icon.png').resize((24, 24), Image.Resampling.LANCZOS))
            notebook.add(grades_frame, text="  My Grades", image=grade_icon, compound=tk.LEFT)
            notebook.add(courses_frame, text="  My Courses", image=course_icon, compound=tk.LEFT)
            notebook.add(enroll_frame, text="  Enroll in Subjects", image=enroll_icon, compound=tk.LEFT)
            notebook._grade_icon = grade_icon
            notebook._course_icon = course_icon
            notebook._enroll_icon = enroll_icon
        except Exception as e:
            # If any icon is missing or fails to load, just use text tabs
            notebook.add(grades_frame, text="My Grades")
            notebook.add(courses_frame, text="My Courses")
            notebook.add(enroll_frame, text="Enroll in Subjects")

        # Continue with the rest of the dashboard setup
        self.create_student_grades_tab(grades_frame, student_id)
        self.create_student_courses_tab(courses_frame, student_id)
        self.create_enrollment_interface(enroll_frame, student_id)
    
    def edit_lecturer_profile(self, lecturer_id):
        lecturer = self.lecturers.get(lecturer_id)
        if not lecturer:
            messagebox.showerror("Error", "Lecturer not found.")
            return

        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Profile - {lecturer['name']}")
        edit_window.geometry("400x300")

        # Edit form
        form_frame = ttk.Frame(edit_window, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Lecturer details form
        ttk.Label(form_frame, text="Email:").grid(row=0, column=0, sticky=tk.W, pady=5)
        email_var = tk.StringVar(value=lecturer.get('email', ''))
        ttk.Entry(form_frame, textvariable=email_var, width=30, style="Padded.TEntry").grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Phone:").grid(row=1, column=0, sticky=tk.W, pady=5)
        phone_var = tk.StringVar(value=lecturer.get('phone', ''))
        ttk.Entry(form_frame, textvariable=phone_var, width=30, style="Padded.TEntry").grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Office:").grid(row=2, column=0, sticky=tk.W, pady=5)
        office_var = tk.StringVar(value=lecturer.get('office', ''))
        ttk.Entry(form_frame, textvariable=office_var, width=30, style="Padded.TEntry").grid(row=2, column=1, pady=5)

        # Password change section
        ttk.Label(form_frame, text="Current Password:").grid(row=3, column=0, sticky=tk.W, pady=5)
        current_pass_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=current_pass_var, show="*", width=30, style="Padded.TEntry").grid(row=3, column=1, pady=5)

        ttk.Label(form_frame, text="New Password:").grid(row=4, column=0, sticky=tk.W, pady=5)
        new_pass_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=new_pass_var, show="*", width=30, style="Padded.TEntry").grid(row=4, column=1, pady=5)

        # Save function
        def save_changes():
            self.lecturers[lecturer_id]['email'] = email_var.get()
            self.lecturers[lecturer_id]['phone'] = phone_var.get()
            self.lecturers[lecturer_id]['office'] = office_var.get()

            # Handle password change if provided
            if current_pass_var.get() and new_pass_var.get():
                username = lecturer.get('username')
                if username in self.users:
                    if self.users[username]['password'] == current_pass_var.get():
                        self.users[username]['password'] = new_pass_var.get()
                        messagebox.showinfo("Success", "Password changed successfully")
                    else:
                        messagebox.showerror("Error", "Current password is incorrect")

            messagebox.showinfo("Success", "Profile information updated")
            edit_window.destroy()

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)

        ttk.Button(btn_frame, text="Save Changes", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=edit_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def assign_grade(self, course, student_id, grade):
        if not (course and student_id and grade):
            messagebox.showerror("Validation Error", "All fields are required")
            return
            
        # Convert grade string to float for calculations later
        try:
            grade_float = float(grade)
        except ValueError:
            messagebox.showerror("Validation Error", "Grade must be a valid number")
            return
            
        # Update the student's grade
        if student_id in self.students:
            # Check if student is enrolled in this course
            if course not in self.students[student_id].get('enrolled_subjects', []):
                messagebox.showinfo("Info", "Student is not enrolled in this course. Adding course to their enrolled subjects.")
                if 'enrolled_subjects' not in self.students[student_id]:
                    self.students[student_id]['enrolled_subjects'] = []
                self.students[student_id]['enrolled_subjects'].append(course)
            
            self.students[student_id]['grades'][course] = grade_float
            messagebox.showinfo("Success", f"Grade assigned successfully")
        else:
            messagebox.showerror("Error", "Student not found")
    
    def calculate_gwa(self, grades):
        if not grades:
            return 0.0
            
        total = 0.0
        count = 0
        for grade in grades.values():
            if isinstance(grade, (int, float)):
                total += float(grade)
                count += 1
                
        return total / count if count > 0 else 0.0
    
    def display_lecturer_students(self, parent_frame, lecturer_id):
        # Clear existing widgets
        for widget in parent_frame.winfo_children():
            widget.destroy()
            
        # Get lecturer's courses
        lecturer_info = self.lecturers[lecturer_id]
        lecturer_courses = lecturer_info.get('courses', [])
        
        # Create a styled frame for student list
        list_frame = ttk.LabelFrame(parent_frame, text="Enrolled Students", 
                                  padding=10, style="InfoCard.TLabelframe")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with scrollbar
        columns = ('id', 'name', 'course', 'grade')
        student_tree = ttk.Treeview(list_frame, columns=columns, 
                                  show='headings', style="Treeview")
        
        # Configure columns
        student_tree.heading('id', text='Student ID')
        student_tree.heading('name', text='Name')
        student_tree.heading('course', text='Course')
        student_tree.heading('grade', text='Grade')
        
        student_tree.column('id', width=100)
        student_tree.column('name', width=200)
        student_tree.column('course', width=100)
        student_tree.column('grade', width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                command=student_tree.yview)
        student_tree.configure(yscroll=scrollbar.set)
        
        # Pack widgets
        student_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate student list
        for student_id, student_info in self.students.items():
            student_courses = student_info.get('courses', {})
            for course_code, grade in student_courses.items():
                if course_code in lecturer_courses:
                    student_tree.insert('', tk.END, values=(
                        student_id,
                        student_info['name'],
                        course_code,
                        grade if grade else 'Not Graded'
                    ))
                    
        # Add search functionality
        search_frame = ttk.Frame(parent_frame, style="Card.TFrame")
        search_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(search_frame, text="Search:", 
                 style="Subheader.TLabel").pack(side=tk.LEFT, padx=5)
        
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, 
                               width=30, style="TEntry")
        search_entry.pack(side=tk.LEFT, padx=5)
        
        def search_students(*args):
            search_term = search_var.get().lower()
            student_tree.delete(*student_tree.get_children())
            
            for student_id, student_info in self.students.items():
                student_courses = student_info.get('courses', {})
                for course_code, grade in student_courses.items():
                    if course_code in lecturer_courses:
                        if (search_term in student_id.lower() or 
                            search_term in student_info['name'].lower() or 
                            search_term in course_code.lower()):
                            student_tree.insert('', tk.END, values=(
                                student_id,
                                student_info['name'],
                                course_code,
                                grade if grade else 'Not Graded'
                            ))
        
        search_var.trace('w', search_students)
        
        # Add filter by course
        filter_frame = ttk.Frame(parent_frame, style="Card.TFrame")
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Filter by Course:", 
                 style="Subheader.TLabel").pack(side=tk.LEFT, padx=5)
        
        filter_var = tk.StringVar()
        filter_combo = ttk.Combobox(filter_frame, textvariable=filter_var, 
                                  width=20, style="TCombobox")
        filter_combo['values'] = ['All Courses'] + lecturer_courses
        filter_combo.current(0)
        filter_combo.pack(side=tk.LEFT, padx=5)
        
        def filter_students(*args):
            selected_course = filter_var.get()
            student_tree.delete(*student_tree.get_children())
            
            for student_id, student_info in self.students.items():
                student_courses = student_info.get('courses', {})
                for course_code, grade in student_courses.items():
                    if course_code in lecturer_courses:
                        if selected_course == 'All Courses' or course_code == selected_course:
                            student_tree.insert('', tk.END, values=(
                                student_id,
                                student_info['name'],
                                course_code,
                                grade if grade else 'Not Graded'
                            ))
        
        filter_var.trace('w', filter_students)
    
    def create_enrollment_interface(self, parent_frame, student_id):
        # Department selection in a styled card
        selection_frame = ttk.LabelFrame(parent_frame, text="Select Department and Program", 
                                       padding=10, style="InfoCard.TLabelframe")
        selection_frame.pack(fill=tk.X, pady=10)
        
        # Configure combobox style
        self.style.configure("TCombobox",
                           background="white",
                           foreground="#2c3e50",
                           fieldbackground="white",
                           font=("Helvetica", 11))
        
        # Department selection
        dept_frame = ttk.Frame(selection_frame, style="InfoCard.TFrame")
        dept_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(dept_frame, text="Department:", 
                 style="Subheader.TLabel").pack(side=tk.LEFT, padx=5)
        dept_var = tk.StringVar()
        dept_combo = ttk.Combobox(dept_frame, textvariable=dept_var, 
                                 width=30, style="TCombobox")
        dept_combo['values'] = list(self.departments.keys())
        dept_combo.pack(side=tk.LEFT, padx=5)
        
        # Program selection
        program_frame = ttk.Frame(selection_frame, style="InfoCard.TFrame")
        program_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(program_frame, text="Program:", 
                 style="Subheader.TLabel").pack(side=tk.LEFT, padx=5)
        program_var = tk.StringVar()
        program_combo = ttk.Combobox(program_frame, textvariable=program_var, 
                                   width=30, style="TCombobox")
        program_combo.pack(side=tk.LEFT, padx=5)
        
        # When department changes, update programs
        def update_programs(*args):
            selected_dept = dept_var.get()
            if selected_dept in self.departments:
                program_combo['values'] = self.departments[selected_dept]['programs']
                program_combo.current(0) if self.departments[selected_dept]['programs'] else None
                
        dept_var.trace("w", update_programs)
        
        # Subjects list in a styled card
        subjects_frame = ttk.LabelFrame(parent_frame, text="Available Subjects", 
                                      padding=10, style="InfoCard.TLabelframe")
        subjects_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Subjects treeview with custom style
        columns = ('code', 'description')
        subjects_tree = ttk.Treeview(subjects_frame, columns=columns, 
                                   show='headings', style="Treeview")
        subjects_tree.heading('code', text='Subject Code')
        subjects_tree.heading('description', text='Description')
        
        # Set column widths
        subjects_tree.column('code', width=150)
        subjects_tree.column('description', width=300)
        
        subjects_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(subjects_frame, orient=tk.VERTICAL, 
                                command=subjects_tree.yview)
        subjects_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Function to display available subjects
        def show_subjects(*args):
            selected_program = program_var.get()
            
            # Clear existing items
            for item in subjects_tree.get_children():
                subjects_tree.delete(item)
                
            # Show subjects for the selected program
            if selected_program in self.program_subjects:
                for subject_code in self.program_subjects[selected_program]:
                    # For simplicity, we'll just use the subject code as the description
                    subjects_tree.insert('', tk.END, values=(subject_code, f"{subject_code} Description"))
                    
        program_var.trace("w", show_subjects)
        
        # Button frame with custom style
        btn_frame = ttk.Frame(parent_frame, style="Card.TFrame")
        btn_frame.pack(fill=tk.X, pady=10)
        
        def enroll_in_selected_subjects():
            selected_items = subjects_tree.selection()
            selected_program = program_var.get()
            
            if not selected_items:
                messagebox.showwarning("No Selection", "Please select subjects to enroll in")
                return
                
            if not selected_program:
                messagebox.showwarning("No Program", "Please select a program first")
                return
            
            # Get selected subjects
            selected_subjects = []
            for item in selected_items:
                subject_code = subjects_tree.item(item, 'values')[0]
                selected_subjects.append(subject_code)
            
            # Add subjects to student's enrollment
            if 'enrolled_subjects' not in self.students[student_id]:
                self.students[student_id]['enrolled_subjects'] = []
                
            # Check for duplicates
            already_enrolled = []
            newly_enrolled = []
            
            for subject in selected_subjects:
                if subject in self.students[student_id]['enrolled_subjects']:
                    already_enrolled.append(subject)
                else:
                    self.students[student_id]['enrolled_subjects'].append(subject)
                    newly_enrolled.append(subject)
                    
                    # Initialize grade for this subject
                    if 'grades' not in self.students[student_id]:
                        self.students[student_id]['grades'] = {}
                    if subject not in self.students[student_id]['grades']:
                        self.students[student_id]['grades'][subject] = None
            
            # Show confirmation message
            if newly_enrolled:
                messagebox.showinfo("Success", f"Successfully enrolled in: {', '.join(newly_enrolled)}")
            
            if already_enrolled:
                messagebox.showinfo("Already Enrolled", f"Already enrolled in: {', '.join(already_enrolled)}")
        
        # Enroll button with custom style
        self.style.configure("Enroll.TButton",
                           font=("Helvetica", 12, "bold"),
                           background="#27ae60",
                           foreground="white",
                           padding=10)
        ttk.Button(btn_frame, text="Enroll in Selected Subjects", 
                  command=enroll_in_selected_subjects,
                  style="Enroll.TButton").pack(side=tk.RIGHT, padx=5)
    
    def edit_student_profile(self, student_id):
        student = self.students[student_id]
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Profile - {student['name']}")
        edit_window.geometry("400x300")
        
        # Edit form
        form_frame = ttk.Frame(edit_window, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Student details form
        ttk.Label(form_frame, text="Email:").grid(row=0, column=0, sticky=tk.W, pady=5)
        email_var = tk.StringVar(value=student.get('email', ''))
        ttk.Entry(form_frame, textvariable=email_var, width=30, style="Padded.TEntry").grid(row=0, column=1, pady=5)
        
        ttk.Label(form_frame, text="Phone:").grid(row=1, column=0, sticky=tk.W, pady=5)
        phone_var = tk.StringVar(value=student.get('phone', ''))
        ttk.Entry(form_frame, textvariable=phone_var, width=30, style="Padded.TEntry").grid(row=1, column=1, pady=5)
        
        ttk.Label(form_frame, text="Address:").grid(row=2, column=0, sticky=tk.W, pady=5)
        address_var = tk.StringVar(value=student.get('address', ''))
        ttk.Entry(form_frame, textvariable=address_var, width=30, style="Padded.TEntry").grid(row=2, column=1, pady=5)
        
        # Password change section
        ttk.Label(form_frame, text="Current Password:").grid(row=3, column=0, sticky=tk.W, pady=5)
        current_pass_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=current_pass_var, show="*", width=30, style="Padded.TEntry").grid(row=3, column=1, pady=5)
        
        ttk.Label(form_frame, text="New Password:").grid(row=4, column=0, sticky=tk.W, pady=5)
        new_pass_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=new_pass_var, show="*", width=30, style="Padded.TEntry").grid(row=4, column=1, pady=5)
        
        # Save function
        def save_changes():
            # Update student information
            self.students[student_id]['email'] = email_var.get()
            self.students[student_id]['phone'] = phone_var.get()
            self.students[student_id]['address'] = address_var.get()
            
            # Handle password change if provided
            if current_pass_var.get() and new_pass_var.get():
                username = student.get('username')
                if username in self.users:
                    if self.users[username]['password'] == current_pass_var.get():
                        self.users[username]['password'] = new_pass_var.get()
                        messagebox.showinfo("Success", "Password changed successfully")
                    else:
                        messagebox.showerror("Error", "Current password is incorrect")
            
            messagebox.showinfo("Success", "Profile information updated")
            edit_window.destroy()
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Save Changes", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=edit_window.destroy).pack(side=tk.LEFT, padx=5)

    def create_student_grades_tab(self, parent_frame, student_id):
        self.style.configure("Treeview",
                           background="white",
                           foreground="black",
                           fieldbackground="white",
                           font=("Helvetica", 11))
        self.style.configure("Treeview.Heading",
                           background="#e74c3c",
                           foreground="white",
                           font=("Helvetica", 12, "bold"))
        self.style.map("Treeview",
                      foreground=[("selected", "black"), ("!selected", "black")],
                      background=[("selected", "#e0e0e0"), ("!selected", "white")])

        columns = ("code", "course_name", "grade")
        grades_tree = ttk.Treeview(parent_frame, columns=columns, show='headings', style="Treeview")
        grades_tree.heading('code', text='Subject Code')
        grades_tree.heading('course_name', text='Course Name')
        grades_tree.heading('grade', text='Grade')
        grades_tree.column('code', width=100)
        grades_tree.column('course_name', width=200)
        grades_tree.column('grade', width=80)
        grades_tree.pack(fill=tk.BOTH, expand=True, pady=10)
        scrollbar = ttk.Scrollbar(parent_frame, orient=tk.VERTICAL, command=grades_tree.yview)
        grades_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        student_info = self.students[student_id]
        for subject in student_info.get('enrolled_subjects', []):
            course = self.courses.get(subject, {"name": "Unknown Course"})
            grade = student_info.get('grades', {}).get(subject, "N/A")
            grades_tree.insert("", "end", values=(subject, course["name"], grade))

    def create_student_courses_tab(self, parent_frame, student_id):
        # Display enrolled courses in a styled treeview
        courses_tree = ttk.Treeview(parent_frame, columns=('code', 'name', 'lecturer'), 
                                  show='headings', style="Treeview")
        courses_tree.heading('code', text='Course Code')
        courses_tree.heading('name', text='Course Name')
        courses_tree.heading('lecturer', text='Lecturer')
        
        # Set column widths
        courses_tree.column('code', width=100)
        courses_tree.column('name', width=200)
        courses_tree.column('lecturer', width=150)
        
        courses_tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent_frame, orient=tk.VERTICAL, command=courses_tree.yview)
        courses_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate with courses
        student_info = self.students[student_id]
        enrollment_info = student_info.get('enrolled_subjects', [])
        for course_code in enrollment_info:
            if course_code in self.courses:
                course = self.courses[course_code]
                lecturer_id = course.get('lecturer')
                lecturer_name = self.lecturers.get(lecturer_id, {}).get('name', 'Unknown') if lecturer_id else 'Unknown'
                courses_tree.insert('', tk.END, values=(course_code, course['name'], lecturer_name))

    def create_lecturer_courses_tab(self, parent_frame, lecturer_id):
        # List courses in a styled treeview
        list_frame = ttk.LabelFrame(parent_frame, text="Your Courses", 
                                  padding=10, style="Section.TLabelframe")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('code', 'name')
        course_tree = ttk.Treeview(list_frame, columns=columns, 
                                 show='headings', style="Treeview")
        course_tree.heading('code', text='Course Code')
        course_tree.heading('name', text='Course Name')
        
        # Set column widths
        course_tree.column('code', width=100)
        course_tree.column('name', width=200)
        
        course_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                command=course_tree.yview)
        course_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate course tree
        lecturer_info = self.lecturers[lecturer_id]
        lecturer_courses = lecturer_info.get('courses', [])
        for course_code in lecturer_courses:
            if course_code in self.courses:
                course_name = self.courses[course_code]['name']
                course_tree.insert('', tk.END, values=(course_code, course_name))

    def create_lecturer_grades_tab(self, parent_frame, lecturer_id):
        # Form for assigning grades in a styled card
        form_frame = ttk.LabelFrame(parent_frame, text="Assign Student Grade", 
                                  padding=10, style="Section.TLabelframe")
        form_frame.pack(fill=tk.X, pady=10)
        
        # Course selection
        course_frame = ttk.Frame(form_frame, style="InfoCard.TFrame")
        course_frame.pack(fill=tk.X, pady=5)
        ttk.Label(course_frame, text="Select Course:", 
                 style="Subheader.TLabel").pack(side=tk.LEFT, padx=5)
        course_var = tk.StringVar()
        course_combo = ttk.Combobox(course_frame, textvariable=course_var, 
                                  width=20, style="TCombobox")
        lecturer_info = self.lecturers[lecturer_id]
        lecturer_courses = lecturer_info.get('courses', [])
        course_combo['values'] = lecturer_courses
        course_combo.pack(side=tk.LEFT, padx=5)
        
        # Student selection
        student_frame = ttk.Frame(form_frame, style="InfoCard.TFrame")
        student_frame.pack(fill=tk.X, pady=5)
        ttk.Label(student_frame, text="Select Student:", 
                 style="Subheader.TLabel").pack(side=tk.LEFT, padx=5)
        student_var = tk.StringVar()
        student_combo = ttk.Combobox(student_frame, textvariable=student_var, 
                                   width=20, style="TCombobox")
        student_list = list(self.students.keys())
        student_combo['values'] = student_list
        student_combo.pack(side=tk.LEFT, padx=5)
        
        # Grade selection
        grade_frame = ttk.Frame(form_frame, style="InfoCard.TFrame")
        grade_frame.pack(fill=tk.X, pady=5)
        ttk.Label(grade_frame, text="Grade:", 
                 style="Subheader.TLabel").pack(side=tk.LEFT, padx=5)
        grade_var = tk.StringVar()
        grade_combo = ttk.Combobox(grade_frame, textvariable=grade_var, 
                                 width=20, style="TCombobox")
        grade_combo['values'] = ('1.00', '1.25', '1.50', '1.75', '2.00', '2.25', '2.50', '3.00', '5.00')
        grade_combo.pack(side=tk.LEFT, padx=5)
        
        # Assign grade button with custom style
        ttk.Button(form_frame, text="Assign Grade", 
                  command=lambda: self.assign_grade(course_var.get(), 
                                                  student_var.get(), 
                                                  grade_var.get()),
                  style="Assign.TButton").pack(pady=10)

# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()


    #add and update the demo accounts to make it work at its full capability and to simulate the actual usage of it. moreover, add red accents to the UI