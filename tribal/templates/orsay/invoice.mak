<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta http-Equiv="Cache-Control" Content="no-cache">
	<meta http-Equiv="Pragma" Content="no-cache">
	<meta http-Equiv="Expires" Content="0">
    <style type="text/css" media="all">
    	body{font-family:Times;font-size:12px;}
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
    		
    	})
    </script>
</head>
<body style='padding:0;margin:0;width:794px;height:1123px;'>
	<div style='padding:15px 0;width:794px;height:1093px;'>
		<div style='padding:20px;margin:22px 27px;width:700px;height:1009px;'>
			<h2>Supreme Trading (Shenzhen) Co Ltd.</h2>
			41F Block A, United Plaza,<br/>
			No. 5022 Binhe Road,<br/>
			Futian Central District, Shenzhen<br/>
			Tel: (755) 2531 7000&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Fax: (755) 2531 7100<br/>
			<h1 style="text-align:center;">INVOICE</h1>
			<div style='clear:both;'>
				<div style='float:left;width:220px;'>
					Bill To:
					<div style='border:1px solid #000;margin:5px 5px 5px 0;padding:5px;'>
						${order.cust_code} (${order.cust_code})<br/>
						${order.billto_address}<br/>
						<br/><br/>
						ATTN: ${order.billto_contact_sales}<br/>
						ORDER BY:<br/>
						TEL: ${order.billto_tel_no}<br/>
						FAX: 
					</div>
				</div>
				<div style='float:left;width:220px;'>
					Ship To:
					<div style='border:1px solid #000;margin:5px 5px 5px 0;padding:5px;'>
						${order.shipto_address}<br/>
						<br/><br/>
						ATTN: ${order.shipto_contact_person}<br/>
						TEL: ${order.shipto_tel_no}<br/>
						FAX:<br/>
					</div>
				</div>
				<div style='float:left;margin:5px 5px 5px 0;padding:5px;width:240px;'><br/>
					<table>
						<tr>
							<td>Inv Number</td>
							<td>: ${invoice_no}</td>
						</tr>
						<tr>
							<td>Cust PO No.</td>
							<td>: ${order.customer_po}</td>
						</tr>
						<tr>
							<td>Ship VIA</td>
							<td>: LAND</td>
						</tr>
						<tr>
							<td>Sales Contact</td>
							<td>: ${order.create_by.display_name}</td>
						</tr>
						<tr>
							<td>Page</td>
							<td>: 1/1</td>
						</tr>
					</table>
				</div>
			</div>
			<div>
				<table style='border-collapse:collapse;width:698px;border:1px solid #000;'>
					<thead style='border:1px solid #000;'>
						<tr>
							<td width="40px">Item No.</td>
							<td width="80px">Item Code</td>
							<td>Description</td>
							<td width="70px">Quantity</td>
							<td width="80px">Unit Price</td>
							<td width="70px" align="right">Amount</td>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>&nbsp;</td>
							<td>&nbsp;</td>
							<td>&nbsp;</td>
							<td>&nbsp;</td>
							<td>&nbsp;</td>
							<td align="right">RMB</td>
						</tr>
						<tr valign="top">
							<td>1</td>
							<td>#10501</td>
							<td>
								Orsay Care Label item ${item_no}
							</td>
							<td style='border-bottom:1px solid #000'>${order.qty} pcs</td>
							<td style='border-bottom:1px solid #000'>${order.price}</td>
							<td style='border-bottom:1px solid #000' align="right">${order.qty*order.price}</td>
						</tr>
						<tr>
							<td>&nbsp;</td>
							<td>&nbsp;</td>
							<td>&nbsp;</td>
							<td>${order.qty} pcs</td>
							<td>sub-total:</td>
							<td align="right">${order.qty*order.price}</td>
						</tr>
						<tr>
							<td>&nbsp;</td>
							<td>增值税(17.0%)</td>
							<td>&nbsp;</td>
							<td style='border-bottom:1px solid #000'>&nbsp;</td>
							<td style='border-bottom:1px solid #000'>&nbsp;</td>
							<td style='border-bottom:1px solid #000' align="right">${order.qty*order.price*0.17}</td>
						</tr>
						<tr>
							<td>&nbsp;</td>
							<td>&nbsp;</td>
							<td>&nbsp;</td>
							<td>&nbsp;</td>
							<td>sub-total:</td>
							<td align="right">${order.qty*order.price*0.17}</td>
						</tr>
					</tbody>
				</table>
				<div style='float:right;clear:both;font-weight:bold;'>
					280&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Total:&nbsp;&nbsp;&nbsp;&nbsp;${order.qty*order.price*1.17}&nbsp;
				</div>
				<br/>
				(RMB)<br/>
				<span style='font-weight:bold;'>Note:</span>
				<table>
					<tr>
						<td>1.</td>
						<td>All price include 17% China VAT.</td>
					</tr>
					<tr>
						<td>2.</td>
						<td>Please contact our sales representative for further information.</td>
					</tr>
					<tr>
						<td>3.</td>
						<td>Please sign and chop for confirmation.</td>
					</tr>
					<tr>
						<td>4.</td>
						<td>Supreme's liability under this contract shall not exceed the replacement of defective items.</td>
					</tr>
					<tr>
						<td valign="top">5.</td>
						<td>
							Bank info :<br/>
				Bank : China Minsheng Banking Corp., Ltd Shenzhen Shennan Branch<br/>
				Address : 1/F, Chuangzhan Centre, Anhui Building, Shennan Road, Futian, Shenzhen.<br/>
				Bank A/C Name : Supreme Trading (Shenzhen) Co Ltd.,<br/>
				Bank A/C No : 1810014180001800<br/>
				SWIFT code : MSBCCNBJ004<br/>
						</td>
					</tr>
					<tr>
						<td>6.</td>
						<td>Any complaints against this invoice must be notified in writing within 7 days of date hereof.</td>
					</tr>
				</table>
				<span style='font-weight:bold;'>Remarks:</span>
				<table style='border-collapse:collapse;width:698px;border:1px solid #000;'>
					<tr>
						<td>&nbsp;</td>
					</tr>
				</table>
				<div style='float:right;clear:both;font-weight:bold;'>
					E. & O. E.
				</div>
				<div style='clear:both;padding-top:40px;'>
					<div style='width:340px;float:left;border-top:1px solid #000;'>
						<span style='font-weight:bold;'>(${order.cust_name})</span><br/>
						Please confirm by signed and chopped
					</div>
					<div style='width:340px;float:left;border-top:1px solid #000;margin-left:18px;'>
						<span style='font-weight:bold;'>Supreme Trading (Shenzhen) Co Ltd. (UAT)</span>
					</div>
				</div>
			</div>
		</div>
	</div>
</body>
</html>