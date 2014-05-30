<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-Equiv="Cache-Control" Content="no-cache">
<meta http-Equiv="Pragma" Content="no-cache">
<meta http-Equiv="Expires" Content="0">

<title>r-pac - Sample Development</title>
<link href="/images/favicon.ico" type="images/x-icon" rel="shortcut icon" />
<link href="/css/screen.css" rel="stylesheet" type="text/css" media="screen,print"/>
<link href="/css/all.css" rel="stylesheet" type="text/css" media="screen,print"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" media="screen,print"/>
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen,print"/>
<link rel="stylesheet" href="/css/impromt.css" type="text/css" media="screen,print"/>
<link rel="stylesheet" href="/css/jquery-ui-1.7.3.custom.css" type="text/css" media="screen,print"/>
<link rel="stylesheet" href="/css/custom/sample.css" type="text/css" media="screen,print"/>
<link rel="stylesheet" href="/css/glowbutton.css" type="text/css" media="screen,print"/>
<style type="text/css" media="screen,print">
.hlfont{font:normal 18px Tahoma, Helvetica, sans-serif;color:#069;margin:0;padding:15px 5px;}
.action-bn{display:inline;float:right;}
.jobs-div{border:1px solid #A6C9E2;margin-bottom:10px;overflow:hidden;width:850px;padding:10px 10px 0;}
.one-job-div{width:800px;margin-bottom:10px;overflow:auto;}
.one-material-div{width:400px;float:left;}
.one-material-div span{width:80px;float:left;}
.sample-table{border:#069 solid 1px;margin:15px;}
.sample-Joblist{font-family:Tahoma, Geneva, sans-serif;font-size:12px;color:#000;text-decoration:none;line-height:20px;padding:10px;}
.title-JL{font-family:Tahoma, Geneva, sans-serif;font-size:12px;line-height:normal;font-weight:700;color:#C90;text-decoration:none;}
.sample-content{border:#069 solid 1px;background-color:#FFC;}
</style>
<script type="text/javascript" src="/js/jquery-1.3.2.js" type="text/javascript"></script>
<script type="text/javascript" src="/js/jquery.loadmask.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/numeric.js" language="javascript"></script>
<script type="text/javascript" src="/js/custom/sample/util.js?6" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-ui-timepicker-addon.js" language="javascript"></script>
%if action=='view':
<script type="text/javascript" src="/js/jquery.progressbar.js" language="javascript"></script>
%endif
<script type="text/javascript" src="${js_url}?6" language="javascript"></script>
<script typ="text/javascript">
    var tab_id, obj_id;
    $(document).ready(function(){
        tab_id = $('#tab_id').val();
        obj_id = tab_id.split('-')[1]
        var index = tab_id.split('-')[2]
        SFNamespace[obj_id].obj.id = SFNamespace[obj_id].obj.id + '-' + index
        SFNamespace[obj_id].obj.install();
        $('.div1 :input').each(function(){
            disableField($(this))
        })
        parent.cancelLoading()
        parent.resetTabLabels()
    })
    function reset_label(title){
        SFNamespace[obj_id].obj.title = title;
    }
</script>
</head>
<body>
    <input type="hidden" name="tab_id" id="tab_id" value="${tab_id}" />
    <div class="div_subform">
        ${html|n}
    </div>
</body>