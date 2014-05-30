<%inherit file="tribal.templates.master"/>
<%def name="extTitle()">r-pac - Cabelas</%def>
<%def name="extCSS()">
<link rel="stylesheet" type="text/css" media="screen" href="/css/custom/cabelas.css"/>
</%def>
<%def name="extJavaScript()">
<script type="text/javascript" src="/js/inlines.min.js"></script>
<script>
$(document).ready(function($) {
	initInlinesForm([
    	["#user_set-group .tabular.inline-related tbody tr", 'user_set', 'Add user account'],
    	["#shipto_set-group .tabular.inline-related tbody tr", 'shipto_set', 'Add ship to address'],
    	["#billto_set-group .tabular.inline-related tbody tr", 'billto_set', 'Add bill to address']
    ])
})
</script>
</%def>
<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/cabelas/development/list_vendor"><img src="/images/images/menu_return_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Cabelas&nbsp;&nbsp;&gt;&nbsp;&nbsp;Vendor&nbsp;&nbsp;&gt;&nbsp;&nbsp;New</div>
<div class='main'>
	<form action='/cabelas/development/save_vendor' method=post enctype="multipart/form-data">
		<div class="ca_box2">
            <fieldset class="module aligned">
                <div class="form-row">
                    <label><span class="red">*</span>Vendor Name:</label>
                    <input type="text" name="vendor_obj-name" class="required"/>
                </div>
            </fieldset>
        </div>
        <div class="inline-group" id="shipto_set-group">
            <div class="tabular inline-related last-related">
                <input type="hidden" name="shipto_set-TOTAL_FORMS" value="0" id="id_shipto_set-TOTAL_FORMS" />
                <input type="hidden" name="shipto_set-MAX_NUM_FORMS" id="id_shipto_set-MAX_NUM_FORMS" />
                <fieldset class="module">
                    <h2>Ship to Address</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Address</th>
                                <th>City,State,Zipcode</th>
                                <th>Country</th>
                                <th>Contact</th>
                                <th>Phone</th>
                                <th>Email</th>
                                <th>Fax</th>
                                <th width="20"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="empty-form" id="shipto_set-empty">
                                <td><input type="text" class="w50" name="shipto_set-__prefix__-address" id="shipto_set-__prefix__-address"/></td>
                                <td><input type="text" class="w50" name="shipto_set-__prefix__-city" id="shipto_set-__prefix__-city"/></td>
                                <td><input type="text" class="w50" name="shipto_set-__prefix__-country" id="shipto_set-__prefix__-country"/></td>
                                <td><input type="text" class="w50" name="shipto_set-__prefix__-contact" id="shipto_set-__prefix__-contact"/></td>
                                <td><input type="text" class="w50" name="shipto_set-__prefix__-phone" id="shipto_set-__prefix__-phone"/></td>
                                <td><input type="text" class="w50" name="shipto_set-__prefix__-email" id="shipto_set-__prefix__-email"/></td>
                                <td><input type="text" class="w50" name="shipto_set-__prefix__-fax" id="shipto_set-__prefix__-fax"/></td>
                                <td></td>
                            </tr>
                        </tbody>
                    </table>
                </fieldset>
            </div>
		</div>
        <div class="inline-group" id="billto_set-group">
            <div class="tabular inline-related last-related">
                <input type="hidden" name="billto_set-TOTAL_FORMS" value="0" id="id_billto_set-TOTAL_FORMS" />
                <input type="hidden" name="billto_set-MAX_NUM_FORMS" id="id_billto_set-MAX_NUM_FORMS" />
                <fieldset class="module">
                    <h2>Bill to Address</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Address</th>
                                <th>City,State,Zipcode</th>
                                <th>Country</th>
                                <th>Contact</th>
                                <th>Phone</th>
                                <th>Email</th>
                                <th>Fax</th>
                                <th width="20"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="empty-form" id="billto_set-empty">
                                <td><input type="text" class="w50" name="billto_set-__prefix__-address" id="billto_set-__prefix__-address"/></td>
                                <td><input type="text" class="w50" name="billto_set-__prefix__-city" id="billto_set-__prefix__-city"/></td>
                                <td><input type="text" class="w50" name="billto_set-__prefix__-country" id="billto_set-__prefix__-country"/></td>
                                <td><input type="text" class="w50" name="billto_set-__prefix__-contact" id="billto_set-__prefix__-contact"/></td>
                                <td><input type="text" class="w50" name="billto_set-__prefix__-phone" id="billto_set-__prefix__-phone"/></td>
                                <td><input type="text" class="w50" name="billto_set-__prefix__-email" id="billto_set-__prefix__-email"/></td>
                                <td><input type="text" class="w50" name="billto_set-__prefix__-fax" id="billto_set-__prefix__-fax"/></td>
                                <td></td>
                            </tr>
                        </tbody>
                    </table>
                </fieldset>
            </div>
        </div>
        <div class="submit-row">
            <input type="submit" value="Create" class="default" name="_create" />
            <!--
            <input type="submit" value="Save and add another" name="_addanother"  />
            <input type="submit" value="Save and continue editing" name="_continue" />
            -->
        </div>
	</form>
</div>
<div class='none' id='hide_logo_file'>
	<div><input type='file' name='logo' />&nbsp;&nbsp;&nbsp;&nbsp;<a class="deletelink" href="javascript:void(0)" onclick='removeLogo(this)'></a></div>
</div>
