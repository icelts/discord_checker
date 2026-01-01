import json, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.utils import load_tokens, load_proxies, save_to_file
import requests

def check_token(token, proxy):
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get("https://discord.com/api/v9/users/@me", headers=headers, proxies=proxies, timeout=10)
        if res.status_code == 403:
            return token, {"status": "banned"}
        if res.status_code != 200:
            return token, None
        user = res.json()
        res2 = requests.get("https://discord.com/api/v9/users/@me/library", headers=headers, proxies=proxies, timeout=10)
        phone_locked = res2.status_code != 200
        return token, {
            "status": "valid",
            "email": user.get("email"),
            "verified": user.get("verified"),
            "phone": user.get("phone"),
            "phone_locked": phone_locked,
            "username": user.get("username"),
            "id": user.get("id")
        }
    except:
        return token, None

def update_progress(done, total, stats):
    with open("result/progress.json", "w", encoding="utf-8") as f:
        json.dump({"done": done, "total": total, "stats": stats}, f, indent=2, ensure_ascii=False)

def process_tokens(token_path, proxy_path):
    tokens = load_tokens(token_path)
    proxy_cycle = load_proxies(proxy_path)
    total = len(tokens)
    os.makedirs("result", exist_ok=True)
    stats = {"valid": 0, "unverified": 0, "no_phone": 0, "verified": 0, "banned": 0, "invalid": 0}
    update_progress(0, total, stats)
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_token, token, next(proxy_cycle)): token for token in tokens}
        for i, future in enumerate(as_completed(futures), 1):
            token = futures[future]
            try:
                token, data = future.result()
                if data is None:
                    stats["invalid"] += 1
                elif data["status"] == "banned":
                    save_to_file("result/banned.txt", token, {})
                    stats["banned"] += 1
                elif not data["verified"]:
                    save_to_file("result/unverified_email.txt", token, data)
                    stats["unverified"] += 1
                elif data["verified"] and not data["phone"]:
                    save_to_file("result/verified_no_phone.txt", token, data)
                    stats["no_phone"] += 1
                elif data["verified"] and data["phone"]:
                    save_to_file("result/verified_and_phone.txt", token, data)
                    stats["verified"] += 1
                stats["valid"] += 1
            except:
                stats["invalid"] += 1
            update_progress(i, total, stats)
    with open("result/stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)