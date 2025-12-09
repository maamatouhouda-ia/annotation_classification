import streamlit as st
import os
from PIL import Image
import pandas as pd
from datetime import datetime
import json

# Configuration de la page
st.set_page_config(
    page_title="Annotation d'images",
    page_icon="🔍",
    layout="centered"
)

# Liste complète des questions - REMPLACEZ PAR VOS DONNÉES COMPLÈTES
data = [{'image': '20250327_143847_400000_004306_0.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': '20250327_143847_400000_004603_3.png', 'label': 'faiencage', 
'prediction': 'faiencage'}, {'image': '20250327_155806_700000_006074_1.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': '20250327_155806_700000_009723_2.png', 'label': 'faiencage', 'prediction': 'joint_ouvert'}, {'image': '20250612_090537_gx010001_f_2580_photo_3.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': '20250612_091811_gx010002_f_288_photo_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': '20250612_091811_gx010002_f_9686_photo_0.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Abedul_Arriere_no_name_20241012_110117_001_001481_0.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_006207_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_007757_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_007773_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_008304_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_008440_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_008961_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009491_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009625_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009738_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_002482_0.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_004007_1.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_004562_9.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_003560_5.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115236_265_002110_0.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004621_4.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004637_1.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004881_5.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_002425_2.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_002517_2.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_002517_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_003157_8.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_122737_974_005852_3.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_122737_974_008402_2.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_003690_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_009171_1.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_010251_11.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_000191_8.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_006198_3.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_010109_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130339_425_001135_10.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_131539_943_000678_1.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_132140_245_001706_1.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_133913_494_004023_1.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_133913_494_004636_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_134438_095_002959_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_002308_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_143050_080_000339_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_143050_080_004536_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240729_142752_966_005982_4.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_151137_539_000000_3.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_160217_840_009269_5.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_092041_831_007027_2.png', 
'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_092642_327_006567_2.png', 'label': 'faiencage', 'prediction': 
'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_094442_978_002043_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_100243_870_007542_1.png', 'label': 'faiencage', 'prediction': 'joint_ouvert'}, {'image': 'Pornic_20240430_154024_004332_1.png', 'label': 'faiencage', 'prediction': 'joint_ouvert'}, {'image': '20250327_155806_700000_005353_0.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': '20250327_155806_700000_010129_0.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': '20250327_155806_700000_010221_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '20250612_090537_gx010001_f_11511_photo_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '20250612_090537_gx010001_f_1223_photo_2.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': '20250612_091811_gx010002_f_11236_photo_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '20250612_091811_gx010002_f_11586_photo_3.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': '20250612_091811_gx010002_f_1472_photo_0.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': '2daNte 3 Ote_Avant_no_name_20241006_094805_233_005171_3.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '2daNte 3 Ote_Avant_no_name_20241006_094805_233_005171_4.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Abedul_Arrière_no_name_20241012_110117_001_001776_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Abedul_Arrière_no_name_20241012_110117_001_002433_3.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Abedul_Arrière_no_name_20241012_110117_001_003523_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_006135_0.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_006207_0.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115236_265_010464_0.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004266_1.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_005469_1.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_006535_2.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_120436_859_004292_5.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_002719_2.png', 'label': 
'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_004574_3.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_122737_974_007971_4.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_004691_5.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_005332_1.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123938_373_002585_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_002717_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_002788_3.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_003598_3.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_009728_8.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_010698_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_005570_2.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_005688_6.png', 'label': 
'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_007828_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130339_425_001123_1.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130939_895_002518_0.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_131539_943_008423_1.png', 'label': 
'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_010545_7.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144250_668_001591_0.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240729_135226_801_003409_1.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240729_153355_853_005476_2.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_142335_290_005125_1.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_153252_124_004272_3.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_154416_977_007193_2.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_155617_498_000399_1.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_094442_978_001268_5.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_095043_239_005563_7.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_095643_526_003456_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_100243_870_003087_5.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_100243_870_009428_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_100844_096_002481_1.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_100844_096_003645_3.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_102644_958_003206_1.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_103845_411_008617_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '20250327_155806_700000_004059_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': '20250327_155806_700000_009333_2.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': '20250612_090537_gx010001_f_11296_photo_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': '20250612_090537_gx010001_f_12432_photo_3.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': '20250612_091811_gx010002_f_1160_photo_3.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_006343_7.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_007529_0.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_007580_5.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009286_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009298_4.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009701_5.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009871_5.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009965_5.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_010044_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_004162_7.png', 'label': 'fissure_significative', 'prediction': 'joint_ouvert'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_004195_3.png', 'label': 'fissure_significative', 'prediction': 'joint_ouvert'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_007150_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_002881_9.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_006172_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114035_586_000725_0.png', 'label': 'fissure_significative', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114035_586_006077_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114636_003_002308_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114636_003_002666_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115236_265_000215_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115236_265_000308_0.png', 'label': 'fissure_significative', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004564_6.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004776_4.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_005125_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_006998_3.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_008965_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logi_cam_1_20221002_145407_942_008323_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_002280_5.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_006496_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_009077_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_009619_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_003354_3.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_122737_974_006677_2.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_122737_974_008992_3.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_004848_4.png', 'label': 
'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_010153_1.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130339_425_001333_2.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_131539_943_000826_6.png', 'label': 'fissure_significative', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_133913_494_005935_0.png', 'label': 'fissure_significative', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_007460_0.png', 'label': 'fissure_significative', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144250_668_006484_1.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240729_153956_197_003809_2.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240730_095159_450_000083_2.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Lezignan_Corbieres_20240416_115331_007381_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_150537_327_005662_0.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_153816_767_004513_0.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_154416_977_009309_0.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_090241_210_009091_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_092041_831_004254_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_100844_096_000356_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': '10 de navarro_Avant_no_name_20241027_091836_433_001698_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250327_143847_400000_001546_1.png', 'label': 'joint_ouvert', 'prediction': 'fissure_significative'}, {'image': '20250327_143847_400000_002977_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250327_155806_700000_002684_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250327_155806_700000_005340_2.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250327_155806_700000_010439_5.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250612_091811_gx010002_f_10957_photo_8.png', 'label': 'joint_ouvert', 'prediction': 'fissure_significative'}, {'image': '20250612_091811_gx010002_f_9270_photo_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_004953_5.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_005093_4.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_005261_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_006189_1.png', 'label': 'joint_ouvert', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_006424_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_009361_2.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_009735_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_009753_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114035_586_002035_2.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114636_003_001912_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114636_003_008348_1.png', 'label': 'joint_ouvert', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_001138_0.png', 'label': 'joint_ouvert', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004353_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_008490_0.png', 'label': 'joint_ouvert', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_120436_859_004800_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logi_cam_1_20221002_140007_673_002956_0.png', 'label': 'joint_ouvert', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logi_cam_1_20221002_140007_673_004019_3.png', 'label': 'joint_ouvert', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logi_cam_1_20221002_154209_995_003761_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_003610_0.png', 'label': 'joint_ouvert', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_005031_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_005831_9.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_006484_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_009723_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_009785_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_010131_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130339_425_005797_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130339_425_008253_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130939_895_002292_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130939_895_002393_4.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_132140_245_001706_11.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_141925_207_003263_1.png', 'label': 'joint_ouvert', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_007341_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_007370_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_008119_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_008300_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144850_978_002605_3.png', 'label': 'joint_ouvert', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144850_978_007006_5.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240729_152755_599_002386_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240730_104156_426_005858_5.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_142935_566_008823_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_153252_124_005801_4.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_153816_767_007277_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_154416_977_006276_8.png', 'label': 'joint_ouvert', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_093842_795_010453_2.png', 'label': 'joint_ouvert', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_095043_239_006079_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_095043_239_006079_1.png', 'label': 'joint_ouvert', 'prediction': 'fissure_degradee'}]

# Filtrer pour garder seulement les erreurs de prédiction
questions = [item for item in data if item['label'] != item['prediction']]

# Initialisation de la session
if "responses" not in st.session_state:
    st.session_state.responses = {}
    for i, q in enumerate(questions):
        st.session_state.responses[i] = {
            "label_choisi": "",
            "commentaire": ""
        }

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "annotator_name" not in st.session_state:
    st.session_state.annotator_name = ""

if "started" not in st.session_state:
    st.session_state.started = False

# Fonction de sauvegarde
def save_responses():
    """Sauvegarde les réponses dans un fichier JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    results = {
        "annotateur": st.session_state.annotator_name,
        "date": timestamp,
        "annotations": []
    }
    
    for i, q in enumerate(questions):
        results["annotations"].append({
            "image": q["image"],
            "label_original": q["label"],
            "prediction_modele": q["prediction"],
            "label_choisi": st.session_state.responses[i]["label_choisi"],
            "commentaire": st.session_state.responses[i]["commentaire"]
        })
    
    return results

# CSS personnalisé
st.markdown("""
    <style>
    .stProgress > div > div > div > div {
        background-color: #00cc66;
    }
    .big-font {
        font-size: 1.2rem !important;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# Interface principale
st.title("🔍 Annotation d'images - Contrôle qualité")
st.markdown("---")

# Écran de démarrage
if not st.session_state.started:
    st.markdown("""
    ### Bienvenue dans l'outil d'annotation
    
    Ce formulaire vous permet de vérifier et corriger les prédictions du modèle d'IA.
    
    **Instructions:**
    - Pour chaque image, confirmez le bon label
    - Ajoutez un commentaire si nécessaire
    - Vos réponses seront automatiquement sauvegardées à la fin
    """)
    
    name = st.text_input("Votre nom/prénom:", key="name_input")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Commencer l'annotation", type="primary", use_container_width=True):
            if name.strip():
                st.session_state.annotator_name = name.strip()
                st.session_state.started = True
                st.rerun()
            else:
                st.error("⚠️ Veuillez entrer votre nom")
    
    st.info(f"📊 Nombre total d'images à annoter: **{len(questions)}**")
    
    # Section info
    with st.expander("ℹ️ Informations complémentaires"):
        st.markdown("""
        **Catégories disponibles:**
        - `faiencage`: Faïençage
        - `fissure_degradee`: Fissure dégradée
        - `fissure_significative`: Fissure significative
        - `joint_ouvert`: Joint ouvert 
        
        **Temps estimé:** ~{} minutes ({}s par image)
        """.format(len(questions) // 2, 30))

else:
    # Interface d'annotation
    q_idx = st.session_state.current_question
    
    # Vérifier si on a terminé
    if q_idx >= len(questions):
        st.success("🎉 **Annotation terminée !**")
        st.balloons()
        
        # Résumé
        st.markdown("### 📊 Résumé de vos annotations")
        
        results_data = save_responses()
        
        results_list = []
        for annotation in results_data["annotations"]:
            results_list.append({
                "Image": annotation["image"],
                "Label original": annotation["label_original"],
                "Prédiction IA": annotation["prediction_modele"],
                "Votre choix": annotation["label_choisi"],
                "Commentaire": annotation["commentaire"]
            })
        
        df = pd.DataFrame(results_list)
        st.dataframe(df, use_container_width=True)
        
        # Statistiques
        col1, col2, col3 = st.columns(3)
        with col1:
            agree_with_original = sum(1 for r in results_data["annotations"] if r["label_choisi"] == r["label_original"])
            st.metric("Accord label original", f"{agree_with_original}/{len(questions)}")
        with col2:
            agree_with_model = sum(1 for r in results_data["annotations"] if r["label_choisi"] == r["prediction_modele"])
            st.metric("Accord prédiction IA", f"{agree_with_model}/{len(questions)}")
        with col3:
            other_labels = sum(1 for r in results_data["annotations"] if r["label_choisi"] not in [r["label_original"], r["prediction_modele"]])
            st.metric("Autres labels", other_labels)
        
        # Boutons de téléchargement
        col1, col2 = st.columns(2)
        
        with col1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger CSV",
                data=csv,
                file_name=f"annotations_{st.session_state.annotator_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            json_str = json.dumps(results_data, ensure_ascii=False, indent=2)
            st.download_button(
                label="📥 Télécharger JSON",
                data=json_str,
                file_name=f"annotations_{st.session_state.annotator_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        if st.button("🔄 Faire une nouvelle annotation", use_container_width=True):
            st.session_state.started = False
            st.session_state.current_question = 0
            st.session_state.responses = {}
            st.rerun()
    
    else:
        question = questions[q_idx]
        
        # Barre de progression
        progress = (q_idx) / len(questions)
        st.progress(progress)
        st.caption(f"Image {q_idx + 1} sur {len(questions)}")
        
        # Informations sur l'annotateur
        col_info1, col_info2 = st.columns([3, 1])
        with col_info1:
            st.markdown(f"**Annotateur:** {st.session_state.annotator_name}")
        with col_info2:
            if st.button("🏠 Accueil"):
                st.session_state.started = False
                st.rerun()
        
        st.markdown("---")
        
        # Affichage de l'image
        label = question['label']
        image_name = question["image"]
        image_path = os.path.join("test", label, image_name)
        
        # Essayer différents chemins si l'image n'est pas trouvée
        if not os.path.exists(image_path):
            # Essayer sans le dossier label
            image_path = os.path.join("test", image_name)
            if not os.path.exists(image_path):
                # Essayer directement le nom
                image_path = image_name
        
        col_img, col_info = st.columns([2, 1])
        
        with col_img:
            if os.path.exists(image_path):
                img = Image.open(image_path)
                st.image(img, use_column_width=True)
            else:
                st.warning(f"⚠️ Image non trouvée localement")
                st.info(f"📁 Chemin attendu: `{image_path}`")
                st.markdown("""
                **Note:** En mode déploiement, assurez-vous que les images 
                sont bien dans le dossier `test/` de votre repository GitHub.
                """)
        
        with col_info:
            st.markdown("### 📋 Informations")
            st.markdown(f"**Fichier:**")
            st.code(image_name, language=None)
            # st.markdown(f"**Label original:**  \n`{question['label']}`")
            # st.markdown(f"**Prédiction IA:**  \n`{question['prediction']}`")
        
        st.markdown("---")
        
        # Zone d'annotation
        st.markdown("### ✏️ Votre annotation")
        
        # Choix du label
        labels_disponibles = [question["label"], question["prediction"], "Autre"]
        
        # Gérer l'index par défaut
        current_choice = st.session_state.responses[q_idx]["label_choisi"]
        if current_choice in labels_disponibles:
            default_index = labels_disponibles.index(current_choice)
        elif current_choice != "":
            default_index = 2  # "Autre"
        else:
            default_index = 0
        
        choice = st.radio(
            "Quel est le **bon label** pour cette image ?",
            labels_disponibles,
            key=f"question_{q_idx}",
            index=default_index
        )
        
        # Champ texte si "Autre" est choisi
        if choice == "Autre":
            new_label = st.text_input(
                "Précisez le nouveau label:",
                key=f"new_label_{q_idx}",
                value=st.session_state.responses[q_idx]["label_choisi"] 
                      if st.session_state.responses[q_idx]["label_choisi"] not in labels_disponibles 
                      else "",
                placeholder="Ex: fissure_longitudinale"
            )
            st.session_state.responses[q_idx]["label_choisi"] = new_label if new_label else ""
        else:
            st.session_state.responses[q_idx]["label_choisi"] = choice
        
        # Commentaire optionnel
        comment = st.text_area(
            "Commentaire (optionnel):",
            key=f"comment_{q_idx}",
            value=st.session_state.responses[q_idx]["commentaire"],
            placeholder="Ex: L'image est floue, difficile à classifier...",
            height=100
        )
        st.session_state.responses[q_idx]["commentaire"] = comment
        
        st.markdown("---")
        
        # Boutons de navigation
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("⬅️ Précédent", disabled=(q_idx == 0), use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
        
        with col2:
            # Vérifier si une réponse a été donnée
            has_response = st.session_state.responses[q_idx]["label_choisi"] != ""
            if not has_response:
                st.warning("⚠️ Veuillez choisir un label avant de continuer")
        
        with col3:
            button_label = "Suivant ➡️" if q_idx < len(questions) - 1 else "✅ Terminer"
            if st.button(button_label, type="primary", disabled=not has_response, use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8rem;'>
    Outil d'annotation - Version 1.0 | Développé avec Streamlit
</div>

""", unsafe_allow_html=True)

