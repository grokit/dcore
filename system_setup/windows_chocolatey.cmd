@powershell -NoProfile -ExecutionPolicy unrestricted -Command "iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))" && SET PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin

rem # As

choco install git
choco install notepadplusplus.install
choco install 7zip.commandline
choco install python2
choco install python
choco install Wget
choco install curl
choco install autohotkey.portable
choco install hg
choco install putty
choco install winmerge
choco install vim

rem # Bs

choco install Console2
choco install launchy
choco install greenshot
choco install PDFCreator
choco install Cygwin
choco install youtube-dl
choco install foobar2000
choco install gimp
choco install vlc
choco install imagemagick
choco install winscp
choco install PDFXChangeViewer
choco install ffmpeg
choco install ditto
choco install windowsessentials
choco install windirstat

rem # Cs

choco install calibre
choco install Graphviz
choco install ConEmu
choco install wireshark
choco install kdiff3
choco install nmap
choco install InkScape
choco install truecrypt
choco install ilspy
choco install windbg
choco install dependencywalker
choco install blender
choco install procmon
choco install ilmerge
choco install filezilla
choco install skype
choco install meld
choco install fiddler

rem # Ds
rem choco install screenpresso
rem choco install virtualbox
rem choco install audacity
rem choco install expresso
rem choco install ConsoleZ
rem choco install rdcman
