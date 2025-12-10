import streamlit as st
import os
from PIL import Image
import pandas as pd
from datetime import datetime
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import io

# Configuration de la page
st.set_page_config(
    page_title="Annotation d'images",
    page_icon="🔍",
    layout="centered"
)

# Données dossier TEST
data = [{'image': '20250327_155806_700000_006404_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': '20250327_155806_700000_010753_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': '20250612_090537_gx010001_f_11380_photo_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': '20250612_090537_gx010001_f_11404_photo_2.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': '20250612_090537_gx010001_f_12372_photo_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': '20250612_090537_gx010001_f_12522_photo_8.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': '20250612_090537_gx010001_f_12689_photo_7.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': '20250612_090537_gx010001_f_8248_photo_6.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': '20250612_091811_gx010002_f_11083_photo_0.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': '20250612_091811_gx010002_f_9686_photo_0.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': '20250612_091811_gx010002_f_9716_photo_3.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Abedul_Arriere_no_name_20241012_110117_001_001463_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Abedul_Arriere_no_name_20241012_110117_001_002177_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Abedul_Arrière_no_name_20241012_110117_001_002845_0.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Abedul_Arrière_no_name_20241012_110117_001_002903_8.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_006207_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_006315_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_006329_1.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_006501_9.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_007623_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_007773_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_007853_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_008061_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_008440_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_008988_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_010010_3.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_002482_0.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_004092_3.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_004493_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_004577_1.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115236_265_002110_0.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004637_1.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004832_7.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004855_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_005272_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_008138_0.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_002357_2.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_002376_10.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_002435_3.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_002517_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_002675_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_002781_3.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_002837_10.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_122737_974_005852_3.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_122737_974_006535_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_122737_974_010309_3.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_004232_5.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_004258_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_004809_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123938_373_004949_3.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_010417_8.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_010494_2.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_005398_2.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_005493_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_005570_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_010109_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130339_425_001333_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130939_895_002393_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_131539_943_005553_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_132140_245_001706_1.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_132140_245_001815_1.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_143050_080_008160_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144250_668_001924_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144250_668_001980_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144250_668_005805_0.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240730_114123_512_007603_2.png', 'label': 'faiencage', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_150537_327_009811_9.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_154416_977_006276_8.png', 'label': 'faiencage', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_092041_831_004254_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_092041_831_007027_2.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_100243_870_007289_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_102044_614_008623_2.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Stenay_goproMax_20240215_121405_010199_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': '20250327_155806_700000_000506_5.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': '20250327_155806_700000_010043_0.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': '20250327_155806_700000_010129_0.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': '20250327_155806_700000_010221_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '20250612_090537_gx010001_f_1223_photo_2.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': '20250612_090537_gx010001_f_12372_photo_3.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '20250612_090537_gx010001_f_7867_photo_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '20250612_091811_gx010002_f_10154_photo_2.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '20250612_091811_gx010002_f_10825_photo_3.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '20250612_091811_gx010002_f_11586_photo_3.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': '20250612_091811_gx010002_f_665_photo_0.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': '20250612_091811_gx010002_f_8958_photo_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '2daNte 3 Ote_Avant_no_name_20241006_094805_233_004616_5.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '2daNte 3 Ote_Avant_no_name_20241006_094805_233_005656_10.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': '2daNte 3 Ote_Avant_no_name_20241006_095613_865_001317_1.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Abedul_Arrière_no_name_20241012_110117_001_001776_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Abedul_Arrière_no_name_20241012_110117_001_002177_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Abedul_Arrière_no_name_20241012_110117_001_003523_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Abejones_Avant_no_name_20241027_094126_566_002037_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_005494_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_006137_1.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_006315_4.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_010055_6.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_003162_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_003202_1.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_003437_2.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114035_586_000641_1.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114636_003_009853_3.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115236_265_010446_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004331_5.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004374_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004548_1.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_005469_1.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_005534_0.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logi_cam_1_20221002_154209_995_007776_3.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_002319_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_006484_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_002719_2.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_002887_4.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_002980_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_122737_974_008654_0.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_122737_974_008667_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_004245_3.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_004394_3.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_005413_8.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_005451_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_009945_2.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_010088_12.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123938_373_004949_5.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_002844_3.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_003598_3.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_009728_8.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_005570_2.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_005688_6.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_006165_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_006576_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_007828_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_133913_494_004411_4.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_134438_095_007784_2.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144250_668_004896_3.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144250_668_005553_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'CD44_20240131_162500_209000_011571_3.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_144136_123_002548_2.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_145336_739_008751_1.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_153252_124_004272_3.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_155017_324_004790_3.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_094442_978_001268_5.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_095643_526_003456_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_100243_870_003087_5.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_100243_870_007289_0.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_100243_870_009428_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_100844_096_002481_1.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_100844_096_003645_3.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': '20250327_143847_400000_005884_5.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': '20250327_155806_700000_004059_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': '20250327_155806_700000_007125_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': '20250327_155806_700000_010519_3.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': '20250612_090537_gx010001_f_12707_photo_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': '20250612_090537_gx010001_f_1702_photo_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': '20250612_090537_gx010001_f_4259_photo_3.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': '20250612_090537_gx010001_f_8239_photo_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': '20250612_091811_gx010002_f_10129_photo_7.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': '20250612_091811_gx010002_f_10825_photo_9.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': '20250612_091811_gx010002_f_6228_photo_3.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': '20250612_091811_gx010002_f_6649_photo_1.png', 'label': 'fissure_significative', 'prediction': 'joint_ouvert'}, {'image': '20250612_091811_gx010002_f_6749_photo_0.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': '7081_photo_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_006301_4.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_007623_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_008831_7.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009004_2.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009754_2.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009965_5.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_010076_5.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_000156_3.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_000266_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_004548_3.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_006633_7.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_005050_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_005072_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_006333_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_009426_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_009861_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114035_586_000725_0.png', 'label': 'fissure_significative', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114035_586_000739_2.png', 'label': 'fissure_significative', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115236_265_002146_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_005293_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_007491_0.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_008232_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_120436_859_008820_5.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logi_cam_1_20221002_140641_542_009586_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_002376_12.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_002425_4.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_002435_5.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_002494_12.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_004890_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_004974_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_006496_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_008555_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_009047_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_009820_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_001039_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_002690_1.png', 'label': 'fissure_significative', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_002804_5.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_002980_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_003000_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_003128_10.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_003464_4.png', 'label': 'fissure_significative', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_003610_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_004309_4.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_006059_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123938_373_008276_1.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_004848_4.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_009958_6.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_010153_1.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130339_425_001333_2.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130939_895_000131_0.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_133913_494_004023_9.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_007953_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144250_668_002384_9.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240730_095759_687_009610_3.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240730_104721_103_009750_0.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240730_105321_362_005649_6.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Lezignan_Corbieres_20240416_115331_007381_8.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_141735_015_009116_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_090241_210_009091_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': '20250327_143847_400000_004890_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250327_155806_700000_002684_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250327_155806_700000_010060_2.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250612_090537_gx010001_f_10493_photo_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '8Mayo_Avant_no_name_20241013_101744_755_003001_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Abedul_Arrière_no_name_20241012_110117_001_003229_5.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_007027_2.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_001663_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_001673_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_002859_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_002891_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_005005_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_005061_2.png', 'label': 'joint_ouvert', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_005497_4.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_006368_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_006481_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_009753_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114035_586_002054_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114035_586_002077_2.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114035_586_004067_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114035_586_005108_2.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114636_003_001977_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114636_003_002451_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114636_003_008348_1.png', 'label': 'joint_ouvert', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115236_265_002110_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115236_265_004958_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115236_265_005031_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115236_265_005132_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_001138_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_007588_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logi_cam_1_20221002_142406_709_008489_7.png', 'label': 'joint_ouvert', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_003578_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_003578_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_003610_0.png', 'label': 'joint_ouvert', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_122213_161_006595_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_122213_161_006986_5.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_004612_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_005831_9.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_002633_1.png', 'label': 'joint_ouvert', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_010153_4.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_010428_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_010541_2.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_010674_3.png', 'label': 'joint_ouvert', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130939_895_002173_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130939_895_002216_2.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130939_895_002719_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130939_895_004427_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_131539_943_000678_7.png', 'label': 'joint_ouvert', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_132140_245_001706_11.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_132140_245_001815_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_132140_245_002013_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_133913_494_004587_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_007265_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_007334_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_007341_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_007377_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_007982_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_008442_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_145451_158_000391_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240730_111122_146_007418_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240730_111122_146_007418_0_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_133008_466_005531_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_144736_340_008953_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_145936_912_009962_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_153252_124_005801_4.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_153816_767_007277_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_092041_831_001739_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_092041_831_002571_7.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_092041_831_002571_8.png', 'label': 'joint_ouvert', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_095043_239_006079_2.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_100243_870_006736_5.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_103244_941_008363_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Pornic_20240506_132519_002817_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}]

#Données dossier Validation

data2 = [{'image': '20250327_143847_400000_004306_0.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': '20250327_143847_400000_004603_3.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': '20250327_143847_400000_007345_2.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': '20250327_155806_700000_006074_1.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': '20250327_155806_700000_006487_5.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': '20250612_090537_gx010001_f_1058_photo_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': '20250612_090537_gx010001_f_12087_photo_0.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': '20250612_090537_gx010001_f_6581_photo_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': '20250612_090537_gx010001_f_9036_photo_0.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': '20250612_091811_gx010002_f_2667_photo_0.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': '20250612_091811_gx010002_f_5221_photo_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': '20250612_091811_gx010002_f_5311_photo_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': '20250612_091811_gx010002_f_6749_photo_0.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': '2daNte 3 Ote_Avant_no_name_20241006_094805_233_004551_1.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': '2daNte 3 Ote_Avant_no_name_20241006_094805_233_007204_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_005693_2.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_006034_0.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_007394_0.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_008466_13.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_008831_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_008874_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009197_3.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009701_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009738_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009899_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_010065_5.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_010286_1.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_010775_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_004007_1.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_004195_4.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_004366_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_002881_9.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_003208_3.png', 'label': 'faiencage', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_003560_5.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_003606_3.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114035_586_000147_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004578_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004881_5.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_005580_0.png', 'label': 'faiencage', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_005596_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_005596_3.png', 'label': 'faiencage', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logi_cam_1_20221002_140641_542_009300_0.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_002425_2.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_003157_8.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_003498_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_000090_3.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_003690_4.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_009945_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_004793_5.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_009728_8.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_009883_2.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_010230_1.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_010251_10.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_010251_11.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_005253_12.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_005806_7.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_006101_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_009768_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130339_425_006731_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_131539_943_001797_2.png', 'label': 'faiencage', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_132140_245_005079_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_133913_494_004636_5.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_143050_080_005810_3.png', 'label': 'faiencage', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_143050_080_008022_5.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144250_668_004991_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144250_668_006495_5.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144250_668_007120_2.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144250_668_007679_0.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240730_085232_352_008297_5.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_092642_327_006567_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_092642_327_009617_1.png', 'label': 'faiencage', 'prediction': 'faiencage'}, {'image': '20250327_143847_400000_007045_5.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '20250327_143847_400000_007345_2.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': '20250327_155806_700000_004047_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '20250327_155806_700000_005353_0.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': '20250327_155806_700000_006496_6.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '20250327_155806_700000_006657_8.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': '20250612_090537_gx010001_f_1750_photo_2.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '20250612_090537_gx010001_f_2565_photo_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '20250612_090537_gx010001_f_3330_photo_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '20250612_090537_gx010001_f_8320_photo_2.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '20250612_091811_gx010002_f_10034_photo_3.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': '20250612_091811_gx010002_f_10489_photo_8.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': '20250612_091811_gx010002_f_11236_photo_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '20250612_091811_gx010002_f_9913_photo_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '2daNte 3 Ote_Avant_no_name_20241006_094805_233_007240_4.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': '2daNte 3 Ote_Avant_no_name_20241006_095613_865_000813_4.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '8Mayo_Avant_no_name_20241013_101744_755_001267_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '8Mayo_Avant_no_name_20241013_102208_003_000435_1.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Abedul_Arrière_no_name_20241012_110117_001_002433_3.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Abedul_Arrière_no_name_20241012_110117_001_002845_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Abedul_Arrière_no_name_20241012_110117_001_005199_2.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Abejones_Avant_no_name_20241027_094126_566_002007_2.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_006034_0.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009437_3.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_010544_3.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_000022_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_003598_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_003878_11.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004217_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004266_1.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004353_3.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_005469_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_005596_3.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_122737_974_006887_2.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_004691_5.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_004703_0.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_004765_3.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_004809_0.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_005210_2.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_005281_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_005579_6.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_010179_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_004404_9.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_006320_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_010178_3.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_001189_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_001375_2.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_002474_8.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130339_425_005556_11.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130939_895_002518_0.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130939_895_008864_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_131539_943_000274_2.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_131539_943_000577_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_131539_943_008423_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_132140_245_002253_6.png', 'label': 'fissure_degradee', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_132140_245_002491_1.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_134438_095_003515_2.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_141925_207_003065_2.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_143050_080_004400_2.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144250_668_003339_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240729_153355_853_005476_2.png', 'label': 'fissure_degradee', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_141735_015_007256_4.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_093842_795_005841_6.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_095043_239_005231_5.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_095043_239_005635_0.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_095043_239_007213_7.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_100243_870_003509_2.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_101444_229_005710_1.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_101444_229_006861_4.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_104445_670_006057_0.png', 'label': 'fissure_degradee', 'prediction': 'faiencage'}, {'image': 'Stenay_goproMax_20240215_121405_010199_0.png', 'label': 'fissure_degradee', 'prediction': 'fissure_degradee'}, {'image': '10 de navarro_Avant_no_name_20241027_091836_433_001846_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': '20250327_155806_700000_001137_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': '20250327_155806_700000_002367_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': '20250327_155806_700000_003753_3.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': '20250327_155806_700000_010027_0.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': '20250612_090537_gx010001_f_11260_photo_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': '20250612_090537_gx010001_f_1163_photo_4.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': '20250612_090537_gx010001_f_12707_photo_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': '20250612_091811_gx010002_f_10957_photo_6.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': '20250612_091811_gx010002_f_1160_photo_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': '20250612_091811_gx010002_f_1169_photo_5.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_005479_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_006377_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_007529_0.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_007603_1.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_007623_4.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_008930_1.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009275_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009286_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009358_0.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009369_2.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_091817_546_009885_5.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_000121_2.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_000225_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_000247_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_004211_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_004872_3.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_009610_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_009716_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_009890_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114035_586_004229_1.png', 'label': 'fissure_significative', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114035_586_004656_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114636_003_009291_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115236_265_008019_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_002551_1.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_004515_2.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_006998_3.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_120436_859_004112_0.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_120436_859_004720_3.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_120436_859_008944_3.png', 'label': 'fissure_significative', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logi_cam_1_20221002_140007_673_003671_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_002129_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_002376_3.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_002468_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_002494_5.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_004869_4.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_006205_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_006886_1.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131005_165_008545_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_003033_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_003464_5.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241007_131605_356_003464_7.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130339_425_009388_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130939_895_001487_5.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130939_895_002802_0.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130939_895_004843_2.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_132140_245_004394_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_134438_095_003121_0.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_002218_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_003968_2.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_008185_1.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144250_668_001712_3.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144250_668_006861_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144850_978_006625_2.png', 'label': 'fissure_significative', 'prediction': 'faiencage'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144850_978_008631_0.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240729_135751_656_003244_3.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'le_port_av_E009_20240229_083030_365_1709181649162000_6.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_144136_123_001993_2.png', 'label': 'fissure_significative', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_151137_539_004256_1.png', 'label': 'fissure_significative', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_092041_831_002571_2.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_102644_958_007512_3.png', 'label': 'fissure_significative', 'prediction': 'fissure_significative'}, {'image': '10 de navarro_Avant_no_name_20241027_091836_433_001698_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250327_143847_400000_001429_0.png', 'label': 'joint_ouvert', 'prediction': 'fissure_significative'}, {'image': '20250327_143847_400000_001429_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250327_143847_400000_001546_6.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250327_143847_400000_002832_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250327_143847_400000_006769_5.png', 'label': 'joint_ouvert', 'prediction': 'fissure_degradee'}, {'image': '20250327_155806_700000_005379_4.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250327_155806_700000_010439_5.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250612_090537_gx010001_f_11499_photo_4.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250612_090537_gx010001_f_12159_photo_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250612_090537_gx010001_f_6599_photo_0.png', 'label': 'joint_ouvert', 'prediction': 'fissure_significative'}, {'image': '20250612_091811_gx010002_f_1037_photo_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250612_091811_gx010002_f_1484_photo_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250612_091811_gx010002_f_2895_photo_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '20250612_091811_gx010002_f_9270_photo_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '2daNte 3 Ote_Avant_no_name_20241006_094805_233_007172_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '2daNte 3 Ote_Avant_no_name_20241006_095613_865_000000_2.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': '2daNte 3 Ote_Avant_no_name_20241006_095613_865_002421_7.png', 'label': 'joint_ouvert', 'prediction': 'faiencage'}, {'image': 'Abejones_Avant_no_name_20241027_094126_566_002070_3.png', 'label': 'joint_ouvert', 'prediction': 'fissure_significative'}, {'image': 'Acanceh Tizimin 1_Avant_no_name_20241027_092342_314_001663_5.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_005093_4.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_006387_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_007775_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_113435_357_009817_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114035_586_002113_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114035_586_004088_4.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114636_003_001950_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_114636_003_002545_4.png', 'label': 'joint_ouvert', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115236_265_000000_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115236_265_000000_2.png', 'label': 'joint_ouvert', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115236_265_010171_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115236_265_010481_1.png', 'label': 'joint_ouvert', 'prediction': 'fissure_degradee'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_001015_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_115836_351_001015_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_120436_859_005714_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_120436_859_007927_1.png', 'label': 'joint_ouvert', 'prediction': 'faiencage'}, {'image': 'Barcelona_Avant_Logiroad-Cam 1_20240625_120436_859_008944_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logi_cam_1_20221002_140007_673_003144_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Barcelona_Avant_Logi_cam_1_20221002_154209_995_003761_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_004741_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123338_144_005387_4.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_123938_373_009067_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_124538_639_009054_0.png', 'label': 'joint_ouvert', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_006329_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125138_894_006508_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_002676_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_003020_1.png', 'label': 'joint_ouvert', 'prediction': 'fissure_degradee'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_125739_105_010131_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130339_425_007163_3.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130939_895_002393_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130939_895_002393_4.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_130939_895_006321_0.png', 'label': 'joint_ouvert', 'prediction': 'fissure_significative'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_131539_943_000566_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_131539_943_000746_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_132140_245_001743_4.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_132140_245_001842_6.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_133913_494_004597_5.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_133913_494_006593_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_134438_095_007192_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_007233_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_007296_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_142449_810_007429_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144250_668_010046_1.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Castres_Avant_Logi_cam_1_20241029_144850_978_002388_4.png', 'label': 'joint_ouvert', 'prediction': 'faiencage'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240729_152755_599_002386_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'La Chevroliere_Avant_Logiroad-Cam 1_20240730_111122_146_004961_0.png', 'label': 'joint_ouvert', 'prediction': 'joint_ouvert'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_154416_977_006276_8.png', 'label': 'joint_ouvert', 'prediction': 'faiencage'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240423_155017_324_001032_0.png', 'label': 'joint_ouvert', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_090841_406_004951_0.png', 'label': 'joint_ouvert', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_095043_239_006079_1.png', 'label': 'joint_ouvert', 'prediction': 'fissure_degradee'}, {'image': 'Pont Saint Martin_Avant_Logiroad-Cam 1_20240424_100243_870_009208_0.png', 'label': 'joint_ouvert', 'prediction': 'faiencage'}]

# Combiner les données avec l'indication du dossier source
questions = []
for item in data:
    new_item = item.copy()
    new_item['source_folder'] = 'test'
    questions.append(new_item)

for item in data2:
    new_item = item.copy()
    new_item['source_folder'] = 'validation'
    questions.append(new_item)

# Filtrer pour garder seulement les erreurs de prédiction
questions = [item for item in questions if item['label'] != item['prediction']]

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
            "source_folder": q["source_folder"],
            "label_original": q["label"],
            "prediction_modele": q["prediction"],
            "label_choisi": st.session_state.responses[i]["label_choisi"],
            "commentaire": st.session_state.responses[i]["commentaire"]
        })
    
    return results

# Fonction d'envoi d'email
def send_email_with_results(results_data, csv_content):
    """Envoie les résultats par email"""
    # CONFIGURATION EMAIL - À PERSONNALISER
    smtp_server = "smtp.gmail.com"  # Pour Gmail
    smtp_port = 587
    sender_email = "maamatou.houda@gmail.com"  # VOTRE EMAIL
    sender_password = "fziq atni xvlb ynwl"  # MOT DE PASSE D'APPLICATION
    receiver_email = "houda.maamatou@logiroad-center.com"  # EMAIL DU DESTINATAIRE
    
    try:
        # Créer le message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"Annotations - {results_data['annotateur']} - {results_data['date']}"
        
        # Corps de l'email
        body = f"""
Bonjour,

Nouvelles annotations reçues de {results_data['annotateur']}.

Statistiques:
- Nombre d'images annotées: {len(results_data['annotations'])}
- Date: {results_data['date']}

Les résultats sont en pièce jointe au format CSV.

Cordialement,
Système d'annotation automatique
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attacher le fichier CSV
        csv_attachment = MIMEBase('application', 'octet-stream')
        csv_attachment.set_payload(csv_content)
        encoders.encode_base64(csv_attachment)
        csv_attachment.add_header(
            'Content-Disposition',
            f'attachment; filename=annotations_{results_data["annotateur"]}_{results_data["date"]}.csv'
        )
        msg.attach(csv_attachment)
        
        # Envoyer l'email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        return True, "Email envoyé avec succès!"
    
    except Exception as e:
        return False, f"Erreur lors de l'envoi: {str(e)}"

# Fonction pour trouver le chemin de l'image
def get_image_path(question):
    """Trouve le chemin de l'image selon son dossier source"""
    source_folder = question['source_folder']
    label = question['label']
    image_name = question['image']
    
    # Chemins possibles
    possible_paths = [
        os.path.join(source_folder, label, image_name),  # source_folder/label/image
        os.path.join(source_folder, image_name),         # source_folder/image
        image_name                                        # image seule
    ]
    
    # Retourner le premier chemin qui existe
    for path in possible_paths:
        if os.path.exists(path):
            return path, True
    
    # Si aucun chemin n'existe, retourner le chemin préféré
    return possible_paths[0], False

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
    .source-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-left: 8px;
    }
    .badge-test {
        background-color: #e3f2fd;
        color: #1976d2;
    }
    .badge-validation {
        background-color: #f3e5f5;
        color: #7b1fa2;
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
        if st.button("Commencer l'annotation", type="primary", width='stretch'):
            if name.strip():
                st.session_state.annotator_name = name.strip()
                st.session_state.started = True
                st.rerun()
            else:
                st.error("⚠️ Veuillez entrer votre nom")
    
    # Statistiques des sources
    test_count = sum(1 for q in questions if q['source_folder'] == 'test')
    validation_count = sum(1 for q in questions if q['source_folder'] == 'validation')
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("📊 Total", len(questions))
    with col_stat2:
        st.metric("🔵 Test", test_count)
    with col_stat3:
        st.metric("🟣 Validation", validation_count)
    
    # Section info
    st.markdown("ℹ️ Informations complémentaires")
    st.markdown("""
        **Catégories disponibles:**
        - `faiencage`: Faïençage
        - `fissure_degradee`: Fissure dégradée
        - `fissure_significative`: Fissure significative
        - `joint_ouvert`: Joint ouvert 
        
        **Sources des images:**
        - 🔵 **Test**: Images du dossier `test/`
        - 🟣 **Validation**: Images du dossier `validation/`
        
        **Temps estimé:** ~{} minutes ({}s par image)
        """.format(len(questions) // 2, 30))

else:
    # Interface d'annotation
    q_idx = st.session_state.current_question
    
    # Vérifier si on a terminé
    if q_idx >= len(questions):
        st.success("🎉 **Annotation terminée !**")
        st.balloons()
        
        # Préparer les résultats
        results_data = save_responses()
        
        results_list = []
        for annotation in results_data["annotations"]:
            results_list.append({
                "Image": annotation["image"],
                "Source": annotation["source_folder"],
                "Label original": annotation["label_original"],
                "Prédiction IA": annotation["prediction_modele"],
                "Votre choix": annotation["label_choisi"],
                "Commentaire": annotation["commentaire"]
            })
        
        df = pd.DataFrame(results_list)
        csv_content = df.to_csv(index=False).encode('utf-8')
        
        # Envoyer l'email automatiquement
        with st.spinner("Envoi des résultats par email..."):
            success, message = send_email_with_results(results_data, csv_content)
        
        if success:
            st.success(f"✅ {message}")
        else:
            st.error(f"❌ {message}")
            st.info("💾 Vous pouvez télécharger les résultats ci-dessous en cas d'échec de l'envoi.")
        
        # Résumé (optionnel - peut être masqué si vous ne voulez pas l'afficher)
        with st.expander("📊 Voir le résumé des annotations", expanded=False):
            st.dataframe(df, width='stretch')
            
            # Statistiques
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                agree_with_original = sum(1 for r in results_data["annotations"] if r["label_choisi"] == r["label_original"])
                st.metric("Accord label original", f"{agree_with_original}/{len(questions)}")
            with col2:
                agree_with_model = sum(1 for r in results_data["annotations"] if r["label_choisi"] == r["prediction_modele"])
                st.metric("Accord prédiction IA", f"{agree_with_model}/{len(questions)}")
            with col3:
                test_annotated = sum(1 for r in results_data["annotations"] if r["source_folder"] == "test")
                st.metric("Images Test", test_annotated)
            with col4:
                val_annotated = sum(1 for r in results_data["annotations"] if r["source_folder"] == "validation")
                st.metric("Images Validation", val_annotated)
        
        # Boutons de téléchargement (backup)
        st.markdown("### 💾 Téléchargement de sauvegarde")
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📥 Télécharger CSV",
                data=csv_content,
                file_name=f"annotations_{st.session_state.annotator_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                width='stretch'
            )
        
        with col2:
            json_str = json.dumps(results_data, ensure_ascii=False, indent=2)
            st.download_button(
                label="📥 Télécharger JSON",
                data=json_str,
                file_name=f"annotations_{st.session_state.annotator_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                width='stretch'
            )
        
        if st.button("🔄 Faire une nouvelle annotation", width='stretch'):
            st.session_state.started = False
            st.session_state.current_question = 0
            st.session_state.responses = {}
            st.rerun()
    
    else:
        question = questions[q_idx]
        
        # Barre de progression
        progress = (q_idx) / len(questions)
        st.progress(progress)
        
        # Badge de source
        source_badge_class = "badge-test" if question['source_folder'] == 'test' else "badge-validation"
        source_icon = "🔵" if question['source_folder'] == 'test' else "🟣"
        
        st.markdown(f"""
        <div style='margin-bottom: 10px;'>
            Image {q_idx + 1} sur {len(questions)}
            <span class='source-badge {source_badge_class}'>{source_icon} {question['source_folder'].upper()}</span>
        </div>
        """, unsafe_allow_html=True)
        
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
        image_path, exists = get_image_path(question)
        
        if exists:
            st.markdown("**Fichier :**")
            st.markdown(
                f"<div style='background-color: #f0f2f6; padding: 8px; "
                f"border-radius: 4px; word-wrap: break-word; overflow-wrap: break-word; "
                f"font-family: monospace; font-size: 0.9rem;'>"
                f"{question['image']}</div>",
                unsafe_allow_html=True
            )
            st.markdown("\n")
            img = Image.open(image_path)

            st.image(img)

        else:
            st.warning("⚠️ Image non trouvée localement")
            st.info(f"📁 Chemin attendu : `{image_path}`")
            st.markdown(f"""
            **Note:** L'image devrait se trouver dans le dossier **`{question['source_folder']}/`**  
            Assurez-vous que les images sont bien organisées dans les dossiers correspondants.
            """)

        
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
            if st.button("⬅️ Précédent", disabled=(q_idx == 0), width='stretch'):
                st.session_state.current_question -= 1
                st.rerun()
        
        with col2:
            # Vérifier si une réponse a été donnée
            has_response = st.session_state.responses[q_idx]["label_choisi"] != ""
            if not has_response:
                st.warning("⚠️ Veuillez choisir un label avant de continuer")
        
        with col3:
            button_label = "Suivant ➡️" if q_idx < len(questions) - 1 else "✅ Terminer"
            if st.button(button_label, type="primary", disabled=not has_response, width='stretch'):
                st.session_state.current_question += 1
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8rem;'>
    Outil d'annotation - Version 2.0 (Deux sources) | Développé par Houda MAAMATOU avec Streamlit
</div>
""", unsafe_allow_html=True)


