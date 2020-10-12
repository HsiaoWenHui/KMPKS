function forget(){
    alert("請寄信至 1205hsiao@gmail.com");
    return (false);
}
function validateForm(form)
{
    
    if (!checkPassword(form.password,form.confirm_password)) {
       
        return false;
    }
    else if (!checkEmail(form.email.value)) {
       
        return false;
    }
    
    form.submit();
    return(true);

}
function checkEmail(email){
    index = email.indexOf ('@', 0);		// 尋找 @ 的位置，0 代表開始尋找的起始位置
    if (email.length==0) {
        alert("請輸入電子郵件地址！");
        return (false);
    } else if (index==-1) {
        alert("錯誤：必須包含「@」。");
        return (false);
    } else if (index==0) {
        alert("錯誤：「@」之前不可為空字串。");
        return (false);
    } else if (index==email.length-1) {
        alert("錯誤：「@」之後不可為空字串。");
        return (false);
    } else
        return (true);
}

function checkUsername(control){
    var username=control.value
    var code;
    if (username==''){
        alert("錯誤：請輸入username ");
        return (false);
    }
    if(username.length>20 ||username.length<6){
        alert("錯誤：username 最長20字元 最短6字元");
        return (false);
    }
    for (i=0;i<username.length;i++){
        code=username[i].charCodeAt();
        if (!((code>=48 && code<=57)||(code>=65 && code<=90)||(code>=97 && code<=122))){
            alert("錯誤：username 只能輸入英數");
            return (false);
        }

    }
    return true
}
function checkPassword(control_1,control_2){
    var pwd=control_1.value
    var conf_pwd=control_2.value
    var code;
    if (pwd==''){
        alert("錯誤：請輸入password ");
        return (false);
    }
    if(pwd.length>20||pwd.length<7){
        alert("錯誤：password 最長20字元 最短6字元");
        return (false);
    }
    for (i=0;i<pwd.length;i++){
        code=pwd[i].charCodeAt();
        if (!((code>=48 && code<=57)||(code>=65 && code<=90)||(code>=97 && code<=122))){
            alert("錯誤：password 只能輸入英數");
            return (false);
        }

    }
    if (pwd != conf_pwd){
        alert("錯誤：password 兩次輸入不同");
        return (false);
    }
    return true
}
var check = function() {
    if (document.getElementById('password').value ==
        document.getElementById('confirm_password').value) {
        document.getElementById('message').style.color = 'green';
        document.getElementById('message').innerHTML = 'matching';
    } else {
        document.getElementById('message').style.color = 'red';
        document.getElementById('message').innerHTML = 'not matching';
    }
}