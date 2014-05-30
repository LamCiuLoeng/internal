<%page args="cf,has_permission,isSameTeam,isPSTeam"/>

<div class="div_status" style="border:1px solid #A6C9E2;padding:3px;overflow:hidden;">
    <div style="float:left">
        <span class="hlfont">Status :</span>
    
%if cf.__class__.__name__ == 'PSSFUpload':
    <span class="status_flag">
        %if cf.status == 0 or cf.status == 1:
            New
        %elif cf.status == 2:
            Under Development
        %elif cf.status == 3:
            Completed
        %elif cf.status == 9:
            Cancelled
        %elif cf.status == 4:
            Pending
        %endif
    </span>
    </div>
    
%elif cf.__class__.__name__ == 'PSSFBarcode':
    %if cf.status == 0:
        <span class="status_flag">New</span></div>
    %elif cf.status == 1:
        <span class="status_flag">New</span></div>
        <div class="action-bn">
            %if isPSTeam: 
                <a href='#' class='btn btn_start' onclick="job_start('PSSFBarcode',${cf.id},'barcode')">Start</a>
            %endif
        </div>
    %elif cf.status == 2:
        <span class="status_flag">Under Development</span></div>
        <div class="action-bn">
          %if isSameTeam or isPSTeam:
                <a href='#' class='btn btn_pending' onclick="job_pending('PSSFBarcode',${cf.id},'barcode')">Pending</a>
          %endif
          %if isPSTeam:
              <a href='#' class='btn btn_complete' onclick="job_complete('PSSFBarcode',${cf.id},'barcode')">Complete</a>
          %endif
        </div> 
    %elif cf.status == 3:
        <span class="status_flag">Completed</span></div>
          
    %elif cf.status == 9:
        <span class="status_flag">Cancelled</span></div>
        <div class="action-bn">
        </div>
        
    %elif cf.status == 4:
        <span class="status_flag">Pending</span></div>
        <div class="action-bn">
            %if isSameTeam or isPSTeam:
                <a href='#' class='btn btn_start' onclick="job_restart('PSSFBarcode',${cf.id},'barcode')">Restart</a>
            %endif
        </div>
    %else:
        </div>
    %endif


%endif
</div>