import math
import rbWindow.editWindow as ew
from rbWindow.ExtensionSetting.extensionValue import *
from jsonConverter.makeJsonFile import *
from testCode.initialization import *
from parseSyllable.configVersionFinal import *
from fontParts.world import CurrentFont, OpenFont
from mojo.UI import *


testPath, testFile = launchFontTool()
if testPath is None:
	quit()


print("testPath(launchFontTool) = ",testPath)
configPreset = ConfigExtensionSetting(DefaultKey)
configPreset.checkLangauge()
configPreset.registerSettings()

groupDict = None
# launchFontTool() 리턴 값과 같다면 지워도 무방할듯...? 일단 안지움
testFile = OpenFont(testPath, showInterface = False)

FileNameList = StartProgram(testPath,testFile,CurrentFont())

setExtensionDefault(DefaultKey + ".font", CurrentFont())
setExtensionDefault(DefaultKey + ".jsonFileName1", FileNameList[0])
setExtensionDefault(DefaultKey + ".jsonFileName2", FileNameList[1])
setExtensionDefault(DefaultKey + ".testPath", testPath)
KoreanCheck = getExtensionDefault(DefaultKey+".korean")

	
menuWindow = ew.EditGroupMenu(groupDict,FileNameList[0],FileNameList[1])
fontWindowObserver()