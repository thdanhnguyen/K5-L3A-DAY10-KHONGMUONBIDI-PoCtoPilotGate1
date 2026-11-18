# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): KHONGMUONBIDI
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-KHONGMUONBIDI-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S6`

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Nguyễn Thành Danh | 2A202603493   | Trưởng nhóm & Sản phẩm / Kinh doanh   |     x        |
|   2 | Lưu Đăng Tuấn          | 2A202603454     | Kỹ sư Cổng, Monitor & Kỹ thuật Vòng 2    |             |
|   3 | Nguyễn Thị Hồng San      | 2A202603513   | Vận hành & Pháp lý      |             |
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

## LuuDangTuan-2A202603454

### Phần việc phụ trách

- Vai trong bàn: Kỹ sư Cổng, Monitor & Kỹ thuật Vòng 2 (cùng tham gia Câu 1.3 ở Khối 1).
- Phụ trách chính: Khối 3 · Sự cố `S6` (Câu 3.0, 3.1, 3.5, 3.6), sửa cổng `lab10/guards.py`, viết chỉ số theo dõi `lab10/monitors.py`, cập nhật cổng `legal` trong `config/operating_gates.json`, hoàn thiện Phiếu C (`templates/form-c-incident.md`) và gom bài nộp `submission/`.

### Đóng góp cụ thể

- Xử lý lỗi đồng bộ ký tự xuống dòng (`CRLF` -> `LF`) trên Windows để khôi phục kiểm tra `1 integrity ✅` và `2 criteria ✅`.
- Chạy mốc `prepared` và dò trace các ca hỏng đại diện trên thẻ `S6` (`S6-01@11`, `S6-04@11`, `S6-20@11`, `S6-42@11`), phân tích 3 nguyên nhân gốc: `agent.py` lấy cứng `parcels[0]` khi gọi `file_carrier_fault`, thiếu xử lý đơn đa kiện bị bỏ trống `parcel_id`, và không chặn vượt trần `2` lỗi/hãng/ngày (`max_auto_strikes_per_carrier_per_day`).
- Bổ sung cổng Vòng 2 trong `lab10/guards.py`: (1) chặn và `escalate` đơn nhiều kiện trễ thiếu `parcel_id` trước `issue_refund`; (2) đối chiếu `H.ticket_parcel` và `Verdict.modify` sửa đúng `parcel_id`, `carrier_id`, `driver_id`, `delay_days` khi gọi `file_carrier_fault`; (3) đếm `fault_rows(carrier_id)` để `deny` khi đạt trần `2` lỗi/hãng/ngày.
- Bổ sung 3 monitor mới trong `lab10/monitors.py` (`wrong_parcel_fault_or_reassigned_rate`, `ambiguous_multi_parcel_rate`, `carrier_daily_strike_excess_rate`) đều sáng đèn trên `S6` và `0.0` trên bộ nền.
- Bật cổng pháp lý trong `config/operating_gates.json` (`carrier_fault_requires_recorded_cause: true`, chặn `recipient_contact` và `customer_note`), đưa kết quả `S6` từ `pass_rate = 0.3333` (40 lỗi hãng oan, 270k hoàn sai) lên `1.0` (`0` lỗi oan, `0đ` hoàn sai, `ROI = 0.91`) và `base` giữ nguyên `1.0`.

### Bằng chứng

- Mã lần chạy:
  + `S6 · prepared` (trước sửa): `R-S6-prepared-20261118-165001-3f6fad` (`R-S6-grade-20261118-164959-3f6fad`)
  + `S6 · after`: `R-S6-after-20261118-165557-edf64c`
  + `base · after`: `R-base-after-20261118-165558-edf64c`
  + `grade S6` (PASS-VISIBLE): `R-S6-grade-20261118-170005-edf64c` (base `R-S6-before-20261118-170006-edf64c`, prepared `R-S6-prepared-20261118-170006-edf64c`, after `R-S6-after-20261118-170006-edf64c`)
- Dòng trong phiếu: Phiếu C mục C0–C12 (`templates/form-c-incident.md`), `lab10/guards.py`, `lab10/monitors.py`, `config/operating_gates.json`, `submission/submission.json`.

### Exit ticket

- Một điều học được: Khi đơn hàng tách nhiều kiện và hệ thống tự động gọi tool ở cấp đơn (`parcels[0]`), lỗi chìm sẽ dồn thiệt hại lên đối tác bên thứ ba mà khách hàng không hề hay biết; phải đặt cổng sửa/chặn tại `write_gate` dựa trên đơn vị sự thật (`parcel_id`) và theo dõi bằng monitor không nhãn.
- Một điều còn chưa chắc: Độ chính xác thực tế của dữ liệu `tracking` từ bưu cục khi đưa vào pilot thật (nếu quét sót ngày giao hoặc ghi nhầm nguyên nhân trễ tại nguồn thì cổng đối chiếu DB vẫn bị phụ thuộc).

## NguyenThanhDanh-2A202603493

### Phần việc phụ trách

- Vai trong bàn: Trưởng nhóm & Sản phẩm / Kinh doanh.
- Phụ trách chính: Khối 1 (câu 1.1–1.6) và ký tiêu chí; câu 2.3 (bản đồ dữ liệu, drift); câu 2.9 (cổng kinh doanh); quyết định Gate 1 v1 và đồng ký v2.
- Phiếu: Phiếu A (A1–A5); Phiếu B các mục B3, B7.4, B8 (PIC ký v1); Phiếu C mục C12 (đồng ký v2).
- File phụ trách: `config/acceptance_criteria.json`, `config/acceptance_criteria.lock`, mục `business` trong `config/operating_gates.json`, `submission/submission.json`.

### Đóng góp cụ thể

- Viết mục tiêu cấp hệ thống, bảng thước đo → dữ liệu → cách tính, câu tiêu chí "Nếu … thì chúng tôi sẽ …" và bốn dòng `decision_rule`, nối với PRD v1.1 và eval card của Lab 9.
- Đặt và ký ngưỡng **trước** lần đánh giá đầu tiên: `pass_rate_min = 0.96`, `pass_k_min = 0.92`, ba chỉ số an toàn bằng 0, `cost_per_ticket_vnd_max = 8500`, `roi_min = 0.25`, `queue_stuck_max = 0`.
- Điền cổng kinh doanh từ `data/world.json`: `daily_refund_cap_vnd = 1600000` (80% ngân sách Finance 2.000.000đ), `cost_budget_per_ticket_vnd = 1100` (chừa 400đ cho các bước LLM sau), `pilot_scope = all`, `roi_min = 0.25`.
- Ra quyết định v1 **Tiếp tục**, khớp dòng "Tiếp tục" của `decision_rule`, có ba bằng chứng từ mốc prepared; chỉ ra kho `?` (10.359đ > làm tay) là phân khúc cần giám sát.

### Bằng chứng

- Mã commit: `cee4503` (`Sign acceptance criteria`, hash tiêu chí `857a0d94`, ký 2026-11-18 15:02:54), `2c45d11` (Phiếu A).
- Mã lần chạy: `R-base-before-20261118-153331-b12d93` (base), `R-base-prepared-20261118-153359-b12d93` (bằng chứng v1), `R-S6-grade-20261118-171915-5bdb05` (bằng chứng v2).
- Dòng trong phiếu: Phiếu A mục A1–A5; Phiếu B mục B3, B5 dòng 2, 6, 9, B7.4, B8; Phiếu C mục C12.

### Exit ticket

- Một điều học được: Ký tiêu chí trước khi xem số buộc cả bàn quyết định bằng ngưỡng đã cam kết, chứ không phải bằng con số mình muốn thấy. Ngưỡng kinh doanh (chi phí, ROI, trần ngày) quan trọng ngang ngưỡng chất lượng.
- Một điều còn chưa chắc: Ngưỡng chi phí 8.500đ/ticket và ROI 0,25 được đặt từ số mock; chưa chắc chúng còn đúng khi chạy với lưu lượng và giá LLM thật trong pilot.

## NguyenThiHongSan-2A202603513

### Phần việc phụ trách

- Vai trong bàn: Vận hành & Pháp lý.
- Phụ trách chính: câu 2.4 (HAZOP vòng 1, checklist 9 nhóm việc); câu 2.10 (cổng con người, vận hành, pháp lý; runbook phần 1–3 và giờ cao điểm); câu 1.2, 1.4 ở Khối 1; theo dõi nhóm 5, 7, 8 của checklist ở cả hai vòng.
- Phiếu: Phiếu A câu 1.2, 1.4; Phiếu B các mục B4, B5, B6 (dòng Con người và vận hành, Pháp lý), B7.5, B7.6; Phiếu C mục C11 (dòng 7, 8 của checklist).
- File phụ trách: mục `operations` và `legal` trong `config/operating_gates.json`.

### Đóng góp cụ thể

- HAZOP vòng 1 trên `file_carrier_fault` (5 dòng kỹ thuật + 3 dòng ngoài kỹ thuật), trong đó chỉ ra trước khi bốc thẻ nhánh **ghi lỗi nhầm kiện ở đơn nhiều kiện** (`parcels[0]`) và nhánh **dồn quá 2 lỗi/hãng/ngày**, đúng hai nguyên nhân của thẻ S6.
- Chạy trace adhoc đơn quà tặng `O-1026` ở mốc prepared, phát hiện tên và SĐT người nhận bị gửi sang GHSH, trong khi `pii_leaks = 0` trên bộ nền chỉ là điểm mù. Đề xuất chặn `recipient_contact`, `customer_note`, được bật ở vòng 2.
- Điền mục `operations` (PIC `NV-TUNG`, người duyệt `NV-HANH`, 1 người trực, 6 ca/giờ, chờ tối đa 60 phút, 3 điều kiện dừng, kênh `#logix-pilot-ops-alerts`, `decision_note`, kiểm mẫu 10%) khớp `staff_behavior.trust_conditions`.
- Viết checklist 9 nhóm việc với PIC có tên cho từng dòng; viết runbook phần 1–3 và giờ cao điểm khớp các con số trong config (gọi người thứ 2 khi chờ ≥ 30 phút hoặc hàng chờ ≥ 4 ca; dừng trong 15 phút do `NV-TUNG` bấm).

### Bằng chứng

- Mã commit: `f8ac03d` (Phiếu B: B4 HAZOP vòng 1 và B5 checklist).
- Mã lần chạy: `R-base-before-20261118-153331-b12d93` (trace `T-002@55` dùng ở dòng WRONG của HAZOP), `R-base-prepared-20261118-153359-b12d93` (bằng chứng checklist), `R-S6-grade-20261118-171915-5bdb05` (`pii_leaks = 0`, `wrongful_carrier_faults = 0` sau khi bật `legal`).
- Dòng trong phiếu: Phiếu B mục B4, B5, B6, B7.5, B7.6; Phiếu C mục C11 (dòng 7, 8).

### Exit ticket

- Một điều học được: Rủi ro lớn nhất không nằm ở model mà ở người và bên thứ ba vắng mặt: hãng bị phạt oan, người nhận quà bị lộ số điện thoại, người duyệt bị quá tải. Những rủi ro này chỉ lộ ra khi áp HAZOP vào cả các thành phần ngoài code.
- Một điều còn chưa chắc: Ngưỡng gọi thêm người (chờ ≥ 30 phút, hàng chờ ≥ 4 ca) mới ước tính từ công suất 6 ca/giờ; chưa đo được trên tải gấp ba thật, nên chưa chắc 2 người đã đủ trong ngày sale.
