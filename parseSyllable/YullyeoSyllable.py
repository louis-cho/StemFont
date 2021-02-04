import pandas as pd 
import numpy as np
import matplotlib.pylab as plt
from sklearn.cluster import KMeans
from groupingTool.parseUnicodeControll import *
from parseSyllable.utility.contourDistributionChart import *
from groupingTool.parseUnicodeControll import *
import os
import json
from mojo.UI import *

"""
create by Heesup Kim
"""

class PositionState:
    """
    컨투어와 컨투어의 번호를 관리하기 위한 클래스

    Args:
        con:: RContour
            관리하고자 하는 RContour 
    """
    def __init__(self,con,conNumber):
        self.con = con
        self.conNumber = conNumber

class PointInfo:
    """
    점의 위치를 관리하기 위한 클래스

    Args:
        x :: RPoint.x
            포인트의 x값
        y :: RPoint.y
            포인트의 y값
    """
    def __init__(self,x,y):
        self.x = x
        self.y = y

class FileExist(Exception):
    """
    그룹 정보를 담는 json파일의 존재 유무를 확인하기 위한 예외 클래스

    Args:
        msg :: str
            예외 메세지

    Returns:
        예외 메세지:: str
    """
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return self.msg
    

class YullyeoSyllableJudgement:
    """
    율려 한글파일(.ufo) 폰트 파일에 대하여 각각의 컨투어의 초성, 중성, 종성을 구분하는 클래스

    Args:
        fontFile :: RFont
            폰트파일 객체
        fontPath :: str
            폰트파일 경로

    Raises:
        파일이 존재하지 않을 시 에러를 반환 :: FileExist
    """
    def __init__(self, fontFile, fontPath):
        """
        한글의 경우를 12가지 케이스로 나눔
        1 group : 'ㅏ','ㅑ','ㅓ','ㅕ','ㅣ','ㅐ'
        2 group : 'ㅔ','ㅖ','ㅒ'
        3 group : 'ㅗ','ㅛ','ㅜ','ㅠ','ㅡ'
        4 group : 'ㅘ','ㅚ','ㅟ', 'ㅢ','ㅙ'
        5 group : 'ㅝ'
        6 group : 'ㅞ'
        (종성의 유무에 따라 각각 2가치 케이스로 더 나뉘고 총 12가지 케이스로 나뉨)
        """

        self.middle_one = ['ㅏ','ㅑ','ㅓ','ㅕ','ㅣ','ㅐ', "ㅒ"]
        self.middle_two = ['ㅔ','ㅖ']
        self.middle_three = ['ㅗ','ㅛ','ㅜ','ㅠ','ㅡ']
        self.middle_four = ['ㅘ','ㅚ','ㅟ', 'ㅢ','ㅙ','ㅝ']
        self.middle_five = ['ㅞ']

        tempFileName = fontPath.split('/')[-1]

        if tempFileName.split('.')[1] == 'ufo':
            try:
                tempFileName = fontPath.split('/')[-1]
                self.jsonFileName = os.path.dirname(os.path.abspath(__file__)) +'/jsonResource/'+ tempFileName.split('.')[0] + '_label.json'
                print("self.jsonFileName : ", self.jsonFileName)
                if os.path.exists(self.jsonFileName):
                    with open(self.jsonFileName, 'r') as jsonFile:
                        self.infoDict = json.load(jsonFile)
                    raise FileExist('라벨 파일은 이미 존재합니다')


                axis_x1 = list()
                axis_x2 = list()
                axis_x4 = list()
                axis_x5 = list()

                axis_y1 = list()
                axis_y2 = list()
                axis_y4 = list()
                axis_y5 = list()

                point_list1 = list()
                point_list2 = list()
                point_list4 = list()
                point_list5 = list()


                check_glyph1 = list()
                check_glyph2 = list()
                check_glyph4 = list()
                check_glyph5 = list()
                bar = ProgressBar('Analysis Progress',len(fontFile),'analysis...')
                barProcess = 0

                #각 케이스대로 데이터를 분류 (종성이 있는 경우)
                for gly in fontFile:
                    puc = parseUnicodeController(gly.unicode)
                    chars = puc.getChars()
                    barProcess += 1
                    # 종성O, 케이스1의 경우
                    if (chars[1] in self.middle_one) and (chars[2] is not None):
                        for i,con in enumerate(gly.contours):
                            temp = getContourPosition(gly,con,10000,10000)
                            point_list1.append(PointInfo(temp[0],temp[1]))
                            axis_x1.append(temp[0])
                            axis_y1.append(temp[1])
                            check_glyph1.append([gly,i])
                    # 종성O, 케이스2의 경우                 
                    elif chars[1] in self.middle_two and (chars[2] is not None):
                        for i,con in enumerate(gly.contours):
                            temp = getContourPosition(gly,con,10000,10000)
                            point_list2.append(PointInfo(temp[0],temp[1]))
                            axis_x2.append(temp[0])
                            axis_y2.append(temp[1])
                            check_glyph2.append([gly,i])
                    # 종성O, 케이스4의 경우
                    elif chars[1] in self.middle_four and (chars[2] is not None):
                        for i,con in enumerate(gly.contours):
                            temp = getContourPosition(gly,con,10000,10000)
                            point_list4.append(PointInfo(temp[0],temp[1]))
                            axis_x4.append(temp[0])
                            axis_y4.append(temp[1])
                            check_glyph4.append([gly,i])
                    # 종성O, 케이스5의 경우
                    elif chars[1] in self.middle_five and (chars[2] is not None):
                        for i,con in enumerate(gly.contours):
                            temp = getContourPosition(gly,con,10000,10000)
                            point_list5.append(PointInfo(temp[0],temp[1]))
                            axis_x5.append(temp[0])
                            axis_y5.append(temp[1])
                            check_glyph5.append([gly,i])

                    if barProcess % 10 == 0:
                        bar.tick(barProcess)

                #데이터 샘플 만들기
                np_axis_x1 = np.array(axis_x1)
                np_axis_y1 = np.array(axis_y1)
                self.samples1 = np.array(list(zip(np_axis_x1, np_axis_y1)))

                np_axis_x2 = np.array(axis_x2)
                np_axis_y2 = np.array(axis_y2)
                self.samples2 = np.array(list(zip(np_axis_x2, np_axis_y2)))

                np_axis_x4 = np.array(axis_x4)
                np_axis_y4 = np.array(axis_y4)
                self.samples4 = np.array(list(zip(np_axis_x4, np_axis_y4)))

                np_axis_x5 = np.array(axis_x5)
                np_axis_y5 = np.array(axis_y5)
                self.samples5 = np.array(list(zip(np_axis_x5, np_axis_y5)))


                #각 데이터 포인트를 그룹화 할 labels을 생성
                self.labels1 = np.zeros(len(np_axis_x1))
                self.labels2 = np.zeros(len(np_axis_x2))
                self.labels4 = np.zeros(len(np_axis_x4))
                self.labels5 = np.zeros(len(np_axis_x5))

                #model들의 생성
                self.labels1 = self.MakeLabel(1,self.samples1)
                self.labels2 = self.MakeLabel(2,self.samples2)
                self.labels4 = self.MakeLabel(4,self.samples4)
                self.labels5 = self.MakeLabel(5,self.samples5)
                bar.close()

                #종성의 라벨을 구함
                num = self.samples1[:,1].argmin()
                self.final_label1 = self.labels1[num]

                num = self.samples2[:,1].argmin()
                self.final_label2 = self.labels2[num]

                num = self.samples4[:,1].argmin()
                self.final_label4 = self.labels4[num]

                num = self.samples5[:,1].argmin()
                self.final_label5 = self.labels5[num]


                #각 라벨에 대한 정보를 json파일에 저장
                insert = dict()
                insert["final label1"] = int(self.final_label1)
                insert["final label2"] = int(self.final_label2)
                insert["final label4"] = int(self.final_label4)
                insert["final label5"] = int(self.final_label5)

                for i,content in enumerate(check_glyph1):
                    insert[content[0].name +'/' +str(content[1])] = int(self.labels1[i])
                for i,content in enumerate(check_glyph2):
                    insert[content[0].name +'/' + str(content[1])] = int(self.labels2[i])
                for i,content in enumerate(check_glyph4):
                    insert[content[0].name +'/' + str(content[1])] = int(self.labels4[i])
                for i,content in enumerate(check_glyph5):
                    insert[content[0].name +'/' + str(content[1])] = int(self.labels5[i])
                        
                with open(self.jsonFileName,'w',encoding = 'utf-8') as make_file:
                    self.infoDict = insert
                    json.dump(insert,make_file,indent = '\t')
            except FileExist as e:
                print(e)

    def MakeLabel(self,case,samples):
        """
        샘플 데이터와 각각의 케이스에 맞게 데이터를 군집화

        Args:
            case :: int
                케이스 번호 이름(종성이 있는 경우만 고려, 케이스 번호는 모음에 따라 분리)
            samples :: Numpy Array
                컨투어 무게중심의 좌표값의 정보를 가지고 있음

        Returns:
            label :: Numpy Array
                각각의 정보에 대한 라벨링의 결과
        """
        #case1
        if case == 1:
            model = KMeans(n_clusters = 3)
            model.fit(samples)
            labels = model.predict(samples)
            centers = model.cluster_centers_

            model = KMeans(n_clusters = 3, init = centers)
            model.fit(samples)
            labels = model.predict(samples)

        #case2
        if case == 2:
            model = KMeans(n_clusters = 3)
            model.fit(samples)
            labels = model.predict(samples)
            centers = model.cluster_centers_

            model = KMeans(n_clusters = 3, init = centers)
            model.fit(samples)
            labels = model.predict(samples)

        #case4
        if case == 4:
            model = KMeans(n_clusters = 4)
            model.fit(samples)
            labels = model.predict(samples)
            centers = model.cluster_centers_

            model = KMeans(n_clusters = 4, init = centers)
            model.fit(samples)
            labels = model.predict(samples)

        #case5
        if case == 5:
            model = KMeans(n_clusters = 4)
            model.fit(samples)
            labels = model.predict(samples)
            centers = model.cluster_centers_

            model = KMeans(n_clusters = 4, init = centers)
            model.fit(samples)
            labels = model.predict(samples)

        return labels

    def GetSyllable(self,glyph):
        """
        글리프에 대한 초성, 중성, 종성 컨투어를 반환
        
        Args:
            glyph :: RGlyph

        Returns:
            글리프에 대한 초성, 중성, 종성 컨투어에 대한 정보를 반환 :: list
            Example
            [[초성 컨투어 숫자], [중성 컨투어 숫자], [종성 컨투어 숫자]]
    
        """

        resultList = list()
        resultDict = dict()
        
        puc = parseUnicodeController(glyph.unicode)
        chars = puc.getChars()
        
        if chars[2] is None:
            if chars[1] in self.middle_one:
                resultList = self.case1(glyph)
            elif chars[1] in self.middle_two:
                resultList = self.case3(glyph)
            elif chars[1] in self.middle_three:
                resultList = self.case5(glyph)
            elif chars[1] in self.middle_four:
                resultList = self.case7(glyph)
            elif chars[1] in self.middle_five:
                resultList = self.case9(glyph)
        else:
            if chars[1] in self.middle_one:
                resultList = self.case2(glyph)
            elif chars[1] in self.middle_two:
                resultList = self.case4(glyph)
            elif chars[1] in self.middle_three:
                resultList = self.case5(glyph)
            elif chars[1] in self.middle_four:
                resultList = self.case8(glyph)
            elif chars[1] in self.middle_five:
                resultList = self.case10(glyph)
                
        resultDict[str(glyph.unicode)] = resultList
        
        return resultDict




    def GetLabelJsonFileName(self):
        """
        라벨 정보 파일이름 반환
        """
        return self.jsonFileName


    """
    글리프 분석을 위한 case분류
    """
    def case1(self,glyph):
        """
        종성X , 중성 그룹1
        """
    
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
        for i in range(0,len(glyph.contours)):
            temp_object = PositionState(glyph.contours[i],i)
            point_list.append(temp_object)
    
        result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
        middle.append(result[-1].conNumber)
    
        for i in range(0, len(result) - 1):
            first.append(result[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output

    def case2(self,glyph):
        """
        종성O , 중성 그룹1
        """
    
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
        print("self.jsonFileName : ", self.jsonFileName)
    
        for i in range(0,len(glyph.contours)):
            if self.infoDict["final label1"] ==  self.infoDict[glyph.name + '/' + str(i)]:
                final.append(i)
            else:
                temp_object = PositionState(glyph.contours[i],i)
                point_list.append(temp_object)
                
        result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
        middle.append(result[-1].conNumber)
    
        for i in range(0, len(result) - 1):
            first.append(result[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output

    def case3(self,glyph):
        """
        종성X , 중성 그룹2
        """
    
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
        for i in range(0,len(glyph.contours)):
            temp_object = PositionState(glyph.contours[i],i)
            point_list.append(temp_object)
    
        result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
        middle.append(result[-1].conNumber)
        middle.append(result[-2].conNumber)
    
        for i in range(0, len(result) - 2):
            first.append(result[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output

    def case4(self,glyph):
        """
        종성 유 , 중성 그룹2
        """
    
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
        for i in range(0,len(glyph.contours)):
            if self.infoDict["final label2"] ==  self.infoDict[glyph.name + '/' + str(i)]:
                final.append(i)
            else:
                temp_object = PositionState(glyph.contours[i],i)
                point_list.append(temp_object)
                
        result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
        middle.append(result[-1].conNumber)
        middle.append(result[-2].conNumber)
    
        for i in range(0, len(result) - 2):
            first.append(result[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output


    def case5(self,glyph):
        """
        종성 유무 상관없음 , 중성 그룹1
        """
    
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
    
        for i in range(0,len(glyph.contours)):
            temp_object = PositionState(glyph.contours[i],i)
            point_list.append(temp_object)
                
        result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
        #값이 가장 큰 것이 중성
        #중성 컨투어 중 miny값 이하면 종성 아니면 초성
        middle.append(result[-1].conNumber)
        cut_line = result[-1].con.bounds[1]
        del(result[-1])
    
        for i in range(0, len(result)):
            if result[i].con.bounds[1] >= cut_line:
                first.append(result[i].conNumber)
            else:
                final.append(result[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output


    def case7(self,glyph):
        """
        종성X , 중성 그룹5
        """
    
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
    
        for i in range(0,len(glyph.contours)):
            temp_object = PositionState(glyph.contours[i],i)
            point_list.append(temp_object)
    
        #중성을 찾는 과정            
        result1 = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
        middle.append(result1[-1].conNumber)
        del(result1[-1])
    
        result2 = sorted(result1, key = lambda PositionState: PositionState.con.bounds[1])
        middle.append(result2[0].conNumber)
        del(result2[0])
    
        for i in range(0, len(result2)):
            first.append(result2[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output

    def case8(self,glyph):
        """
        종성O , 중성 그룹5
        """
    
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
        for i in range(0,len(glyph.contours)):
            if self.infoDict["final label4"] ==  self.infoDict[glyph.name + '/' + str(i)]:
                final.append(i)
            else:
                temp_object = PositionState(glyph.contours[i],i)
                point_list.append(temp_object)
    
        #중성을 찾는 과정            
        result1 = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
        middle.append(result1[-1].conNumber)
        del(result1[-1])
    
        result2 = sorted(result1, key = lambda PositionState: PositionState.con.bounds[1])
        middle.append(result2[0].conNumber)
        del(result2[0])
    
        for i in range(0, len(result2)):
            first.append(result2[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output

    def case9(self,glyph):
        """
        종성X , 중성 그룹6
        """
    
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
        for i in range(0,len(glyph.contours)):
            temp_object = PositionState(glyph.contours[i],i)
            point_list.append(temp_object)
    
        #중성을 찾는 과정            
        result1 = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
        middle.append(result1[-1].conNumber)
        del(result1[-1])
        middle.append(result1[-1].conNumber)
        del(result1[-1])
    
        result2 = sorted(result1, key = lambda PositionState: PositionState.con.bounds[1])
        middle.append(result2[0].conNumber)
        del(result2[0])
    
        for i in range(0, len(result2)):
            first.append(result2[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output

    def case10(self,glyph):
        """
        종성O , 중성 그룹1
        """
        
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
    
        for i in range(0,len(glyph.contours)):
            if self.infoDict["final label5"] ==  self.infoDict[glyph.name + '/' + str(i)]:
                final.append(i)
            else:
                temp_object = PositionState(glyph.contours[i],i)
                point_list.append(temp_object)
    
        #중성을 찾는 과정            
        result1 = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
        middle.append(result1[-1].conNumber)
        del(result1[-1])
        middle.append(result1[-1].conNumber)
        del(result1[-1])
    
        result2 = sorted(result1, key = lambda PositionState: PositionState.con.bounds[1])
        middle.append(result2[0].conNumber)
        del(result2[0])
    
        for i in range(0, len(result2)):
            first.append(result2[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output




