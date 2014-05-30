<%inherit file="tribal.templates.master"/>

<%
  from repoze.what.predicates import not_anonymous, in_group, has_permission
%>

<%def name="extTitle()">r-pac - Report</%def>

<div class="main-div">
	<div id="main-content">
	
        %if has_permission('DBA_REPORT'):
          <div class="block">
	    	<a href="/dba/report"><img src="/images/dba.jpg" width="55" height="55" alt="" /></a>
	    	<p><a href="/dba/report">DIM</a></p>
	    	<div class="block-content">The module is for the "DIM" .</div>
	      </div>
        <div class="block">
	    	<a href="/dba2/report"><img src="/images/dba.jpg" width="55" height="55" alt="" /></a>
	    	<p><a href="/dba2/report">PLAYTEX / WONDERBRA / SHOCK ABSORBER</a></p>
	    	<div class="block-content">The module is for the "PLAYTEX / WONDERBRA / SHOCK ABSORBER" .</div>
	      </div>
        %endif
		
		%if in_group('Admin') or has_permission('SAMPLE_DEVELOPMENT'):
	     <div class="block">
	    	<a href="/sample/report"><img src="/images/sample.jpg" width="55" height="55" alt="" /></a>
	    	<p><a href="/sample/report">Structural/Flexible Development</a></p>
	    	<div class="block-content">The module is for the "Structural/Flexible Development" .</div>
	      </div>
	    %endif
	    
	    %if in_group('Admin') or has_permission('PREPRESS_ASSIGN'):
	     <div class="block">
	    	<a href="/prepress/report"><img src="/images/prepress.jpg" width="55" height="55" alt="" /></a>
	    	<p><a href="/prepress/report">Prepress</a></p>
	    	<div class="block-content">The module is for the "Prepress" .</div>
	      </div>
	    %endif

            %if in_group('Admin') or has_permission('BBY'):
            <div class="block">
		    	<a href="/bbyreport/report"><img src="/images/bby_pif.jpg" width="55" height="55" alt="" /></a>
		    	<p><a href="/bbyreport/report">BBY Report</a></p>
		    	<div class="block-content">The module is for the "BBY Report" .</div>
		    </div>

            <div class="block">
		    	<a href="/bbymockup/report"><img src="/images/bby_pif.jpg" width="55" height="55" alt="" /></a>
		    	<p><a href="/bbymockup/report">(BBY)Mockup Report</a></p>
		    	<div class="block-content">The module is for the "(BBY)Mockup Report" .</div>
		    </div>
		    
		    <div class="block">
		    	<a href="/bbyreport/raw_report"><img src="/images/bby_pif.jpg" width="55" height="55" alt="" /></a>
		    	<p><a href="/bbyreport/raw_report">(BBY)Raw Report</a></p>
		    	<div class="block-content">The module is for the "(BBY)Raw Report" .</div>
		    </div>
            %endif
	    
	</div>
</div>