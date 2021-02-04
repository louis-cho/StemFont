# 익스텐션 초기 기본 값 설정 (프로그램 초기 구동 시에 딱 한 번만 수행되고 이후론 수행하지 않음)
from AppKit import NSColor
from mojo.extensions import *
from rbWindow.Controller.CircularQueue import *
from fontParts.world import CurrentFont, OpenFont, AllFonts
from mojo.UI import *
from mojo.events import addObserver


DefaultKey = "com.robofontTool.rbFontGroup"
rewindBufferSize = 50

def launchFontTool():

	currentFont = CurrentFont()
	if currentFont is not None:
		# 전에 열었던 폰트 파일과 같다면 굳이 물어볼 필요가 없다. (getExtensionDefault가 잘 안먹히는 오류가 있긴 함)
		if currentFont == getExtensionDefault(DefaultKey+".font"):
			return getExtensionDefault(DefaultKey+".testPath"), currentFont
		
		testPath = currentFont.path

		if testPath is None:
			Message('폰트 파일 경로를 알 수 없습니다.'
				, informativeText='.ttf의 경우, 폰트 파일 경로를 알 수 없어 ufo 변환을 해야 합니다.\n.ttf를 .ufo로 바꾸려면 [File]-[Save]를 눌러주세요')
			return None, None

	return testPath, currentFont

class fontWindowObserver:

	def __init__(self):
		addObserver(self, 'windowCallback', 'fontDidOpen')

	def windowCallback(self, info):
		fontList = AllFonts()
		if len(fontList) > 1:
			Message("툴 사용 시 폰트 파일은 1개까지 열람할 수 있습니다!")
			
			i = 0
			fontListLen = len(fontList)
			while True:
				if i == fontList:
					break
				fontList[-i].close()

class ConfigExtensionSetting:

	def __init__(self, registerKey):

		bufferStack = CircularQueue(rewindBufferSize)
		setExtensionDefault(DefaultKey+".restoreStack", bufferStack)
		self.registerKey = registerKey
		self.defaults = {
			self.registerKey + ".registered": True,
		    
		    self.registerKey + ".korean": False,
		    self.registerKey + ".font": None,
		    self.registerKey + ".jsonFilePath": None,
		    self.registerKey + ".jsonFileName1": None,
		    self.registerKey + ".jsonFileName2": None,
		    self.registerKey + ".testPath": None,

		    
		    self.registerKey + ".mode": 0,
		    self.registerKey + ".state": False,

		    self.registerKey + ".margin": 20,
		    self.registerKey + ".width": 100,
		    self.registerKey + ".height": 100,
		    self.registerKey + ".k": 500,

		    self.registerKey + ".matrix_margin": 20,
		    self.registerKey + ".matrix_size": 3,
		    self.registerKey + ".raster_margin": 45,
		    self.registerKey + ".topology_margin": 500,
		    
		    self.registerKey + ".groupDict": None,
		    self.registerKey + ".contourNumber": None,
		    self.registerKey + ".smartSet": None,
		    self.registerKey + ".standardContour": None,
		    self.registerKey + ".standardGlyph": None,
		    self.registerKey + ".matrix": None,
		    
		    self.registerKey + ".syllableJudgementController": None,
		    self.registerKey + ".smartSetIndex": None,
		    self.registerKey + ".restoreStack": bufferStack,
		    
		    self.registerKey + ".index": 0,
		    self.registerKey + ".step": 30,
		    self.registerKey + ".color": NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 0, 0, .5)
		}

		self.checkLangauge()
		

	def registerSettings(self):
		"""
			2020/05/06 created by Cho Hyun Woo
			Extension에 대한 기본적인 설정값을 등록한다.
		"""
		registerExtensionDefaults(self.defaults)

		# registerExtensionDefaults가 잘 동작하지 않을 때도 많아서 중요 고정값들은 틀리지 않게 설정
		setExtensionDefault(self.registerKey + ".margin", 20)
		setExtensionDefault(self.registerKey + ".width", 100)
		setExtensionDefault(self.registerKey + ".height", 100)
		setExtensionDefault(self.registerKey + ".k", 500)
		setExtensionDefault(self.registerKey + ".raster_margin", 45)

		setExtensionDefault(self.registerKey + ".matrix_margin", 20)
		setExtensionDefault(self.registerKey + ".matrix_size", 3)
		setExtensionDefault(self.registerKey + ".topology_margin", 500)

	def removeSettings(self):

		"""
			익스텐션 세팅이 제대로 동작하지 않을 때 메인 코드에 한 번 넣고 돌린 후 지우고 다시 설치하여 사용한다.
		"""
		removeExtensionDefault(self.registerKey)

	def checkLangauge(self):
		"""
			현재 띄워져 있는 폰트의 첫번째 glyphOrder를 참고하여 한글 폰트인지 한자 폰트인지 판별한다.
			한자, 한글이 섞여있거나 첫번째 glyphOrder에 해당하는 글자에 이상이 있으면 정확한 판별이 되지 않는다.

			수행 도중 알 수 없는 이유로 에러가 나면 None으로 세팅
		"""
		font = CurrentFont()

		idx = 0
		
		#만약 ufo파일에 글자 수가 10개 미만인 경우 고려 + 첫번째 글리프 오더가 이상한 경우 고려
		for idx in range(min(len(font.glyphOrder),10)):
		    try:
		        int(font.glyphOrder[idx][3:],16)
		        break
		    except ValueError:
		        continue    

		try:
			print(font.glyphOrder[idx][3:])
			if not 0xAC00 <= int(font.glyphOrder[idx][3:], 16) <= 0xD7A3:
				setExtensionDefault(self.registerKey+".korean", False)
			else:
				setExtensionDefault(self.registerKey+".korean", True)
		except Exception as e:
			print("언어(한글, 한자) 판별 중 예외가 발생했습니다.")
			print(e)
			setExtensionDefault(self.registerKey+".korean", None)

class NotRegisteredException(Exception):
    def __init__(self):
        super().__init__('First Started Program, Register Operated...')




