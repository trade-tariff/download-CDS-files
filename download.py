from classes.downloader import Downloader
import os 

# === TEST MODE HANDLING ===
TEST_MODE = os.getenv('GITHUB_ACTIONS') and os.getenv('TEST_RETRIES') == 'true'

if TEST_MODE:
    # SAFE TEST BLOCK (won't touch real functionality)
    print("🔧 TEST MODE ACTIVE - Validating retry mechanism")
    
    attempt_file = 'retry_attempt.txt'
    max_attempts = 2  # Match your workflow's test setting
    
    if not os.path.exists(attempt_file):
        # First attempt - fail
        with open(attempt_file, 'w') as f:
            f.write('1')
        raise RuntimeError("🛑 Simulated failure (attempt 1/3)")
    
    with open(attempt_file, 'r+') as f:
        attempts = int(f.read())
        if attempts < max_attempts:
            # Subsequent failing attempts
            f.seek(0)
            f.write(str(attempts + 1))
            raise RuntimeError(f"🛑 Simulated failure (attempt {attempts + 1}/3)")
    
    # Final success
    os.remove(attempt_file)
    print("✅ Retry test completed successfully")
    exit(0)  # Explicit clean exit

# === NORMAL OPERATION (protected by test check) ===
print("🚀 Starting normal download operation")
d = Downloader()
# d.download_files()
