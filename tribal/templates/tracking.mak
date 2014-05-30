<%inherit file="tribal.templates.master"/>

<%
  from repoze.what.predicates import not_anonymous, in_group, has_permission
%>

<%def name="extTitle()">r-pac - Main</%def>

<div class="main-div">
	<div id="main-content">
        %if in_group('Admin') or has_permission('DBA'):
          <div class="block">
	    	<a href="/dba/search"><img src="/images/dba.jpg" width="55" height="55" alt="" /></a>
	    	<p><a href="/dba/search"> DIM</a></p>
	    	<div class="block-content">The module is for the " DIM" .</div>
	      </div>
        <div class="block">
	    	<a href="/dba2/search"><img src="/images/dba.jpg" width="55" height="55" alt="" /></a>
	    	<p><a href="/dba2/search">PLAYTEX / WONDERBRA / SHOCK ABSORBER</a></p>
	    	<div class="block-content">The module is for the "PLAYTEX / WONDERBRA / SHOCK ABSORBER" .</div>
	      </div>
	    %endif
		
			
		%if in_group('Admin') or has_permission('ORSAY'):
	      <div class="block">
	    	<a href="/orsay/search"><img src="/images/orsay.jpg" width="55" height="55" alt="" /></a>
	    	<p><a href="/orsay/search">ORSAY&reg;</a></p>
	    	<div class="block-content">The module is for the "ORSAY&reg;" .</div>
	      </div>
	    %endif
	    
	    %if in_group('Admin') or has_permission('TAG'):
	     <div class="block">
	    	<a href="/tag/historyitems"><img src="/images/dba.jpg" width="55" height="55" alt="" /></a>
	    	<p><a href="/tag/historyitems">History Items</a></p>
	    	<div class="block-content">The module is for the "Tag" .</div>
	      </div>
		
		%endif


	</div>
</div>