Set WshShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Bu scriptin çalıştığı klasörü bul
strPath = Wscript.ScriptFullName
Set objFile = objFSO.GetFile(strPath)
strFolder = objFSO.GetParentFolderName(objFile)

' pythonw.exe'nin sistemde kurulu olup olmadığını kontrol et
Dim returnCode
returnCode = WshShell.Run("cmd /c where pythonw.exe >nul 2>&1", 0, True)

If returnCode <> 0 Then
    MsgBox "Python bulunamadi!" & vbCrLf & vbCrLf & _
           "Elektrik kesintisi takip sistemi baslatilAmadi." & vbCrLf & _
           "Lutfen Python'u kurun: https://www.python.org/downloads/" & vbCrLf & vbCrLf & _
           "Kurulum sirasinda 'Add Python to PATH' secenegini isaretlemeyi unutmayin.", _
           vbCritical, "Hata - Python Bulunamadi"
    WScript.Quit 1
End If

' Aynı klasördeki takip.py dosyasını Python'un arkaplan penceresiz sürümüyle (pythonw.exe) çalıştırır.
' Sondaki 0 parametresi CMD penceresinin tamamen gizli olmasını sağlar.
WshShell.Run "pythonw.exe """ & strFolder & "\takip.py""", 0
Set WshShell = Nothing
