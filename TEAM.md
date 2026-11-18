# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): KHONGMUONBIDI
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-KHONGMUONBIDI-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8):

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Nguyễn Thành Danh | 2A202603493   | Trưởng nhóm & Sản phẩm / Kinh doanh   |     x        |
|   2 | Lưu Đăng Tuấn          | 2A202603454     | Kỹ sư Cổng, Monitor & Kỹ thuật Vòng 2    |             |
|   3 | Nguyễn Thị Hồng San      | 2A202603513   | Vận hành & Pháp lý      |     |             |
|   4 | Võ Lê Hải Đăng      | 2A202603577     |  Kỹ sư Cổng Vòng 1 & QA   |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## VoLeHaiDang-2A202603577

### Phần việc phụ trách

- Vai trong bàn: Kỹ sư Cổng Vòng 1 & QA / Bằng chứng Vòng 2.
- Phụ trách chính: Câu 2.1, 2.2, 2.6, 2.7, 2.8, chốt mốc prepared Vòng 1 (Câu 2.6–2.10, B8 v1).
- Phiếu: Điền Phiếu B các mục B0, B1, B2, B7.1, B7.2, B7.3, B8; phối hợp QA và tổng hợp bằng chứng kỹ thuật ở Phiếu C (C0, C1, C5, C6).
- File code phụ trách: `lab10/guards.py`, bản chốt `lab10/guards_round1.py`.

### Đóng góp cụ thể

- Kiểm tra môi trường ban đầu, chạy bộ 13 unit tests công khai đảm bảo PASS 100%.
- Đo đạc mốc baseline, phân tích trace chuyên sâu ticket `T-002@55`, vạch rõ lỗi model tin lời khách khai dẫn tới hoàn tiền sai và phạt oan hãng VNX.
- Thiết kế và code 3 cổng an toàn trong `lab10/guards.py` sử dụng `write_gate`: Cổng 1 (đối chiếu DB trước khi hoàn tiền), Cổng 2 (chặn vượt trần ngân sách ngày và hạn mức khách), Cổng 3 (ngăn ghi lỗi oan cho đối tác vận chuyển khi DB không có ghi nhận nguyên nhân).
- Chạy 2 behavioral test adhoc chứng minh tính tổng quát của cổng; chạy mốc `after` và thực hiện chốt checkpoint mốc `prepared` (hash `082a9a38`) đưa kết quả đạt 100% tiêu chí chấp nhận.
- Bàn giao cấu trúc cổng và phối hợp cùng Anh Tuấn (Kỹ sư Vòng 2) làm QA, đối chiếu regression và kiểm tra gom bài.

### Bằng chứng

- Mã commit: `cee4503` (ký tiêu chí), commit merge và chốt mốc Vòng 1.
- Mã lần chạy:
  + Baseline: `R-base-before-20261118-153331-b12d93`
  + Thử cổng Vòng 1: `R-base-after-20261118-153341-b12d93`
  + Mốc Prepared chốt: `R-base-prepared-20261118-153359-b12d93`
- Dòng trong phiếu: Phiếu B mục B0 (dòng 1–3), B1, B2, B7.1–B7.3, B8; Phiếu C mục C0, C1.

### Exit ticket

- Một điều học được: Guardrails cấp hệ thống nằm ngoài mô hình (code gate trước các thao tác ghi DB) là phòng tuyến bắt buộc để bảo vệ sự toàn vẹn của sổ cái và ngân sách, không bao giờ được tin cậy hoàn toàn vào prompt hay lời khai của người dùng.
- Một điều còn chưa chắc: Cần xem xét cách thức cổng thích ứng khi có sự thay đổi chính sách giữa các mốc thời gian (như chuyển giao REFUND-v3 sang REFUND-v4) nếu tracking DB gặp độ trễ đồng bộ.
