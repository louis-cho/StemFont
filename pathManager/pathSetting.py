import mojo.extensions

toolName = "FontTool"
fontToolBundle = mojo.extensions.ExtensionBundle(toolName)
baseDir = fontToolBundle.resourcesPath() + "/GroupDict/"
saveFilePath = baseDir
ufoPath = "/Users/font/Desktop/groupTest2350.ufo"
ImagePath = fontToolBundle.resourcesPath()+"/"
resourcePath = ImagePath

attrImgList = ["innerFill", "penPair", "dependX", "dependY", "stroke", "rubbish", "select"]

