setTimeout(function(){phantom.exit()}, 60*1000);

var page = new WebPage(),
	//url = 'http://tribaltest.r-pac.com.hk/sku/update?id=57';
	url, tabQty, imgDir;

var monitor = function(url, positions, imgDir, files, index){
    page.open(url+'&selected='+positions[index], function(status){
        if(status !== 'success'){
            console.log('Unable to load the address!');
        }else{
            var currentUrl = page.evaluate(function(){
                return window.location.href;
            });
            var pos = positions[index].split('-');
            page.injectJs('jquery-1.6.4.min.js');
            page.injectJs('jquery-ui-1.7.3.custom.min.js');
            //console.log('**************************************')
            //console.log('url:'+url+'&selected='+positions[index]);
            //console.log('currentUrl:'+currentUrl);
            if(currentUrl.indexOf('login') != -1){
                //console.log('logining...');
                page.evaluate(function(){
                    $('#login_name').val('admin');
                    $('#login_password').val('ecrmadmin');
                    $('form').first().submit();
                });
            }else if(currentUrl.indexOf(url) != -1){
                //console.log('opening...');
                var height = page.evaluate(function() { return document.body.offsetHeight }),
                    width = page.evaluate(function() { return document.body.offsetWidth });
                //console.log('width:'+width+';height:'+height);
                page.viewportSize = {width: width, height: height};
                var d = new Date();
                var tmpName = imgDir + '/' + pos[1]
                            + '_' + d.getFullYear() + (d.getMonth()+1) 
                            + d.getDate() + d.getHours() + d.getMinutes() 
                            + d.getSeconds() + d.getMilliseconds();
                for(var j=0; j<files.length; j++){
                    var tmpFileName = tmpName + '.' + files[j];
                    var pr = page.render(tmpFileName);
                    if(pr){
                        console.log(tmpFileName); // do not comment this line
                    }
                }

                if(index==positions.length-1){
                    //console.log('monitor ends...');
                    phantom.exit();
                }else{
                    //console.log('monitor next...');
                    monitor(url, positions, imgDir, files, index+1)
                }
            }
            //console.log('**************************************')
        }
    });
}

if(phantom.args.length <= 3){
	console.log('Usage: snapshot.js URL positions img_dir files');
    phantom.exit();
}else{
    url = phantom.args[0];
    positions = phantom.args[1].split('|');
    imgDir = phantom.args[2];
    files = phantom.args[3].split('-');
    monitor(url, positions, imgDir, files, 0)
}