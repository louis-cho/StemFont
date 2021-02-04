# RBFontGroup
Fonts are designed by designers, and robotic fonts are one of the design tools.

It was created to work in Myeongjo Hangul and Chinese characters.

This is a tool that preprocesses fonts to make STEMFONT(various font from a main font).

After analyzing the font using libraries such as Numpy, Pandas, sklearn, mojoui, vanilla and using the Bezier curve concept, contours with the same shape were classified.

After classifying the shape, it was possible to add properties for METAFONT conversion to the constituent points of the font.

## ScreenShots

### 1. ToolBar
![ToolBar](https://user-images.githubusercontent.com/51118441/91861371-b2b32580-eca7-11ea-8e66-5772ec8ca859.PNG)
#### 1. search
You can automatically find contour groups after searching for letters in Unicode.

#### 2,Attribute
For METAFONT production, it allows pre-processing by putting attributes on font points.

#### 3,Except
After grouping, the user can visually check and exclude it from the group.

#### 4, Rewind, Undo
The user can reverse or recover the work progress.

#### 5, Setting
Users can make grouped contours easier to see, or group them by adjusting margin values.

#### 6, Exit
You can exit the tool.

#### 7, Help
You can inquire how to use the tool.

### 2. SearchMenu
<img width="252" alt="Setting" src="https://user-images.githubusercontent.com/51118441/91865228-21927d80-ecac-11ea-892a-af07ace6bfad.png">

### 3. SettingMenu
<img width="252" alt="Setting" src="https://user-images.githubusercontent.com/51118441/91861832-3a009900-eca8-11ea-83d6-75f5e6bd38d6.png">

### 4.Grouping Example 
![group3](https://user-images.githubusercontent.com/51118441/91861860-408f1080-eca8-11ea-898d-c43e3463772e.PNG)

<img width="800" alt="grouping1" src="https://user-images.githubusercontent.com/51118441/91861879-4553c480-eca8-11ea-8582-579bc52e6f4e.png">

<img width="800" alt="grouping2" src="https://user-images.githubusercontent.com/51118441/91861903-4ab10f00-eca8-11ea-95e9-0de2d9be077a.png">
