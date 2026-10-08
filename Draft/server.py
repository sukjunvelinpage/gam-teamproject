"""
Lightweight Local Web Server for Trump Tweet Impact Classifier
--------------------------------------------------------------
Features:
- Serves Draft/ directory on http://localhost:8000
- Automatically opens default browser
- Provides /save_csv POST endpoint to save trade_tweets_manual_audited.csv directly to disk
"""

import http.server
import socketserver
import os
import webbrowser
import json

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/save_csv':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            output_path = os.path.join(DIRECTORY, 'trade_tweets_manual_audited.csv')
            with open(output_path, 'w', encoding='utf-8-sig') as f:
                f.write(post_data)
                
            print(f"[Server] Saved updated results directly to: {output_path}")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok', 'saved_path': output_path}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print("=" * 70)
        print("🚀 [Trump Tweet Classifier] 로컬 웹서버가 구동되었습니다!")
        print(f"👉 접속 주소: {url}")
        print("   (브라우저가 자동으로 열리지 않으면 위 주소를 복사하여 접속하세요)")
        print("   서버 종료: Ctrl + C")
        print("=" * 70)
        try:
            webbrowser.open(url)
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[Server] 서버를 종료합니다.")
