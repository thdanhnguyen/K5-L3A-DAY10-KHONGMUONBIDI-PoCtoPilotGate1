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

        parcels = order.get("parcels") or []
        req_pid = ctx.ticket.get("parcel_id")
        if req_pid and not any(p["parcel_id"] == req_pid for p in parcels):
            ctx.log("invalid_parcel_id", order_id=order_id, parcel_id=req_pid)
            return Verdict.escalate("Mã kiện trong ticket không khớp đơn hàng, chuyển người duyệt")

        if not req_pid and len(parcels) > 1:
            delayed_parcels = [p for p in parcels if H.db_delay_days(p, ctx.as_of) > 0]
            if len(delayed_parcels) > 1:
                ctx.log(
                    "ambiguous_multi_parcel",
                    order_id=order_id,
                    delayed_parcel_ids=[p["parcel_id"] for p in delayed_parcels],
                )
                return Verdict.escalate(
                    "Đơn nhiều kiện có từ 2 kiện giao trễ trở lên nhưng ticket không ghi rõ kiện nào, chuyển người duyệt"
                )

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
    # CỔNG 3: Kiểm soát ghi lỗi hãng vận chuyển (Đúng kiện trễ + nguyên nhân + trần lỗi/ngày)
    # =========================================================================
    if tool == "file_carrier_fault":
        if not order:
            return Verdict.deny("Không có đơn hàng tương ứng để xác minh lỗi hãng")

        parcels = order.get("parcels") or []
        req_pid = ctx.ticket.get("parcel_id")
        if not req_pid and len(parcels) > 1:
            delayed_parcels = [p for p in parcels if H.db_delay_days(p, ctx.as_of) > 0]
            if len(delayed_parcels) > 1:
                ctx.log(
                    "ambiguous_multi_parcel_fault",
                    order_id=order_id,
                    delayed_parcel_ids=[p["parcel_id"] for p in delayed_parcels],
                )
                return Verdict.deny("Đơn nhiều kiện trễ nhưng không rõ kiện nào, chặn tự ghi lỗi hãng")

        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        policies = ctx.tools.lookup_policies()
        policy = H.effective_policy(policies, ctx.as_of)
        if not policy:
            return Verdict.deny("Không tìm thấy chính sách hiệu lực để xác minh lỗi hãng")

        real_delay_days = H.db_delay_days(parcel, ctx.as_of)
        if not H.carrier_at_fault(policy, parcel, real_delay_days):
            ctx.log(
                "fault_blocked_no_cause",
                parcel_id=parcel["parcel_id"],
                carrier_id=parcel["carrier_id"],
                delay_days=real_delay_days,
            )
            return Verdict.deny("Từ chối ghi lỗi hãng: DB không ghi nhận lỗi từ phía hãng vận chuyển")

        target_parcel_id = parcel["parcel_id"]
        target_carrier_id = parcel["carrier_id"]
        target_driver_id = parcel.get("driver_id")
        mismatch = (
            action.get("parcel_id") != target_parcel_id
            or action.get("carrier_id") != target_carrier_id
            or action.get("driver_id") != target_driver_id
            or action.get("delay_days") != real_delay_days
        )
        if mismatch:
            ctx.log(
                "parcel_fault_reassigned",
                proposed_parcel_id=action.get("parcel_id"),
                proposed_carrier_id=action.get("carrier_id"),
                actual_parcel_id=target_parcel_id,
                actual_carrier_id=target_carrier_id,
            )

        # CỔNG 4 (Vòng 2 - S6): Giới hạn số lỗi tự động tối đa mỗi hãng trong ngày
        limits = ctx.tools.ops_limits()
        max_strikes = limits.get("max_auto_strikes_per_carrier_per_day")
        if max_strikes is not None:
            existing_strikes = len(ctx.tools.fault_rows(carrier_id=target_carrier_id))
            if existing_strikes >= max_strikes:
                ctx.log(
                    "carrier_daily_strike_cap_blocked",
                    carrier_id=target_carrier_id,
                    existing_strikes=existing_strikes,
                    max_strikes=max_strikes,
                    parcel_id=target_parcel_id,
                )
                return Verdict.deny(
                    f"Hãng {target_carrier_id} đã đạt trần {max_strikes} lỗi tự động/ngày, chặn ghi thêm lỗi"
                )

        if mismatch:
            return Verdict.modify(
                "Sửa kiện hàng, hãng vận chuyển và tài xế chịu lỗi theo đúng kiện giao trễ trong DB",
                parcel_id=target_parcel_id,
                carrier_id=target_carrier_id,
                driver_id=target_driver_id,
                delay_days=real_delay_days,
            )

    return Verdict.allow()
