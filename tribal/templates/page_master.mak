<%inherit file="tribal.templates.master"/>

<%!
	from tg.flash import get_flash,get_status
	from repoze.what.predicates import not_anonymous,in_group,has_permission,has_any_permission
%>

<%def name="extTitle()">r-pac - Master</%def>

<div class="main-div">
    <div id="main-content">
        %if in_group('Admin') or has_permission('DBA'):
        <div class="box1 module">
            <table>
                <caption>DBA</caption>
                <tr><th scope="row"><a href="/dbacustomer/index">Customer</th></tr>
                <tr><th scope="row"><a href="/dbacategory/index">Item Category</a></th></tr>
                <tr><th scope="row"><a href="/dbaitemtype/index">Item Type</a></th></tr>
                <tr><th scope="row"><a href="/dbaitem/index">Item</a></th></tr>
                %if in_group('DBA_AE') or in_group('Admin'):
                <tr><th scope="row"><a href="/dba/customer_item">Customer & Item</a></th></tr>
                %endif
            </table>
        </div>
        %endif

        %if in_group('Admin') or has_permission("PEI"):
        <div class="box1 module">
            <table>
                <caption>PEI</caption>
                <tr><th scope="row"><a href="/itemcode/index">Item Code</th></tr>
                <tr><th scope="row"><a href="/itemattr/index">Item Attributes</a></th></tr>
                <tr><th scope="row"><a href="/itemclass/index">Item Class</a></th></tr>
                <tr><th scope="row"><a href="/material/index">Fabric Contents</a></th></tr>
                <tr><th scope="row"><a href="/size/index">Size</a></th></tr>
                <tr><th scope="row"><a href="/style/index">Style</a></th></tr>
                <tr><th scope="row"><a href="/color/index">Color</a></th></tr>
                <tr><th scope="row"><a href="/upc/index">UPC</a></th></tr>
            </table>
        </div>
        %endif

        %if in_group('Admin') or has_permission('BBY'):
        <div class="box1 module">
            <table>
                <caption>BBY</caption>
                <tr><th scope="row"><a href="/bby_brand">Brand</th></tr>
                <tr><th scope="row"><a href="/bby_pf">Packaging Format</th></tr>
                <tr><th scope="row"><a href="/bby_material">Material</th></tr>
                <tr><th scope="row"><a href="/bby_spec">Spec</th></tr>
                <tr><th scope="row"><a href="/bby_closure">Closure</th></tr>
                <tr><th scope="row"><a href="/bby_dm">Display Mode</th></tr>
                <tr><th scope="row"><a href="/bby_fr">Failure Reason</th></tr>
                <tr><th scope="row"><a href="/bby_courier">Courier</th></tr>
                <tr><th scope="row"><a href="/bby_mc">Mockup Content</th></tr>
                <tr><th scope="row"><a href="/bby_vendor">Vendor</th></tr>
                <tr><th scope="row"><a href="/bby_tm">Teammate</th></tr>
                <tr><th scope="row"><a href="/bby_source">Source</th></tr>
                <tr><th scope="row"><a href="/bby_material_spec">Component-Material-Spec-color relation</th></tr>
                <tr><th scope="row"><a href="/bby_agent">Agent</th></tr>
                <tr><th scope="row"><a href="/bby_contact">BBY Packaging Team Contact</th></tr>
            </table>
        </div>
        %endif

        %if in_group('Admin') or has_permission('SAMPLE_DEVELOPMENT'):
        <div class="box1 module">
            <table>
                <caption>Structural/Flexible Development</caption>
                <tr><th scope="row"><a href="/sample_customer">Vendor/Customer</th></tr>
                <tr><th scope="row"><a href="/sample_program">Corporate Customer</th></tr>
                <tr><th scope="row"><a href="/sample_project">Brand</th></tr>
                <tr><th scope="row"><a href="/sample_region">Region</th></tr>
                <tr><th scope="row"><a href="/sample_stock">Stock</th></tr>
                <tr><th scope="row"><a href="/sample_team">Team</th></tr>
                <tr><th scope="row"><a href="/sample_extra_info">Extra Info</th></tr>
                <tr><th scope="row"><a href="/sample_type_mapping">Type Mapping</th></tr>
                <tr><th scope="row"><a href="/sample_item_category">Item Category</th></tr>
            </table>
        </div>
        %endif
        
        %if in_group('Admin') or has_permission('PREPRESS_SYSTEM'):
        <div class="box1 module">
            <table>
                <caption>Prepress System</caption>
                <tr><th scope="row"><a href="/prepress_item_category">Item Category</th></tr>
            </table>
        </div>
        %endif
    </div>
</div>
