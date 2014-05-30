<%inherit file="tribal.templates.master"/>

<%
  from repoze.what.predicates import not_anonymous, in_group, has_permission
%>

<%def name="extTitle()">r-pac - Main</%def>

<div class="main-div">
	<div id="main-content">
      	    
	    
	  %if in_group('Admin') or has_permission("PEI"):
	    <div class="block">
	    	<a href="/pei/index"><img src="/images/pei.jpg" width="55" height="55" alt="" /></a>
	    	<p><a href="/pei/index">PEI&reg;</a></p>
	    	<div class="block-content">The module is for the "PEI&reg;" .</div>
	    </div>
	  %endif
	    
      %if in_group('Admin'):
	    <div class="block">
	    	<a href="/order/index"><img src="/images/tribal.jpg" width="55" height="55" alt="" /></a>
	    	<p><a href="/order/index">Tribal Sportsware</a></p>
	    	<div class="block-content">The module is for the "r-pac-Tribal" .</div>
	    </div>
      %endif
      
      %if in_group('Admin') or has_permission('ORSAY'):
	    <div class="block">
	    	<a href="/orsay/index"><img src="/images/orsay.jpg" width="55" height="55" alt="" /></a>
	    	<p><a href="/orsay/index">ORSAY&reg;</a></p>
	    	<div class="block-content">The module is for the "ORSAY&reg;" .</div>
	    </div>
	  %endif
		%if in_group('Admin') or has_permission('CABELAS'):
		<div class="block">
			<a href="/cabelas/index"><img src="/images/log_cabelas.png" width="55" height="55" alt="" /></a>
			<p><a href="/cabelas/index">Cabelas&reg;</a></p>
			<div class="block-content">The module is for the "Cabelas&reg;" .</div>
		</div>
	    %endif


      %if in_group('Admin') or has_permission('SAMPLE_DEVELOPMENT'):
	    <div class="block">
	    	<a href="/sample/index"><img src="/images/sample.jpg" width="55" height="55" alt="" /></a>
	    	<p><a href="/sample/index">Structural/Flexible Development</a></p>
	    	<div class="block-content">The module is for the "Structural/Flexible Development" .</div>
	    </div>
      %endif
      
      
      %if has_permission('DBA'):
        <div class="block">
	    	<a href="/dba/index"><img src="/images/dba.jpg" width="55" height="55" alt="" /></a>
	    	<p><a href="/dba/index">DIM</a></p>
	    	<div class="block-content">The module is for the "DIM" .</div>
	    </div>
      <div class="block">
	    	<a href="/dba2/index"><img src="/images/dba.jpg" width="55" height="55" alt="" /></a>
	    	<p><a href="/dba2/index">PLAYTEX / WONDERBRA / SHOCK ABSORBER</a></p>
	    	<div class="block-content">The module is for the "PLAYTEX / WONDERBRA / SHOCK ABSORBER" .</div>
	    </div>
	  %endif

      %if in_group('Admin') or has_permission('BBY'):
	    <div class="block">
	        <a href="/sku/index"><img src="/images/bby_pif.jpg" width="55" height="55" alt="" /></a>
	        <p><a href="/sku/index">(BBY)New SKU</a></p>
	        <div class="block-content">The module is for the "(BBY)New SKU" .</div>
	      </div>
	      
	      <div class="block">
	        <a href="/bbymockup/index"><img src="/images/bby_mockup.jpg" width="55" height="55" alt="" /></a>
	        <p><a href="/bbymockup/index">(BBY)Mockup</a></p>
	        <div class="block-content">The module is for the "(BBY)Mockup" .</div>
	      </div>
	 
	      <div class="block">
	        <a href="/bbycasepack/index"><img src="/images/bby_casepack.jpg" width="55" height="55" alt="" /></a>
	        <p><a href="/bbycasepack/index">(BBY)Case pack</a></p>
	        <div class="block-content">The module is for the "(BBY)Case pack" .</div>
	      </div>
      %endif



	  %if in_group('Admin') or has_permission('TAG'):
	      <div class="block">
		    <a href="/tag/index"><img src="/images/tag.jpg" width="55" height="55" alt="" /></a>
		    <p><a href="/tag/index">TAG&reg;</a></p>
		    <div class="block-content">The module is for the "TAG&reg;" .</div>
	      </div>
      %endif
      
      %if in_group('Admin') or has_permission('LEMMI'):
      	  <div class="block">
		    <a href="/lemmi/index"><img src="/images/tag.jpg" width="55" height="55" alt="" /></a>
		    <p><a href="/lemmi/index">LEMMI</a></p>
		    <div class="block-content">The module is for the "LEMMI" .</div>
	      </div>
      %endif

      %if in_group('Admin') or has_permission('TMW'):
      	  <div class="block">
		    <a href="/tmw/index"><img src="/images/tag.jpg" width="55" height="55" alt="" /></a>
		    <p><a href="/tmw/index">TMW</a></p>
		    <div class="block-content">The module is for the "TMW" .</div>
	      </div>
      %endif
	
	  %if in_group('Admin') or has_permission('PREPRESS_SYSTEM'):
		 <div class="block">
		    <a href="/prepress/index"><img src="/images/prepress.jpg" width="55" height="55" alt="" /></a>
		    <p><a href="/prepress/index">Prepress</a></p>
		    <div class="block-content">The module is for the "Prepress" .</div>
	      </div>
	  %endif
	</div>
</div>