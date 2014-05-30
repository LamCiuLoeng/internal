<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta http-Equiv="Cache-Control" Content="no-cache">
	<meta http-Equiv="Pragma" Content="no-cache">
	<meta http-Equiv="Expires" Content="0">
    <style type="text/css" media="all">
    	body{font-family:Arial;}
    	@font-face{font-family:Arial;src:url(/fonts/mac/Arial.ttf);}
    	@font-face{font-family:AvenirLTStd-Light;src:url(/fonts/mac/AvenirLTStd-Light.otf);}
    	@font-face{font-family:AvenirLTStd-Book;src:url(/fonts/mac/AvenirLTStd-Book.otf);}
    	@font-face{font-family:Futura;src:url(/fonts/mac/Futura.dfont);}
    	@font-face{font-family:MyriadPro;src: url(/fonts/MyriadPro-Regular.otf) format('truetype');}
    	@font-face{font-family:CARESYMASTM;src: url(/fonts/CARESYMASTM-0055.ttf);}
    	@font-face{font-family:Futura;src: url(/fonts/Futura-0050.cff);}
    	@font-face{font-family:SimHei;src:url(/fonts/SimHei-0078.ttf);}
    	@font-face{font-family:SimSun;src:url(/fonts/SimSun-0073.ttf) format('truetype');}
    	@font-face{font-family:verdana;src:url(/fonts/verdana.ttf);}
    	@font-face{font-family:AdobeHeitiStd;src:url(/fonts/AdobeHeitiStd-Regular.otf);}
    </style>
    <script type="text/javascript" src="/js/jquery-1.3.2.js"></script>
    <script>
    	$(document).ready(function(){
    		var height = Math.ceil($('#label').height()/4);
    		$('#size_h').html(height)
    	})
    </script>
</head>
<body style='padding:0;margin:0;width:794px;height:1123px;'>
	<div style='padding:15px 0;width:794px;height:1093px;'>
		<div style='border:7px solid #00285E;padding:20px;margin:15px 20px;text-align:center;width:700px;height:1009px;'>
		    ORC LABEL<br/>
			SIZE: 30mm X <span id='size_h'>xxx</span>mm
			<div style='border:1px solid #00ADEE;width:120px;color:black;text-align:center;margin:0 auto;font-size:9px;' id='label'>
				<div style='height:30px;line-height:30px;border-bottom:1px dashed #00ADEE;color:#00ADEE;font-size:12px;'>7.5mm sew</div>
				<div style='height:14px;line-height:14px;font-family:MyriadPro;font-size:10px;'>Orchestra Kazibao France</div>
				<div style='margin:3px 0;line-height:10px;'>
					%if order.sku:
					款号 ${order.sku}<br/>
					%endif
					%if order.height:
					年龄/身高 ${order.height}<br/>
					%elif order.head_size:
					年龄/头围 ${order.head_size}<br/>
					%endif
					%if order.specification:
					规格:${order.specification}
					%endif
					%if order.item_info1 and order.item.info1:
					<br/>
					${order.item.info1}${order.item_info1}
					%endif
				</div>
				%if order.product_family_id:
				<div style='margin-bottom:8px;line-height:10px;'>
					<% product_family_langs = order.product_family_langs.split(',') if order.product_family_langs else [] %>
					%for index, i in enumerate(product_family_langs):
						${order.product_family.__dict__[i]}
						%if not index==len(product_family_langs)-1:
						<br/>
						%endif
					%endfor
				</div>
				%endif
				%if order.origin_id:
				<div style='margin-bottom:3px;line-height:11px;'>
					<% origin_langs = ['english', 'spanish', 'arabic', 'chinese'] %>
					%for index, i in enumerate(origin_langs):
						${order.origin.__dict__[i]}
						%if not index==len(origin_langs)-1:
						<br/>
						%endif
					%endfor
				</div>
				%endif
				<div style='margin-bottom:6px;'>CA 45314</div>

				%if order.fabrics:
					<% fabric_langs = ['french', 'english', 'arabic', 'chinese'] if team=='HK' else ['french', 'english', 'spanish', 'portugese', 'german', 'chinese', 'arabic', 'russian'] %>
					<% composition_langs = ['french', 'english', 'spanish', 'portugese', 'german', 'chinese', 'arabic', 'russian'] %>
					%for fabric_index, fabric in enumerate(order.fabrics):
						<div style='margin:8px 3px 0 3px;word-wrap:break-word;font-weight:bold;'>
							%if fabric:
							%for lang_index, fabric_lang in enumerate(fabric_langs):
								${fabric.__dict__[fabric_lang]}
								%if fabric_lang!='chinese':
									&nbsp;/&nbsp;
								%else:
									&nbsp;:
								%endif
							%endfor
							%endif
						</div>
						
						%for composition_index, composition in enumerate(order.compositions[fabric_index]):
						<div style='margin:4px 3px 0 3px;word-wrap:break-word;'>
							${order.percents[fabric_index][composition_index]}%<br/>
							%for lang_index, composition_lang in enumerate(composition_langs):
								${composition.__dict__[composition_lang]}
								%if composition_lang!='russian':
									/
									%if composition.__dict__[composition_lang]=='Algodon':
									<br/>
									%endif
								%endif
							%endfor
						</div>
						%endfor
					%endfor
				%endif
				
				<div style='font-size:10px;color:red;font-family:AdobeHeitiStd;margin:10px 0 8px 0;'>
					TENIR ELOIGNE DU FEU /<br/> 
					KEEP AWAY FROM FIRE
				</div>
				
				%if order.care_img_ids:
				<div>
					%if order.care_imgs:
						%for care_img in order.care_imgs:
						<img src='${care_img.path}' height='20px'>
						%endfor
					%endif
				</div>
				%endif
				
				<div style='margin-top:3px;'>&reg; C1416</div>
				
				%if order.care_ids:
				<% care_langs = ['french', 'english', 'spanish', 'portugese', 'german', 'chinese', 'arabic', 'russian'] %>
				%for care in order.cares:
				<div style='margin:5px 8px 8px 8px;line-height:9px;font-size:8px;'>
					%for care_index, care_lang in enumerate(care_langs):
					%if care_lang=='arabic' and care.id==5:
					<img src='/images/care_label/arabic/care_5.jpg' height='25px'>
					%else:
					${care.__dict__[care_lang]}
					%endif
					%if not care_index == len(care_langs)-1:
					<br/>
					%endif
					%endfor
				</div>
				%endfor
				%endif
				
				<div style='font-family:AvenirLTStd-Book;margin:8px 0 3px 0;'>
					Service consommateurs<br/>
					ORCHESTRA<br/>
					400 Avenue Marcel Dassault<br/>
					34170 Castelnau le lez<br/>
					shop.orchestra.fr
				</div>
				<div style='height:30px;line-height:30px;border-top:1px dashed #00ADEE;color:#00ADEE;font-size:12px;'>7.5mm sew</div>
			</div>
		</div>
	</div>
</body>
</html>