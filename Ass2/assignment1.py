"""
In this assignment you should interpolate the given function.
"""

import numpy as np
import time
import random


class Assignment1:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        starting to interpolate arbitrary functions.
        """
        self.cache = {
            9: (np.array([np.float64(1.0), np.float64(0.9238795325112867), np.float64(0.7071067811865476), np.float64(0.38268343236508984), np.float64(6.123233995736766e-17), np.float64(-0.3826834323650897), np.float64(-0.7071067811865475), np.float64(-0.9238795325112867), np.float64(-1.0)]), np.array([np.float64(0.5), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(0.5)])),
            10: (np.array([np.float64(1.0), np.float64(0.9396926207859084), np.float64(0.766044443118978), np.float64(0.5000000000000001), np.float64(0.17364817766693041), np.float64(-0.1736481776669303), np.float64(-0.4999999999999998), np.float64(-0.7660444431189779), np.float64(-0.9396926207859083), np.float64(-1.0)]), np.array([np.float64(0.5), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-0.5)])),
            19: (np.array([np.float64(1.0), np.float64(0.984807753012208), np.float64(0.9396926207859084), np.float64(0.8660254037844387), np.float64(0.766044443118978), np.float64(0.6427876096865394), np.float64(0.5000000000000001), np.float64(0.3420201433256688), np.float64(0.17364817766693041), np.float64(6.123233995736766e-17), np.float64(-0.1736481776669303), np.float64(-0.3420201433256685), np.float64(-0.4999999999999998), np.float64(-0.6427876096865394), np.float64(-0.7660444431189779), np.float64(-0.8660254037844385), np.float64(-0.9396926207859083), np.float64(-0.984807753012208), np.float64(-1.0)]), np.array([np.float64(0.5), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(0.5)])),
            20: (np.array([np.float64(1.0), np.float64(0.9863613034027223), np.float64(0.9458172417006346), np.float64(0.8794737512064891), np.float64(0.7891405093963936), np.float64(0.6772815716257411), np.float64(0.5469481581224269), np.float64(0.40169542465296953), np.float64(0.24548548714079924), np.float64(0.0825793454723324), np.float64(-0.08257934547233227), np.float64(-0.2454854871407989), np.float64(-0.4016954246529694), np.float64(-0.546948158122427), np.float64(-0.6772815716257409), np.float64(-0.7891405093963935), np.float64(-0.879473751206489), np.float64(-0.9458172417006347), np.float64(-0.9863613034027223), np.float64(-1.0)]), np.array([np.float64(0.5), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-0.5)])),
            49: (np.array([np.float64(1.0), np.float64(0.9978589232386035), np.float64(0.9914448613738104), np.float64(0.9807852804032304), np.float64(0.9659258262890683), np.float64(0.9469301294951057), np.float64(0.9238795325112867), np.float64(0.8968727415326884), np.float64(0.8660254037844387), np.float64(0.8314696123025452), np.float64(0.7933533402912352), np.float64(0.7518398074789774), np.float64(0.7071067811865476), np.float64(0.6593458151000688), np.float64(0.6087614290087207), np.float64(0.5555702330196024), np.float64(0.5000000000000001), np.float64(0.44228869021900125), np.float64(0.38268343236508984), np.float64(0.3214394653031617), np.float64(0.25881904510252074), np.float64(0.19509032201612833), np.float64(0.1305261922200517), np.float64(0.06540312923014327), np.float64(6.123233995736766e-17), np.float64(-0.06540312923014314), np.float64(-0.1305261922200516), np.float64(-0.1950903220161282), np.float64(-0.25881904510252063), np.float64(-0.3214394653031616), np.float64(-0.3826834323650895), np.float64(-0.44228869021900113), np.float64(-0.4999999999999998), np.float64(-0.5555702330196023), np.float64(-0.6087614290087207), np.float64(-0.6593458151000688), np.float64(-0.7071067811865475), np.float64(-0.7518398074789773), np.float64(-0.793353340291235), np.float64(-0.831469612302545), np.float64(-0.8660254037844387), np.float64(-0.8968727415326881), np.float64(-0.9238795325112867), np.float64(-0.9469301294951056), np.float64(-0.9659258262890682), np.float64(-0.9807852804032304), np.float64(-0.9914448613738104), np.float64(-0.9978589232386035), np.float64(-1.0)]), np.array([np.float64(0.5), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(0.5)])),
            50: (np.array([np.float64(1.0), np.float64(0.9979453927503363), np.float64(0.9917900138232462), np.float64(0.9815591569910653), np.float64(0.9672948630390295), np.float64(0.9490557470106686), np.float64(0.9269167573460217), np.float64(0.9009688679024191), np.float64(0.8713187041233894), np.float64(0.8380881048918406), np.float64(0.8014136218679566), np.float64(0.7614459583691345), np.float64(0.7183493500977277), np.float64(0.6723008902613168), np.float64(0.6234898018587336), np.float64(0.5721166601221697), np.float64(0.5183925683105252), np.float64(0.4625382902408352), np.float64(0.4047833431223938), np.float64(0.3453650544213078), np.float64(0.28452758663103245), np.float64(0.22252093395631445), np.float64(0.15959989503337954), np.float64(0.09602302590768189), np.float64(0.03205157757165533), np.float64(-0.03205157757165521), np.float64(-0.09602302590768176), np.float64(-0.15959989503337918), np.float64(-0.22252093395631434), np.float64(-0.28452758663103234), np.float64(-0.3453650544213075), np.float64(-0.40478334312239367), np.float64(-0.4625382902408351), np.float64(-0.518392568310525), np.float64(-0.5721166601221698), np.float64(-0.6234898018587335), np.float64(-0.6723008902613168), np.float64(-0.7183493500977275), np.float64(-0.7614459583691342), np.float64(-0.8014136218679565), np.float64(-0.8380881048918406), np.float64(-0.8713187041233892), np.float64(-0.900968867902419), np.float64(-0.9269167573460216), np.float64(-0.9490557470106685), np.float64(-0.9672948630390295), np.float64(-0.9815591569910653), np.float64(-0.991790013823246), np.float64(-0.9979453927503363), np.float64(-1.0)]), np.array([np.float64(0.5), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-0.5)])),
            99: (np.array([np.float64(1.0), np.float64(0.9994862162006879), np.float64(0.9979453927503363), np.float64(0.9953791129491982), np.float64(0.9917900138232462), np.float64(0.9871817834144502), np.float64(0.9815591569910653), np.float64(0.9749279121818236), np.float64(0.9672948630390295), np.float64(0.9586678530366606), np.float64(0.9490557470106686), np.float64(0.9384684220497604), np.float64(0.9269167573460217), np.float64(0.9144126230158125), np.float64(0.9009688679024191), np.float64(0.8865993063730001), np.float64(0.8713187041233894), np.float64(0.8551427630053461), np.float64(0.8380881048918406), np.float64(0.820172254596956), np.float64(0.8014136218679566), np.float64(0.7818314824680298), np.float64(0.7614459583691345), np.float64(0.7402779970753156), np.float64(0.7183493500977277), np.float64(0.6956825506034864), np.float64(0.6723008902613168), np.float64(0.6482283953077884), np.float64(0.6234898018587336), np.float64(0.598110530491216), np.float64(0.5721166601221697), np.float64(0.5455349012105487), np.float64(0.5183925683105252), np.float64(0.4907175520039379), np.float64(0.4625382902408352), np.float64(0.4338837391175582), np.float64(0.4047833431223938), np.float64(0.3752670048793742), np.float64(0.3453650544213078), np.float64(0.31510821802362077), np.float64(0.28452758663103245), np.float64(0.2536545839095075), np.float64(0.22252093395631445), np.float64(0.19115862870137248), np.float64(0.15959989503337954), np.float64(0.127877161684506), np.float64(0.09602302590768189), np.float64(0.06407021998071295), np.float64(0.03205157757165533), np.float64(6.123233995736766e-17), np.float64(-0.03205157757165521), np.float64(-0.06407021998071283), np.float64(-0.09602302590768176), np.float64(-0.12787716168450589), np.float64(-0.15959989503337918), np.float64(-0.19115862870137235), np.float64(-0.22252093395631434), np.float64(-0.2536545839095072), np.float64(-0.28452758663103234), np.float64(-0.31510821802362066), np.float64(-0.3453650544213075), np.float64(-0.3752670048793741), np.float64(-0.40478334312239367), np.float64(-0.43388373911755806), np.float64(-0.4625382902408351), np.float64(-0.4907175520039376), np.float64(-0.518392568310525), np.float64(-0.5455349012105485), np.float64(-0.5721166601221698), np.float64(-0.598110530491216), np.float64(-0.6234898018587335), np.float64(-0.6482283953077885), np.float64(-0.6723008902613168), np.float64(-0.6956825506034864), np.float64(-0.7183493500977275), np.float64(-0.7402779970753154), np.float64(-0.7614459583691342), np.float64(-0.7818314824680297), np.float64(-0.8014136218679565), np.float64(-0.820172254596956), np.float64(-0.8380881048918406), np.float64(-0.8551427630053461), np.float64(-0.8713187041233892), np.float64(-0.8865993063730001), np.float64(-0.900968867902419), np.float64(-0.9144126230158124), np.float64(-0.9269167573460216), np.float64(-0.9384684220497602), np.float64(-0.9490557470106685), np.float64(-0.9586678530366607), np.float64(-0.9672948630390295), np.float64(-0.9749279121818236), np.float64(-0.9815591569910653), np.float64(-0.9871817834144501), np.float64(-0.991790013823246), np.float64(-0.9953791129491982), np.float64(-0.9979453927503363), np.float64(-0.9994862162006879), np.float64(-1.0)]), np.array([np.float64(0.5), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(0.5)])),
            100: (np.array([np.float64(1.0), np.float64(0.9994965423831851), np.float64(0.9979866764718844), np.float64(0.9954719225730846), np.float64(0.9919548128307953), np.float64(0.9874388886763943), np.float64(0.9819286972627067), np.float64(0.975429786885407), np.float64(0.9679487013963562), np.float64(0.9594929736144974), np.float64(0.9500711177409454), np.float64(0.9396926207859084), np.float64(0.9283679330160727), np.float64(0.9161084574320696), np.float64(0.9029265382866213), np.float64(0.8888354486549235), np.float64(0.8738493770697849), np.float64(0.8579834132349771), np.float64(0.8412535328311812), np.float64(0.8236765814298328), np.float64(0.8052702575310586), np.float64(0.7860530947427875), np.float64(0.7660444431189781), np.float64(0.7452644496757547), np.float64(0.7237340381050702), np.float64(0.7014748877063213), np.float64(0.6785094115571322), np.float64(0.6548607339452851), np.float64(0.6305526670845225), np.float64(0.6056096871376666), np.float64(0.5800569095711983), np.float64(0.5539200638661104), np.float64(0.5272254676105024), np.float64(0.5000000000000001), np.float64(0.4722710747726827), np.float64(0.44406661260577424), np.float64(0.41541501300188644), np.float64(0.38634512569312857), np.float64(0.3568862215918719), np.float64(0.3270679633174218), np.float64(0.2969203753282749), np.float64(0.26647381369003514), np.float64(0.23575893550942728), np.float64(0.20480666806519085), np.float64(0.17364817766693064), np.float64(0.14231483827328512), np.float64(0.1108381999010111), np.float64(0.07924995685678844), np.float64(0.0475819158237424), np.float64(0.015865963834808153), np.float64(-0.01586596383480803), np.float64(-0.04758191582374228), np.float64(-0.07924995685678854), np.float64(-0.11083819990101099), np.float64(-0.142314838273285), np.float64(-0.1736481776669303), np.float64(-0.20480666806519052), np.float64(-0.23575893550942695), np.float64(-0.26647381369003503), np.float64(-0.2969203753282748), np.float64(-0.32706796331742144), np.float64(-0.3568862215918718), np.float64(-0.38634512569312845), np.float64(-0.41541501300188655), np.float64(-0.4440666126057741), np.float64(-0.4722710747726826), np.float64(-0.4999999999999998), np.float64(-0.5272254676105025), np.float64(-0.5539200638661103), np.float64(-0.580056909571198), np.float64(-0.6056096871376665), np.float64(-0.6305526670845225), np.float64(-0.654860733945285), np.float64(-0.6785094115571321), np.float64(-0.7014748877063214), np.float64(-0.7237340381050702), np.float64(-0.7452644496757547), np.float64(-0.7660444431189779), np.float64(-0.7860530947427873), np.float64(-0.8052702575310586), np.float64(-0.8236765814298327), np.float64(-0.8412535328311811), np.float64(-0.8579834132349768), np.float64(-0.8738493770697849), np.float64(-0.8888354486549234), np.float64(-0.9029265382866211), np.float64(-0.9161084574320695), np.float64(-0.9283679330160725), np.float64(-0.9396926207859082), np.float64(-0.9500711177409454), np.float64(-0.9594929736144974), np.float64(-0.9679487013963562), np.float64(-0.975429786885407), np.float64(-0.9819286972627066), np.float64(-0.9874388886763943), np.float64(-0.9919548128307953), np.float64(-0.9954719225730846), np.float64(-0.9979866764718843), np.float64(-0.9994965423831851), np.float64(-1.0)]), np.array([np.float64(0.5), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-1.0), np.float64(1.0), np.float64(-0.5)])),
        }

    def interpolate(self, f: callable, a: float, b: float, n: int) -> callable:
        """
        Interpolate the function f in the closed range [a,b] using at most n 
        points. Your main objective is minimizing the interpolation error.
        Your secondary objective is minimizing the running time. 
        The assignment will be tested on variety of different functions with 
        large n values. 
        
        Interpolation error will be measured as the average absolute error at 
        2*n random points between a and b. See test_with_poly() below. 

        Note: It is forbidden to call f more than n times. 

        Note: This assignment can be solved trivially with running time O(n^2)
        or it can be solved with running time of O(n) with some preprocessing.
        **Accurate O(n) solutions will receive higher grades.** 
        
        Note: sometimes you can get very accurate solutions with only few points, 
        significantly less than n. 
        
        Parameters
        ----------
        f : callable. it is the given function
        a : float
            beginning of the interpolation range.
        b : float
            end of the interpolation range.
        n : int
            maximal number of points to use.

        Returns
        -------
        The interpolating function.
        """
        
        if n == 1:
            return lambda x: f((a + b) / 2)

        def get_cheb_canonical(N):
            # Check cache first
            if N in self.cache:
                return self.cache[N]
                
            if N == 1:
                return np.array([0.0]), np.array([1.0])

            # Chebyshev nodes of the second kind (Extrema) in [-1, 1]
            j = np.arange(N)
            z = np.cos(j * np.pi / (N - 1))
            
            # Barycentric Weights (Chebyshev 2nd kind)
            weights = np.ones(N)
            weights[0] = 0.5
            weights[N - 1] = 0.5
            weights[1::2] = -1 * weights[1::2]
            
            self.cache[N] = (z, weights)
            return z, weights

        # Attempt to use n points with vectorization
        z_nodes, weights = get_cheb_canonical(n)
        
        # Map z from [-1, 1] to [a, b]
        nodes = (b - a) / 2 * z_nodes + (a + b) / 2
        
        used_n = n
        
        try:
            # Vectorization attempt (consumes 1 invocation)
            res = f(nodes)
            
            # Verify result format
            if np.isscalar(res):
                # Optimization for Constant Functions:
                # If f(x) returns a scalar for a vector input, it implies 
                # f is likely a constant function y = c. 
                # We can return a constant lambda immediately.
                return lambda x: res
            elif np.shape(res) == (n,):
                y_values = np.array(res)
            else:
                raise ValueError("Shape mismatch or invalid return")
                
        except Exception:
            # Fallback: Vectorization failed. We used 1 invocation.
            # We must proceed with n-1 points to stay within budget.
            used_n = n - 1
            if used_n < 1:
               # Should only happen if input n=1 (handled) or n=1 failed?
               # If input n=2 -> used_n=1.
               pass
            
            # Recompute nodes/weights for n-1
            z_nodes_fallback, weights_fallback = get_cheb_canonical(used_n)
            nodes = (b - a) / 2 * z_nodes_fallback + (a + b) / 2
            weights = weights_fallback
            
            y_values = np.zeros(used_n)
            for i in range(used_n):
                y_values[i] = f(nodes[i])

        # --- Adaptive Log-Interpolation Check ---
        # Heuristic: If values are strictly positive and cover a huge dynamic range,
        # interpolating in Log-space might be much more accurate (e.g. exp(x), exp(exp(x))).
        # We only apply this if the ratio max/min is large enough to justify the overhead.
        
        use_log = False
        try:
            min_y = np.min(y_values)
            max_y = np.max(y_values)
            
            if min_y > 1e-30:  # Strictly positive (avoid log(0) or instability near 0)
                ratio = max_y / min_y
                if ratio > 1000:  # Threshold for "Exponential-like" behavior
                    y_values = np.log(y_values)
                    use_log = True
        except:
            pass # Safety fallback
        # ----------------------------------------

        self.nodes = nodes
        self.y_values = y_values
        self.weights = weights

        def result(x):
            # Barycentric Interpolation Evaluation Formula (2nd form)
            # P(x) = sum(w_j * y_j / (x - x_j)) / sum(w_j / (x - x_j))
            
            diff = x - nodes
            
            close_mask = np.abs(diff) < 1e-14
            if np.any(close_mask):
                val = y_values[np.argmax(close_mask)]
                return np.exp(val) if use_log else val
            
            t = weights / diff
            numerator = np.dot(t, y_values)
            denominator = np.sum(t)
            
            if denominator == 0:
                return 0 
            
            res = numerator / denominator
            return np.exp(res) if use_log else res

        return result


##########################################################################


import unittest
from functionUtils import *
# from tqdm import tqdm


class TestAssignment1(unittest.TestCase):

    def test_with_poly(self):
        T = time.time()

        ass1 = Assignment1()
        mean_err = 0

        d = 30
        for i in range(100):
            a = np.random.randn(d)

            f = np.poly1d(a)

            ff = ass1.interpolate(f, -10, 10, 100)

            xs = np.random.random(200)
            err = 0
            for x in xs:
                yy = ff(x)
                y = f(x)
                err += abs(y - yy)

            err = err / 200
            mean_err += err
        mean_err = mean_err / 100

        T = time.time() - T
        print(T)
        print(mean_err)

    def test_with_poly_restrict(self):
        ass1 = Assignment1()
        a = np.random.randn(5)
        f = RESTRICT_INVOCATIONS(10)(np.poly1d(a))
        ff = ass1.interpolate(f, -10, 10, 10)
        xs = np.random.random(20)
        for x in xs:
            yy = ff(x)

if __name__ == "__main__":
    unittest.main()
