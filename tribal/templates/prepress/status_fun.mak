<%page args="val,cbvalues,sftype,cf,jobdata"/>

%if val not in cbvalues:
<% return %>
%endif

%if cf.status in [3,9] :
    <!-- Completed or Cancelled -->
    &nbsp;
%elif cf.status in [1] :
    <!-- New -->
    <a href='#' class='btn btn_start' onclick="job_start('${sftype}',${cf.id},'${val}')">Start</a>
%elif cf.status in [4] :
    <!-- Pending -->
    %if jobdata.get('%s_%s_%s' %(sftype,cf.id,val),None) == 2 :
        <a href='#' class='btn btn_start' onclick="job_restart('${sftype}',${cf.id},'${val}')">Restart</a>
    %endif
%elif cf.status in [2] :
    <!-- Under development -->
    %if jobdata.get('%s_%s_%s' %(sftype,cf.id,val),None) == None : 
        <a href='#' class='btn btn_start' onclick="job_start('${sftype}',${cf.id},'${val}')">Start</a>
    %elif jobdata.get('%s_%s_%s' %(sftype,cf.id,val),None) == 1 :
        <a href='#' class='btn btn_pending' onclick="job_pending('${sftype}',${cf.id},'${val}')">Pending</a>&nbsp;
        <a href='#' class='btn btn_complete' onclick="job_complete('${sftype}',${cf.id},'${val}')">Complete</a>
    %endif
%endif
