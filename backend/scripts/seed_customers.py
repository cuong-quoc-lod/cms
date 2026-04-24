"""
Seed script: Add test customers to CMS via REST API.

Usage:
    python scripts/seed_customers.py [--url http://localhost:8000]

Options:
    --url    Base URL of the server (default: http://localhost:8000)
"""

import sys
import io

# Force UTF-8 output on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import argparse
import json
import urllib.request
import urllib.error
from datetime import datetime

# ── Dữ liệu khách hàng mẫu ────────────────────────────────────────────────────

SAMPLE_CUSTOMERS = [
    {
        "name": "Nguyễn Văn An",
        "email": "nguyen.van.an@example.com",
        "phone": "+84901234001",
        "address": "123 Nguyễn Huệ, Quận 1, TP.HCM",
        "note": "Khách hàng VIP, ưu tiên hỗ trợ 24/7",
    },
    {
        "name": "Trần Thị Bích",
        "email": "tran.thi.bich@example.com",
        "phone": "+84901234002",
        "address": "45 Lê Lợi, Quận Hải Châu, Đà Nẵng",
        "note": "Khách hàng doanh nghiệp",
    },
    {
        "name": "Lê Quốc Cường",
        "email": "le.quoc.cuong@example.com",
        "phone": "+84901234003",
        "address": "78 Trần Phú, TP. Huế",
        "note": "",
    },
    {
        "name": "Phạm Minh Dũng",
        "email": "pham.minh.dung@example.com",
        "phone": "+84901234004",
        "address": "12 Hoàng Diệu, Quận Hà Đông, Hà Nội",
        "note": "Liên hệ qua Zalo",
    },
    {
        "name": "Hoàng Thị Ế",
        "email": "hoang.thi.e@example.com",
        "phone": "+84901234005",
        "address": "99 Lý Tự Trọng, Quận Ninh Kiều, Cần Thơ",
        "note": "Khách hàng mới, cần tư vấn sản phẩm",
    },
    {
        "name": "Vũ Thành Phong",
        "email": "vu.thanh.phong@example.com",
        "phone": "+84901234006",
        "address": "5 Bạch Đằng, Quận Hải An, Hải Phòng",
        "note": "",
    },
    {
        "name": "Đặng Ngọc Giang",
        "email": "dang.ngoc.giang@example.com",
        "phone": "+84901234007",
        "address": "33 Điện Biên Phủ, Quận Bình Thạnh, TP.HCM",
        "note": "Ưu tiên giao hàng buổi sáng",
    },
    {
        "name": "Bùi Văn Hải",
        "email": "bui.van.hai@example.com",
        "phone": "+84901234008",
        "address": "17 Hùng Vương, TP. Pleiku, Gia Lai",
        "note": "Khách hàng khu vực Tây Nguyên",
    },
    {
        "name": "Ngô Thị Bảo Như",
        "email": "ngo.thi.bao.nhu@example.com",
        "phone": "+84901234009",
        "address": "88 Trường Chinh, Quận Thanh Xuân, Hà Nội",
        "note": "Đã mua hàng 3 lần",
    },
    {
        "name": "Đinh Trọng Khải",
        "email": "dinh.trong.khai@example.com",
        "phone": "+84901234010",
        "address": "21 Ngô Quyền, Quận Sơn Trà, Đà Nẵng",
        "note": "Thanh toán qua chuyển khoản",
    },
]

# ── HTTP helpers (không cần thư viện ngoài) ────────────────────────────────────

def _request(method: str, url: str, body: dict | None = None) -> tuple[int, dict]:
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body else None
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = {}
        try:
            body = json.loads(e.read().decode("utf-8"))
        except Exception:
            pass
        return e.code, body


def check_server(base_url: str) -> bool:
    status, data = _request("GET", f"{base_url}/api/health")
    if status == 200:
        print(f"[Health] Server: {data.get('server')} | DB: {data.get('database')}")
        return True
    print(f"[Error] Server không phản hồi (status {status})")
    return False


# ── Seed logic ────────────────────────────────────────────────────────────────

def seed(base_url: str) -> None:
    endpoint = f"{base_url}/api/customer"
    success, skipped, failed = 0, 0, 0

    print(f"\nSeeding {len(SAMPLE_CUSTOMERS)} customers...\n")

    for i, customer in enumerate(SAMPLE_CUSTOMERS, 1):
        status, resp = _request("POST", endpoint, customer)

        if status == 201:
            print(f"  [{i:02d}] [OK]   {customer['name']} | id: {resp.get('id')}")
            success += 1
        elif status == 409:
            detail = resp.get("detail", "duplicate")
            print(f"  [{i:02d}] [SKIP] {customer['name']} | {detail}")
            skipped += 1
        else:
            detail = resp.get("detail", resp)
            print(f"  [{i:02d}] [FAIL] {customer['name']} | {status}: {detail}")
            failed += 1

    print(f"\n{'─'*50}")
    print(f"  Success  : {success}")
    print(f"  Skipped  : {skipped}")
    print(f"  Failed   : {failed}")
    print(f"  Total    : {len(SAMPLE_CUSTOMERS)}")
    print(f"{'─'*50}\n")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Seed test customers into CMS API")
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL of the CMS server (default: http://localhost:8000)",
    )
    args = parser.parse_args()

    base_url = args.url.rstrip("/")
    print(f"Target: {base_url}")

    if not check_server(base_url):
        sys.exit(1)

    seed(base_url)


if __name__ == "__main__":
    main()
