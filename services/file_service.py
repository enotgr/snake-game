class FileService:
  def getTextFileByPath(self, path: str):
    text = ''
    try:
      file = open(path, 'r', encoding='utf-8')
      text = file.read()
    except:
      print('Error: cannot read text file.')
    return text

  def saveTextFile(self, text: str, path: str):
    try:
      file = open(path, 'w', encoding='utf-8')
      file.write(text)
      file.close()
      return True
    except:
      print('Error: cannot save text file.')
      return False

file_service = FileService()
