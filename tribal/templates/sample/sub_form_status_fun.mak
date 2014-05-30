<%page args="cf,has_permission,getManagerByTeam,isSameTeam,isPDTeam"/>


<div class="div_status" style="border:1px solid #A6C9E2;padding:3px;overflow:hidden;">
  <div style="float:left">
    <span class="hlfont">Status :</span>     
      %if cf.status == -1:
          <span class="status_flag">Wait For Approval</span></div>
          %if has_permission("SAMPLE_APPROVE") and request.identity['user'].user_id in getManagerByTeam(cf.main.team_id):
	          <div class="action-bn">
	            <a href='#' class='btn btn_start' onclick="ajaxMark({form_ids:'${'%s_%d' %(cf.__class__.__name__,cf.id)}',action:'A'})">Approve</a>
	          	<a href='#' class='btn btn_revise' onclick="ajaxMark({form_ids:'${'%s_%d' %(cf.__class__.__name__,cf.id)}',action:'D'})">Revision Required</a>
	          </div>
	      %elif isSameTeam or isPDTeam:
	          <div class="action-bn">
          	  	<a href='#' class='btn btn_cancel' onclick="ajaxMark({form_ids:'${'%s_%d' %(cf.__class__.__name__,cf.id)}',action:'X'})">Cancel</a>
          	  </div>
          %endif
        

      %elif cf.status == 0:
        <span class="status_flag">New</span></div>
        <div class="action-bn">
        	%if isPDTeam:
          		<a href='#' class='btn btn_start' onclick="ajaxMark({form_ids:'${'%s_%d' %(cf.__class__.__name__,cf.id)}',action:'S'})">Start Work</a>
          	%endif
        	%if isSameTeam or isPDTeam:
        		<a href='#' class='btn btn_pending' onclick="ajaxMark({form_ids:'${'%s_%d' %(cf.__class__.__name__,cf.id)}',action:'P'})">Pending</a>
        		<a href='#' class='btn btn_cancel' onclick="ajaxMark({form_ids:'${'%s_%d' %(cf.__class__.__name__,cf.id)}',action:'X'})">Cancel</a>
        	%endif
        </div>

        
      %elif cf.status == 2:
        <span class="status_flag">Under Development</span></div>
        <div class="action-bn">
          %if isSameTeam or isPDTeam:
          		<a href='#' class='btn btn_pending' onclick="ajaxMark({form_ids:'${'%s_%d' %(cf.__class__.__name__,cf.id)}',action:'P'})">Pending</a>
          		<a href='#' class='btn btn_cancel' onclick="ajaxMark({form_ids:'${'%s_%d' %(cf.__class__.__name__,cf.id)}',action:'X'})">Cancel</a>
          %endif
         
          %if isPDTeam:
          	  <a href='#' class='btn btn_complete' onclick="ajaxMark({form_ids:'${'%s_%d' %(cf.__class__.__name__,cf.id)}',action:'C'})">Complete</a>
          %endif
        </div>
               
        
      %elif cf.status == 1:
        <span class="status_flag">Completed</span></div>


      %elif cf.status == -2:
        <span class="status_flag">Disapproval</span></div>
        <div class="action-bn">
        	%if isSameTeam or isPDTeam:
	          <a href='#' class='btn btn_revise' onclick="ajaxMark({form_ids:'${'%s_%d' %(cf.__class__.__name__,cf.id)}',action:'R'})">Revision</a>
        	  <a href='#' class='btn btn_cancel' onclick="ajaxMark({form_ids:'${'%s_%d' %(cf.__class__.__name__,cf.id)}',action:'X'})">Cancel</a>
        	%endif
        </div>      
        
      %elif cf.status == -9:
        <span class="status_flag">Cancelled</span></div>
        <div class="action-bn">
            <!--
	        %if isSameTeam or isPDTeam:
		        	<a href='#' class='btn btn_revise' onclick="ajaxMark({form_ids:'${'%s_%d' %(cf.__class__.__name__,cf.id)}',action:'U'})">Revision</a>
	      	%endif
	      	-->
	    </div>
        
      %elif cf.status == 3:
        <span class="status_flag">Pending</span></div>
        <div class="action-bn">
        	%if isSameTeam or isPDTeam:
	        	%if cf.status_back == 2:
	        		<a href='#' class='btn btn_start' onclick="ajaxMark({form_ids:'${'%s_%d' %(cf.__class__.__name__,cf.id)}',action:'G'})">Restart</a>
	        	%elif cf.status_back == 0:
	        		<a href='#' class='btn btn_start' onclick="ajaxMark({form_ids:'${'%s_%d' %(cf.__class__.__name__,cf.id)}',action:'U'})">Restart</a>
	        	%endif
	        %endif
        </div>
      %else:
        </div>
      %endif
	        		



  <div class="clear"></div>
</div>
