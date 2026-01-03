"""
Test username validation for XSS and input sanitization
"""
import requests

BASE_URL = "http://localhost:8000"

test_cases = [
    # (username, score, should_pass, description)
    ("Player123", 50, True, "Valid username with letters and numbers"),
    ("Cool_Player-7", 75, True, "Valid username with underscore and hyphen"),
    ("Test User", 80, True, "Valid username with space"),
    ("<script>alert('xss')</script>", 90, False, "XSS attack with script tag"),
    ("admin' OR '1'='1", 100, False, "SQL injection attempt"),
    ("a" * 50, 60, False, "Username too long (50 chars)"),
    ("", 70, False, "Empty username"),
    ("@#$%^&*()", 80, False, "Special characters not allowed"),
    ("Player<b>123</b>", 85, False, "HTML tags in username"),
    ("User123!", 90, False, "Exclamation mark not allowed"),
    ("正常用户", 95, False, "Non-ASCII characters (Chinese)"),
    ("a", 40, True, "Single character username"),
    ("Player_Test-123", 100, True, "Valid complex username"),
]

print("=" * 80)
print("USERNAME VALIDATION TESTS")
print("=" * 80)

passed = 0
failed = 0

for username, score, should_pass, description in test_cases:
    try:
        response = requests.post(
            f"{BASE_URL}/leaderboard",
            json={"username": username, "score": score},
            timeout=5
        )
        
        if response.status_code == 200:
            # Request succeeded
            if should_pass:
                print(f"✅ PASS: {description}")
                print(f"   Username: '{username}' → Accepted")
                passed += 1
            else:
                print(f"❌ FAIL: {description}")
                print(f"   Username: '{username}' → Should have been rejected!")
                failed += 1
        else:
            # Request failed (validation error)
            if not should_pass:
                error_detail = response.json().get("detail", [{}])
                if isinstance(error_detail, list):
                    error_msg = error_detail[0].get("msg", "Unknown error")
                else:
                    error_msg = error_detail
                print(f"✅ PASS: {description}")
                print(f"   Username: '{username}' → Correctly rejected")
                print(f"   Error: {error_msg}")
                passed += 1
            else:
                print(f"❌ FAIL: {description}")
                print(f"   Username: '{username}' → Should have been accepted!")
                print(f"   Status: {response.status_code}")
                print(f"   Error: {response.json()}")
                failed += 1
                
    except requests.exceptions.RequestException as e:
        print(f"⚠️  ERROR: {description}")
        print(f"   Could not connect to server: {e}")
        failed += 1
    
    print()

print("=" * 80)
print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
print("=" * 80)

if failed == 0:
    print("🎉 All tests passed! Username validation is working correctly.")
else:
    print(f"⚠️  {failed} test(s) failed. Please review the validation logic.")
