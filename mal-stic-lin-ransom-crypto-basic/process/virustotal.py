#!/usr/bin/env python3
import requests
import sys
import re

def is_valid_sha256(hash_string):
    """Kiểm tra chuỗi có phải là SHA256 hash hợp lệ không"""
    if len(hash_string) != 64:
        return False
    return bool(re.match('^[a-fA-F0-9]{64}$', hash_string))

def scan_hash(hash_value, api_key):
    """Quét file bằng SHA256 hash"""
    if not is_valid_sha256(hash_value):
        print("Lỗi: Hash không đúng định dạng SHA256")
        sys.exit(1)
        
    params = {
        'apikey': api_key,
        'resource': hash_value
    }
    headers = {
        "Accept-Encoding": "gzip, deflate",
    }
    
    print(f"Đang kiểm tra hash: {hash_value}")
    response = requests.get(
        "https://www.virustotal.com/vtapi/v2/file/report",
        params=params,
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get('response_code') == 1:
            return result
        else:
            print("Hash chưa được quét trước đó trên VirusTotal")
            return None
    else:
        print(f"Lỗi khi truy vấn API: {response.status_code}")
        return None

def display_results(results):
    """Hiển thị kết quả quét"""
    if not results:
        return
        
    print("\nKết quả quét:")
    print(f"SHA256: {results.get('sha256', 'N/A')}")
    print(f"Tổng số engine đã quét: {results['total']}")
    print(f"Số lượng phát hiện: {results['positives']}")
    print(f"Ngày quét: {results.get('scan_date', 'N/A')}")
    
    if results['positives'] > 0:
        print("\nChi tiết các phát hiện:")
        for engine, result in results['scans'].items():
            if result['detected']:
                print(f"{engine}: {result['result']}")

def main():
    if len(sys.argv) != 2:
        print("Sử dụng: ./vt_scan.py <sha256_hash> <api_key>")
        sys.exit(1)
        
    file_hash = sys.argv[1]
    api_key = "f661a3ad33a0d0ad041dd9478c29caf39689766b07665051c541e6ea6f3cddb8"
    
    results = scan_hash(file_hash, api_key)
    display_results(results)

if __name__ == "__main__":
    main()