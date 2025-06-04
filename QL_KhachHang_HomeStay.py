import json
import os
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from uuid import uuid4  # Tạo ID duy nhất cho khách hàng
from api_gialap import APIService
from PIL import Image, ImageTk
from tkinter import Label, Frame

import sys

class HomestayBookingSystem:

    def __init__(self, root):
        self.username_entry = None
        self.root = root
        self.root.title("Hệ thống Quản lý Khách đặt Homestay")

        try:
            self.root.iconbitmap('hs1.ico')  # Thay 'qlhss.ico' bằng tên file icon của bạn
        except:
            pass  # Bỏ qua nếu không tìm thấy file icon

        # File dữ liệu
        self.customers_file = "customers.json"
        self.users_file = "users.json"

        # Khởi tạo dữ liệu nếu chưa có
        self.init_data_files()

        # Biến giao diện
        self.current_user = None
        self.create_login_ui()

    def init_data_files(self):
        """Khởi tạo file dữ liệu nếu chưa tồn tại"""
        if not os.path.exists(self.customers_file):
            with open(self.customers_file, 'w') as f:
                json.dump([], f)

        if not os.path.exists(self.users_file):
            # Tạo admin mặc định
            default_users = [
                {
                    "username": "admin",
                    "password": "admin123",
                    "role": "admin"
                },
                {
                    "username": "user",
                    "password": "user123",
                    "role": "user"
                }
            ]
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f)

    def center_window(self, width, height):
        """Đặt vị trí cửa sổ ở giữa màn hình"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Tính toán vị trí x, y
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f'{width}x{height}+{x}+{y}')
    def create_login_ui(self):
        """Tạo giao diện đăng nhập chuyên nghiệp với logo"""
        self.clear_ui()
        self.root.geometry("420x450")

        self.root.configure(bg="#f4f6f9")


        # === Load Logo ===
        try:
            logo_image = Image.open("qlhss.png")
            logo_image = logo_image.resize((80, 80), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_image)
            logo_label = Label(self.root, image=self.logo, bg="#f4f6f9")
            logo_label.pack(pady=(30, 10))
        except Exception as e:
            print("Không thể tải logo:", e)

        # === Tiêu đề chính ===
        title_label = Label(self.root,
                            text="ĐĂNG NHẬP HỆ THỐNG",
                            font=("Segoe UI", 18, "bold"),
                            fg="#2c3e50",
                            bg="#f4f6f9")
        title_label.pack()

        # === Frame chính chứa login form ===
        login_frame = Frame(self.root, bg="#ffffff", bd=1, relief="solid")

        def show_login_form():
            login_frame.pack(pady=30, padx=30, fill=BOTH)

            Label(login_frame,
                  text="Tên đăng nhập",
                  font=("Segoe UI", 10, "bold"),
                  fg="#2c3e50",
                  bg="#ffffff").pack(pady=(20, 5), anchor=W, padx=20)

            self.username_entry = Entry(login_frame,
                                        font=("Segoe UI", 12),
                                        relief="flat",
                                        bg="#ecf0f1",
                                        highlightthickness=1,
                                        highlightbackground="#bdc3c7",
                                        highlightcolor="#3498db")
            self.username_entry.pack(pady=(0, 15), padx=20, fill=X)

            self.username_entry.bind("<Return>", lambda event: self.password_entry.focus_set())

            Label(login_frame,
                  text="Mật khẩu",
                  font=("Segoe UI", 10, "bold"),
                  fg="#2c3e50",
                  bg="#ffffff").pack(pady=(5, 5), anchor=W, padx=20)

            self.password_entry = Entry(login_frame,
                                        font=("Segoe UI", 12),
                                        relief="flat",
                                        bg="#ecf0f1",
                                        show="*",
                                        highlightthickness=1,
                                        highlightbackground="#bdc3c7",
                                        highlightcolor="#3498db")
            self.password_entry.pack(pady=(0, 20), padx=20, fill=X)

            self.password_entry.bind("<Return>", lambda event: self.login())

            # Nút đăng nhập
            login_btn = Button(login_frame,
                               text="ĐĂNG NHẬP",
                               command=self.login,
                               font=("Segoe UI", 11, "bold"),
                               fg="white",
                               bg="#2980b9",
                               activebackground="#3498db",
                               relief="flat")
            login_btn.pack(pady=(0, 25), padx=20, fill=X)

        self.root.after(200, show_login_form)

    def login(self):
        """Xử lý đăng nhập"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        with open(self.users_file, 'r') as f:
            users = json.load(f)

        for user in users:
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                self.create_main_ui()
                return

        messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng")

    def create_main_ui(self):
        """Tạo giao diện chính sau khi đăng nhập"""
        self.clear_ui()
        self.root.geometry("1200x700")
        self.center_window(1200, 700)
        self.root.configure(bg="#f4f6f9")  # Background color

        # Menu bar
        menubar = Menu(self.root)
        system_menu = Menu(menubar, tearoff=0)
        system_menu.add_command(label="Đăng xuất", command=self.create_login_ui)
        system_menu.add_separator()
        system_menu.add_command(label="Thoát", command=self.root.quit)
        menubar.add_cascade(label="Hệ thống", menu=system_menu)

        # Admin-only menu
        if self.current_user['role'] == 'admin':
            manage_menu = Menu(menubar, tearoff=0)
            manage_menu.add_command(label="Quản lý người dùng", command=self.manage_users)
            menubar.add_cascade(label="Quản lý", menu=manage_menu)

        self.root.config(menu=menubar)



        # Tạo frame riêng cho tiêu đề để dễ canh chỉnh
        title_frame = Frame(self.root, bg="#f4f6f9")
        title_frame.pack(pady=(10, 15), fill='x')

        # Tiêu đề chính với font và màu sắc đẹp hơn, canh giữa
        title_label = Label(title_frame,
                            text="QUẢN LÝ KHÁCH ĐẶT PHÒNG HOMESTAY",
                            font=("Segoe UI", 26, "bold"),
                            fg="#2c3e50",
                            bg="#f4f6f9")
        title_label.pack()

        # Tiêu đề phụ chào mừng với font nhỏ hơn, màu dịu nhẹ
        welcome_label = Label(title_frame,
                              text=f"Xin chào {self.current_user['username']}",
                              font=("Segoe UI", 14, "italic"),
                              fg="#34495e",
                              bg="#f4f6f9")
        welcome_label.pack(pady=(2, 5))

        # Đường kẻ ngang phân tách
        separator = Frame(self.root, bg="#2980b9", height=3)
        separator.pack(fill='x', padx=100, pady=(0, 15))

        # Frame for buttons
        button_frame = Frame(self.root, bg="#f4f6f9")
        button_frame.pack(pady=10)

        # Helper function to create styled buttons with hover effect
        def create_button(parent, text, command):
            btn = Button(parent, text=text, command=command,
                         bg="#4a90e2", fg="white",
                         activebackground="#357ABD", activeforeground="white",
                         font=("Arial", 12, "bold"),
                         bd=0,
                         relief="ridge",
                         padx=12, pady=6,
                         cursor="hand2")

            def on_enter(e):
                btn['bg'] = "#357ABD"

            def on_leave(e):
                btn['bg'] = "#4a90e2"

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            return btn

        col = 0
        if self.current_user['role'] == 'admin':
            create_button(button_frame, "Thêm khách hàng", self.add_customer_ui).grid(row=0, column=col, padx=10)
            col += 1

        create_button(button_frame, "Xem danh sách", self.view_customers).grid(row=0, column=col, padx=10)
        col += 1
        create_button(button_frame, "Tìm kiếm", self.search_customer_ui).grid(row=0, column=col, padx=10)
        col += 1

        if self.current_user['role'] == 'admin':
            create_button(button_frame, "Nhập dữ liệu từ API", self.import_from_api).grid(row=0, column=col, padx=10)

        # Frame to show data (e.g., customer list)
        self.data_frame = Frame(self.root, bg="#f4f6f9")
        self.data_frame.pack(fill=BOTH, expand=True, padx=20, pady=15)

        # Display default data view (customers)
        self.view_customers()

    def manage_users(self):
        """Giao diện quản lý người dùng"""
        self.clear_data_frame()

        Label(self.data_frame, text="QUẢN LÝ NGƯỜI DÙNG", font=("Arial", 14, "bold")).pack(pady=10)

        # Treeview hiển thị danh sách người dùng
        columns = ("username", "role")
        self.users_tree = ttk.Treeview(self.data_frame, columns=columns, show="headings", selectmode='extended')

        self.users_tree.heading("username", text="Tên đăng nhập")
        self.users_tree.heading("role", text="Vai trò")

        self.users_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Nút chức năng
        button_frame = Frame(self.data_frame, bg="#f4f6f9")
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Thêm người dùng", command=self.add_user_ui).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Xóa người dùng", command=self.delete_user).grid(row=0, column=1, padx=5)

        # Load dữ liệu người dùng
        self.load_users_data()

    def load_users_data(self):
        """Tải dữ liệu người dùng vào treeview"""
        with open(self.users_file, 'r') as f:
            users = json.load(f)

        # Xóa dữ liệu cũ
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)

        # Thêm dữ liệu mới
        for user in users:
            self.users_tree.insert("", END, values=(user['username'], user['role']))

    def add_user_ui(self):
        """Giao diện thêm người dùng mới"""
        self.user_form_window = Toplevel(self.root)
        self.user_form_window.title("Thêm người dùng mới")
        self.user_form_window.geometry("400x300")

        Label(self.user_form_window, text="Thêm người dùng mới", font=("Arial", 14)).pack(pady=10)

        form_frame = Frame(self.user_form_window)
        form_frame.pack(pady=10)

        Label(form_frame, text="Tên đăng nhập:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.new_username = Entry(form_frame, width=25)
        self.new_username.grid(row=0, column=1, padx=10, pady=10)

        Label(form_frame, text="Mật khẩu:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.new_password = Entry(form_frame, width=25, show="*")
        self.new_password.grid(row=1, column=1, padx=10, pady=10)

        Label(form_frame, text="Xác nhận mật khẩu:").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.confirm_password = Entry(form_frame, width=25, show="*")
        self.confirm_password.grid(row=2, column=1, padx=10, pady=10)

        Label(form_frame, text="Vai trò:").grid(row=3, column=0, padx=10, pady=10, sticky=W)
        self.user_role = StringVar(value="user")
        ttk.Radiobutton(form_frame, text="Quản trị", variable=self.user_role, value="admin").grid(row=3, column=1,
                                                                                                  padx=10,
                                                                                                  pady=5, sticky=W)
        ttk.Radiobutton(form_frame, text="Người dùng", variable=self.user_role, value="user").grid(row=4, column=1,
                                                                                                   padx=10,
                                                                                                   pady=5, sticky=W)

        button_frame = Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Lưu", command=self.save_new_user).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Hủy", command=self.user_form_window.destroy).pack(side=LEFT, padx=5)

    def save_new_user(self):
        """Lưu người dùng mới"""
        username = self.new_username.get()
        password = self.new_password.get()
        confirm = self.confirm_password.get()
        role = self.user_role.get()

        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return

        if password != confirm:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp")
            return

        with open(self.users_file, 'r') as f:
            users = json.load(f)

        # Kiểm tra username đã tồn tại chưa
        for user in users:
            if user['username'] == username:
                messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại")
                return

        # Thêm người dùng mới
        users.append({
            "username": username,
            "password": password,
            "role": role
        })

        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)

        messagebox.showinfo("Thành công", "Thêm người dùng mới thành công")
        self.user_form_window.destroy()
        self.load_users_data()

    def delete_user(self):
        """Xóa nhiều người dùng được chọn cùng lúc"""
        selected_items = self.users_tree.selection()
        if not selected_items:
            messagebox.showerror("Lỗi", "Vui lòng chọn ít nhất một người dùng cần xóa")
            return

        # Lấy danh sách thông tin user được chọn
        selected_users = [{
            'username': self.users_tree.item(item)['values'][0],
            'role': self.users_tree.item(item)['values'][1]
        } for item in selected_items]

        # Kiểm tra các ràng buộc
        error_messages = []
        usernames_to_delete = []

        for user in selected_users:
            if user['username'] == "admin":
                error_messages.append(f"- Không thể xóa tài khoản admin mặc định")
            elif user['username'] == self.current_user['username']:
                error_messages.append(f"- Bạn không thể tự xóa tài khoản của chính mình")
            else:
                usernames_to_delete.append(user['username'])

        if error_messages:
            messagebox.showerror("Lỗi", "Không thể xóa các tài khoản sau:\n" + "\n".join(error_messages))
            if not usernames_to_delete:  # Nếu không có user nào hợp lệ để xóa
                return

        # Tạo thông báo xác nhận chi tiết
        confirm_message = [
            f"Bạn có chắc chắn muốn xóa {len(usernames_to_delete)} người dùng sau?",
            "\nDanh sách:",
            *[f"• {username}" for username in usernames_to_delete],
            "\nHành động này không thể hoàn tác!"
        ]

        if not messagebox.askyesno("Xác nhận xóa", "\n".join(confirm_message)):
            return

        # Thực hiện xóa
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)

            # Lọc ra những user không nằm trong danh sách xóa
            updated_users = [user for user in users if user['username'] not in usernames_to_delete]

            with open(self.users_file, 'w') as f:
                json.dump(updated_users, f, indent=4)

            # Thông báo kết quả
            success_message = [
                f"Đã xóa thành công {len(usernames_to_delete)} người dùng:",
                *[f"• {username}" for username in usernames_to_delete]
            ]
            messagebox.showinfo("Thành công", "\n".join(success_message))

            # Làm mới danh sách
            self.load_users_data()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi xóa người dùng: {str(e)}")

    def add_customer_ui(self):
        """Giao diện thêm khách hàng mới"""
        self.customer_form_window = Toplevel(self.root)
        self.customer_form_window.title("Thêm khách đặt phòng mới")
        self.customer_form_window.geometry("600x500")

        Label(self.customer_form_window, text="Thông tin khách đặt phòng", font=("Arial", 14)).pack(pady=10)

        form_frame = Frame(self.customer_form_window)
        form_frame.pack(pady=10)

        # Các trường thông tin
        fields = [
            ("Tên khách hàng:", "name"),
            ("Số điện thoại:", "phone"),
            ("CCCD:", "cccd"),
            ("Ngày sinh (dd/mm/yyyy):", "dob"),
            ("Giới tính:", "gender"),
            ("Ngày check-in (dd/mm/yyyy):", "checkin"),
            ("Ngày check-out (dd/mm/yyyy):", "checkout"),
            ("Loại phòng:", "room_type")
        ]

        self.customer_fields = {}

        for i, (label, field_name) in enumerate(fields):
            Label(form_frame, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=W)

            if field_name == "gender":
                gender_var = StringVar(value="Nam")
                self.customer_fields[field_name] = gender_var
                Radiobutton(form_frame, text="Nam", variable=gender_var, value="Nam").grid(row=i, column=1, padx=10,
                                                                                           pady=5, sticky=W)
                Radiobutton(form_frame, text="Nữ", variable=gender_var, value="Nữ").grid(row=i, column=1, padx=100,
                                                                                         pady=5, sticky=W)
            elif field_name == "room_type":
                room_var = StringVar()
                self.customer_fields[field_name] = room_var
                OptionMenu(form_frame, room_var, "Phòng đơn", "Phòng đôi", "Phòng gia đình").grid(row=i, column=1,
                                                                                                  padx=10, pady=5,
                                                                                                  sticky=EW)
            else:
                entry = Entry(form_frame, width=30)
                entry.grid(row=i, column=1, padx=10, pady=5, sticky=W)
                self.customer_fields[field_name] = entry

        ttk.Button(self.customer_form_window, text="Lưu thông tin", command=self.save_customer).pack(pady=20)

    def save_customer(self):
        """Lưu thông tin khách hàng mới"""
        customer_data = {
            "id": str(uuid4()),  # Tạo ID duy nhất
            "created_by": self.current_user['username']
        }

        # Lấy dữ liệu từ các trường nhập liệu
        for field_name, widget in self.customer_fields.items():
            if isinstance(widget, Entry):
                value = widget.get()
                if not value:
                    messagebox.showerror("Lỗi", f"Vui lòng nhập {field_name}")
                    return
                customer_data[field_name] = value
            elif isinstance(widget, StringVar):
                customer_data[field_name] = widget.get()

        # Kiểm tra định dạng ngày tháng
        date_fields = ["dob", "checkin", "checkout"]
        for date_field in date_fields:
            try:
                date_str = customer_data[date_field]
                datetime.strptime(date_str, "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Lỗi",
                                     f"Định dạng ngày {date_field} không hợp lệ. Vui lòng nhập theo định dạng dd/mm/yyyy")
                return

        # Kiểm tra ngày check-out phải sau ngày check-in
        checkin = datetime.strptime(customer_data["checkin"], "%d/%m/%Y")
        checkout = datetime.strptime(customer_data["checkout"], "%d/%m/%Y")
        if checkout <= checkin:
            messagebox.showerror("Lỗi", "Ngày check-out phải sau ngày check-in")
            return

        # Đọc dữ liệu hiện có
        with open(self.customers_file, 'r', encoding='utf-8') as f:
            customers = json.load(f)

        # Thêm khách hàng mới
        customers.append(customer_data)

        # Lưu lại
        with open(self.customers_file, 'w', encoding='utf-8') as f:
            json.dump(customers, f, indent=4)

        messagebox.showinfo("Thành công", "Thêm khách hàng mới thành công")
        self.customer_form_window.destroy()
        self.view_customers()

    def view_customers(self):
        """Hiển thị danh sách khách hàng"""
        self.clear_data_frame()

        # Màu sắc cho dark mode
        bg_color = "#2d2d2d"
        header_color = "#3a3a3a"
        text_color = "#ffffff"

        header_frame = Frame(self.data_frame, bg=header_color, height=50)
        header_frame.pack(fill=X, pady=(0, 10))

        Label(header_frame,
              text="DANH SÁCH KHÁCH ĐẶT PHÒNG",
              font=("Segoe UI", 16, "bold"),
              bg=header_color,
              fg=text_color,
              padx=20,
              pady=10).pack(side=LEFT)

        # Tạo Treeview để hiển thị dữ liệu
        columns = ("name", "phone", "cccd", "dob", "gender", "checkin", "checkout", "room_type")
        self.customers_tree = ttk.Treeview(self.data_frame, columns=columns, show="headings")

        # Đặt tiêu đề cho các cột
        self.customers_tree.heading("name", text="Tên khách hàng")
        self.customers_tree.heading("phone", text="Số điện thoại")
        self.customers_tree.heading("cccd", text="CCCD")
        self.customers_tree.heading("dob", text="Ngày sinh")
        self.customers_tree.heading("gender", text="Giới tính")
        self.customers_tree.heading("checkin", text="Ngày check-in")
        self.customers_tree.heading("checkout", text="Ngày check-out")
        self.customers_tree.heading("room_type", text="Loại phòng")

        # Đặt chiều rộng cột
        self.customers_tree.column("name", width=150)
        self.customers_tree.column("phone", width=100)
        self.customers_tree.column("cccd", width=120)
        self.customers_tree.column("dob", width=100)
        self.customers_tree.column("gender", width=80)
        self.customers_tree.column("checkin", width=100)
        self.customers_tree.column("checkout", width=100)
        self.customers_tree.column("room_type", width=100)

        self.customers_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(self.customers_tree, orient="vertical", command=self.customers_tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.customers_tree.configure(yscrollcommand=scrollbar.set)

        # Nút chức năng
        button_frame = Frame(self.data_frame, bg="#f4f6f9")
        button_frame.pack(pady=10)
        if self.current_user['role'] == 'admin':
            ttk.Button(button_frame, text="Làm mới", command=self.view_customers).grid(row=0, column=0, padx=5)
        if self.current_user['role'] == 'admin':
            ttk.Button(button_frame, text="Sửa", command=self.edit_customer).grid(row=0, column=1, padx=5)
        if self.current_user['role'] == 'admin':
            ttk.Button(button_frame, text="Xóa", command=self.delete_customer).grid(row=0, column=2, padx=5)
        if self.current_user['role'] == 'admin':
            ttk.Button(button_frame, text="Xóa tất cả", command=self.delete_all_customers).grid(row=0, column=3, padx=5)

        # Tải dữ liệu
        self.load_customers_data()

    def load_customers_data(self):
        """Tải dữ liệu khách hàng vào Treeview"""
        try:
            with open(self.customers_file, 'r', encoding='utf-8') as f:
                customers = json.load(f)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc dữ liệu: {e}")
            customers = []

        # Xóa dữ liệu cũ
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)

        # Thêm dữ liệu mới
        for customer in customers:
            self.customers_tree.insert("", END,
                                       values=(customer['name'],
                                               customer['phone'],
                                               customer['cccd'],
                                               customer['dob'],
                                               customer['gender'],
                                               customer['checkin'],
                                               customer['checkout'],
                                               customer['room_type']),
                                       tags=(customer['id'],))

    def edit_customer(self):
        """Sửa thông tin khách hàng"""
        selected_item = self.customers_tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn khách hàng cần sửa")
            return

        # Lấy ID của khách hàng được chọn
        customer_id = self.customers_tree.item(selected_item)['tags'][0]

        # Tìm khách hàng trong dữ liệu
        with open(self.customers_file, 'r', encoding='utf-8') as f:
            customers = json.load(f)

        customer = None
        for c in customers:
            if c['id'] == customer_id:
                customer = c
                break

        if not customer:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin khách hàng")
            return

        # Tạo giao diện chỉnh sửa
        self.edit_customer_window = Toplevel(self.root)
        self.edit_customer_window.title("Chỉnh sửa thông tin khách hàng")
        self.edit_customer_window.geometry("600x500")

        Label(self.edit_customer_window, text="Chỉnh sửa thông tin khách hàng", font=("Arial", 14)).pack(pady=10)

        form_frame = Frame(self.edit_customer_window)
        form_frame.pack(pady=10)

        # Các trường thông tin
        fields = [
            ("Tên khách hàng:", "name", customer['name']),
            ("Số điện thoại:", "phone", customer['phone']),
            ("CCCD:", "cccd", customer['cccd']),
            ("Ngày sinh (dd/mm/yyyy):", "dob", customer['dob']),
            ("Giới tính:", "gender", customer['gender']),
            ("Ngày check-in (dd/mm/yyyy):", "checkin", customer['checkin']),
            ("Ngày check-out (dd/mm/yyyy):", "checkout", customer['checkout']),
            ("Loại phòng:", "room_type", customer['room_type'])
        ]

        self.edit_customer_fields = {}

        for i, (label, field_name, value) in enumerate(fields):
            Label(form_frame, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=W)

            if field_name == "gender":
                gender_var = StringVar(value=value)
                self.edit_customer_fields[field_name] = gender_var
                Radiobutton(form_frame, text="Nam", variable=gender_var, value="Nam").grid(row=i, column=1, padx=10,
                                                                                           pady=5, sticky=W)
                Radiobutton(form_frame, text="Nữ", variable=gender_var, value="Nữ").grid(row=i, column=1, padx=100,
                                                                                         pady=5, sticky=W)
            elif field_name == "room_type":
                room_var = StringVar(value=value)
                self.edit_customer_fields[field_name] = room_var
                OptionMenu(form_frame, room_var, "Phòng đơn", "Phòng đôi", "Phòng gia đình").grid(row=i, column=1,
                                                                                                  padx=10, pady=5,
                                                                                                  sticky=EW)
            else:
                entry = Entry(form_frame, width=30)
                entry.insert(0, value)
                entry.grid(row=i, column=1, padx=10, pady=5, sticky=W)
                self.edit_customer_fields[field_name] = entry

        # Lưu ID khách hàng để cập nhật
        self.editing_customer_id = customer_id

        ttk.Button(self.edit_customer_window, text="Lưu thay đổi", command=self.update_customer).pack(pady=20)

    def update_customer(self):
        """Cập nhật thông tin khách hàng"""
        updated_data = {
            "id": self.editing_customer_id,
            "created_by": self.current_user['username']
        }

        # Lấy dữ liệu từ các trường nhập liệu
        for field_name, widget in self.edit_customer_fields.items():
            if isinstance(widget, Entry):
                value = widget.get()
                if not value:
                    messagebox.showerror("Lỗi", f"Vui lòng nhập {field_name}")
                    return
                updated_data[field_name] = value
            elif isinstance(widget, StringVar):
                updated_data[field_name] = widget.get()

        # Kiểm tra định dạng ngày tháng
        date_fields = ["dob", "checkin", "checkout"]
        for date_field in date_fields:
            try:
                date_str = updated_data[date_field]
                datetime.strptime(date_str, "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Lỗi",
                                     f"Định dạng ngày {date_field} không hợp lệ. Vui lòng nhập theo định dạng dd/mm/yyyy")
                return

        # Kiểm tra ngày check-out phải sau ngày check-in
        checkin = datetime.strptime(updated_data["checkin"], "%d/%m/%Y")
        checkout = datetime.strptime(updated_data["checkout"], "%d/%m/%Y")
        if checkout <= checkin:
            messagebox.showerror("Lỗi", "Ngày check-out phải sau ngày check-in")
            return

        # Đọc dữ liệu hiện có
        with open(self.customers_file, 'r', encoding='utf-8') as f:
            customers = json.load(f)

        # Cập nhật thông tin khách hàng
        for i, customer in enumerate(customers):
            if customer['id'] == self.editing_customer_id:
                customers[i] = updated_data
                break

        # Lưu lại
        with open(self.customers_file, 'w', encoding='utf-8') as f:
            json.dump(customers, f, indent=4)

        messagebox.showinfo("Thành công", "Cập nhật thông tin khách hàng thành công")
        self.edit_customer_window.destroy()
        self.view_customers()

    def delete_customer(self):
        """Xóa nhiều khách hàng được chọn"""
        selected_items = self.customers_tree.selection()
        if not selected_items:
            messagebox.showerror("Lỗi", "Vui lòng chọn ít nhất một khách hàng để xóa")
            return

        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa {len(selected_items)} khách hàng đã chọn?"):
            return

        try:
            with open(self.customers_file, 'r', encoding='utf-8') as f:
                customers = json.load(f)

            # Lấy danh sách các ID cần xóa
            selected_ids = [self.customers_tree.item(item)['tags'][0] for item in selected_items]

            # Lọc lại danh sách khách hàng
            updated_customers = [c for c in customers if c['id'] not in selected_ids]

            with open(self.customers_file, 'w', encoding='utf-8') as f:
                json.dump(updated_customers, f, indent=4)

            messagebox.showinfo("Thành công", f"Đã xóa {len(selected_ids)} khách hàng")
            self.view_customers()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi xóa khách hàng: {e}")

    def delete_all_customers(self):
        """Xóa tất cả khách hàng trong danh sách"""
        # Kiểm tra quyền admin
        if self.current_user['role'] != 'admin':
            messagebox.showerror("Lỗi", "Chỉ quản trị viên mới có thể thực hiện chức năng này")
            return

        # Xác nhận trước khi xóa
        if not messagebox.askyesno("Xác nhận",
                                   "Bạn có CHẮC CHẮN muốn xóa TẤT CẢ khách hàng? Hành động này không thể hoàn tác!"):
            return

        try:
            # Ghi file trống
            with open(self.customers_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

            messagebox.showinfo("Thành công", "Đã xóa tất cả khách hàng")
            self.view_customers()  # Làm mới danh sách
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi khi xóa dữ liệu: {str(e)}")

    def search_customer_ui(self):
        """Giao diện tìm kiếm khách hàng"""
        self.search_window = Toplevel(self.root)
        self.search_window.title("Tìm kiếm khách hàng")
        self.search_window.geometry("400x300")

        Label(self.search_window, text="Tìm kiếm khách hàng", font=("Arial", 14)).pack(pady=10)

        search_frame = Frame(self.search_window)
        search_frame.pack(pady=10)

        Label(search_frame, text="Tìm theo:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.search_by = StringVar(value="name")
        OptionMenu(search_frame, self.search_by, "Tên", "Số điện thoại", "CCCD").grid(row=0, column=1, padx=10, pady=10,
                                                                                      sticky=EW)

        Label(search_frame, text="Từ khóa:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.search_keyword = Entry(search_frame, width=25)
        self.search_keyword.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self.search_window, text="Tìm kiếm", command=self.search_customer).pack(pady=20)

    def search_customer(self):
        """Tìm kiếm khách hàng"""
        search_by = self.search_by.get()
        keyword = self.search_keyword.get().lower()

        if not keyword:
            messagebox.showerror("Lỗi", "Vui lòng nhập từ khóa tìm kiếm")
            return

        # Ánh xạ tùy chọn tìm kiếm sang tên trường dữ liệu
        field_map = {
            "Tên": "name",
            "Số điện thoại": "phone",
            "CCCD": "cccd"
        }

        field_name = field_map[search_by]

        # Đọc dữ liệu
        with open(self.customers_file, 'r') as f:
            customers = json.load(f)

        # Tìm kiếm
        results = []
        for customer in customers:
            if keyword in customer[field_name].lower():
                results.append(customer)

        # Hiển thị kết quả
        self.clear_data_frame()

        if not results:
            Label(self.data_frame, text="Không tìm thấy khách hàng nào phù hợp", font=("Arial", 12)).pack(pady=20)
            return

        Label(self.data_frame, text=f"KẾT QUẢ TÌM KIẾM ({len(results)} kết quả)", font=("Arial", 14, "bold")).pack(
            pady=10)

        # Sử dụng self.customers_tree thay vì results_tree
        columns = ("name", "phone", "cccd", "dob", "gender", "checkin", "checkout", "room_type")
        self.customers_tree = ttk.Treeview(self.data_frame, columns=columns, show="headings")

        # Đặt tiêu đề cho các cột
        self.customers_tree.heading("name", text="Tên khách hàng")
        self.customers_tree.heading("phone", text="Số điện thoại")
        self.customers_tree.heading("cccd", text="CCCD")
        self.customers_tree.heading("dob", text="Ngày sinh")
        self.customers_tree.heading("gender", text="Giới tính")
        self.customers_tree.heading("checkin", text="Ngày check-in")
        self.customers_tree.heading("checkout", text="Ngày check-out")
        self.customers_tree.heading("room_type", text="Loại phòng")

        self.customers_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(self.customers_tree, orient="vertical", command=self.customers_tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.customers_tree.configure(yscrollcommand=scrollbar.set)

        # Thêm dữ liệu kết quả (kèm tags chứa ID)
        for customer in results:
            self.customers_tree.insert("", END,
                                       values=(customer['name'],
                                               customer['phone'],
                                               customer['cccd'],
                                               customer['dob'],
                                               customer['gender'],
                                               customer['checkin'],
                                               customer['checkout'],
                                               customer['room_type']),
                                       tags=(customer['id'],))  # Quan trọng: Thêm tags

        # Nút chức năng
        button_frame = Frame(self.data_frame, bg="#f4f6f9")
        button_frame.pack(pady=10)
        if self.current_user['role'] == 'admin':
            ttk.Button(button_frame, text="Làm mới", command=self.view_customers).grid(row=0, column=0, padx=5)
            ttk.Button(button_frame, text="Sửa", command=self.edit_customer).grid(row=0, column=1, padx=5)
            ttk.Button(button_frame, text="Xóa", command=self.delete_customer).grid(row=0, column=2, padx=5)
            ttk.Button(button_frame, text="Xóa tất cả", command=self.delete_all_customers).grid(row=0, column=3, padx=5)

        self.search_window.destroy()
    def import_from_api(self):
        """Nhập dữ liệu từ API"""
        count, error = APIService.import_customers(self.current_user, self.customers_file)

        if error:
            messagebox.showerror("Lỗi", f"Có lỗi khi nhập dữ liệu từ API: {error}")
        else:
            messagebox.showinfo("Thành công", f"Đã nhập {count} khách hàng từ API")
            self.view_customers()

    def clear_ui(self):
        """Xóa toàn bộ giao diện hiện tại"""
        for widget in self.root.winfo_children():
            widget.destroy()


    def clear_data_frame(self):
        """Xóa nội dung trong khung dữ liệu"""
        for widget in self.data_frame.winfo_children():
            widget.destroy()



# Khởi chạy ứng dụng
if __name__ == "__main__":
    root = Tk()
    app = HomestayBookingSystem(root)
    root.mainloop()
