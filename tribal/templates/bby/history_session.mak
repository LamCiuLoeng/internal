<style type="text/css">
<!--
.bold_font {
	padding-left:20px;
	font-size: 12px;
	line-height: 28px;
	font-weight: bold;
	color: #069;
	text-decoration: none;
}
.text_td {
	padding-left:20px;
}

td {
		font-family: Tahoma, Geneva, sans-serif;
		font-size: 12px;
		line-height: normal;
		color: #000;
		text-decoration: none;
	}

	.date-session{
		list-style : none;
		padding-left : 0px;
	}
	.date-session li{
		padding-bottom : 3px;
	}
-->
</style>
<%page args="header,history"/>


<div><br class="clear"/><br /></div>

<table width="900" border="0" cellpadding="0" cellspacing="0">
  <tr>
    <td bgcolor="#003366"><table width="900" border="0" cellpadding="0" cellspacing="1">
      <tr>
        <td width="150" bgcolor="#FFFFFF" class="bold_font">SKU#</td>
        <td bgcolor="#FFFFFF" class="text_td">${header.sku}&nbsp;</td>
      </tr>
    </table>
      <table width="900" border="0" cellpadding="0" cellspacing="1">
        <tr>
          <td width="150" bgcolor="#FFFFFF" class="bold_font">Brand</td>
          <td width="300" bgcolor="#FFFFFF" class="text_td">${header.brand}&nbsp;</td>
          <td width="150" bgcolor="#FFFFFF" class="bold_font">Vendor</td>
          <td bgcolor="#FFFFFF" class="text_td">${header.vendor}&nbsp;</td>
        </tr>
        <tr>
          <td bgcolor="#FFFFFF" class="bold_font">Issued By</td>
          <td bgcolor="#FFFFFF" class="text_td">${header.create_by}&nbsp;</td>
          <td bgcolor="#FFFFFF" class="bold_font">Issued Time</td>
          <td bgcolor="#FFFFFF" class="text_td">${header.create_time.strftime('%Y-%m-%d %H:%M:%S')}&nbsp;</td>
        </tr>
        <tr>
          <td bgcolor="#FFFFFF" class="bold_font">Updated By</td>
          <td bgcolor="#FFFFFF" class="text_td">${header.update_by}&nbsp;</td>
          <td bgcolor="#FFFFFF" class="bold_font">Updated Time</td>
          <td bgcolor="#FFFFFF" class="text_td">${header.update_time.strftime('%Y-%m-%d %H:%M:%S')}&nbsp;</td>
        </tr>
    </table></td>
  </tr>
</table>
<br />

<table cellspacing="0" cellpadding="0" border="0" class="gridTable" style="width:1000px">
	<thead>
	<tr>
		<th style="width:150px;">Time</th>
		<th style="width:150px">User</th>
		<th style="width:100px">Action Type</th>
		<th>Description</td>
	</tr>
	</thead>
	%for h in history:
		<tr>
			<td style="border-left:1px solid #CCCCCC">${h.create_time.strftime('%Y-%m-%d %H:%M:%S')}&nbsp;</td>
			<td>${h.create_by}&nbsp;</td>
			<td>${h.action_type}&nbsp;</td>
			<td style="text-align:left;">${h.remark}&nbsp;</td>
		</tr>
	%endfor
</table>
