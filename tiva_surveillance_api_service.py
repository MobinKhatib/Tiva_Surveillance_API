import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess
import os

class PythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = "TivaSurveillance"
    _svc_display_name_ = "Tiva Surveillance Service"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogInfoMsg("Tiva Surveillance Service is starting...")
        # Change to your directory
        working_dir = r"E:\University\Semesters\Work\Tiva_Surveillance_API"
        script = os.path.join(working_dir, "server.py")
        python = r"C:\Users\IT-Center\AppData\Local\Programs\Python\Python312"

        # Run the script as a subprocess
        process = subprocess.Popen([python, script], cwd=working_dir)

        # Wait for stop event
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        process.terminate()
