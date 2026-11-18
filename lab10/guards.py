"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    order_id = action.get("order_id")
    order = ctx.tools.lookup_order(order_id) if order_id else None

    # =========================================================================
    # CỔNG 1: Đối chiếu DB trước khi hoàn tiền (Chặn nghe lời khách khai khống)
    # =========================================================================
    if tool == "issue_refund":
        if not order:
            return Verdict.escalate("Không tìm thấy thông tin đơn hàng trong hệ thống")

        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        policies = ctx.tools.lookup_policies()
        policy = H.effective_policy(policies, ctx.as_of)

        if not policy:
            return Verdict.escalate("Không tìm thấy chính sách hoàn tiền tương ứng")

        # Quyền lợi thực tế tính từ tracking DB
        real_delay_days = H.db_delay_days(parcel, ctx.as_of)
        entitled_vnd = H.entitlement_vnd(policy, order, real_delay_days, parcel.get("delay_cause"))

        req_amount = action.get("amount_vnd", 0)
        if req_amount > entitled_vnd:
            if entitled_vnd == 0:
                # Không đủ điều kiện hoàn -> Từ chối thẳng lệnh ghi hoàn tiền
                return Verdict.deny("Đơn hàng không đủ điều kiện hoàn tiền theo ghi nhận thực tế từ DB")
            else:
                # Điều chỉnh số tiền về đúng quyền lợi theo DB
                return Verdict.modify(
                    "Điều chỉnh số tiền hoàn về đúng quyền lợi ghi nhận trong DB",
                    amount_vnd=entitled_vnd
                )

        # =====================================================================
        # CỔNG 2: Kiểm tra trần hoàn tiền tối đa (Daily cap & Ops limits)
        # =====================================================================
        limits = ctx.tools.ops_limits()
        daily_cap = limits.get("daily_auto_refund_budget_vnd", 2000000)
        spent_today = ctx.tools.auto_refund_today_vnd()

        if spent_today + req_amount > daily_cap:
            return Verdict.escalate("Vượt hạn mức ngân sách hoàn tự động trong ngày, chuyển người duyệt")

        cust_limit = limits.get("max_auto_refund_per_customer_per_day_vnd", 300000)
        if req_amount > cust_limit:
            return Verdict.escalate("Khoản hoàn vượt trần tự động trên mỗi khách, chuyển người duyệt")

    # =========================================================================
    # CỔNG 3: Kiểm soát ghi lỗi hãng vận chuyển (Phải có nguyên nhân hợp lệ trong DB)
    # =========================================================================
    if tool == "file_carrier_fault":
        if not order:
            return Verdict.deny("Không có đơn hàng tương ứng để xác minh lỗi hãng")

        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        policies = ctx.tools.lookup_policies()
        policy = H.effective_policy(policies, ctx.as_of)

        real_delay_days = H.db_delay_days(parcel, ctx.as_of)
        if not H.carrier_at_fault(policy, parcel, real_delay_days):
            return Verdict.deny("Từ chối ghi lỗi hãng: DB không ghi nhận lỗi từ phía hãng vận chuyển")

    return Verdict.allow()
