<%
	from tribal.util.mako_filter import b
%>
<div id="item_variables">
<div style="float: left; padding-top: 3px;">
	&nbsp;&nbsp;
	<strong class="fonts-c-369">Edit Variables</strong>
</div>
<div style="float: right; padding-top: 3px;">
  	<a href="#" onclick="saveCAHangTagDiv(${include_item.id});"><strong>Save</strong></a>
  	&nbsp;&nbsp;
  	<a href="#" onclick="closeDiv();"><strong>Close</strong></a>
  	&nbsp;&nbsp;
</div>
<div style="float: left; padding-left: 360px; padding-top: 3px;">
    <label class="fieldlabel"><strong>Item:</strong>&nbsp;</label>
    % if include_item:
    <strong>${include_item}</strong>
    % endif
</div>
<div style="clear:both; padding-right: 10px; padding-top: 5px;">
	<input type="image" src="/images/new_item.jpg" onclick="toAdd();return false;"/>
</div>
<br />
<div style="padding-left: 20px; padding-bottom: 5px;">
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
				<td height="25" class="t-td">
					<select id="styleOne_1_ext" class="input-style1-40fonts" name="styleOne_1_ext">
						<option value=""></option>
						% for style in styles:
						<option value="${style.id}">${style.mainPart}</option>
						% endfor
					</select>
				</td>
				<td align="center" class="t-td">
					<select id="styleTwo_1_ext" class="input-style1-40fonts" name="styleTwo_1_ext">
						<option value=""></option>
						% for style in styles:
						<option value="${style.id}">${style.extraPart}</option>
						% endfor
					</select>
				</td>
				<td align="center" class="t-td">
					<select id="colorName_1_ext" class="input-style1-40fonts" name="colorName_1_ext">
						<option value=""></option>
						% for color in colors:
						<option value="${color.id}">${color.name}</option>
						% endfor
					</select>
				</td>
				<td align="center" class="t-td">
					<select id="colorCode_1_ext" class="input-style1-40fonts" name="colorCode_1_ext">
						<option value=""></option>
						% for color in colors:
						<option value="${color.id}">${color.code}</option>
						% endfor
					</select>
				</td>
				<td align="center" class="t-td">
					<select id="upc_1_ext" class="input-style1-40fonts" name="upc_1_ext">
						<option value=""></option>
						% for upc in upcs:
						<option value="${upc.id}">${upc.name}</option>
						% endfor
					</select>
				</td>
				<td align="center" class="t-td">
					<select id="size_1_ext" class="input-style1-40fonts" name="size_1_ext">
						<option value=""></option>
						% for size in sizes:
						<option value="${size.id}">${size.content}</option>
						% endfor
					</select>
				</td>
				<td align="center" class="bt-td">
					<input type="text" class="required numeric" name="qty_1_ext" style="text-align:right;" />
				</td>
			</tr>
			<tr class="template" style="display:none">
				<td height="25" class="t-td">
					<select id="styleOne_x_ext" class="input-style1-40fonts" name="styleOne_x_ext">
						<option value=""></option>
						% for style in styles:
						<option value="${style.id}">${style.mainPart}</option>
						% endfor
					</select>
				</td>
				<td align="center" class="t-td">
					<select id="styleTwo_x_ext" class="input-style1-40fonts" name="styleTwo_x_ext">
						<option value=""></option>
						% for style in styles:
						<option value="${style.id}">${style.extraPart}</option>
						% endfor
					</select>
				</td>
				<td align="center" class="t-td">
					<select id="colorName_x_ext" class="input-style1-40fonts" name="colorName_x_ext">
						<option value=""></option>
						% for color in colors:
						<option value="${color.id}">${color.name}</option>
						% endfor
					</select>
				</td>
				<td align="center" class="t-td">
					<select id="colorCode_x_ext" class="input-style1-40fonts" name="colorCode_x_ext">
						<option value=""></option>
						% for color in colors:
						<option value="${color.id}">${color.code}</option>
						% endfor
					</select>
				</td>
				<td align="center" class="t-td">
					<select id="upc_x_ext" class="input-style1-40fonts" name="upc_x_ext">
						<option value=""></option>
						% for upc in upcs:
						<option value="${upc.id}">${upc.name}</option>
						% endfor
					</select>
				</td>
				<td align="center" class="t-td">
					<select id="size_x_ext" class="input-style1-40fonts" name="size_x_ext">
						<option value=""></option>
						% for size in sizes:
						<option value="${size.id}">${size.content}</option>
						% endfor
					</select>
				</td>
				<td align="center" class="bt-td">
					<input type="text" class="required numeric" name="qty_x_ext" style="text-align:right;" />
				</td>
			</tr>
		</tbody>
	</table>
</div>
</div>