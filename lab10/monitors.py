"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def wrong_parcel_fault_or_reassigned_rate(trials):
    """Tỉ lệ trial ghi lỗi hãng sang kiện sai/không trễ (before) hoặc được gate sửa đúng kiện (after)."""
    hits = 0
    for t in trials:
        guard_hit = any(
            e.get("type") == "guard" and e.get("kind") == "parcel_fault_reassigned"
            for e in t.get("events", [])
        )
        if guard_hit:
            hits += 1
            continue
        req_pid = (t.get("ticket") or {}).get("parcel_id")
        tracking = next((e for e in t.get("events", []) if e.get("type") == "tracking"), None)
        parcel_delays = {p["parcel_id"]: p["delay"] for p in (tracking or {}).get("parcels", [])}
        max_delay = max(parcel_delays.values(), default=0)
        faults = t.get("faults") or []
        if any(
            (req_pid and f.get("parcel_id") != req_pid)
            or (f.get("parcel_id") in parcel_delays and parcel_delays[f["parcel_id"]] < max_delay)
            for f in faults
        ):
            hits += 1
    return hits / max(1, len(trials))


def ambiguous_multi_parcel_rate(trials):
    """Tỉ lệ trial đơn nhiều kiện có >= 2 kiện giao trễ nhưng thiếu parcel_id."""
    hits = 0
    for t in trials:
        guard_hit = any(
            e.get("type") == "guard" and e.get("kind") == "ambiguous_multi_parcel"
            for e in t.get("events", [])
        )
        if guard_hit:
            hits += 1
            continue
        if (t.get("ticket") or {}).get("parcel_id"):
            continue
        tracking = next((e for e in t.get("events", []) if e.get("type") == "tracking"), None)
        delayed = [p for p in (tracking or {}).get("parcels", []) if p.get("delay", 0) > 0]
        if len(delayed) > 1:
            hits += 1
    return hits / max(1, len(trials))


def carrier_daily_strike_excess_rate(trials):
    """Tỉ lệ trial ghi vượt quá 2 lỗi/hãng/ngày (before) hoặc bị cổng chặn vượt trần lỗi/ngày (after)."""
    daily_counts: dict[tuple, int] = {}
    hits = 0
    for t in trials:
        if any(
            e.get("type") == "guard" and e.get("kind") == "carrier_daily_strike_cap_blocked"
            for e in t.get("events", [])
        ):
            hits += 1
            continue
        for f in t.get("faults") or []:
            key = (t.get("day"), t.get("seed"), f.get("carrier_id"))
            daily_counts[key] = daily_counts.get(key, 0) + 1
            if daily_counts[key] > 2:
                hits += 1
    return hits / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "wrong_parcel_fault_or_reassigned_rate": wrong_parcel_fault_or_reassigned_rate,
    "ambiguous_multi_parcel_rate": ambiguous_multi_parcel_rate,
    "carrier_daily_strike_excess_rate": carrier_daily_strike_excess_rate,
}
STARTER_MONITORS = ("escalation_rate",)
