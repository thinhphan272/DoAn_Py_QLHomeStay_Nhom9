import json
from uuid import uuid4

class APIService:
    @staticmethod
    def get_mock_customers():
        """Giả lập dữ liệu từ API"""
        return [
            {
                "name": "Nguyễn Văn Minh",
                "phone": "0987654321",
                "cccd": "123456789012",
                "dob": "15/05/1990",
                "gender": "Nam",
                "checkin": "20/06/2023",
                "checkout": "25/06/2023",
                "room_type": "Phòng đôi"
            },
            {
                "name": "Trần Thị Hằng",
                "phone": "0912345678",
                "cccd": "987654321098",
                "dob": "22/10/1985",
                "gender": "Nữ",
                "checkin": "10/07/2023",
                "checkout": "15/07/2023",
                "room_type": "Phòng đơn"
            },
            {
                "name": "Lê Văn Nam",
                "phone": "0901234567",
                "cccd": "123450987654",
                "dob": "01/01/1988",
                "gender": "Nam",
                "checkin": "01/07/2023",
                "checkout": "05/07/2023",
                "room_type": "Phòng gia đình"
            },
            {
                "name": "Phạm Thị Mai",
                "phone": "0934567890",
                "cccd": "456789123456",
                "dob": "14/02/1992",
                "gender": "Nữ",
                "checkin": "12/07/2023",
                "checkout": "18/07/2023",
                "room_type": "Phòng đơn"
            },
            {
                "name": "Hoàng Văn Dũng",
                "phone": "0978123456",
                "cccd": "789123456789",
                "dob": "23/03/1985",
                "gender": "Nam",
                "checkin": "05/06/2023",
                "checkout": "10/06/2023",
                "room_type": "Phòng đôi"
            },
            {
                "name": "Đỗ Thị Huyền",
                "phone": "0961234567",
                "cccd": "321654987321",
                "dob": "30/04/1990",
                "gender": "Nữ",
                "checkin": "20/07/2023",
                "checkout": "25/07/2023",
                "room_type": "Phòng gia đình"
            },
            {
                "name": "Ngô Văn Khánh",
                "phone": "0945678901",
                "cccd": "654987321654",
                "dob": "10/06/1980",
                "gender": "Nam",
                "checkin": "15/06/2023",
                "checkout": "20/06/2023",
                "room_type": "Phòng đơn"
            },
            {
                "name": "Vũ Thị Bích",
                "phone": "0931234567",
                "cccd": "987321654987",
                "dob": "25/12/1991",
                "gender": "Nữ",
                "checkin": "22/06/2023",
                "checkout": "27/06/2023",
                "room_type": "Phòng gia đình"
            },
            {
                "name": "Trịnh Văn Cường",
                "phone": "0919876543",
                "cccd": "159753486231",
                "dob": "19/11/1987",
                "gender": "Nam",
                "checkin": "10/08/2023",
                "checkout": "15/08/2023",
                "room_type": "Phòng đôi"
            },
            {
                "name": "Lý Thị Thảo",
                "phone": "0981122334",
                "cccd": "753159846321",
                "dob": "08/09/1995",
                "gender": "Nữ",
                "checkin": "03/09/2023",
                "checkout": "08/09/2023",
                "room_type": "Phòng đơn"
            },
            {
                "name": "Nguyễn Hữu Toàn",
                "phone": "0973344556",
                "cccd": "246813579135",
                "dob": "02/07/1993",
                "gender": "Nam",
                "checkin": "01/08/2023",
                "checkout": "06/08/2023",
                "room_type": "Phòng gia đình"
            },
            {
                "name": "Trần Ngọc Hà",
                "phone": "0909988776",
                "cccd": "135792468024",
                "dob": "11/05/1984",
                "gender": "Nữ",
                "checkin": "05/07/2023",
                "checkout": "10/07/2023",
                "room_type": "Phòng đơn"
            },
            {
                "name": "Bùi Văn Hòa",
                "phone": "0935566778",
                "cccd": "987654123321",
                "dob": "07/01/1979",
                "gender": "Nam",
                "checkin": "10/06/2023",
                "checkout": "15/06/2023",
                "room_type": "Phòng đôi"
            },
            {
                "name": "Đặng Thị Phương",
                "phone": "0911122233",
                "cccd": "321456987654",
                "dob": "29/02/1988",
                "gender": "Nữ",
                "checkin": "01/09/2023",
                "checkout": "06/09/2023",
                "room_type": "Phòng gia đình"
            },
            {
                "name": "Hồ Văn Kiên",
                "phone": "0956677889",
                "cccd": "456321789123",
                "dob": "16/08/1990",
                "gender": "Nam",
                "checkin": "15/07/2023",
                "checkout": "20/07/2023",
                "room_type": "Phòng đơn"
            },
            {
                "name": "Tạ Thị Quỳnh",
                "phone": "0944556677",
                "cccd": "789654123987",
                "dob": "03/03/1982",
                "gender": "Nữ",
                "checkin": "10/08/2023",
                "checkout": "14/08/2023",
                "room_type": "Phòng đôi"
            },
            {
                "name": "Lâm Văn Tài",
                "phone": "0939988775",
                "cccd": "951357852456",
                "dob": "09/09/1996",
                "gender": "Nam",
                "checkin": "20/06/2023",
                "checkout": "25/06/2023",
                "room_type": "Phòng gia đình"
            },
            {
                "name": "Mai Thị Lan",
                "phone": "0967766554",
                "cccd": "147258369741",
                "dob": "12/12/1983",
                "gender": "Nữ",
                "checkin": "01/08/2023",
                "checkout": "06/08/2023",
                "room_type": "Phòng đơn"
            },
            {
                "name": "Chu Văn Phúc",
                "phone": "0914455667",
                "cccd": "369258147852",
                "dob": "05/04/1975",
                "gender": "Nam",
                "checkin": "03/07/2023",
                "checkout": "08/07/2023",
                "room_type": "Phòng đôi"
            },
            {
                "name": "Dương Thị Như",
                "phone": "0982233445",
                "cccd": "753951456852",
                "dob": "28/10/1989",
                "gender": "Nữ",
                "checkin": "12/07/2023",
                "checkout": "17/07/2023",
                "room_type": "Phòng gia đình"
            },
            {
                "name": "Trịnh Văn Quang",
                "phone": "0947788990",
                "cccd": "654321987654",
                "dob": "17/06/1994",
                "gender": "Nam",
                "checkin": "10/07/2023",
                "checkout": "15/07/2023",
                "room_type": "Phòng đơn"
            },
            {
                "name": "Lê Thị Hoa",
                "phone": "0932233445",
                "cccd": "789321654987",
                "dob": "13/03/1987",
                "gender": "Nữ",
                "checkin": "25/08/2023",
                "checkout": "30/08/2023",
                "room_type": "Phòng đôi"
            },
            {
                "name": "Phan Văn Sơn",
                "phone": "0923344556",
                "cccd": "852456789321",
                "dob": "21/09/1991",
                "gender": "Nam",
                "checkin": "07/07/2023",
                "checkout": "12/07/2023",
                "room_type": "Phòng gia đình"
            },
            {
                "name": "Nguyễn Thị Minh",
                "phone": "0918899776",
                "cccd": "963852741258",
                "dob": "20/01/1986",
                "gender": "Nữ",
                "checkin": "15/08/2023",
                "checkout": "20/08/2023",
                "room_type": "Phòng đơn"
            },
            {
                "name": "Trần Văn Đức",
                "phone": "0961122334",
                "cccd": "741852963147",
                "dob": "04/05/1990",
                "gender": "Nam",
                "checkin": "01/09/2023",
                "checkout": "06/09/2023",
                "room_type": "Phòng đôi"
            },
            {
                "name": "Đinh Thị Lệ",
                "phone": "0952233445",
                "cccd": "321789456123",
                "dob": "06/06/1992",
                "gender": "Nữ",
                "checkin": "10/06/2023",
                "checkout": "15/06/2023",
                "room_type": "Phòng gia đình"
            },
            {
                "name": "Lưu Văn Hiếu",
                "phone": "0943344556",
                "cccd": "456987123654",
                "dob": "02/10/1980",
                "gender": "Nam",
                "checkin": "18/06/2023",
                "checkout": "23/06/2023",
                "room_type": "Phòng đơn"
            },
            {
                "name": "Võ Thị Yến",
                "phone": "0906677889",
                "cccd": "789456321987",
                "dob": "24/12/1988",
                "gender": "Nữ",
                "checkin": "28/07/2023",
                "checkout": "02/08/2023",
                "room_type": "Phòng đôi"
            },
            {
                "name": "Đoàn Văn Thịnh",
                "phone": "0915566778",
                "cccd": "147369258963",
                "dob": "19/02/1983",
                "gender": "Nam",
                "checkin": "01/07/2023",
                "checkout": "06/07/2023",
                "room_type": "Phòng gia đình"
            }
        ]

    @staticmethod
    def import_customers(current_user, customers_file):
        """Nhập dữ liệu từ API vào hệ thống"""
        try:
            # Lấy dữ liệu từ API
            mock_data = APIService.get_mock_customers()

            # Đọc dữ liệu hiện có
            with open(customers_file, 'r') as f:
                current_customers = json.load(f)

            # Thêm ID và người tạo cho mỗi khách hàng mới
            for customer in mock_data:
                customer['id'] = str(uuid4())
                customer['created_by'] = current_user['username']
                current_customers.append(customer)

            # Lưu lại
            with open(customers_file, 'w') as f:
                json.dump(current_customers, f, indent=4)

            return len(mock_data), None  # Trả về số lượng và lỗi (nếu có)

        except Exception as e:
            return 0, str(e)