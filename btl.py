import os

# Tên file lưu dữ liệu
FILE_SAN = "danh_sach_san.txt"
FILE_DAT_SAN = "danh_sach_dat_san.txt"

# ----------------- HÀM TIỆN ÍCH & KIỂM TRA DỮ LIỆU (VALIDATION) -----------------

def nhap_so_nguyen(thong_bao):
    """Nhập số nguyên an toàn, chống crash khi nhập chữ."""
    while True:
        try:
            return int(input(thong_bao))
        except ValueError:
            print("[LỖI] Vui lòng nhập một số nguyên hợp lệ!")

def nhap_so_thuc(thong_bao):
    """Nhập số thực (giá, số giờ) an toàn."""
    while True:
        try:
            val = float(input(thong_bao))
            if val < 0:
                print("[LỖI] Giá trị không được âm. Vui lòng nhập lại!")
                continue
            return val
        except ValueError:
            print("[LỖI] Vui lòng nhập một số hợp lệ!")

def nhap_sdt():
    """Kiểm tra số điện thoại không được bỏ trống và đúng định dạng cơ bản."""
    while True:
        sdt = input("Nhập số điện thoại khách hàng: ").strip()
        if not sdt:
            print("[LỖI] Số điện thoại không được để trống!")
            continue
        if not sdt.isdigit() or len(sdt) < 9 or len(sdt) > 11:
            print("[LỖI] Số điện thoại không hợp lệ (phải từ 9-10 chữ số)!")
            continue
        return sdt

# ----------------- CHỨC NĂNG 1: QUẢN LÝ SÂN -----------------

def hien_thi_danh_sach_san(danh_sach):
    """Hiển thị danh sách sân dưới dạng bảng trực quan."""
    if not danh_sach:
        print("\n[THÔNG BÁO] Danh sách sân hiện đang trống!")
        return
    print("\n" + "="*85)
    print(f"{'Mã Sân':<10} | {'Tên Sân':<20} | {'Loại Sân':<15} | {'Địa Điểm':<20} | {'Giá Thuê/Giờ':<12}")
    print("="*85)
    for san in danh_sach:
        print(f"{san['ma_san']:<10} | {san['ten_san']:<20} | {san['loai_san']:<15} | {san['dia_diem']:<20} | {san['gia_thue']:<12,.0f}")
    print("="*85)

def them_san(danh_sach):
    """Thêm sân mới với kiểm tra trùng mã sân."""
    print("\n--- THÊM SÂN MỚI ---")
    while True:
        ma_san = input("Nhập mã sân: ").strip()
        if not ma_san:
            print("[LỖI] Mã sân không được để trống!")
            continue
        # Kiểm tra mã sân trùng
        if any(s['ma_san'].lower() == ma_san.lower() for s in danh_sach):
            print(f"[LỖI] Mã sân '{ma_san}' đã tồn tại. Vui lòng nhập mã khác!")
        else:
            break

    ten_san = input("Nhập tên sân: ").strip()
    loai_san = input("Nhập loại sân (Ví dụ: Bóng đá 5, Cầu lông...): ").strip()
    dia_diem = input("Nhập địa điểm: ").strip()
    gia_thue = nhap_so_thuc("Nhập giá thuê theo giờ (VNĐ): ")

    san_moi = {
        'ma_san': ma_san,
        'ten_san': ten_san,
        'loai_san': loai_san,
        'dia_diem': dia_diem,
        'gia_thue': gia_thue
    }
    danh_sach.append(san_moi)
    print(f"[THÀNH CÔNG] Đã thêm sân '{ten_san}' thành công!")

def cap_nhat_san(danh_sach):
    """Cập nhật thông tin sân dựa theo mã sân."""
    print("\n--- CẬP NHẬT THÔNG TIN SÂN ---")
    ma_san = input("Nhập mã sân cần cập nhật: ").strip()
    for san in danh_sach:
        if san['ma_san'].lower() == ma_san.lower():
            print(f"Tìm thấy sân: {san['ten_san']}. Nhập thông tin mới (bỏ trống nếu giữ nguyên):")
            
            ten_moi = input(f"Tên sân mới [{san['ten_san']}]: ").strip()
            if ten_moi: san['ten_san'] = ten_moi

            loai_moi = input(f"Loại sân mới [{san['loai_san']}]: ").strip()
            if loai_moi: san['loai_san'] = loai_moi

            dia_diem_moi = input(f"Địa điểm mới [{san['dia_diem']}]: ").strip()
            if dia_diem_moi: san['dia_diem'] = dia_diem_moi

            gia_nhap = input(f"Giá thuê mới [{san['gia_thue']}]: ").strip()
            if gia_nhap:
                try:
                    san['gia_thue'] = float(gia_nhap)
                except ValueError:
                    print("[CẢNH BÁO] Giá nhập không hợp lệ, giữ nguyên giá cũ.")

            print("[THÀNH CÔNG] Cập nhật thông tin sân thành công!")
            return
    print(f"[LỖI] Không tìm thấy sân có mã '{ma_san}'!")

def xoa_san(danh_sach, danh_sach_dat):
    """Xóa sân khỏi hệ thống nếu không có lịch đặt liên quan."""
    print("\n--- XÓA SÂN ---")
    ma_san = input("Nhập mã sân cần xóa: ").strip()
    
    # Kiểm tra xem sân có đang nằm trong lịch đặt hay không
    dang_dat = any(d['ma_san'].lower() == ma_san.lower() for d in danh_sach_dat)
    if dang_dat:
        print("[LỖI] Không thể xóa sân này vì đang có lịch đặt sân liên quan!")
        return

    for i, san in enumerate(danh_sach):
        if san['ma_san'].lower() == ma_san.lower():
            xac_nhan = input(f"Bạn có chắc chắn muốn xóa sân '{san['ten_san']}' không? (y/n): ").strip().lower()
            if xac_nhan == 'y':
                danh_sach.pop(i)
                print("[THÀNH CÔNG] Đã xóa sân thành công!")
            else:
                print("[THÔNG BÁO] Hủy thao tác xóa.")
            return
    print(f"[LỖI] Không tìm thấy sân có mã '{ma_san}'!")

# ----------------- CHỨC NĂNG 2: TÌM KIẾM & SẮP XẾP -----------------

def tim_kiem_san(danh_sach):
    """Tìm kiếm sân theo mã, loại, địa điểm hoặc tên khách hàng (tùy biến)."""
    print("\n--- TÌM KIẾM SÂN ---")
    print("1. Tìm theo Mã sân")
    print("2. Tìm theo Loại sân")
    print("3. Tìm theo Địa điểm")
    chon = input("Chọn tiêu chí tìm kiếm (1-3): ").strip()
    
    tu_khoa = input("Nhập từ khóa cần tìm: ").strip().lower()
    ket_qua = []

    if chon == '1':
        ket_qua = [s for s in danh_sach if tu_khoa in s['ma_san'].lower()]
    elif chon == '2':
        ket_qua = [s for s in danh_sach if tu_khoa in s['loai_san'].lower()]
    elif chon == '3':
        ket_qua = [s for s in danh_sach if tu_khoa in s['dia_diem'].lower()]
    else:
        print("[LỖI] Lựa chọn không hợp lệ!")
        return

    if ket_qua:
        print(f"\n[KẾT QUẢ] Tìm thấy {len(ket_qua)} sân phù hợp:")
        hien_thi_danh_sach_san(ket_qua)
    else:
        print("[THÔNG BÁO] Không tìm thấy sân nào phù hợp với từ khóa!")

def sap_xep_san(danh_sach):
    """Sắp xếp danh sách sân theo giá thuê hoặc tên sân."""
    if not danh_sach:
        print("[THÔNG BÁO] Danh sách sân trống!")
        return
    print("\n--- SẮP XẾP SÂN ---")
    print("1. Sắp xếp theo Giá thuê (Tăng dần)")
    print("2. Sắp xếp theo Tên sân (Alphabet)")
    chon = input("Chọn cách sắp xếp (1-2): ").strip()

    if chon == '1':
        danh_sach.sort(key=lambda x: x['gia_thue'])
        print("[THÀNH CÔNG] Đã sắp xếp theo giá thuê tăng dần!")
    elif chon == '2':
        danh_sach.sort(key=lambda x: x['ten_san'])
        print("[THÀNH CÔNG] Đã sắp xếp theo tên sân thành công!")
    else:
        print("[LỖI] Lựa chọn không hợp lệ!")
        return
    hien_thi_danh_sach_san(danh_sach)

# ----------------- CHỨC NĂNG 3: ĐẶT SÂN & HỦY ĐẶT SÂN -----------------

def dat_san(danh_sach_san, danh_sach_dat):
    """Thực hiện đặt sân và kiểm tra trùng lịch, tính tiền."""
    print("\n--- ĐẶT SÂN THỂ THAO ---")
    hien_thi_danh_sach_san(danh_sach_san)
    if not danh_sach_san:
        return

    ma_san = input("Nhập mã sân muốn đặt: ").strip()
    san_chon = next((s for s in danh_sach_san if s['ma_san'].lower() == ma_san.lower()), None)
    
    if not san_chon:
        print("[LỖI] Sân không tồn tại trong hệ thống!")
        return

    ten_khach = input("Nhập tên khách hàng: ").strip()
    if not ten_khach:
        print("[LỖI] Tên khách hàng không được để trống!")
        return

    sdt = nhap_sdt()
    ngay_dat = input("Nhập ngày đặt (Định dạng YYYY-MM-DD, VD: 2026-11-01): ").strip()
    
    gio_bat_dau = nhap_so_thuc("Nhập giờ bắt đầu (Ví dụ: 14.5 cho 14h30): ")
    if not (0 <= gio_bat_dau <= 24):
        print("[LỖI] Giờ bắt đầu phải nằm trong khoảng từ 0 đến 24!")
        return

    so_gio_thue = nhap_so_thuc("Nhập số giờ thuê: ")
    if so_gio_thue <= 0:
        print("[LỖI] Số giờ thuê phải lớn hơn 0!")
        return

    gio_ket_thuc = gio_bat_dau + so_gio_thue

    # Kiểm tra trùng lịch đặt sân trong cùng ngày
    for dat in danh_sach_dat:
        if dat['ma_san'].lower() == ma_san.lower() and dat['ngay_dat'] == ngay_dat:
            D_start = dat['gio_bat_dau']
            D_end = dat['gio_bat_dau'] + dat['so_gio_thue']
            # Kiểm tra khoảng thời gian có bị chồng chéo không
            if not (gio_ket_thuc <= D_start or gio_bat_dau >= D_end):
                print(f"[LỖI] Sân này đã được đặt vào khung giờ {D_start} - {D_end} ngày {ngay_dat}!")
                return

    # Tính tiền thuê
    tong_tien = san_chon['gia_thue'] * so_gio_thue
    ma_dat_san = f"DAT_{len(danh_sach_dat) + 1:03d}"

    phieu_dat = {
        'ma_dat_san': ma_dat_san,
        'ma_san': san_chon['ma_san'],
        'ten_khach': ten_khach,
        'sdt': sdt,
        'ngay_dat': ngay_dat,
        'gio_bat_dau': gio_bat_dau,
        'so_gio_thue': so_gio_thue,
        'tong_tien': tong_tien
    }
    danh_sach_dat.append(phieu_dat)
    print(f"\n[THÀNH CÔNG] Đặt sân thành công! Mã đặt sân: {ma_dat_san}")
    print(f"Tổng tiền thanh toán: {tong_tien:,.0f} VNĐ")

def huy_dat_san(danh_sach_dat):
    """Hủy lượt đặt sân dựa theo mã đặt sân."""
    print("\n--- HỦY ĐẶT SÂN ---")
    if not danh_sach_dat:
        print("[THÔNG BÁO] Chưa có lịch đặt sân nào!")
        return

    print(f"{'Mã Đặt':<10} | {'Mã Sân':<10} | {'Khách Hàng':<20} | {'Ngày Đặt':<12}")
    print("-" * 60)
    for d in danh_sach_dat:
        print(f"{d['ma_dat_san']:<10} | {d['ma_san']:<10} | {d['ten_khach']:<20} | {d['ngay_dat']:<12}")

    ma_dat = input("\nNhập mã đặt sân cần hủy: ").strip()
    for i, d in enumerate(danh_sach_dat):
        if d['ma_dat_san'].lower() == ma_dat.lower():
            danh_sach_dat.pop(i)
            print(f"[THÀNH CÔNG] Đã hủy thành công phiếu đặt sân {ma_dat}!")
            return
    print(f"[LỖI] Không tìm thấy mã đặt sân '{ma_dat}'!")

# ----------------- CHỨC NĂNG 4: THỐNG KÊ -----------------

def thong_ke(danh_sach_san, danh_sach_dat):
    """Thống kê tổng quan hoạt động kinh doanh sân."""
    print("\n" + "="*40 + " THỐNG KÊ HỆ THỐNG " + "="*40)
    print(f"1. Tổng số sân trong hệ thống: {len(danh_sach_san)}")
    
    # Số sân đang được đặt (tính theo số lượt đặt hiện tại)
    print(f"2. Tổng số lượt đặt sân: {len(danh_sach_dat)}")
    
    # Sân có giá thuê cao nhất
    if danh_sach_san:
        max_gia = max(s['gia_thue'] for s in danh_sach_san)
        san_max = [s['ten_san'] for s in danh_sach_san if s['gia_thue'] == max_gia]
        print(f"3. Sân có giá thuê cao nhất ({max_gia:,.0f} VNĐ/h): {', '.join(san_max)}")
    else:
        print("3. Sân có giá thuê cao nhất: Không có dữ liệu")

    # Tổng doanh thu
    tong_doanh_thu = sum(d['tong_tien'] for d in danh_sach_dat)
    print(f"4. Tổng doanh thu dự kiến: {tong_doanh_thu:,.0f} VNĐ")

    # Loại sân được đặt nhiều nhất
    if danh_sach_dat:
        dem_loai = {}
        for d in danh_sach_dat:
            # Tìm loại sân tương ứng với mã sân đặt
            s = next((item for item in danh_sach_san if item['ma_san'].lower() == d['ma_san'].lower()), None)
            if s:
                loai = s['loai_san']
                dem_loai[loai] = dem_loai.get(loai, 0) + 1
        if dem_loai:
            loai_nhieu_nhat = max(dem_loai, key=dem_loai.get)
            print(f"5. Loại sân được đặt nhiều nhất: {loai_nhieu_nhat} ({dem_loai[loai_nhieu_nhat]} lượt)")
    else:
        print("5. Loại sân được đặt nhiều nhất: Chưa có dữ liệu")
    print("="*98)

# ----------------- CHỨC NĂNG 5: LƯU VÀ ĐỌC DỮ LIỆU TỪ FILE TXT -----------------

def luu_du_lieu(danh_sach_san, danh_sach_dat):
    """Lưu danh sách sân và lịch đặt vào file TXT."""
    try:
        # Lưu file sân
        with open(FILE_SAN, "w", encoding="utf-8") as f:
            for s in danh_sach_san:
                f.write(f"{s['ma_san']}|{s['ten_san']}|{s['loai_san']}|{s['dia_diem']}|{s['gia_thue']}\n")
        
        # Lưu file đặt sân
        with open(FILE_DAT_SAN, "w", encoding="utf-8") as f:
            for d in danh_sach_dat:
                f.write(f"{d['ma_dat_san']}|{d['ma_san']}|{d['ten_khach']}|{d['sdt']}|{d['ngay_dat']}|{d['gio_bat_dau']}|{d['so_gio_thue']}|{d['tong_tien']}\n")
        
        print("[THÀNH CÔNG] Dữ liệu đã được lưu vào file TXT an toàn!")
    except Exception as e:
        print(f"[LỖI] Không thể lưu file: {e}")

def doc_du_lieu():
    """Đọc dữ liệu sân và lịch đặt từ file TXT."""
    danh_sach_san = []
    danh_sach_dat = []
    
    try:
        if os.path.exists(FILE_SAN):
            with open(FILE_SAN, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 5:
                        danh_sach_san.append({
                            'ma_san': parts[0],
                            'ten_san': parts[1],
                            'loai_san': parts[2],
                            'dia_diem': parts[3],
                            'gia_thue': float(parts[4])
                        })
        
        if os.path.exists(FILE_DAT_SAN):
            with open(FILE_DAT_SAN, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 8:
                        danh_sach_dat.append({
                            'ma_dat_san': parts[0],
                            'ma_san': parts[1],
                            'ten_khach': parts[2],
                            'sdt': parts[3],
                            'ngay_dat': parts[4],
                            'gio_bat_dau': float(parts[5]),
                            'so_gio_thue': float(parts[6]),
                            'tong_tien': float(parts[7])
                        })
        print("[THÀNH CÔNG] Đọc dữ liệu từ file TXT thành công!")
    except Exception as e:
        print(f"[LỖI] Đọc file gặp sự cố: {e}")
    
    return danh_sach_san, danh_sach_dat

# ----------------- MENU CHÍNH -----------------

def main():
    # Tự động đọc dữ liệu khi khởi động chương trình nếu file tồn tại
    danh_sach_san, danh_sach_dat = doc_du_lieu()

    while True:
        print("\n" + "="*40 + " QUẢN LÝ ĐẶT SÂN THỂ THAO " + "="*40)
        print("1. Thêm sân")
        print("2. Hiển thị danh sách sân")
        print("3. Cập nhật sân")
        print("4. Xóa sân")
        print("5. Tìm kiếm sân")
        print("6. Sắp xếp sân")
        print("7. Đặt sân")
        print("8. Hủy đặt sân")
        print("9. Thống kê")
        print("10. Lưu dữ liệu")
        print("11. Đọc dữ liệu")
        print("0. Thoát")
        print("="*85)
        
        chon = nhap_so_nguyen("Lựa chọn của bạn (0-11): ")

        if chon == 1:
            them_san(danh_sach_san)
        elif chon == 2:
            hien_thi_danh_sach_san(danh_sach_san)
        elif chon == 3:
            cap_nhat_san(danh_sach_san)
        elif chon == 4:
            xoa_san(danh_sach_san, danh_sach_dat)
        elif chon == 5:
            tim_kiem_san(danh_sach_san)
        elif chon == 6:
            sap_xep_san(danh_sach_san)
        elif chon == 7:
            dat_san(danh_sach_san, danh_sach_dat)
        elif chon == 8:
            huy_dat_san(danh_sach_dat)
        elif chon == 9:
            thong_ke(danh_sach_san, danh_sach_dat)
        elif chon == 10:
            luu_du_lieu(danh_sach_san, danh_sach_dat)
        elif chon == 11:
            danh_sach_san, danh_sach_dat = doc_du_lieu()
        elif chon == 0:
            # Tự động lưu trước khi thoát để an toàn dữ liệu
            luu_du_lieu(danh_sach_san, danh_sach_dat)
            print("\n[THÔNG BÁO] Cảm ơn bạn đã sử dụng chương trình. Tạm biệt!")
            break
        else:
            print("[LỖI] Lựa chọn không hợp lệ từ 0 đến 11. Vui lòng thử lại!")

if __name__ == "__main__":
    main()