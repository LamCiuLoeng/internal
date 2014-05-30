<%
	from tribal.util.mako_filter import b
%>
<div id="item_variables">
<div style="float: left; padding-top: 3px;">
	&nbsp;&nbsp;
	<strong class="fonts-c-369">View Variables</strong>
</div>
<div style="float: right; padding-top: 3px;">
  	<a href="#" onclick="closeDiv();"><strong>Close</strong></a>
  	&nbsp;&nbsp;
</div>
<div style="float: left; padding-left: 360px; padding-top: 3px;">
    <label class="fieldlabel"><strong>Item:</strong>&nbsp;</label>
    <strong>${item}</strong>
</div>
<div style="clear: both; padding-left: 20px; padding-bottom: 5px; padding-top: 5px;">
	<table cellspacing="0" cellpadding="0" border="0" class="gridTable">
		<thead>
			<tr>
				<td height="35" align="center" width="130" class="wt-td">Style I</td>
				<td align="center" width="130" class="wt-td">Style II</td>
				<td align="center" width="130" class="wt-td">Color</td>
				<td align="center" width="130" class="wt-td">Color Code</td>
				<td align="center" width="130" class="wt-td">UPC</td>
				<td align="center" width="130" class="wt-td">Size</td>
				<td align="center" width="130" class="wt-td">Quantity</td>
			</tr>
		</thead>
		<tbody>
			<tr>
				% for row in range(rows):
				<td height="25" class="t-td">
					${mainStyles[row + 1]|b}
				</td>
				<td align="center" class="t-td">
					${extraStyles[row + 1]|b}
				</td>
				<td align="center" class="t-td">
					${colorNames[row + 1]|b}
				</td>
				<td align="center" class="t-td">
					${colorCodes[row + 1]|b}
				</td>
				<td align="center" class="t-td">
					${upcs[row + 1]|b}
				</td>
				<td align="center" class="t-td">
					${sizes[row + 1]|b}
				</td>
				<td align="center" class="bt-td">
					% for detail in itemDetails:
					% if detail.attr.attrName == 'Size_Qty':
					% if detail.itemGroup == (row + 1):
						${detail.attrContent}
					% endif
					% endif
					% endfor
					&nbsp;
				</td>
			</tr>
			% endfor
		</tbody>
	</table>
</div>
</div>