/**
 * Created by xujiantao_sx on 2017/4/17.
 */

function AjaxRequest(url,data,func) {
    $.ajax({
        type: 'POST',
        url: url,
        data:data,
        cache: false,
        async: true,
        success: func
    });
}

$(function () {
   $("#bar").children().click(function () {
       $(this).parent().children().removeClass('active');
       $(this).addClass('active');
   });
});

function tab(date1,date2){
    var oDate1 = new Date(date1);
    var oDate2 = new Date(date2);
    if(oDate1.getTime() > oDate2.getTime()){
        return false;
    } else {
        return true;
    }
}

function clearp() {
  $('.cpwd :password').val('');
}

$(function () {
   $('#pwd').click(function(){
        $('.shadow,.infoedit').removeClass('hide');
   });
});

function back(arg) {
    var data = JSON.parse(arg);
    if(data.hasOwnProperty('error_code')){
        var flag = data['error_code'];
        if(flag == 1){
            alert('your password is uncorrect');
        }
        else if(flag == 0){
            alert('change your password successful,please relogin');
            window.location.href = '/';
        }
    }
}

$(function () {
    $('#submitEdit').click(function () {
        $('.cpwd :password').each(function () {
            if(!$(this).val().trim()){
                $(this).addClass('blur');
            }
            else {
                if($(this).hasClass('blur')){
                    $(this).removeClass('blur');
                }
            }
        });
        var orgp = $('#orgpwd').val().trim();
        var newp = $('#newpwd').val().trim();
        var conp = $('#conpwd').val().trim();
        if(orgp && newp && conp){
            if(newp == conp){
                if($('#cpwdts').hasClass('font-red')) {
                    $('#cpwdts').toggleClass('font-red');
                }
                clearp();
                AjaxRequest('/changpwd/',{'orgp':orgp,'newp':newp},back);
            }
            else{
                $('#cpwdts').toggleClass('font-red');
            }
        }
    });
});


$(function () {
   $('#cancelEdit').click(function () {
       clearp();
       $('.shadow,.infoedit').addClass('hide');
   });
});