#!/usr/bin/env python3
"""
YouTube Downloader GUI
A simple GUI wrapper for yt-dlp (youtube-dl) using tkinter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import sys
import json
from pathlib import Path
from config import Config

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader GUI")
        
        #Apply dark theme
        self.setup_dark_theme()
        
        #Load configuration
        self.config = Config()
        
        #Set window geometry from config
        geometry = self.config.get("window_geometry", "800x600")
        self.root.geometry(geometry)
        self.root.resizable(True, True)
        
        #Variables
        self.download_path = tk.StringVar(value=self.config.get("download_path"))
        self.url_var = tk.StringVar(value=self.config.get("last_url", ""))
        self.format_var = tk.StringVar(value=self.config.get("default_format"))
        self.audio_only_var = tk.BooleanVar(value=self.config.get("audio_only"))
        self.audio_format_var = tk.StringVar(value=self.config.get("audio_format", "best"))
        self.is_downloading = False
        
        self.setup_ui()
        
        #Bind window close event to save config
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        #Bind window state events to close dropdowns (more selective)
        self.root.bind('<Unmap>', self.close_dropdowns)  #Handles minimize only
        
    def setup_dark_theme(self):
        """Setup dark theme with purple/magenta accents"""
        #Configure the root window
        self.root.configure(bg='#1e1e1e')
        
        #Create custom style
        style = ttk.Style()
        
        #Configure dark theme colors
        colors = {
            'bg': '#1e1e1e',           #Dark background
            'fg': '#ffffff',           #White text
            'select_bg': '#7c3aed',    #Softer purple selection
            'select_fg': '#ffffff',    #White text on selection
            'entry_bg': '#2d2d2d',     #Darker entry background
            'button_bg': '#9d4edd',    #Purple buttons
            'button_hover': '#c77dff', #Lighter purple on hover
            'frame_bg': '#252525',     #Frame background
            'accent': '#e0aaff'        #Light purple accent
        }
        
        #Configure ttk styles
        style.theme_use('clam')
        
        #Frame style
        style.configure('Custom.TFrame',
                       background=colors['bg'],
                       borderwidth=0,
                       relief='flat')
        
        #Label style
        style.configure('Custom.TLabel',
                       background=colors['bg'],
                       foreground=colors['fg'],
                       font=('Segoe UI', 9),
                       relief='flat',
                       borderwidth=0)
        
        #Bold Label style for headings
        style.configure('Heading.TLabel',
                       background=colors['bg'],
                       foreground=colors['fg'],
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat',
                       borderwidth=0)
        
        #Entry style
        style.configure('Custom.TEntry',
                       foreground=colors['fg'],
                       fieldbackground=colors['entry_bg'],
                       borderwidth=1,
                       insertcolor=colors['fg'],
                       relief='flat',
                       selectbackground=colors['select_bg'],
                       selectforeground=colors['select_fg'])
        
        #Button style
        style.configure('Custom.TButton',
                       background=colors['button_bg'],
                       foreground=colors['fg'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 9, 'bold'),
                       padding=(15, 8),
                       relief='flat')
        
        style.map('Custom.TButton',
                 background=[('active', colors['button_hover']),
                           ('pressed', colors['select_bg'])])
        
        #Combobox style
        style.configure('Custom.TCombobox',
                       foreground=colors['fg'],
                       fieldbackground=colors['entry_bg'],
                       background=colors['entry_bg'],
                       arrowcolor=colors['accent'],
                       borderwidth=1,
                       relief='flat',
                       selectbackground=colors['select_bg'],
                       selectforeground=colors['select_fg'])
        
        #Fix combobox dropdown and listbox
        style.map('Custom.TCombobox',
                 fieldbackground=[('readonly', colors['entry_bg'])],
                 background=[('readonly', colors['entry_bg'])],
                 foreground=[('readonly', colors['fg'])],
                 arrowcolor=[('readonly', colors['accent'])])
        
        #Configure the dropdown listbox (this fixes the white dropdown)
        self.root.option_add('*TCombobox*Listbox.background', colors['entry_bg'])
        self.root.option_add('*TCombobox*Listbox.foreground', colors['fg'])
        self.root.option_add('*TCombobox*Listbox.selectBackground', colors['select_bg'])
        self.root.option_add('*TCombobox*Listbox.selectForeground', colors['select_fg'])
        
        #Checkbutton style
        style.configure('Custom.TCheckbutton',
                       background=colors['bg'],
                       foreground=colors['fg'],
                       focuscolor='none',
                       font=('Segoe UI', 10),
                       relief='flat',
                       borderwidth=0)
        
        #Fix checkbutton hover colors
        style.map('Custom.TCheckbutton',
                 background=[('active', colors['bg']),
                           ('selected', colors['bg'])],
                 foreground=[('active', colors['fg']),
                           ('selected', colors['fg'])])
        
        #Progressbar style
        style.configure('Custom.Horizontal.TProgressbar',
                       background=colors['button_bg'],
                       troughcolor=colors['entry_bg'],
                       borderwidth=0,
                       lightcolor=colors['button_bg'],
                       darkcolor=colors['button_bg'])
        
        #LabelFrame style
        style.configure('Custom.TLabelframe',
                       background=colors['bg'],
                       foreground=colors['accent'],
                       borderwidth=1,
                       relief='flat',
                       font=('Segoe UI', 9, 'bold'))
        
        style.configure('Custom.TLabelframe.Label',
                       background=colors['bg'],
                       foreground=colors['accent'],
                       font=('Segoe UI', 9, 'bold'))
        
    def setup_ui(self):
        """Setup the user interface"""
        #Create main frame with custom style
        main_frame = ttk.Frame(self.root, padding="15", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        #Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        #URL input section with styling
        ttk.Label(main_frame, text="🎬 Video URL:", style='Heading.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        url_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        url_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        url_frame.columnconfigure(0, weight=1)
        
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, 
                                  font=("Segoe UI", 10), style='Custom.TEntry')
        self.url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(url_frame, text="Paste", command=self.paste_url, 
                  style='Custom.TButton').grid(row=0, column=1, padx=(10, 0))
        
        #Download options frame with custom styling
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ Download Options", 
                                     padding="15", style='Custom.TLabelframe')
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        options_frame.columnconfigure(1, weight=1)
        
        #Download path with icons (bigger icons)
        ttk.Label(options_frame, text="📁 Download Path:", style='Custom.TLabel', font=('Segoe UI', 11)).grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        path_frame = ttk.Frame(options_frame, style='Custom.TFrame')
        path_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        path_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(path_frame, textvariable=self.download_path, state="readonly", 
                 style='Custom.TEntry').grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(path_frame, text="Browse", command=self.browse_download_path, 
                  style='Custom.TButton').grid(row=0, column=1, padx=(10, 0))
        
        #Format selection with styling (bigger icons)
        ttk.Label(options_frame, text="🎯 Quality:", style='Custom.TLabel', font=('Segoe UI', 11)).grid(row=2, column=0, sticky=tk.W, pady=(8, 8))
        format_combo = ttk.Combobox(options_frame, textvariable=self.format_var, 
                                   style='Custom.TCombobox', state='readonly', values=[
            "best", "worst", "720p", "480p", "360p", "240p", "144p"
        ])
        format_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(8, 8))
        
        #Store reference to format combo for dropdown management
        self.format_combo = format_combo
        
        #Checkboxes with icons and custom styling (bigger icons)
        ttk.Checkbutton(options_frame, text="🎵 Audio only", variable=self.audio_only_var, 
                       style='Custom.TCheckbutton').grid(row=3, column=0, sticky=tk.W, pady=(15, 0))
        
        #Audio format selection with custom styling
        self.audio_format_label = ttk.Label(options_frame, text="🎶 Audio Format:", style='Custom.TLabel', font=('Segoe UI', 11))
        self.audio_format_var = tk.StringVar(value=self.config.get("audio_format", "best"))
        self.audio_format_combo = ttk.Combobox(options_frame, textvariable=self.audio_format_var, 
                                             style='Custom.TCombobox', state='readonly', values=[
            "best", "m4a", "webm", "mp3"
        ])
        
        #Store reference to audio format combo for dropdown management
        self.audio_format_combo_ref = self.audio_format_combo
        
        #Bind audio only checkbox to show/hide audio format options
        self.audio_only_var.trace('w', self.toggle_audio_format)
        
        #Buttons frame with custom styling
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=3, column=0, columnspan=3, pady=(15, 15))
        
        self.download_btn = ttk.Button(button_frame, text="Download", command=self.start_download, 
                                      style='Custom.TButton')
        self.download_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.info_btn = ttk.Button(button_frame, text="Get Info", command=self.get_video_info, 
                                  style='Custom.TButton')
        self.info_btn.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log, 
                  style='Custom.TButton').grid(row=0, column=2, padx=(0, 10))
        
        #FFmpeg install button
        ttk.Button(button_frame, text="Install FFmpeg", command=self.install_ffmpeg, 
                  style='Custom.TButton').grid(row=0, column=3)
        
        #Progress section with custom styling
        self.progress_var = tk.StringVar(value="Ready ✅")
        ttk.Label(main_frame, textvariable=self.progress_var, style='Heading.TLabel').grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(0, 8))
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate', 
                                          style='Custom.Horizontal.TProgressbar')
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(8, 15))
        
        #Log output with custom styling
        ttk.Label(main_frame, text="📄 Output Log:", style='Heading.TLabel').grid(row=6, column=0, sticky=tk.W, pady=(0, 8))
        
        #Create a frame for the log text with custom styling
        log_frame = tk.Frame(main_frame, bg='#1e1e1e')
        log_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(8, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80,
                                                 bg='#2d2d2d', fg='#ffffff',
                                                 insertbackground='#ffffff',
                                                 selectbackground='#7c3aed',
                                                 selectforeground='#ffffff',
                                                 font=('Consolas', 9),
                                                 borderwidth=0,
                                                 highlightthickness=0)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        #Configure grid weights for resizing
        main_frame.rowconfigure(7, weight=1)
        
        #Initially hide audio format options
        self.toggle_audio_format()
        
    def toggle_audio_format(self, *args):
        """Show/hide audio format options based on audio only checkbox"""
        if self.audio_only_var.get():
            self.audio_format_label.grid(row=4, column=0, sticky=tk.W, pady=(8, 8))
            self.audio_format_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(8, 8))
        else:
            self.audio_format_label.grid_remove()
            self.audio_format_combo.grid_remove()
    
    def close_dropdowns(self, event=None):
        """Close any open dropdown menus"""
        try:
            #Only close dropdowns when window is minimized/unmapped
            if event and event.type == '18':  #UnmapNotify event
                #Try to close format combo dropdown
                if hasattr(self, 'format_combo'):
                    self.format_combo.event_generate('<Escape>')
                
                #Try to close audio format combo dropdown  
                if hasattr(self, 'audio_format_combo_ref'):
                    self.audio_format_combo_ref.event_generate('<Escape>')
        except Exception:
            #Ignore any errors when trying to close dropdowns
            pass
        
    def paste_url(self):
        """Paste URL from clipboard"""
        try:
            clipboard_content = self.root.clipboard_get()
            self.url_var.set(clipboard_content)
        except tk.TclError:
            messagebox.showwarning("Warning", "No valid content in clipboard")
    
    def browse_download_path(self):
        """Browse for download directory"""
        folder = filedialog.askdirectory(initialdir=self.download_path.get())
        if folder:
            self.download_path.set(folder)
    
    def log_message(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log text"""
        self.log_text.delete(1.0, tk.END)
    
    def check_ffmpeg(self):
        """Check if FFmpeg is installed"""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                          capture_output=True, text=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def get_downloader_command(self):
        """Get the appropriate downloader command (yt-dlp or youtube-dl)"""
        try:
            subprocess.run(['yt-dlp', '--version'], 
                          capture_output=True, text=True, check=True)
            return 'yt-dlp'
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                subprocess.run(['youtube-dl', '--version'], 
                              capture_output=True, text=True, check=True)
                return 'youtube-dl'
            except (subprocess.CalledProcessError, FileNotFoundError):
                return None
    
    def check_dependencies(self):
        """Check if yt-dlp is installed"""
        downloader = self.get_downloader_command()
        if downloader:
            try:
                result = subprocess.run([downloader, '--version'], 
                                      capture_output=True, text=True, check=True)
                return True, f"{downloader} {result.stdout.strip()}"
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False, None
        return False, None
    
    def get_video_info(self):
        """Get video information without downloading"""
        if not self.url_var.get().strip():
            messagebox.showwarning("Warning", "Please enter a video URL")
            return
        
        def info_thread():
            try:
                self.progress_var.set("Getting video info... 🔍")
                self.progress_bar.start()
                
                #Check which downloader is available
                downloader = self.get_downloader_command()
                if not downloader:
                    self.log_message("Error: yt-dlp or youtube-dl not found. Please install one of them.")
                    return
                
                #Use the available downloader
                cmd = [downloader, '--dump-json', self.url_var.get().strip()]
                
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                
                #Parse JSON output
                info = json.loads(result.stdout)
                
                #Display relevant information
                self.log_message(f"Title: {info.get('title', 'N/A')}")
                self.log_message(f"Uploader: {info.get('uploader', 'N/A')}")
                self.log_message(f"Duration: {info.get('duration_string', 'N/A')}")
                self.log_message(f"View Count: {info.get('view_count', 'N/A')}")
                self.log_message(f"Upload Date: {info.get('upload_date', 'N/A')}")
                self.log_message("-" * 50)
                
            except subprocess.CalledProcessError as e:
                self.log_message(f"Error getting video info: {e.stderr}")
            except json.JSONDecodeError:
                self.log_message("Error parsing video information")
            except Exception as e:
                self.log_message(f"Unexpected error: {str(e)}")
            finally:
                self.progress_bar.stop()
                self.progress_var.set("Ready ✅")
        
        threading.Thread(target=info_thread, daemon=True).start()
    
    def start_download(self):
        """Start the download process"""
        if self.is_downloading:
            messagebox.showinfo("Info", "Download already in progress")
            return
        
        if not self.url_var.get().strip():
            messagebox.showwarning("Warning", "Please enter a video URL")
            return
        
        #Check dependencies
        downloader = self.get_downloader_command()
        if not downloader:
            response = messagebox.askyesno(
                "Missing Dependencies", 
                "yt-dlp or youtube-dl not found. Would you like to install yt-dlp?"
            )
            if response:
                self.install_dependencies()
            return
        
        self.is_downloading = True
        self.download_btn.config(state="disabled")
        
        def download_thread():
            try:
                self.progress_var.set("Downloading... ⬇️")
                self.progress_bar.start()
                
                #Build command using the available downloader
                downloader = self.get_downloader_command()
                if not downloader:
                    self.log_message("Error: No downloader available!")
                    return
                    
                cmd = [downloader]
                
                #Add options
                if self.audio_only_var.get():
                    audio_format = self.audio_format_var.get()
                    
                    if audio_format == "mp3":
                        if self.check_ffmpeg():
                            #FFmpeg available, force MP3 conversion
                            #Use a format that guarantees conversion will happen
                            cmd.extend(['--format', 'best[acodec!=mp3]/bestaudio'])
                            cmd.extend(['-x', '--audio-format', 'mp3', '--audio-quality', '0'])
                            self.log_message("FFmpeg detected. Will force conversion to MP3.")
                        else:
                            #No FFmpeg, try to get MP3 directly or fallback to M4A
                            self.log_message("FFmpeg not found. Trying to download MP3 directly or will fallback to M4A...")
                            cmd.extend(['--format', 'bestaudio[ext=mp3]/bestaudio[ext=m4a]/bestaudio'])
                            cmd.extend(['--extract-audio'])
                    elif audio_format == "best":
                        cmd.extend(['--format', 'bestaudio'])
                    elif audio_format in ["m4a", "webm"]:
                        cmd.extend(['--format', f'bestaudio[ext={audio_format}]/bestaudio'])
                    else:
                        cmd.extend(['--format', 'bestaudio'])
                else:
                    if self.format_var.get() != "best":
                        if self.format_var.get() == "worst":
                            cmd.append('--format=worst')
                        else:
                            #Extract resolution number (e.g., "720p" -> "720")
                            resolution = self.format_var.get().replace('p', '')
                            cmd.append(f'--format=best[height<={resolution}]')
                
                #Always use no-playlist to download single videos only
                cmd.append('--no-playlist')
                
                #Set output directory
                cmd.extend(['-o', os.path.join(self.download_path.get(), '%(title)s.%(ext)s')])
                
                #Add URL
                cmd.append(self.url_var.get().strip())
                
                self.log_message(f"Executing: {' '.join(cmd)}")
                
                #Run download
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                         text=True, universal_newlines=True)
                
                #Read output in real-time
                for line in process.stdout:
                    self.log_message(line.strip())
                
                process.wait()
                
                if process.returncode == 0:
                    self.log_message("✅ Download completed successfully!")
                    messagebox.showinfo("Success", "✅ Download completed!")
                else:
                    self.log_message("❌ Download failed!")
                    
            except Exception as e:
                self.log_message(f"Error: {str(e)}")
                messagebox.showerror("Error", f"Download failed: {str(e)}")
            finally:
                self.is_downloading = False
                self.download_btn.config(state="normal")
                self.progress_bar.stop()
                self.progress_var.set("Ready ✅")
        
        threading.Thread(target=download_thread, daemon=True).start()
    
    def install_ffmpeg(self):
        """Install FFmpeg using winget (Windows Package Manager)"""
        def install_thread():
            try:
                self.progress_var.set("Installing FFmpeg... 🔧")
                self.progress_bar.start()
                self.log_message("🔧 Installing FFmpeg via winget...")
                
                #Try to install FFmpeg using winget
                result = subprocess.run(['winget', 'install', 'FFmpeg'], 
                                      capture_output=True, text=True, check=True)
                
                self.log_message("✅ FFmpeg installed successfully!")
                self.log_message("Note: You may need to restart the application for FFmpeg to be detected.")
                messagebox.showinfo("Success", "✅ FFmpeg installed successfully!\n\nYou may need to restart the application for FFmpeg to be detected.")
                
            except subprocess.CalledProcessError as e:
                error_msg = f"Installation failed. You may need to install FFmpeg manually.\n\nError: {e.stderr if e.stderr else 'Unknown error'}"
                self.log_message(f"FFmpeg installation failed: {error_msg}")
                
                #Provide manual installation instructions
                manual_msg = """FFmpeg installation failed. Please install manually:

1. Visit https://ffmpeg.org/download.html
2. Download FFmpeg for Windows
3. Extract and add to your system PATH

Or try installing winget first:
- Go to Microsoft Store and install "App Installer"
- Then try the FFmpeg install button again"""
                
                messagebox.showinfo("Manual Installation Required", manual_msg)
                
            except FileNotFoundError:
                #winget not found
                manual_msg = """Windows Package Manager (winget) not found.

To install FFmpeg manually:
1. Visit https://ffmpeg.org/download.html
2. Download FFmpeg for Windows
3. Extract and add to your system PATH

Or install winget first:
- Go to Microsoft Store and install "App Installer" """
                
                self.log_message("winget not found. Manual FFmpeg installation required.")
                messagebox.showinfo("Manual Installation Required", manual_msg)
                
            finally:
                self.progress_bar.stop()
                self.progress_var.set("Ready ✅")
        
        threading.Thread(target=install_thread, daemon=True).start()
    
    def install_dependencies(self):
        """Install yt-dlp using pip"""
        def install_thread():
            try:
                self.progress_var.set("Installing yt-dlp... 📦")
                self.progress_bar.start()
                self.log_message("📦 Installing yt-dlp...")
                
                result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'yt-dlp'], 
                                      capture_output=True, text=True, check=True)
                
                self.log_message("✅ yt-dlp installed successfully!")
                messagebox.showinfo("Success", "✅ yt-dlp installed successfully!")
                
            except subprocess.CalledProcessError as e:
                self.log_message(f"Installation failed: {e.stderr}")
                messagebox.showerror("Error", f"Installation failed: {e.stderr}")
            finally:
                self.progress_bar.stop()
                self.progress_var.set("Ready ✅")
        
        threading.Thread(target=install_thread, daemon=True).start()
    
    def on_closing(self):
        """Handle window closing - save configuration"""
        #Save current settings
        self.config.update(
            download_path=self.download_path.get(),
            default_format=self.format_var.get(),
            audio_only=self.audio_only_var.get(),
            audio_format=self.audio_format_var.get(),
            window_geometry=self.root.geometry(),
            last_url=self.url_var.get()
        )
        self.config.save_config()
        self.root.destroy()

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    
    #Set minimum window size
    root.minsize(600, 400)
    
    #Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
