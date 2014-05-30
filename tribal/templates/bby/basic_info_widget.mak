<%namespace name="tw" module="tw.core.mako_util"/>

%if value_for("eol"):
    <table border="1" cellpadding="3" cellspacing="0" class="eol">
%else:
    <table border="1" cellpadding="3" cellspacing="0">
%endif

	<tr>
		<td width="150" height="30"  class="title-td">SKU#</td>
		<td>${value_for("sku")}&nbsp;
		    %if value_for("eol"):
                <b><span class="red">(EOL)</span></b>
			%elif value_for("completed"):
				<b><span class="red">(COMPLETED)</span></b>
			%elif value_for("cancel"):
				<b><span class="red">(CANCEL)</span></b>
			%elif value_for("on_hold"):
				<b><span class="red">(ON HOLD)</span></b>
			%endif
		</td>
		<td width="150" class="title-td">Brand</td>
		<td width="250">${value_for("brand")}&nbsp;</td>
	</tr>
	<tr>
		<td width="150" height="30"  class="title-td">Agent</td>
		<td width="250">${value_for("agent")}&nbsp;</td>
		<td width="150" class="title-td">Vendor</td>
		<td width="250">${value_for("vendor")}&nbsp;</td>
	</tr>
	<tr>
		<td width="150" height="30"  class="title-td">Package Format</td>
		<td>${value_for("packaging_format")}&nbsp;</td>
		<td width="150" class="title-td">UPC#</td>
		<td>${value_for("upc_no")}&nbsp;</td>
	</tr>
	<tr>
		<td width="150" height="30"  class="title-td">Closure</td>
		<td>${value_for("closure")}&nbsp;</td>
		<td width="150" class="title-td">Display Mode</td>
		<td>${value_for("display_mode")}&nbsp;</td>
	</tr>
	<tr>
		<td width="150" height="30" class="title-td">IOQ</td>
		<td>${value_for("ioq")}&nbsp;</td>
		<td width="150"class="title-td">AOQ</td>
		<td>${value_for("aoq")}&nbsp;</td>
	</tr>
	<tr>
		<td width="150" height="30"  class="title-td">Product Description</td>
		<td colspan="3">${value_for("product_description")}&nbsp;</td>
	</tr>
	<tr>
		<td width="150" height="30"  class="title-td">PD</td>
		<td>${value_for("pd")}&nbsp;</td>
		<td class="title-td">AE</td>
		<td>${value_for("ae")}&nbsp;</td>
	</tr>
	<tr>
		<td width="150" height="30"  class="title-td">Formed Size</td>
		<td colspan="3">${value_for("formed_size")}&nbsp;&nbsp;(L * W * H  Unit:inch)</td>
	</tr>
	<tr>
		<td width="150" height="30"  class="title-td">Asia Packaging Team Contact</td>
		<td>${value_for("bby_asia_contact")}&nbsp;</td>
		<td class="title-td">US Packaging Team Contact</td>
		<td>${value_for("bby_us_contact")}&nbsp;</td>
	</tr>
</table>